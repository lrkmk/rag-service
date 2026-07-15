# 预订后 API

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

使用本部分获取端点级别的预订后参考。

在需要以下内容时从此处开始：

* 退款端点详情
* 作废端点详情
* 辅助服务、维护或 PNR 预订后 API

### 主要 API 分组

* [退款](/api-wen-dang/api-reference/post-booking-apis/refunds.md)
* [作废](/api-wen-dang/api-reference/post-booking-apis/void.md)
* [出票后辅助服务](/api-wen-dang/api-reference/post-booking-apis/post-ticketing-ancillaries.md)
* [重新生成订单](/api-wen-dang/api-reference/post-booking-apis/regenerate-order.md)
* [停止出票](/api-wen-dang/api-reference/post-booking-apis/stop-ticket-issuance.md)
* [订单列表](/api-wen-dang/api-reference/post-booking-apis/order-list.md)
* [PNR 认领](/api-wen-dang/api-reference/post-booking-apis/pnr-claim.md)
* [提取 PNR](/api-wen-dang/api-reference/post-booking-apis/extract-pnr.md)

### 常见问题

#### 已出票订单应使用哪个 API？

根据任务选择端点。退款使用退款 API。作废使用作废 API。

需要恢复订单数据时，使用重新生成订单或 PNR 相关 API。

#### 作废和退款有什么区别？

作废适用于仍符合航司作废条件的订单。

不符合条件时，应使用退款流程。先检查订单状态和业务规则。

### 后续步骤

先阅读[预订后操作](/api-wen-dang/product-guides/post-booking.md)以选择正确流程。

随后打开与任务匹配的端点页，确认请求字段和响应处理方式。
