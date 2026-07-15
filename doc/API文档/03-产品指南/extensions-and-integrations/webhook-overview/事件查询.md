# 事件查询

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当 webhook 投递或事件状态需要确认时，使用此页面搜索事件记录。

当您需要以下操作时，请从这里开始：

* 核对遗漏或不清楚的 webhook 事件
* 按订单、航司、旅客或时间范围搜索事件
* 调查日程变更或取消历史

### 常见问题

#### 何时应使用事件查询？

当 webhook 投递、事件历史或事件确认仍需要更深入的核对时，请使用事件查询。

#### 应从哪些过滤器开始？

从 `orderNo` 开始，针对单个受影响的预订。

当事件集范围更广时，添加 `eventType`、航司或时间范围过滤器。

### 主要 API

* `event/getPageList.do`

### 在以下情况使用

* 核对遗漏的 webhook 事件
* 按订单、旅客或航司过滤事件
* 查看事件确认状态
* 调查日程变更或取消历史

### 常见查询模式

#### 查找单个订单的事件

使用：

* `orderNo`
* `pageSize`

#### 查找单个航司的日程变更

使用：

* `eventType`
* `airline`
* `eventTimeStart`
* `eventTimeEnd`
* `pageSize`

#### 查找未解决的事件

使用：

* `eventStatus`
* `pageSize`

### 常用过滤器

* `eventId`
* `orderNo`
* `eventType`
* `pnr`
* `paxName`
* `paxEmail`
* `airline`
* `eventStatus`
* `eventTimeStart`
* `eventTimeEnd`
* `pageIndex`
* `pageSize`

### 必填字段

* `pageSize`

### 响应要点

* `records`
* `pageIndex`
* `pageSize`
* `total`
* 事件状态和确认字段

### 提示

* 始终发送 `pageSize`
* 调试单个受影响的预订时，从 `orderNo` 开始
* 查询广泛事件集时，添加时间范围
* 将此与 webhook 负载日志和订单查询结果结合使用

### 下一步是什么？

将查询结果与[查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)和[事件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-notification.md)结合使用，以确认最终运营状态。

### 完整 API 参考

在此查看端点级别的详细信息：

* [Webhook 注册与事件](/api-wen-dang/api-reference/webhook-and-incident-apis/webhook-registration-and-incidents.md)

### 相关页面

* [事件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-notification.md)
* [日程变更通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/schedule-change-notification.md)
* [查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)
