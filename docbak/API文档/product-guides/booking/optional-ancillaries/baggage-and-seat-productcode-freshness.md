# 行李与座位产品代码时效性

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当座位或行李选择因附加服务映射可能过期而失败时，使用此页面。

### 简要说明

将行李和座位的 `productCode` 值视为预订上下文数据，而不是可重用的目录 ID。

如果验证上下文、报价上下文、行程、乘客组合或预订时机发生变化，请在 `order.do` 之前刷新附加服务。

### 常见问题

#### 我可以重复使用旧的行李 `productCode` 吗？

不安全。

使用当前附加服务响应返回的 `productCode` 用于当前预订上下文。

#### 我可以重复使用旧的座位选择吗？

不安全。

座位可用性可能在预订或出票前发生变化。

#### 何时应刷新附加服务？

当预订上下文发生变化或预订被延迟时刷新。

### 这里的新鲜度含义

`productCode` 仅在当前预订上下文中有意义。

该上下文包括：

* 当前行程
* 当前乘客组合
* 当前验证或报价状态
* 当前附加服务响应

不要将附加服务代码视为长期有效的静态值。

### 什么会使附加服务选择过期

当以下任何一项发生变化时，刷新行李或座位选择：

* `sessionId`
* `OfferId`
* 目标航班
* 航段结构
* 乘客数量或乘客类型
* 运价或库存状态
* 预订延迟足够长，使旧上下文变得不可靠

### 行李新鲜度规则

#### 使用最新的行李响应

使用当前 `getLuggage.do` 响应中的行李 `productCode`。

#### 保持航段映射精确

确保每个行李选择仍然匹配正确的航段。

#### 保持同向连接选择的一致性

对于联程航班，行李可能需要在同一方向上的连接航段间保持一致。

### 座位新鲜度规则

#### 使用最新的座位响应

使用当前 `seatAvailability.do` 响应中的座位数据。

#### 不要假设座位之后仍然存在

座位库存可能在预订前发生变化，在出票时也可能再次变化。

#### 保持出票行为明确

在 `order.do` 中设置座位处理模式。

这控制在出票时所选座位消失时的处理方式。

### 常见失败信号

典型的过期附加服务失败包括：

* `309` — 附加服务 `productCode` 无效或过期
* `409` — 行李 `productCode` 与航段不匹配
* 会话或报价更改后的座位或行李不匹配

### 快速决策规则

在生产中使用此规则：

* 新的 `sessionId` 或新的 `OfferId` — 刷新附加服务
* 行程或乘客组合发生变化 — 刷新附加服务
* 预订延迟 — 在 `order.do` 之前刷新附加服务

### 常见错误

#### 在新的验证会话中重复使用行李 `productCode`

不要这样做。

新的 `sessionId` 意味着旧的附加服务上下文可能已过期。

#### 行程更改后重复使用座位选择

不要这样做。

即使小的航班更改也可能破坏座位映射。

#### 将 `productCode` 视为永久的 SKU

不要这样做。

它是与上下文绑定的预订数据。

### 最佳实践

将附加服务选择保持在接近订单创建的位置。

如果预订被延迟，在 `order.do` 之前重新运行附加服务查询。

### 相关页面

* [座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)
* [行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
