# RAG 灌库脚本

## 依赖

```bash
pip install chromadb sentence-transformers
```

`sentence-transformers` 用于本地跑中文 embedding 模型（`BAAI/bge-large-zh-v1.5`）。Chroma 自带的默认 embedder 是英文模型，对中文效果差；一开始用的是多语言模型，后来换成了纯中文的 BGE，因为这批语料几乎全是中文，专门中文模型的语义捕捉比"被稀释"的多语言模型更准。如果你更想用云端 embedding（OpenAI/智谱等），把 `EMBEDDER` 换成 `embedding_functions.OpenAIEmbeddingFunction(...)` 之类即可，其余逻辑不用动。

**BGE 的不对称前缀，容易踩坑**：BGE 系列建议给*查询*文本加指令前缀（"为这个句子生成表示以用于检索相关文章："），但*文档*不用加。`ingest_chroma.py` 里灌库时是不加前缀的（符合规范）；`query_example.py` 里没有用 Chroma 的 `query_texts=` 自动 embedding（那样查询和文档会用同一套无前缀逻辑，前缀效果就丢了），而是直接用 `sentence-transformers` 手动 encode 查询文本（带前缀）后传 `query_embeddings=`。如果你以后自己加新的查询代码，记得也走这条路径，别偷懒用 `query_texts=`。

## 用法

```bash
python ingest_chroma.py   # 灌库，幂等，可重复跑
python query_example.py   # 三个查询示例：语义检索 / 航司过滤检索 / FAQ检索
```

## 产出

- `../chroma_db/` — Chroma 持久化目录（自动创建）
- `parents_lookup.json` — 44 条文章级 parent 摘要，按 `article_id` 存成扁平 JSON，不进向量库，查询时按 id 直接取

## 两个 collection

| collection | 来源 | 数量 | embed 的字段 |
|---|---|---|---|
| `atlas_rule_chunks` | 所有 `_rag-chunks/children.jsonl` | 221 | `section + text` |
| `atlas_faq_chunks` | `10-常见问题/_rag-chunks/*.jsonl` | 136 | `question`（answer 不参与embedding，只存metadata） |

`atlas_rule_chunks` 里每条记录的 metadata 额外拼了 `level1_category`/`level2_category`（从对应 parent 记录关联过来的，因为 Chroma 不支持跨 collection join，只能在灌库时就把这两个字段冗余写进 child 的 metadata，否则没法按分类过滤）。

## 没有进向量库的东西

`04-售后票务/退票/_rag-chunks/退票时限结构化表.json`（131家航司的退票时限）故意没有 ingest 进来——这是精确查表场景，不是语义检索场景。查询层建议单独加一个"航司代码 + 时限"的正则/规则匹配，命中了直接读这个 JSON，不要让它跟语义检索抢召回。

## 未验证

当前开发环境没有装 Python，这两个脚本没有实际跑过。逻辑本身是对着你现有的 jsonl schema 写的（字段名、null 处理、chunk_id 唯一性都核对过），但建议你本地先跑一遍 `ingest_chroma.py` 确认没有环境相关的报错（比如 sentence-transformers 首次运行会下载模型，需要联网）。
