# 核价出票

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要履约 API 中的 `getOfferPrice.do` 行为、时机和恢复规则时，使用此页面。

当您需要完整的端到端预订序列时，从[履约 API](/api-wen-dang/product-guides/booking/booking-flows/fulfillment-flow.md) 开始。

此页面仅涵盖履约 API 的入口步骤。

它不替代完整的履约 API 路径。

当主要问题是产品契合度、与现有接口的共存、定价模式或航司覆盖范围时，请使用[履约 API 常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/fulfilment-api-faq.md)。

当您已经知道目标订单上下文，并且需要 Atlas 在严格的出票窗口内启动快速履约链时，使用此步骤。

### 常见问题

#### 何时应使用 `getOfferPrice.do`？

当您需要更广泛的展示规则和快速的出票截止时间时，使用 `getOfferPrice.do`。

此步骤适用于紧急出票、高风险库存情况以及被标准 Get Offer 展示策略有意排除的场景。

#### `getOfferPrice.do` 与 `getOffers.do` 有何不同？

`getOfferPrice.do` 是履约 API 的核心入口 API。

它允许更广泛的报价可见性，使用自己的请求限制策略，并在订单创建后应用 5 分钟的履约窗口。

#### 我可以将 `getOfferPrice.do` 与现有的 Atlas 接口一起使用吗？

可以。

履约 API 是一个额外的履约渠道。

当不同的业务场景需要不同的预订路径时，可以与标准流程并行使用。

#### 此步骤放宽了哪些限制？

此步骤可以返回通常在标准 Get Offer 路径中被过滤的报价。

放宽的规则包括：

* 临近出发的航班
* 售罄风险场景
* 高于 `OW + OW` 的往返价格

对于临近出发的情况，此路径不受请求提交后相同缓存过期压力的约束。

#### 此步骤触发了什么下游截止时间？

通过履约 API 创建的订单有 5 分钟的支付和出票窗口。

如果出票未及时完成，Atlas 将自动取消订单。

### 主要 API

* `getOfferPrice.do`

### 此路径中的下游 API

在 `getOfferPrice.do` 之后，通常的履约 API 链继续：

* `getLuggage.do`
* `seatAvailability.do`
* `order.do`
* `pay.do`
* `queryOrderDetails.do`

### `getOfferPrice.do` 的变化

#### 更广泛的报价可见性

`getOfferPrice.do` 可以显示标准 `getOffers.do` 可能隐藏的库存。

这使得它对紧急或更难履约的场景很有用。

#### 独立的请求治理

`getOfferPrice.do` 使用自己的 QPM 策略。

不要假设它与 `verify.do` 或 `getOffers.do` 共享相同的池。

#### 更快的操作截止时间

此步骤导致的操作窗口比标准预订保留时间短得多。

规划完整链以实现即时支付和主动跟进。

#### 不同的集成范围

这是履约 API 中的一个入口接口，而不是完整的标准搜索链。

对于已经持有所需订单上下文的团队，集成通常可以在大约 1 小时内完成。

### 5 分钟履约规则

Atlas 期望整个履约 API 链快速完成。

使用以下规则：

* 仅在准备好支付时才创建订单
* 立即完成支付，不要延迟
* 持续轮询直到最终出票或最终失败
* 当订单已超出允许窗口时停止重试

{% hint style="warning" %}
不要将履约 API 视为标准订单保留流程。

操作窗口是 5 分钟，而不是 30 分钟。
{% endhint %}

### 重试和超时处理

在每次重试前检查剩余时间。

作为工作规则，仅在订单仍在安全的 4 分钟操作窗口内时重试。

如果订单已接近超时，避免另一次支付重试，先查询最新的订单状态。

如果出票在 5 分钟内仍未完成，Atlas 将自动取消订单。

### 订单标识和恢复

通过履约 API 创建的订单应保留其履约 API 标识。

如果您需要在支持的取消路径后重新生成订单，在重新生成的订单上保留相同的履约 API 标记。

仅当原始订单不再可支付且恢复路径支持重新生成时，使用 `regenerateOrder.do`。

### 航司范围

默认范围是所有航司。

U2 和 9C 目前被排除在履约 API 之外。

它们无法可靠地满足 5 分钟出票要求。

对于 U2 和 9C，请改用标准预订路径。

在这些排除之外，履约 API 由 Atlas 的 100 多个直接官方航司连接支持，并持续扩展。

### 此步骤在完整路径中的位置

{% stepper %}
{% step %}

### 获取报价

调用 `getOfferPrice.do` 并保留返回的 `OfferId`。
{% endstep %}

{% step %}

### 在需要时添加附加服务

当座位或行李追加销售是您产品的一部分时，在订单创建前查询 `getLuggage.do` 或 `seatAvailability.do`。

在履约 API 中使用返回的 `OfferId` 作为附加服务上下文。
{% endstep %}

{% step %}

### 创建订单

仅在支付可以立即开始时，使用 `OfferId` 调用 `order.do`。

将订单创建视为严格履约窗口的开始。
{% endstep %}

{% step %}

### 支付订单

一旦订单准备就绪，立即调用 `pay.do`。

在履约 API 中不要延迟支付。
{% endstep %}

{% step %}

### 跟进出票到最终状态

使用 `queryOrderDetails.do` 直到订单出票或取消。

Webhook 可以提供帮助，但不应该是您唯一的确认路径。
{% endstep %}
{% endstepper %}

### 最佳实践

* 仅将履约 API 连接到快速支付用户体验
* 保持重试逻辑保守
* 使用 `orderNo` 记录履约 API 标记
* 对超时取消和支付失败进行分开监控
* 使用符合 5 分钟 SLA 的航司允许列表或阻止列表

### 失败告警时机

失败告警会在出票失败确认后的 6 分钟内发出。

请使用 `queryOrderDetails.do` 作为最终订单状态的真实来源。

### 相关页面

* [履约 API](/api-wen-dang/product-guides/booking/booking-flows/fulfillment-flow.md)
* [履约 API 常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/fulfilment-api-faq.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)
* [API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)
* [核价出票](/api-wen-dang/api-reference/booking-apis/get-offer-price.md)
