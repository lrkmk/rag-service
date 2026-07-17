# Webhook 与事件 API

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

使用本部分配置 Atlas 事件通知，并查询已发生的事件。

Webhook 支持订单和航空公司相关的异步状态跟进。

### 常见问题

#### 如何接收 Atlas 订单事件？

使用[Webhook 注册与事件](/api-wen-dang/api-reference/webhook-and-incident-apis/webhook-registration-and-incidents.md)配置通知端点。

保存投递结果，并按业务流程处理每个事件。

#### Webhook 未收到事件时应怎么办？

先确认注册配置和接收端可用性。

然后使用事件查询核对预期事件与已处理记录。

### 相关指南

* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md) — 了解事件覆盖范围和投递预期。
* [多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md) — 配置 webhook、邮件和协作工具通知。

### 后续步骤

在生产环境启用前，使用沙箱验证事件接收、去重和异常处理。
