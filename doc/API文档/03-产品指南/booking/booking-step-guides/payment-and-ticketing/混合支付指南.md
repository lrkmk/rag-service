# 混合支付指南

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当 VCC pass-through 失败且需要安全回退路径时使用此页面。

### 什么是混合支付

混合支付是针对单个预订的重试策略。

它在一次支付尝试失败后切换支付路径。

最常见的模式是：

* 首先尝试 **VCC pass-through**
* 如果失败，使用 **Deposit** 重试
* 或使用 **另一张卡** 重试

{% hint style="info" %}
混合支付是一种回退模式。

它不是 split payment（分拆支付）。
{% endhint %}

### 何时使用

在以下情况下使用混合支付：

* VCC pass-through 支付失败
* `pay.do` 成功，但航司拒绝扣款
* 原卡受限或无法继续使用
* 您希望将 Deposit 作为回退路径
* 搜索、验证或下单显示支持 VCC，但仍需要恢复路径

### 履约流程注意事项

对于通过 `getOfferPrice.do` 创建的订单，每次回退决策必须在 5 分钟出票窗口内完成。

不要等待延迟的人工审批。

每次重试前查询订单。

如果原订单已取消且支持重新生成，请在重新生成的订单上保持履约流程标识。

### 开始 VCC pass-through 前

首先检查以下要点：

* 确认运价在 `VendorFare` 中支持 VCC
* 设置 `paymentMethod: 3`
* 发送 `supportCreditTransPayment: "1"`
* 发送完整的 `creditCard` 数据
* 当航司要求时，发送完整的账单地址数据
* 如果运价或渠道不支持 VCC，直接使用 Deposit

```json
{
  "orderNo": "XXX",
  "supportCreditTransPayment": "1",
  "paymentMethod": 3,
  "creditCard": {
    "cardNumber": "4111111111111111",
    "cardExpireMonth": "12",
    "cardExpireYear": "2028",
    "cardCVV": "***",
    "cardHolderLastName": "ZHANG",
    "cardHolderFirstName": "SAN",
    "cardHolderCountry": "CN",
    "cardHolderCity": "SHANGHAI",
    "cardHolderPostCode": "200000",
    "cardHolderAddress": "XXX Road"
  }
}
```

### 混合支付与其他情况的区别

#### 混合支付 vs 普通重试

普通重试保持相同的支付方式。

示例：

* 超时后重试同一张 VCC
* 网络问题后重试同一个 `pay.do`

混合支付会更改支付路径。

示例：

* 从 VCC 切换到 Deposit
* 从一张失败的卡切换到另一张卡

#### 混合支付 vs 更换卡片

更换为另一张卡是一种常见的混合情况。

如果第一张 VCC 失败且订单仍可支付，用另一张 VCC 重试仍然算作回退路径。

#### 混合支付 vs 分拆支付

混合支付 **不** 意味着：

* 将一个订单金额分两次支付
* 部分用卡支付、部分用余额支付
* 在一个 `pay.do` 中提交两个支付来源

如果您的业务场景需要金额分拆，请使用其他方案处理。

### 决策指南

每次按以下顺序操作：

{% stepper %}
{% step %}

### 检查支付结果

确认 `pay.do` 是否失败，或者成功但后续在航司侧失败。
{% endstep %}

{% step %}

### 检查原订单是否仍可用

在任何重试前先查询订单。

仅在订单仍处于未支付且仍可支付时继续使用同一订单。

在履约流程中，请立即做出此决策。
{% endstep %}

{% step %}

### 选择下一个支付路径

使用通常的优先级：

1. 对于临时问题，重试原支付路径
2. 切换到另一张卡
3. 切换到 Deposit
   {% endstep %}

{% step %}

### 跟踪最终结果

支付后，持续查询订单直到出票完成或订单达到最终失败状态。
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
`pay.do` 成功并不意味着航司已经接受支付。

在检查最新订单状态之前不要重试。
{% endhint %}

### 常见支付场景

#### 场景 A：`pay.do` 失败

这是较简单的情况。

如果订单仍处于未支付状态，通常可以：

1. 重试相同的支付方式
2. 切换到另一张卡
3. 切换到 Deposit

