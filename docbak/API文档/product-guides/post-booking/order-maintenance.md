# 订单维护

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此页面处理标准预订流程之外的订单跟进操作。

当您需要以下内容时从这里开始：

* 重建已过期或失败的订单
* 在流程支持时停止出票
* 查询订单以进行运营跟进

### 常见问题

#### 何时应该使用订单维护？

在标准搜索到出票流程之外的运营订单操作时使用此页面。

#### 应该先使用哪个维护 API？

对于符合条件的订单重建使用 `regenerateOrder.do`，当必须停止出票时使用 `stopTicket.do`，当需要运营订单查询时使用 `orderList.do`。

#### 履约流程订单可以重建吗？

可以，当恢复路径支持该订单状态的恢复操作时即可。

首先确认原始订单已不可用。

当下游流程需要时，在重建的订单上保留履约流程身份标识。

### 主要 API

* `regenerateOrder.do`
* `stopTicket.do`
* `orderList.do`

### 在以下情况使用此页面

* 重建已过期或失败的订单
* 在支持时停止出票操作
* 搜索运营订单列表
* 在取消或航司侧支付失败后恢复符合条件的 `getOfferPrice.do` 订单

### 履约流程维护

谨慎对 `getOfferPrice.do` 订单执行维护操作。

在重建之前，确认原始订单已达到最终取消或不可支付状态。

不要使用维护操作来延长 5 分钟出票截止期限。

### 后续步骤

打开下方的精确端点页面查看请求和响应详情，然后根据需要将结果与当前订单状态进行核对。

### 完整 API 参考

在此查看端点级详细信息：

* [重建订单](/api-wen-dang/api-reference/post-booking-apis/regenerate-order.md)
* [停止出票](/api-wen-dang/api-reference/post-booking-apis/stop-ticket-issuance.md)
* [订单列表](/api-wen-dang/api-reference/post-booking-apis/order-list.md)

### 相关页面

* [预订后操作](/api-wen-dang/product-guides/post-booking.md)
* [预订后 API](/api-wen-dang/api-reference/post-booking-apis.md)
* [混合支付指南](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing/hybrid-payment-guide.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
