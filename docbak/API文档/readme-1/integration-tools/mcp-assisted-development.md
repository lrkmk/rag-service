# MCP 辅助开发

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用 GitBook MCP 加速 Atlas API 开发。

它帮助您找到正确的页面、理解流程并更快地确定下一步。

如果您想要一个打包的助手设置，请使用 [Atlas AI 助手技能](/api-wen-dang/readme-1/integration-tools/atlas-ai-assistant-skill.md)。

### 何时使用 MCP

当您需要以下内容时，使用 MCP：

* 找到任务的正确 API 流程
* 了解下一步需要哪个标识符
* 比较类似 API，例如 `search.do` 和 `getOffer.do`
* 找到错误的正确故障排除页面
* 在沙箱中更快地推进，无需猜测

### MCP 最擅长的领域

MCP 在开发期间作为文档助手效果最佳。

用它来：

* 绘制从 `Search` 到 `Pay` 的预订流程
* 识别哪个页面解释了某个字段或状态
* 查找 Webhook、退款或工具 API 的相关指南
* 在编码前缩小要打开的页面范围

### 推荐的 Atlas 使用场景

#### 开始沙箱构建

让 MCP 概述最低限度的沙箱流程。

然后根据这些页面进行验证：

* [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [API 参考](/api-wen-dang/api-reference.md)

#### 在预订流程中推进

每次成功调用后，使用 MCP 确认下一步。

典型序列：

* `Search` → 保留 `routingIdentifier`
* `Verify` → 保留 `sessionId`
* `Create Order` → 保留 `orderNo`
* `Payment & Ticketing` → 轮询并确认最终状态

#### 更快地排除故障

使用 MCP 将错误路由到正确的故障排除部分。

好的起点：

* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)

### 效果良好的提示模式

使用简短、基于任务的提示。

示例：

* 展示最低限度的 Atlas 沙箱预订流程。
* 我有 `routingIdentifier`。下一步应该调用什么？
* 比较 `Verify` 和 `Get Offer` 在新集成中的使用。
* 在实现出票轮询之前，我应该阅读哪些页面？
* 支付拒绝故障排除应该去哪里查找？
* 出票完成后，哪些 Webhook 页面重要？

### 基本规则

将 MCP 用作导航和实施辅助工具。

遵守这些规则：

* 将 [API 参考](/api-wen-dang/api-reference.md) 视为字段和模式的权威来源
* 不要在提示中包含生产密钥
* 根据您的实际环境验证请求详情
* 在上线前完成 [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)

{% hint style="info" %}
GitBook MCP 可在 [MCP 端点](https://resources.atriptech.com/~gitbook/mcp) 获取。
{% endhint %}

### 建议的工作流程

1. 使用 MCP 找到正确的流程。
2. 打开匹配的概述或指南页面。
3. 在 [API 参考](/api-wen-dang/api-reference.md) 中确认字段和模式。
4. 在 [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md) 中构建和验证。
5. 当调用或状态转换失败时，使用故障排除页面。
6. 流程稳定后，进入 [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)。

### 相关页面

* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [故障排除与支持](/api-wen-dang/support-and-reference/troubleshooting-and-support.md)
