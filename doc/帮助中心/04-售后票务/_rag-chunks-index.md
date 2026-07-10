# 售后票务 — RAG 切片总索引

按 [退票/_rag-chunks/README.md](退票/_rag-chunks/README.md) 中定义的 7 条原则，对「04-售后票务」下全部 9 个子类完成切片。每个子类目录内的 `_rag-chunks/` 文件夹含 `parents.jsonl`（文章级摘要）、`children.jsonl`（规则单元级 chunk）、`README.md`（切法说明与该子类的具体判断记录）。

全部 `parents.jsonl` / `children.jsonl`已做 JSON 有效性校验，且 child → parent 的 `parent_id` 引用全部可解析，无孤儿引用。

| 子类 | parent 数 | child 数 | 备注 |
|---|---|---|---|
| [退票](退票/_rag-chunks/README.md) | 5 | 23 | 含结构化时限表（131家航司）+ FR/IJ 两个航司特例 |
| [废票](废票/_rag-chunks/README.md) | 3 | 23 | 快速指南文章本身是文档索引结构，故 chunk 偏多 |
| [改期](改期/_rag-chunks/README.md) | 4 | 13 | 两张航司适用清单（22/10家）各自成 chunk |
| [改乘客信息](改乘客信息/_rag-chunks/README.md) | 2 | 14 | 5 类改信息场景（姓名/证件/生日/国籍/性别）各自打 applicable_carrier |
| [辅营服务](辅营服务/_rag-chunks/README.md) | 2 | 5 | |
| [航班及客票状态](航班及客票状态/_rag-chunks/README.md) | 5 | 12 | |
| [获取出票信息](获取出票信息/_rag-chunks/README.md) | 2 | 7 | |
| [特殊航司](特殊航司/_rag-chunks/README.md) | 2 | 5 | Wizz 相关内容标注 `W4/W6/W9`（源文明确覆盖三个航司代码，未按标题简单标 W6） |
| [工单](工单/_rag-chunks/README.md) | 1 | 6 | |
| **合计** | **26** | **108** | |

另：[常见问题/FAQ](../10-常见问题/_rag-chunks/) 采用不同 schema（一问一答对，不做 rule_type 细分），136 条 QA chunk，按板块拆成 4 个 jsonl 文件（API集成相关 81、客户服务相关 27、功能和内容相关 18、支付相关 10）。

## 统一 schema

**parents.jsonl**：`article_id, title, level1_category, level2_category, applicable_carrier, updated_at, source_path, summary, child_chunk_ids`

**children.jsonl**：`chunk_id, parent_id, section, rule_type, applicable_carrier, updated_at, text`

## 已知的跨子类风险点

「退票 / 废票 / 改期」三个子类场景高度相似（都涉及申请流程、时限、SLA），检索时最容易互相混淆。建议：
1. 检索命中 child 后务必带出 parent 摘要，让模型先确认这条规则属于哪个子类，再作答；
2. 如果上层能拿到用户明确提到的动作词（退票/废票/改期），可以直接用 `level2_category` 做检索前过滤，而不是完全依赖向量相似度。
