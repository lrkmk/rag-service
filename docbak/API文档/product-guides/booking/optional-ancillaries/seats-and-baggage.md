# 座位

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此页面将座位选择集成到预订流程中。

在以下情况下从此页面开始：

* 在预订前展示座位选项
* 确认是否支持座位选择
* 将座位选择添加到预订体验中

### 服务范围

Atlas 支持以下场景的座位选择：

* 支持 Atlas API 座位能力的航司
* Atlas 签发的订单
* 在预订流程中随机票购买的座位选择

Atlas 不支持以下场景的座位选择：

* 非 Atlas 签发的订单
* 出票后座位选择

非 Atlas 签发的订单由其他方出票。

在这种情况下，Atlas 仅用于在出票后添加座位服务。

### 常见问题

#### 何时应调用 `seatAvailability.do`？

建议在支付前调用 `seatAvailability.do` 作为一个推荐步骤。

座位选择有助于提高旅客信心和订单转化率。

在 `verify.do`、`getOffers.do` 或 `getOfferPrice.do` 之后调用。

#### 可以使用哪些标识符？

使用来自 `verify.do` 的有效 `sessionId`，或来自 `getOffers.do` 或 `getOfferPrice.do` 的 `OfferId`。

不要仅凭航班数据调用。

#### 如果所选座位变得不可用怎么办？

这是一个出票阶段的规则。

适用于所选座位在出票时不再可用的情况。

Atlas 支持以下处理模式：

* `STOP_TICKET` — 停止出票，取消整个订单并退款
* `STOP_SEAT` — 出票，移除座位并退还座位金额
* `SIMILAR_SEAT` — 出票，由运营选择类似座位

对于 Deposit 客户，`STOP_SEAT` 可能需要分拆资金订单和 `credit note`。

Atlas 不公开 `SIMILAR_SEAT` 的相似性规则。

如果需要人工处理，运营人员在 OPSDeck 中选择类似座位。

在该预订的订单创建请求中选择处理模式。

#### `seatAvailability.do` 的请求限制是多少？

`seatAvailability.do` 与 `getLuggage.do` 共享一个 `60 QPM` 的附加服务池。

超过限制的请求返回 Atlas 错误码 `429`。

在重试前遵守返回的 `retryAfter` 值。

### 附加服务请求限制

Atlas 将 `seatAvailability.do` 和 `getLuggage.do` 在一个滚动 60 秒窗口内共同计数。

默认共享限制为 `60 QPM`。

一个繁忙的附加服务 API 可能消耗共享池，影响另一个。

#### 如何减少限制压力

避免在没有预订上下文变化的情况下重复查询座位。

在上游缓存当前的 `sessionId` 或 `OfferId` 映射。

当返回 `429` 时遵守 `retryAfter`。

### 主要 API

* `seatAvailability.do`

### SeatAvailability 调用规则

`seatAvailability.do` 仅支持与事务关联的调用。

使用以下标识符之一：

* 来自 `verify.do` 的 `sessionId`
* 来自 `getOffers.do` 的 `OfferId`
* 来自 `getOfferPrice.do` 的 `OfferId`

独立模式已不再可用。

不支持仅航班的座位报价请求。

### 应首先确认什么？

确认航司支持当前流程的座位选择。

确认当前会话或报价上下文对附加服务请求仍然有效。

确认座位请求仍然映射到原始预订上下文。

### 适用场景

* 座位图和座位升级支持
* 座位选择支持检查
* 支付前的座位决策

### 最佳实践

首先选择行程。

然后在支付前作为推荐的转化步骤查询座位。

将座位选择定位为预订旅程的标准部分。

在 `order.do` 之前，保持附加服务映射与当前预订上下文一致。

如果您的上游座位请求没有当前预订上下文，请先缓存 `sessionId` 或 `OfferId`。

然后将传入的航班匹配到缓存的 `sessionId` 或 `OfferId`。

如果没有匹配项，不要发送仅航班的 `seatAvailability.do` 请求。

### 注意事项

* 可用性取决于航司支持
* `seatAvailability.do` 需要有效的 `sessionId` 或 `OfferId`
* 不支持仅航班的座位请求
* 座位规则可能因承运商而异
* 座位出票处理应在 `order.do` 之前选择

### 下一步操作

使用[创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)在需要时将所选附加服务数据随预订一起发送。

如果您还需要行李选项，请使用[行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)。

### 相关页面

* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [获取报价价格](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)
* [出票后附加服务](/api-wen-dang/product-guides/post-booking/post-ticketing-ancillaries.md)

### 完整 API 参考

在此查看完整的端点架构和示例：

[座位](/api-wen-dang/api-reference/booking-apis/inflow-seat-and-baggage.md)
