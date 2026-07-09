# Webhook 注册与事件

{% hint style="info" %}
💬 **Need help?** If you're stuck, ask Eva in the Help Center for instant diagnostics.

<a href="https://resources.atriptech.com/?fallback=true" class="button primary" data-icon="comments">Ask Eva</a>
{% endhint %}

使用此页面从 API 参考层注册你的 webhook 端点和查询事件记录。

在需要以下内容时从此处开始：

* 在上线前注册或更新 webhook URL
* 在错过或未解决的事件后查询事件记录
* 将 webhook 投递与事件记录进行对账

### 常见问题

#### 何时应注册 webhook URL？

在上线前注册 webhook URL。

然后在接收端点发生变更时更新它。

同一 URL 接收所有支持的事件，包括 `order.void`。

#### 何时应查询事件？

当 webhook 投递、航班时刻变更处理或运营跟进需要更深层次对账时，查询事件。

当事件轨迹不完整或在 webhook 处理后仍不清楚时，使用事件查询。

#### 履约流程订单应如何使用 webhook 和事件查询？

将 webhook 用作早期信号。

当事件轨迹不完整时，使用事件查询。

在 5 分钟履约窗口期间保持主动订单轮询。

### 本页面涵盖内容

* `updateWebhookURL.do` 用于 webhook 注册
* `event/getPageList.do` 用于事件查询

### 后续步骤

使用 [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)了解运营模式和事件覆盖范围。

当需要更深入的事件跟进时，使用[事件查询](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-query.md)和[事件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-notification.md)。

### 典型流程

{% stepper %}
{% step %}

### 注册你的 webhook URL

保存 Atlas 应调用的端点以进行 webhook 投递。
{% endstep %}

{% step %}

### 接收 webhook 事件

处理出票、作废、航班时刻变更、航司状态、邮件和事件通知。

对于履约流程订单，使用这些事件减少响应时间，而非替代订单查询。
{% endstep %}

{% step %}

### 在需要时查询事件

使用事件查询来对账错过或未解决的事件。
{% endstep %}
{% endstepper %}

### 在需要时使用此功能

* 初始 webhook 设置
* webhook 端点更新
* 事件对账
* 航班时刻变更或取消后的运营跟进

### 注册范围

使用 `updateWebhookURL.do` 注册一个 webhook URL。

Atlas 将该 URL 用于所有支持的 webhook 事件类型。

包括 `order.void`。

在开始使用 `getOfferPrice.do` 进行履约流量之前，应已完成同一注册。

### 相关页面

* [Webhooks](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [履约 API](/api-wen-dang/api-reference/booking-apis/get-offer-price.md)
* [事件查询](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-query.md)
* [事件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-notification.md)

## Register Webhook

> \*\*Endpoint:\*\*\
> <https://sandbox.atriptech.com/updateWebhookURL.do>

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/updateWebhookURL.do":{"post":{"summary":"Register Webhook","deprecated":false,"description":"**Endpoint:**\nhttps://sandbox.atriptech.com/updateWebhookURL.do","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"url":{"type":"string","description":"The URL for receiving webhook notifications"}},"required":["url"]}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"type":"integer"},"msg":{"$ref":"#/components/schemas/ResponseMessage","nullable":true}},"required":["status"]}}},"headers":{}}}}}},"components":{"schemas":{"ResponseMessage":{"type":"string","description":"It serves as an additional description of the response result. Especially when the interface reports an error (`status` !=`0`), it is usually a human-readable error message. Note: Do not use this field in any programming scenarios. For example, do not judge whether the interface responds successfully based on this field. Instead, you should only determine it by checking whether the status is equal to`0`at any time."}}}}
```

## Incident List

> \*\*Endpoint:\*\*\
> <https://sandbox.atriptech.com/event/getPageList.do>

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/event/getPageList.do":{"post":{"summary":"Incident List","deprecated":false,"description":"**Endpoint:**\nhttps://sandbox.atriptech.com/event/getPageList.do","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"eventId":{"type":"string","description":"Incident ID"},"orderNo":{"type":"string","description":"Order number"},"eventType":{"type":"string","description":"Incident type:\n- `email.schedulechange`: Schedule Change-Email Notification\n- `abnormal.cancelled`: Unacounted Cancellation\n- `order.schedulechange`: Schedule Change-API Notification"},"pnr":{"type":"string","description":"Order's pnr."},"paxName":{"type":"string","description":"Order's passenger names."},"paxEmail":{"type":"string","description":"Order's passenger Email. Email address passed to the Airline."},"airline":{"type":"string","description":"Airline IATA code."},"eventStatus":{"type":"array","items":{"type":"integer"},"description":"A list containing incident stauses\n- `0`: Unconfirmed\n- `1`: Confirmed"},"eventTimeStart":{"type":"string","description":"Incident Receiving Time Start\nFormat: yyyy-MM-dd HH:mm:ss UTC+08:00"},"eventTimeEnd":{"type":"string","description":"Incident Receiving Time End\nFormat: yyyy-MM-dd HH:mm:ss UTC+08:00"},"depTimeStart":{"type":"string","description":"Departure Time Start(Departure local time)\nFormat: yyyy-MM-dd HH:mm:ss"},"depTimeEnd":{"type":"string","description":"Departure Time End(Departure local time)\nFormat: yyyy-MM-dd HH:mm:ss"},"updateTimeStart":{"type":"string"},"pageIndex":{"type":"integer","default":1,"description":"Pagination","nullable":true},"pageSize":{"type":"integer","description":"Number of records per page"}},"required":["pageSize"]}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"type":"integer"},"msg":{"type":"string","nullable":true},"records":{"type":"array","items":{"type":"object","properties":{"eventId":{"type":"string","description":"Incident Id."},"orderNo":{"type":"string","description":"Order Number."},"eventType":{"type":"string","description":"Incident type\n-`email.schedulechange`: Schedule Change-Email Notification\n-`abnormal.cancelled`: Unacounted Cancellation\n-`order.schedulechange`: Schedule Change-API Notification"},"eventStatus":{"type":"integer","description":"Incident staus\n-`0`: Unconfirmed\n-`1`: Confirmed"},"eventTime":{"type":"string","description":"Incident recieving time.\nFormat: yyyy-MM-dd HH:mm:ss UTC+08:00"},"confirmedResult":{"type":"string","description":"Incident Reason. Schedule Change Type & Cancelled Type.","nullable":true},"confirmedRemark":{"type":"string","description":"Remark.","nullable":true},"createTime":{"type":"string","description":"Incident create time.\nFormat: yyyy-MM-dd HH:mm:ss UTC+08:00"},"airline":{"type":"string","description":"Airline IATA code."},"depTime":{"type":"string","description":"Flight depature time. Depature local time."},"confirmTime":{"type":"string","description":"Confirmed Time.\nFormat: yyyy-MM-dd HH:mm:ss UTC+08:00","nullable":true},"notified":{"type":"integer","description":"Send the notification or not. 1: YES. 0: No","nullable":true},"pnr":{"type":"string","description":"Order's pnr."},"paxName":{"type":"string","description":"Order's passenger names."},"paxEmail":{"type":"string","description":"Order's passenger Email. Email address passed to the Airline."}},"required":["eventId","orderNo","eventType","eventStatus","eventTime","createTime","airline","depTime","pnr","paxName","paxEmail"]}},"pageIndex":{"type":"string","description":"Current pagination"},"pageSize":{"type":"string","description":"Page size"},"total":{"type":"string","description":"Total number of records"}},"required":["status","pageIndex","pageSize","total","records"]}}},"headers":{}}}}}}}
```
