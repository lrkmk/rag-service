# 行李

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此页面将行李选择集成到预订流程中。

在以下情况下从此页面开始：

* 在预订前展示行李选项
* 获取当前行程的精确行李报价
* 将行李选择添加到预订体验中

### 常见问题

#### 何时应调用 `getLuggage.do`？

建议在支付前调用 `getLuggage.do` 作为一个推荐步骤。

展示行李信息有助于减少犹豫并提高转化率。

在 `verify.do`、`getOffers.do` 或 `getOfferPrice.do` 之后调用。

#### 应使用哪个标识符？

在 `getLuggage.do` 中发送 `offerId`。

使用来自 `verify.do` 的 `sessionId` 作为 `offerId`。

直接使用来自 `getOffers.do` 或 `getOfferPrice.do` 的 `OfferId`。

#### `getLuggage.do` 的请求限制是多少？

`getLuggage.do` 与 `seatAvailability.do` 共享一个 `60 QPM` 的附加服务池。

超过限制的请求返回 Atlas 错误码 `429`。

在重试前遵守返回的 `retryAfter` 值。

### 附加服务请求限制

Atlas 将 `getLuggage.do` 和 `seatAvailability.do` 在一个滚动 60 秒窗口内共同计数。

默认共享限制为 `60 QPM`。

一个繁忙的附加服务 API 可能消耗共享池，影响另一个。

#### 如何减少限制压力

避免在短时间内对同一行程重复查询行李。

在当前验证或报价上下文仍有效时重复使用。

当返回 `429` 时遵守 `retryAfter`。

### 主要 API

* `getLuggage.do`

### 应首先检查什么？

确认航司支持当前流程的行李升级。

确认当前验证或报价上下文仍然有效。

确认返回的行李产品仍然匹配您计划预订的行程。

### `getLuggage.do` 返回什么？

它返回当前行程的行李产品。

每个产品有自己的 `productCode`。

在选择行李时，在 `order.do` 中使用该 `productCode`。

### 适用场景

* 行李选项查询
* 预订前的精确行李定价
* 用于 `order.do` 的行李升级映射

### 最佳实践

首先选择行程。

然后在支付前作为推荐的转化步骤查询行李。

清晰的行李定价有助于提高旅客信心和附加率。

在 `order.do` 之前，保持行李映射在当前预订上下文中一致。

对于联程航班，保持同一方向连接航段间的行李选择一致。

### 注意事项

* 可用性取决于航司支持
* 行李规则因承运商而异
* 使用当前验证或报价上下文以获得准确定价

### 下一步操作

使用[创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)发送所选行李的 `productCode`（如需要）。

如果还需要座位选择，请使用[座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)。

### 相关页面

* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [获取报价价格](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [出票后附加服务](/api-wen-dang/product-guides/post-booking/post-ticketing-ancillaries.md)

### 完整 API 参考

在此查看完整的端点架构和示例：

[行李](/api-wen-dang/api-reference/booking-apis/baggage.md)