当 VCC 失败且同一订单仍支持支付时，使用 Deposit。

```json
{
  "orderNo": "XXX",
  "paymentMethod": 1
}
```

#### 场景 B：`pay.do` 成功，但航司支付失败

这种情况需要特别谨慎。

Atlas 可能接受请求，但航司可能在后续拒绝扣款。

原订单随后可能会被自动取消。

在这种情况下：

1. 确认最终订单状态
2. 如果适用，等待取消事件
3. 重新生成订单
4. 使用 Deposit 或其他支持的卡支付新订单

对于 `getOfferPrice.do` 订单，仅在恢复路径仍在活跃履约窗口内时执行此操作。

### 简化示例

这是最常见的混合支付流程：

1. 创建订单
2. 使用 VCC 调用 `pay.do`
3. 航司拒绝扣款
4. 原订单被取消
5. 调用 `regenerateOrder.do`
6. 对新订单使用 Deposit 调用 `pay.do`
7. 查询订单直到出票完成

### 重新生成后支付

当原订单已取消或不再可支付时，从原订单号创建新订单。

```json
{
  "originalOrderNo": "{原订单号}"
}
```

然后支付新订单：

```json
{
  "orderNo": "{新订单号}",
  "paymentMethod": 1
}
```

### Webhook 示例

如果航司拒绝支付且订单被自动取消，可将 webhook 数据作为早期信号使用。

```json
{
  "type": "order.cancelled",
  "data": {
    "orderNo": "{被取消的订单号}",
    "errorCode": "604",
    "errorMessage": "Payment declined by airline"
  }
}
```

### VCC pass-through 的主要风险

以下是混合支付场景中的常见问题：

* `pay.do` 成功并非最终业务结果
* 航司可能在 Atlas 接受请求后拒绝支付
* 卡品牌或卡类型不匹配可能直接导致失败
* 缺少账单地址可能触发航司拒绝
* 退款通常返回原卡，而非 Deposit
* 未经状态检查的重试可能导致重复扣款风险

### ATRIP 流程

{% stepper %}
{% step %}

### 找到原订单

打开 **ATRIP Flight Deck** 并进入 **My Orders**。

首先找到失败的订单。
{% endstep %}

{% step %}

### 如果需要，重新生成订单

当原订单已取消或无法再支付时，使用 **Regenerate Order**。
{% endstep %}

{% step %}

### 使用回退方式支付

打开新订单并选择 **Deposit** 或其他支持的卡。
{% endstep %}
{% endstepper %}

如果您遇到 API 集成问题，也可以登录 Eva 寻求支持。

### API 流程

{% stepper %}
{% step %}

### 重试前查询

在每次支付重试前检查最新的订单状态。
{% endstep %}

{% step %}

### 决定是否复用订单

仅在订单仍处于未支付且仍可支付时复用同一订单。

如果已取消，先重新生成。

当订单来自 `getOfferPrice.do` 时，在流程支持的情况下，在重新生成的订单上保持履约流程标识。
{% endstep %}

{% step %}

### 使用支持的方式重试

对于临时问题，使用相同方式重试。

当回退路径支持时，切换到 Deposit 或其他卡。
{% endstep %}
{% endstepper %}

### 最佳实践

* 在每次支付尝试前检查支持的支付方式
* 在首次 VCC 支付前确认 `VendorFare` 中支持 VCC
* 在需要时发送完整的卡数据和账单地址
* 不要重复使用被拒绝或一次性 VCC
* 航司拒绝后不要继续支付原订单
* 在自动取消情况下监听 webhook 事件
* 记录原订单号、新订单号、错误码和切换原因
* 将 VCC 退款与 Deposit 退款分开对账
* 在切换到 Deposit 时保留原始失败原因
* 在履约流程中避免依赖需要缓慢人工审核的回退路径

### 相关页面

* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [履约 API](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)
* [支付](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-payments.md)
* [查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)
* [支付错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/payment-errors.md)
* [订单维护](/api-wen-dang/product-guides/post-booking/order-maintenance.md)
* [重新生成订单](/api-wen-dang/api-reference/post-booking-apis/regenerate-order.md)
