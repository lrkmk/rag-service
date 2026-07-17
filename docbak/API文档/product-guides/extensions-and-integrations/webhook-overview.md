# Webhook 概述

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此部分注册 webhook 端点并消费事件通知。

当您需要以下操作时，请从这里开始：

* 在上线前注册 webhook 投递
* 了解 Atlas 可以通知哪些预订事件
* 决定 webhook 如何与订单查询和航司邮件配合使用
* 将 webhook 配置为 Atlas 通知中的一种投递选项

{% hint style="info" %}
需要在 webhook、电子邮件和团队聊天中设置 ATRIP 通知？请从[多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)开始。
{% endhint %}

如果您需要先进行渠道设置，请在阅读 webhook 事件详情之前打开[多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)。

### 常见问题

#### Atlas webhook 是保证投递的吗？

不是。

Webhook 投递是尽力而为的。

请使用订单查询、航司邮件和事件跟进进行最终核对。

#### Webhook 应该用于什么场景？

将 webhook 用作 Atlas 通知中的服务器到服务器投递选项。

使用 webhook 加速出票完成、作废更新、日程变更、航司状态更新、邮件捕获和事件跟进等事件的处理。

当您还需要通过电子邮件、钉钉、企业微信、Slack 或 Teams 进行 ATRIP 投递时，请使用[多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)。

不要将 webhook 视为预订状态的唯一来源。

#### Webhook 能否取代履行流程中的订单查询？

不能。

将 webhook 用作早期信号。

使用 `queryOrderDetails.do` 进行最终出票确认。

### 概述

Webhooks 会在影响客户预订的航司变更时自动通知您。例如，当航司更改了影响您某个订单的航班日程时，Atlas API 将向您的服务器发送关于此事件的通知，您可以对其进行处理。例如，您可以通过更新数据库或向客户发送电子邮件来采取行动。

> Atlas 在"尽可能提供"的基础上提供 webhook 功能。Atlas 不负责提供所有通知。对于任何日程变更，请始终参考航司发送到预订请求中提供的电子邮件地址的邮件。

### 推荐的 webhook 模式

将 webhook 用作近实时信号。

然后，在需要时通过订单查询、事件查询或航司邮件确认最终状态。

### 履行流程告警

对于通过 `getOfferPrice.do` 创建的订单，请在 5 分钟出票窗口内主动监控订单。

使用 webhook 缩短出票完成、取消和事件跟进的响应时间。

然后使用 `queryOrderDetails.do` 确认最终结果。

{% hint style="warning" %}
Webhook 不应该是履行流程中唯一的超时检测器。

请在出票窗口期间保持主动的订单轮询。
{% endhint %}

### 典型流程

{% stepper %}
{% step %}

### 注册您的端点

使用 [Webhook 注册与事件](/api-wen-dang/api-reference/webhook-and-incident-apis/webhook-registration-and-incidents.md) 在上线前保存 webhook URL。

如果您还使用邮箱或聊天投递，请在[多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)中配置这些渠道。
{% endstep %}

{% step %}

### 接收并处理事件

处理出票、作废、日程、航司、邮件和事件通知。

Atlas 针对以下常见场景发送 webhook 通知：

1. 已出票：[出票完成通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/ticketing-complete-notification.md)
2. 已提交或更新作废：[作废通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/void-notification.md)
3. 航班日程变更：[日程变更通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/schedule-change-notification.md)
4. 航司状态更新：[航司状态更新通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/airline-status-update-notification.md)
5. 收到邮件：[电子邮件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/email-notification.md)
   {% endstep %}

{% step %}

### 在需要时进行核对

使用事件查询和订单 API 确认最终状态。

1. 事件通知：[事件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-notification.md)
2. 事件查询：[事件查询](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-query.md)
   {% endstep %}
   {% endstepper %}

### Webhook 不应取代的内容

Webhook 不应取代：

* 用于最终出票确认的 `queryOrderDetails.do`
* 用于最终作废核对的 `queryVoidOrders.do`
* 用于日程变更感知的航司邮件
* 用于深入事件核对的事件查询
* 在履行流程截止时间内的主动订单监控
