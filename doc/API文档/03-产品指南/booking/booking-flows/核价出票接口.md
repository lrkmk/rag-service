# 核价出票接口

路径：`Get Offer Price → Order → Payment → Query Order`

当您需要履约路径且您的系统可以立即进入支付时，使用此流程。

本页面定义了该路径的端到端序列。

当您需要某一端点的步骤级详情时，请使用[预订步骤指南](/api-wen-dang/product-guides/booking/booking-step-guides.md)。

### 何时使用此流程

当以下任一情况适用时，使用此流程：

1. **临近起飞出票**：避免标准路径的缓存过期压力。
2. **已有订单上下文**：您已持有航班或运价，并需要 Atlas 完成履约。
3. **多人订单实时核价**：在出票前确认价格，降低价格漂移风险。
4. **需要更多报价或附加服务**：使用更广泛的展示规则，并在订单前添加座位或行李。
5. **支持即时支付**：使用预存款或 VCC 直通支付，并能立即创建和支付订单。

{% hint style="warning" %}
此流程不适合无法立即支付的体验。

订单创建后，必须在 **5 分钟内**完成支付和出票。

**U2 和 9C** 不支持此流程。请对这些航司使用标准预订路径。
{% endhint %}

### 完整流程

{% stepper %}
{% step %}

### 获取报价价格

调用[获取报价价格](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)。

保留返回的 `OfferId`。
{% endstep %}

{% step %}

### 可选附加服务

此步骤为可选。

当座位或行李追加销售是您产品的一部分时，在订单创建前使用[可选附加服务](/api-wen-dang/product-guides/booking/optional-ancillaries.md)。
{% endstep %}

{% step %}

### 创建订单

仅在可以立即开始支付时，使用 `OfferId` 调用[创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)。

保留 `orderNo`。
{% endstep %}

{% step %}

### 支付与出票

立即调用[支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)。

将 5 分钟支付和出票窗口视为严格的。
{% endstep %}

{% step %}

### 查询订单

使用[查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)作为支付后的标准跟进步骤。

持续跟进订单，直到出票或取消。

使用[支付后轮询](/api-wen-dang/product-guides/booking/booking-step-guides/query-order/post-payment-polling.md)了解轮询时机和重试指导。
{% endstep %}
{% endstepper %}

### 关键规则

* 从 `getOfferPrice.do` 保留 `OfferId` 直到 `order.do`
* 订单创建后立即开始支付
* 将 5 分钟履约窗口视为严格的
* 在 `order.do` 后保留 `orderNo`
* 通过订单查询或 webhook 跟进最终状态
* 出票完成后保留航司 PNR 和 `ticketNos`

### 决策支持

当您在获取报价和获取报价价格之间做选择时，使用[获取报价 vs 获取报价价格](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/get-offer-vs-get-offer-price.md)。

当您需要了解适用场景、支付路径、定价或失败处理时，使用[Fulfilment API FAQ](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/fulfilment-api-faq.md)。

当您需要预订前 API 的请求限制指导时，使用[API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)。

当您需要精确的请求和响应字段时，使用[API 参考](/api-wen-dang/api-reference.md)。
