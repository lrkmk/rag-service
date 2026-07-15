# Atlas功能子分类 — RAG 切片

对「09-Atlas功能」下唯一的一篇源文章做的切片。跳过 `Atlas功能.md`（纯导航/链接列表，无实质内容）。

`Atlas Security and Compliance.md` 和 `Atlas票务承诺.md` 曾经也在本目录下并被切过片，但两者都不在导航文件 `Atlas功能.md` 的链接列表中——核实为 GitBook 爬取时带出的未发布/隐藏页面，不是站点实际可导航到的内容，已连同源文件和对应 chunk 一起删除。

## 文件

- `parents.jsonl` — 文章级 parent 记录（1 条），含一句话摘要 + child_chunk_ids
- `children.jsonl` — 规则单元级 child 记录（5 条）

## 源文章覆盖

| article_id | 源文件 | level2_category | child 数 |
|---|---|---|---|
| af-atlas-youjian-fuwu | Atlas邮件服务.md | 邮件服务 | 5 |

## 切分依据

1. **文章为最小一级边界**。
2. **规则单元整段保留**：按源文档的条款小标题切分。
3. **航司特例**：本文章为Atlas平台通用条款，不涉及具体航司差异，`applicable_carrier` 统一为"通用"。
4. **Metadata 字段**：含 `level1_category`（Atlas功能）、`level2_category`（邮件服务）、`applicable_carrier`（"通用"）、`updated_at`、`source_path`。
5. **`updated_at` 为 `null`**：源文档未标注"最后更新日期"。
