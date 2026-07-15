# RAG 灌库脚本

## 目录结构

```
scripts/
  crawl/      从 resources.atriptech.com (GitBook) 抓取源文档 -> doc/ 下的原始 .md
  chunking/   源文档 .md -> _rag-chunks/*.jsonl 切片脚本
  ingest/     _rag-chunks/*.jsonl -> chroma_db 灌库脚本，含 parents_lookup.json
  search/     运行时查询/检索服务（rag_search.py / mcp_server.py 等），也是 Docker 镜像的实际负载
  eval/       检索质量评估（读写仓库根目录的 eval/*.jsonl，跟这里的 scripts/eval/ 是两回事：一个放数据一个放代码）
  deploy/     chroma_db 打包与分发脚本
  webapp/     本地切片对照浏览工具，不进 Docker 镜像
```

## 爬取（更新/新增文档）

`crawl/crawl_gitbook.py` 基于站点自带的两个特性：`https://resources.atriptech.com/llms.txt`（全站索引，title+url+简介）和"任意页面 URL 后加 `.md` 直接返回干净原始 markdown"。三个子命令：

```bash
python crawl/crawl_gitbook.py list 产品介绍           # 列出该语料库在 llms.txt 里的全部页面，找本地没有的新页面
python crawl/crawl_gitbook.py fetch <url> <output.md>  # 抓一篇存到指定路径
python crawl/crawl_gitbook.py diff-check 产品介绍 [--apply]  # 按标题把本地文件跟 llms.txt 匹配，抓新内容比对是否有改动（内容漂移检测），--apply 直接覆盖有改动的本地文件
```

不自动分类到编号目录（`01-ATRIP`、`04-售后票务`这类）——GitBook 的 URL slug 是拼音转写，不是分类路径，新页面放哪个类目是判断题，不是脚本能替你做的决定，`list`/`diff-check` 只负责把内容和改动找出来，人工/agent 读完再决定放哪、按什么类型切片（配合 `doc-chunking` skill）。

## 依赖

```bash
pip install chromadb sentence-transformers
```

`sentence-transformers` 用于本地跑中文 embedding 模型（`BAAI/bge-large-zh-v1.5`）。Chroma 自带的默认 embedder 是英文模型，对中文效果差；一开始用的是多语言模型，后来换成了纯中文的 BGE，因为这批语料几乎全是中文，专门中文模型的语义捕捉比"被稀释"的多语言模型更准。如果你更想用云端 embedding（OpenAI/智谱等），把 `EMBEDDER` 换成 `embedding_functions.OpenAIEmbeddingFunction(...)` 之类即可，其余逻辑不用动。

**BGE 的不对称前缀，容易踩坑**：BGE 系列建议给*查询*文本加指令前缀（"为这个句子生成表示以用于检索相关文章："），但*文档*不用加。`ingest/ingest_help_center.py` 里灌库时是不加前缀的（符合规范）；`search/query_example.py` 里没有用 Chroma 的 `query_texts=` 自动 embedding（那样查询和文档会用同一套无前缀逻辑，前缀效果就丢了），而是直接用 `sentence-transformers` 手动 encode 查询文本（带前缀）后传 `query_embeddings=`。如果你以后自己加新的查询代码，记得也走这条路径，别偷懒用 `query_texts=`。

## 用法

```bash
python ingest/ingest_help_center.py   # 帮助中心灌库，幂等，可重复跑
python ingest/ingest_api_docs.py      # API文档灌库
python ingest/ingest_product_intro.py # 产品介绍/资讯灌库
python search/query_example.py        # 三个查询示例：语义检索 / 航司过滤检索 / FAQ检索
```

## 增量更新（改/增/删文档）

- **改文档**：重新跑对应的 `chunking/chunk_*.py` 生成新的 `_rag-chunks/*.jsonl`，再跑 `ingest/ingest_*.py`。只要 `chunk_id` 没变，`upsert` 会直接覆盖旧内容。
- **新增文档**：正常走切片流程产出 `_rag-chunks/`，`ingest/ingest_*.py` 里的 `glob` 会自动捡到，`upsert` 新增即可，不用改脚本。
- **删文档 / 重新切片换了 chunk_id**：把对应的 `_rag-chunks/` 目录也一并删掉（否则下次 ingest 时 glob 还会捡到旧文件，等于没删），然后重新跑 `ingest/ingest_*.py`——每个 collection 的 `ingest_*` 函数末尾都会调用 `reconcile()`，把 Chroma 里存在但这次源文件没产出的 id 删掉。**只靠 `upsert` 不会清理这些孤儿向量**，必须靠 `reconcile()`（或手动 `collection.delete(ids=[...])`）。

跑完 `ingest/ingest_*.py` 之后，用 `scripts/eval/eval_retrieval.py` 跑一遍检索评估确认没有回归，再用 `scripts/deploy/publish_chroma_db.sh` 发布、服务器端 `scripts/deploy/deploy_chroma_db.sh` 拉取部署。

## 产出

- `../chroma_db/` — Chroma 持久化目录（自动创建）
- `ingest/parents_lookup.json` — 44 条文章级 parent 摘要，按 `article_id` 存成扁平 JSON，不进向量库，查询时按 id 直接取（由 `ingest/ingest_help_center.py` 生成，`search/rag_search.py` 查询时读取）

## 两个 collection

| collection | 来源 | 数量 | embed 的字段 |
|---|---|---|---|
| `atlas_rule_chunks` | 所有 `_rag-chunks/children.jsonl` | 221 | `section + text` |
| `atlas_faq_chunks` | `10-常见问题/_rag-chunks/*.jsonl` | 136 | `question`（answer 不参与embedding，只存metadata） |

`atlas_rule_chunks` 里每条记录的 metadata 额外拼了 `level1_category`/`level2_category`（从对应 parent 记录关联过来的，因为 Chroma 不支持跨 collection join，只能在灌库时就把这两个字段冗余写进 child 的 metadata，否则没法按分类过滤）。

## 没有进向量库的东西

`04-售后票务/退票/_rag-chunks/退票时限结构化表.json`（131家航司的退票时限）故意没有 ingest 进来——这是精确查表场景，不是语义检索场景。查询层建议单独加一个"航司代码 + 时限"的正则/规则匹配，命中了直接读这个 JSON，不要让它跟语义检索抢召回。
