# 通知提醒 — RAG 切片

对「07-通知提醒」下 3 篇源文章做的切片，沿用「04-售后票务/退票」示例的同一套原则与字段结构。已跳过 `通知提醒.md`（纯导航/链接列表，无实质内容）。

## 文件

- `parents.jsonl` — 文章级 parent 记录（3 条），每条含一句话摘要 + child_chunk_ids
- `children.jsonl` — 规则单元级 child 记录（27 条）

## 切分依据

1. **文章为最小一级边界**：3 篇文章互不跨界拼接，每篇独立产出 1 个 parent + N 个 child（机票延迟通知 10 条、通知订阅 5 条、邮件列表 12 条）。
2. **规则单元整段保留**：没有按字数/token 数机械切断。例如 `yc-c06`（服务请求创建条件）把"仅延迟原因为等待客户确认"这一条件与"需回复响应"的结论保持在同一 chunk；`yj-c08`（处理电子邮件）把两种处理入口（View+Handle / 批量处理）与其后可选的 5 种处理状态作为一个不可拆分的操作单元完整保留。
3. **航司特例单独打标签**：本类目三篇文章均为平台通用功能说明，不涉及具体航司差异化规则，因此 `applicable_carrier` 全部为 `通用`，未出现航司特例标签。
4. **Parent-Child 结构**：每个 child 都有 `parent_id`，检索命中 child 后可回带 parent 的一句话摘要，帮助模型判断这条规则出自"机票延迟通知""通知订阅"还是"邮件列表"——三者场景相近（都涉及邮件/Webhook 配置），容易混淆。
5. **操作步骤按步骤号切分**：DingTalk、Slack 的两步配置流程（获取机器人参数 → 运营台配置客户端/Webhook URL）分别拆成独立 child（如 `yc-c07`/`yc-c08`），保持每步的前置条件与产出值（access_token、secret、webhook URL）完整可查。
6. **Metadata 字段**：每条 child 含 `level1_category`（通知提醒）、`level2_category`（按文章区分为"机票延迟通知"/"通知订阅"/"邮件列表"）、`applicable_carrier`、`updated_at`（本类目三篇源文章均未在导航文件中标注"最后更新日期"，故全部记为 null）、`source_path`（可追溯到本地归档原文件）。
7. **API/接口字段说明整体保留**：`邮件列表.md` 中的 Email List API 请求参数、响应字段、Webhook 通知字段分别整体保留为 `yj-c10`/`yj-c11`/`yj-c12` 三个 chunk，不逐字段拆分——检索"这个 API 有哪些参数"时应返回完整字段表，拆散会丢失参数之间的关联（如 `emailReceivingDateEnd` 与"最多查询一个月"的限制必须绑在同一条里）。

## 示例：一条完整 child 记录

```json
{
  "chunk_id": "yj-c10",
  "parent_id": "youjian-liebiao",
  "section": "Email List API－请求",
  "rule_type": "功能说明",
  "applicable_carrier": "通用",
  "updated_at": null,
  "text": "电子邮件列表API请求：端点为 https://api-sg.atriptech.com/mail.do。请求字段：orderNo（可选，订单号）；emailReceivingDateStart（可选，接收时间起）；emailReceivingDateEnd（可选，接收时间止，一次只能查询最多一个月的数据）；……pageIndex（必填，分页页码）；pageSize（必填，每页记录数，最大值为1000）。"
}
```

## 未覆盖范围

`通知提醒.md`（导航列表页）未纳入切片。若后续新增该类目下的文章，可按同一方式补充。
