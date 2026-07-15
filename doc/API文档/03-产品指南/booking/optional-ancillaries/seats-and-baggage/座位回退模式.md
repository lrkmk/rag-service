# 座位回退模式

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您的预订流程包含付费座位且您必须决定如果所选座位不再可用时 Atlas 应如何处理时，使用此页面。

### 简要说明

当座位对预订是强制性的时候，使用 `STOP_TICKET`。

当出票比座位更重要时，使用 `STOP_SEAT`。

当 Atlas 可以使用替代座位完成出票时，使用 `SIMILAR_SEAT`。

### 常见问题

#### 这些模式何时使用？

它们在所选座位在出票时不可用时应用。

您在 `order.do` 中选择模式。

#### 模式是否影响出票？

是的。

每种模式定义 Atlas 是应停止出票、继续出票但不含座位，还是继续出票并使用类似座位。

#### 相似性逻辑是否在 API 中公开？

否。

Atlas 不公开 `SIMILAR_SEAT` 的相似性规则。

### 核心区别

#### `STOP_TICKET`

**作用**

停止出票。

取消整个订单。

退款。

**何时使用**

当所选座位对业务至关重要时使用。

适用于失去座位意味着旅客不应被出票的产品。

#### `STOP_SEAT`

**作用**

出票。

移除座位。

退还座位金额。

**何时使用**

当出票比座位确定性更重要时使用。

适用于即使付费座位失败也应继续行程的产品。

**操作说明**

对于 Deposit 客户，这可能需要分拆资金订单和 `credit note`。

#### `SIMILAR_SEAT`

**作用**

由运营选择类似座位后出票。

**何时使用**

当旅客希望获得座位结果但不需要完全相同的原始座位时使用。

**操作说明**

如果需要人工处理，运营人员在 OPSDeck 中选择类似座位。

### 快速决策规则

在生产中使用此规则：

* 精确座位是强制性的 — `STOP_TICKET`
* 即使没有座位也必须继续行程 — `STOP_SEAT`
* 类似座位可接受 — `SIMILAR_SEAT`

### 常见错误

#### 在业务设计中未定义模式

不要这样做。

缺失业务规则会使座位失败处理变得不可预测。

#### 为低价值座位升级选择 `STOP_TICKET`

默认情况下不要这样做。

它可能因非关键附加服务而取消整个预订。

#### 未经业务接受选择 `SIMILAR_SEAT`

不要这样做。

您的产品团队必须接受最终座位可能不同。

### 最佳实践

将回退模式作为产品决策，而不仅仅是技术字段。

在 `order.do` 之前决定，并使其与您的旅客承诺保持一致。

### 相关页面

* [座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [行李和座位 productCode 新鲜度](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage-and-seat-productcode-freshness.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
