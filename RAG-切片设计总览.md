# RAG 切片设计总览

本文档汇总 [帮助中心](帮助中心/_rag-chunks-index.md) 和 [API文档](API文档/) 两套语料的切片思路、schema 和最终数据量，供后续接入检索系统时参考。

## 为什么分开存

帮助中心是客服/运营场景的政策与操作说明（退票时限、SLA、账单、安全合规……），API文档是开发者集成场景的技术参考（端点定义、字段类型、错误码、Webhook）。两者面向的问题类型完全不同，混在一个 collection 里会互相稀释检索结果。路由判断已经在 skill 里做了，不在本文档范围内——这里只记录两边各自"怎么切"的设计。

## 共同的设计原则

不管切哪一边，都遵守这几条（最早在帮助中心"退票"那篇上验证，后来在 API 文档上原样复用）：

1. **文章为最小一级边界**，不跨文章拼接 chunk。
2. **规则单元/对比整体保留**——条件和结论、触发和后果、两个被对比的对象，不能因为凑 chunk size 被拆到两个 chunk 里。
3. **数字类/枚举类大表不做语义切片**，转成结构化 JSON，检索走精确查表而不是向量相似度。
4. **FAQ 单独一种 schema**（问答对），不套用规则单元的切法。
5. **metadata 要能支撑"先精确过滤、再语义检索"**——分类字段、适用范围字段（航司/航司代码/API endpoint）要冗余写进每条 child，不要指望查询时再做 join。

---

## 帮助中心：7 条原则 + 两种 schema

详细设计见 [帮助中心/_rag-chunks-index.md](帮助中心/_rag-chunks-index.md) 和最初的 [退票/_rag-chunks/README.md](帮助中心/04-售后票务/退票/_rag-chunks/README.md)。

**规则单元 schema**（parent + child 两层）：

```
parents.jsonl: article_id, title, level1_category, level2_category,
               applicable_carrier, updated_at, source_path, summary,
               child_chunk_ids
children.jsonl: chunk_id, parent_id, section, rule_type,
                 applicable_carrier, updated_at, text
```

parent 摘要不进向量库，检索命中 child 后按 `parent_id` 回带，用于让模型判断"这条规则属于退票还是废票"这类易混淆场景。

**FAQ schema**（扁平问答对，无 parent 层）：

```
chunk_id, parent_id, topic, level1_category, level2_category,
question, answer, source_path
```

**结构化表**：131 家航司的退票时限表（原文是一个巨大的 HTML table，逐行切片会丢失整体可查询性，所以整体转成 JSON，不进向量库）。

**最终数据量**：

| | 数量 |
|---|---|
| Parent（文章摘要） | 44 |
| Child（规则单元） | 221 |
| FAQ 问答对 | 136 |
| 结构化表 | 1（131 行） |

---

## API文档：三种内容形态 + 对应切法

API 文档的内容形态比帮助中心复杂得多，不能只用一套规则单元切法，实际分成三类分别处理，另加一个 FAQ 变体：

### A类：概念/流程说明

跟帮助中心的规则单元几乎一样——按 H2/H3 切，条件+结论不拆开。覆盖集成指南、集成工具、产品指南里的流程说明文档（预订概述、booking-flows、标识符、webhook通知等）。

Schema（无 parent 层，直接是 children）：
```
chunk_id, doc_type, level1_category, level2_category,
applicable_carrier, source_path, section, text
```

### B类：对比消歧文档（"confusable pairs"）

站点里有一整批固定模板的文档，专门用来区分容易混淆的错误码或 API 选型（"429 vs 110""搜索 vs 报价""验证 vs 下单"），模板固定为：简要回答 / 常见问题 / 核心区别 / 处理方式 / 常见错误 / 相关页面。

切法的关键：**每个 chunk 仍然要同时覆盖被对比的双方/多方**，不能按对象拆开——"429 和 110 的核心区别"这个 chunk 必须同时包含两个代码的说明，拆开就答不出"区别是什么"。这跟帮助中心里"退票/废票/改期容易混淆"是同一类问题，只是这里站点自己已经把易混淆内容显式模板化了。

Schema 比 A 类多一个 `compares` 字段：
```
chunk_id, doc_type: "对比消歧", compares: [...], level1_category,
level2_category, source_path, section, text
```

`compares` 支持精确匹配任一方再 fallback 语义检索，例如查"429"或查"110"都应该命中同一批 chunk。

### C类：API参考端点（内嵌 OpenAPI JSON）

`04-API参考` 下 25 个端点文档，正文很短，核心内容是一整块内嵌的 OpenAPI 3.0 JSON（几十个字段、十几个可复用 component）。这类**不按 Markdown 标题切，而是写 Python 脚本解析 JSON 结构**：人工摘抄大段生成式 schema 风险高（容易漏字段、看错 required/类型），程序化解析更可靠。

每个端点产出：
- 1 个端点概览 chunk（URL、方法、用途）
- 请求头 / 请求体字段 chunk
- 响应字段 chunk（非 `$ref` 的顶层字段）
- 每个可复用 component（如 `Routing`、`RoutingSegment`）各一个 chunk，列出全部字段

