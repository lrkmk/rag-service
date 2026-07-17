# 沙箱开发

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此页面在沙箱中构建并验证完整的 Atlas 集成。

{% hint style="warning" %}
首次接入时，Atlas 中可能尚未配置结算币种。

在沙箱环境下，在账户设置完成前，请在 `Search` 请求中手动添加 `"currency":"USD"`。
{% endhint %}

{% hint style="info" %}
在构建集成之前，运行 [沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)。

用它来确认凭证、网络访问以及核心快乐路径，无需编写代码。
{% endhint %}

当您需要以下内容时，从这里开始：

* 构建完整的沙箱预订流程
* 验证 Webhook 处理和跟进逻辑
* 确认集成已准备好进行 UAT

### 常见问题

#### 沙箱开发开始前应该完成什么？

沙箱凭证应首先可用。

请求头、请求格式和 gzip 处理也应准备就绪。

#### 什么证明沙箱开发已完成？

完整的预订流程应能稳定地端到端运行。

您的团队还应能够重现预期的成功和失败路径。

### 本阶段的目标

在沙箱中构建端到端的集成流程。

此阶段应涵盖 API 执行和 Webhook 跟进。

### 快速设置检查

在完整的开发工作之前，使用 [沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)。

它验证 `搜索`、`校验`、`下单` 和 `支付`。

如果最终的检索步骤超时，将其视为出票轮询期间的预期行为。

### 沙箱可以验证什么

使用沙箱验证：

* 请求格式和请求头
* 搜索、校验、下单、支付和查询流程
* Webhook 处理和跟进逻辑
* 失败处理和边缘情况
* UAT 就绪性

### 沙箱不能证明什么

沙箱 **不** 证明：

* 生产库存质量
* 生产定价准确性
* 真实卡扣款行为
* 所有情况下的最终航司侧行为

将沙箱运价和结果仅视为测试用途。

### 开始之前

确保您已具备：

* 来自 ATRIP 的沙箱凭证
* 沙箱基础 URL：`https://sandbox.atriptech.com/`
* 已配置的请求头
* 准备好测试的基本服务端集成

### 在开发过程中使用 MCP

当您需要帮助找到正确的流程、页面或下一个 API 步骤时，使用 [MCP 辅助开发](/api-wen-dang/readme-1/integration-tools/mcp-assisted-development.md)。

它适用于：

* 映射从 `Search` 到 `Pay` 的流程
* 检查需要保留和重复使用的标识符
* 将错误路由到正确的故障排除页面

### 开发检查清单

在沙箱中完成以下项目：

* 配置身份验证和请求头
* 将您的客户端指向沙箱
* 实现搜索、校验、下单、支付和查询
* 注册并验证 Webhook
* 测试失败处理和边缘情况

在此阶段，保留并重复使用：

* `routingIdentifier`
* `sessionId`
* `orderNo`

### 推荐的构建顺序

{% stepper %}
{% step %}

### 确认沙箱设置

确保凭证、请求头、gzip 处理和沙箱基础 URL 正常工作。
{% endstep %}

{% step %}

### 构建预订流程

实现搜索、校验、订单创建、支付和订单查询。
{% endstep %}

{% step %}

### 添加 Webhook 处理

注册 Webhook 端点并验证事件投递和处理。
{% endstep %}

{% step %}

### 测试预期的失败场景

模拟支付和流程失败，确认错误处理按预期工作。
{% endstep %}

{% step %}

### 准备 UAT

保留可追溯的测试订单，并确认完整的沙箱流程稳定且可重复。
{% endstep %}
{% endstepper %}

### 测试模式

在测试模式下：

* 预订是模拟的
* 出票不会在真实航司执行
* 运价是沙箱运价
* 测试凭证仅适用于沙箱
* 生产凭证仅适用于生产环境

使用测试模式验证：

* 请求构造
* 预订状态转换
* 支付和出票逻辑
* 预期的错误处理
* Webhook 和跟进行为

### 沙箱运价行为

沙箱搜索结果来自 Atlas 沙箱数据。

覆盖范围和定价与生产环境不同。

不要将沙箱价格用于商业比较。

### 支付失败模拟

您可以在 `pay.do` 中触发常见的 VCC 错误路径。

#### 触发支付拒绝

使用：

* 持卡人名字：`Reject`

预期结果：

* `604` — 支付被航司拒绝

#### 触发 3DS 错误

使用：

* 持卡人名字：`Three DS`

预期结果：

* `616` — 3DS 身份验证

可以使用任何卡号和姓氏进行此特定的失败模拟。

### 沙箱参考数据

当您需要已发布的沙箱输入时，使用这些共享参考页面：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [沙箱测试航线](/api-wen-dang/support-and-reference/integration-reference/sandbox-test-data/sandbox-test-routes.md)
* [沙箱测试卡](/api-wen-dang/support-and-reference/integration-reference/sandbox-test-data/sandbox-test-cards.md)
* [集成参考](/api-wen-dang/support-and-reference/integration-reference.md)

### 完成此阶段的标准

您可以在沙箱中可靠地完成以下所有操作：

* 端到端运行预订流程
* 保留并重复使用 `routingIdentifier`、`sessionId` 和 `orderNo`
* 验证所需的支付路径
* 接收并处理所需的 Webhook 事件
* 重现预期的成功和失败案例

### 本阶段的产出

* 稳定的沙箱预订流程
* 已验证的 Webhook 处理
* 为 UAT 准备好的证据

### 下一步

沙箱流程稳定后，进入 [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)。

### 相关页面

* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [沙箱访问](/api-wen-dang/readme-1/making-requests.md)
* [沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)
* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
