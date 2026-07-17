# 预订 API

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

{% hint style="warning" %}
本网站中的 API 参考端点示例均使用 **沙箱** 基础 URL。

生产流量请使用 ATRIP 中 **My Profile** → **Company Information** 显示的生产 API 基础 URL。

生产环境使用 **两个** API 基础 URL：

* 一个用于 `search` 流量
* 一个用于其他所有交易类 API

不要将生产流量发送到沙箱端点。
{% endhint %}

使用本部分获取预订流程的端点级参考。

在需要请求字段、响应字段或端点示例时，从此处开始。

### 常见问题

#### 预订 Atlas 航班应使用哪些 API？

标准流程通常为搜索、验价、创建订单、支付与出票。

根据工作流，你还可以使用获取报价、座位或行李 API。

#### 应先阅读产品指南还是 API 参考？

需要选择流程或理解顺序时，先阅读[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)。

需要精确的字段、模式和示例时，使用本部分的端点页。

### 按任务选择端点

* [搜索](/api-wen-dang/api-reference/booking-apis/search.md) — 搜索航班报价。
* [验价](/api-wen-dang/api-reference/booking-apis/verify.md) — 确认实时价格和预订条件。
* [创建订单](/api-wen-dang/api-reference/booking-apis/create-order.md) — 建立待支付订单。
* [支付与出票](/api-wen-dang/api-reference/booking-apis/payment-and-ticketing.md) — 支付订单并跟进出票。
* [获取报价](/api-wen-dang/api-reference/booking-apis/get-offer.md) — 为已知行程获取独立报价。
* [Get Offer Price](/api-wen-dang/api-reference/booking-apis/get-offer-price.md) — 在履约路径中为报价定价。
* [座位](/api-wen-dang/api-reference/booking-apis/inflow-seat-and-baggage.md) — 查询和选择座位。
* [行李](/api-wen-dang/api-reference/booking-apis/baggage.md) — 查询和添加行李服务。

### 后续步骤

完成端点实现后，使用[API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)确认速率限制和重试行为。