同时会自动识别藏在字段 `description` 里的"伪装成文字的表格"——比如 `status` 字段的 description 其实是一长串"- 100: xxx - 101: xxx"的错误码枚举，这种会被识别出来单独提取成结构化 JSON（`lookup-table-<endpoint>-<field>.json`），不进语义检索。全站还有一张更大的权威错误码表（`错误码.md` 里的 43 行 markdown 表格），同样整体提取成 JSON。

脚本：[chunk_api_reference.py](scripts/chunk_api_reference.py)、[chunk_disambiguation.py](scripts/chunk_disambiguation.py)、[extract_error_code_table.py](scripts/extract_error_code_table.py)

### FAQ变体：troubleshooting-faqs

跟帮助中心 FAQ 同样是问答对 schema，但源文件本身有站点自己的 GitBook 生成瑕疵——很多问题会同时以 `####`（短答案）和 `###`（长答案，文字几乎一样）出现两次。写了专门的解析脚本按问题文本去重、保留更长的答案，同时把文中嵌的大数据表（如 40 家航司的持卡人信息必填矩阵）单独提出成结构化 JSON。

脚本：[chunk_faq_api.py](scripts/chunk_faq_api.py)

### 最终数据量

| doc_type | 数量 | 说明 |
|---|---|---|
| 概念说明 | 154 | A类，流程/概念 prose |
| 响应字段 | 146 | C类，OpenAPI 响应顶层字段 |
| 响应组件 | 93 | C类，可复用 schema component |
| 对比消歧 | 91 | B类，错误码/API选型对比 |
| 请求参数 | 50 | C类，请求头/请求体 |
| 操作步骤 | 50 | A类，编号步骤流程 |
| 错误处理 | 31 | A类，5篇分类错误指南 |
| 端点概览 | 25 | C类，每端点1条 |
| 流程说明 | 15 | A类 |
| 参考数据 | 12 | A类，集成参考/沙箱测试数据 |
| 字段说明 / 决策导航 / 环境说明 / Webhook说明 / 错误处理总览 / 服务范围说明 / 导航概览 / API说明 | 47 | 各类零散 doc_type |
| **children 小计** | **719** | |
| FAQ 问答对 | 104 | 去重后，另有1个40行表格单独提取 |
| **总计** | **823** | |
| 结构化表（JSON，不进向量库） | 16 | 9个端点错误码枚举 + 1张全站权威错误码表 + 3张集成参考数据表(区域设置/测试卡号/测试航线) + 1张FAQ内嵌的支付卡矩阵表 + 2个其他端点 |

---

## 两边对比一览

| | 帮助中心 | API文档 |
|---|---|---|
| 内容性质 | 客服/运营政策与操作 | 开发者技术参考 |
| 文章数 | 80 | 123 |
| 是否分内容类型处理 | 否，统一规则单元 | 是，A/B/C三类+FAQ变体 |
| parent 层 | 有（44条摘要） | 无（C类的"端点概览"起类似作用） |
| 特有 metadata 字段 | `applicable_carrier`（航司代码） | `compares`（对比消歧文档专用） |
| 结构化表数量 | 1（131行退票时限） | 16（错误码×10 + 参考数据×3 + 支付矩阵×1+ 其他×2） |
| 切片方式 | 人工/subagent 阅读后编写 | C类程序化解析OpenAPI，B/FAQ写专用脚本，A类人工/subagent |
| chunk 总数 | 357（221规则+136FAQ） | 823 |

## 踩过的坑（写给以后维护这套流水线的人）

1. **多个 agent/脚本共享同一输出文件夹时，用 `parent_id`/`endpoint_id` 精确匹配去重，不要用 `chunk_id.startswith()` 前缀匹配**——`get-offer` 是 `get-offer-price` 的字面前缀，会导致后者被误删。
2. **chunk_id 不能靠"去掉非ASCII字符"生成 slug**——不同的中文标题可能被一起清空成同一个短 slug（比如"获取报价 vs 获取报价价格"和"验证 vs 下单"曾经都被清成了 `"vs"`），必须用英文短语手选或 hash 保证唯一。
3. **脚本默认要用"合并写入"而不是"覆盖写入"**——同一个 `_rag-chunks/` 目录会被多次调用（不同端点、不同文章共享一个输出文件），每次开成 `"w"` 模式会把之前跑的内容全部冲掉。
4. **OpenAPI schema 里 `$ref` 和 `description` 可能共存**——按 spec `$ref` 旁边的 sibling key 应该被忽略，但这批文档的生成器把真实的人类可读说明（包括伪装成表格的错误码枚举）放在了 `$ref` 字段旁边，如果看到 `$ref` 就跳过会丢数据。
5. **Windows 终端默认编码不是 UTF-8**，Python 脚本要显式设 `PYTHONUTF8=1`，PowerShell 里带中文字面量的 `.ps1` 脚本文件要避免把中文写进代码逻辑本身（哪怕只是注释），否则脚本在某些编码环境下会静默出错。
