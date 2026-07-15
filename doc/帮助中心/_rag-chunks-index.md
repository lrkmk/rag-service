# Atlas 帮助中心 — RAG 切片总索引

对全部 80 篇源文章完成切片，覆盖站点全部 11 个一级分类。切法依据见 [04-售后票务/退票/_rag-chunks/README.md](04-售后票务/退票/_rag-chunks/README.md) 中定义的 7 条原则；FAQ 板块采用不同 schema（见下）。所有 `parents.jsonl`/`children.jsonl` 已做 JSON 有效性校验 + parent/child 引用完整性校验，全部通过，0 错误、0 孤儿引用。

## 售后票务（9 子类，详见 [04-售后票务/_rag-chunks-index.md](04-售后票务/_rag-chunks-index.md)）

| 子类 | parent | child |
|---|---|---|
| 退票 | 5 | 23 |
| 废票 | 3 | 23 |
| 改期 | 4 | 13 |
| 改乘客信息 | 2 | 14 |
| 辅营服务 | 2 | 5 |
| 航班及客票状态 | 5 | 12 |
| 获取出票信息 | 2 | 7 |
| 特殊航司 | 2 | 5 |
| 工单 | 1 | 6 |
| 小计 | **26** | **108** |

## 其余 8 个一级分类

| 分类 | 目录 | parent | child |
|---|---|---|---|
| ATRIP | [01-ATRIP/_rag-chunks/](01-ATRIP/_rag-chunks/) | 1 | 5 |
| 支付 | [02-支付/_rag-chunks/](02-支付/_rag-chunks/) | 3 | 15 |
| 售前票务 | [03-售前票务/_rag-chunks/](03-售前票务/_rag-chunks/) | 3 | 12 |
| 财务 | [05-财务/_rag-chunks/](05-财务/_rag-chunks/) | 2 | 9 |
| 账单管理 | [06-账单管理/_rag-chunks/](06-账单管理/_rag-chunks/) | 1 | 6 |
| 通知提醒 | [07-通知提醒/_rag-chunks/](07-通知提醒/_rag-chunks/) | 3 | 27 |
| 安全与合规 | [08-安全与合规/_rag-chunks/](08-安全与合规/_rag-chunks/) | 2 | 17 |
| Atlas功能 | [09-Atlas功能/_rag-chunks/](09-Atlas功能/_rag-chunks/) | 1 | 5 |
| 小计 | | **16** | **96** |

## 常见问题 FAQ（[10-常见问题/_rag-chunks/](10-常见问题/_rag-chunks/)）

不用 rule-unit schema，改为一问一答对（`chunk_id, parent_id, topic, level1_category, level2_category, question, answer, source_path`）：

| 板块 | QA 数 |
|---|---|
| API集成相关 | 81 |
| 客户服务相关 | 27 |
| 功能和内容相关 | 18 |
| 支付相关 | 10 |
| 小计 | **136** |

## 全站合计

- Rule-unit 结构（parent+child）：**44 parent / 221 child**
- FAQ QA 结构：**136 QA chunk**
- 结构化数据表：1 份（[退票时限结构化表.json](04-售后票务/退票/_rag-chunks/退票时限结构化表.json)，131 家航司）

## 统一 schema

**parents.jsonl**：`article_id, title, level1_category, level2_category, applicable_carrier, updated_at, source_path, summary, child_chunk_ids`

**children.jsonl**：`chunk_id, parent_id, section, rule_type, applicable_carrier, updated_at, text`

**FAQ jsonl**（10-常见问题 专用）：`chunk_id, parent_id, topic, level1_category, level2_category, question, answer, source_path`

## 需要注意的跨分类风险点

1. **售后票务内部**：退票/废票/改期三者场景高度相似，检索最容易混淆——已在 [04-售后票务/_rag-chunks-index.md](04-售后票务/_rag-chunks-index.md) 中给出建议（parent 摘要回带 + `level2_category` 前置过滤）。
2. **`09-Atlas功能` 已清理未发布页面**：`Atlas Security and Compliance.md` 和 `Atlas票务承诺.md` 曾被切片，后确认两者都不在该分类导航文件 `Atlas功能.md` 的链接列表中（GitBook 爬取带出的隐藏页面），已连同源文件和对应 chunk 删除，目前该分类只剩 `Atlas邮件服务.md` 一篇。
3. **`applicable_carrier` 字段口径不完全统一**：多数子类只有"通用"，但 04-售后票务/特殊航司 用了具体航司代码（W4/W6/W9），04-售后票务/改期 在个别 chunk 上用了"通用（仅适用于清单内航司）"这种半结构化写法——用这个字段做精确匹配前，建议先看一眼各子类 README 里的判断说明，不要假设它是严格枚举值。
