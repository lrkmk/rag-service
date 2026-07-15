# 支付与出票

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此页面完成支付并等待出票。

在以下情况下从此页面开始：

* 支付现有订单
* 选择正确的支付方式
* 在 `pay.do` 之后追踪最终出票状态

### 常见问题

#### 调用 `pay.do` 前需要准备什么？

您需要有效的 `orderNo`、支持的支付方式，以及当使用卡支付时需要卡数据。

订单必须仍处于未支付状态且仍支持所选支付路径。

#### 支付成功是否意味着出票已完成？

否。

支付成功并不总是意味着航司 PNR 和票号已经是最终状态。

请使用订单跟进直到最终出票状态得到确认。

#### 履约 API 订单的截止时间是否不同？

是。

通过 `getOfferPrice.do` 创建的订单使用 5 分钟支付和出票窗口。

如果出票未能及时完成，Atlas 会自动取消订单。

#### 履约 API 支持哪些支付路径？

Fulfilment API 支持预存款（Deposit）和 VCC 直通（VCC pass-through）两种支付方式。

这为您提供了两条可操作的支付路径。

当其中一条路径不可用时，只要当前订单状态允许，您可以切换到另一条。

### 主要 API

* `pay.do`

### 适用场景

* Deposit 支付
* VCC pass-through 支付
* BYOA 支付
* MoR 支付
* 支付后出票跟踪

### 调用前确认

首先确认以下要点：

* 订单已存在
* 订单仍处于未支付状态
* 订单支持所选支付方式
* 如果使用卡支付，卡数据已准备好

对于标准流程，在 `pay.do` 之前先调用 `order.do`。

### 支付后需要注意什么？

持续使用 `orderNo` 进行订单跟进。

通过订单查询读取最终出票状态。

当支付可能正在进行或已完成时，不要发送重复的支付请求。

### 支付方式

* `1`：Deposit
* `3`：VCC pass-through
* `4`：BYOA
* `5`：MoR

### 关键输入

始终发送：

* `orderNo`
* `paymentMethod`

在以下情况下发送 `creditCard`：

* VCC pass-through
* MoR

`threeDS.ip` 仅与 MoR 相关。

### 下一步操作

在 `pay.do` 之后，使用[查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)直到确认最终出票状态。

使用 webhook 作为补充，而不是唯一的确认方式。

### 注意事项

* 支持的支付方式因航司和运价而异
* 卡品牌必须符合订单要求
* 如果预订超过截止时间，支付可能失败
* 支付成功并不总是意味着出票已完成
* 仍需订单跟进直到最终出票状态得到确认

### 最佳实践

* 在支付前从预订流程中读取支持的支付方式
* 当需要在支付后获得运价保证时，使用 Deposit
* 仅在运价支持时使用 VCC
* 支付后轮询订单状态直到出票完成
* 谨慎处理支付重试以避免重复扣款

### 履约 API 截止时间

当订单来自 `getOfferPrice.do` 时，应用以下额外规则：

* 订单创建后立即开始支付
* 每次重试前检查剩余时间
* 仅在订单仍在安全操作窗口内时重试
* 订单接近超时时停止重试

{% hint style="warning" %}
不要将标准的 30 分钟订单保留期应用于履约 API 订单。

此流程围绕 5 分钟出票截止时间设计。
{% endhint %}

### 履约 API 支付适配

在以下情况下使用履约 API：

* 订单创建后立即支付
* Deposit 和 VCC pass-through 作为双支付路径
* 临近出发的出票，无需在请求提交后承受相同的缓存过期压力

对于已经持有所需订单上下文的团队，集成通常可以在大约 1 小时内完成。

### 安全重试规则

如果支付可能已经开始，请先查询订单。

在收到 `402`、`404`、`406` 或类似的订单状态错误后，不要盲目重试支付。

### 常见失败情况

常见的支付响应失败包括：

* 请求数据无效
* 超过截止时间后支付
* 不支持的支付方式
* 订单已支付
* 支付正在进行中
* 缺少乘客数据
* 卡不支持
* 卡不匹配
* 在 FR 流程中订单未确认

以 API 响应 `status` 作为事实依据。

### 履约 API 失败告警时机

失败告警会在出票失败确认后的 6 分钟内发出。

请使用 `queryOrderDetails.do` 作为最终订单状态的真实来源。

### 相关页面

* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [确认订单](/api-wen-dang/product-guides/booking/booking-step-guides/confirm-order.md)
* [查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)
* [混合支付指南](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing/hybrid-payment-guide.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [预订 API](/api-wen-dang/api-reference/booking-apis.md)

### 完整 API 参考

在此查看端点级别的详细信息：

* [支付与出票](/api-wen-dang/api-reference/booking-apis/payment-and-ticketing.md)
