# 多渠道通知

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要在 ATRIP 中配置 Atlas 业务通知并为团队选择合适的投递渠道时使用此页面。

当您需要以下内容时从这里开始：

* 在 webhook、电子邮件和团队聊天投递之间进行选择
* 在 ATRIP 中配置通知投递
* 了解哪个场景优先上线

### 支持的渠道

Atlas 支持以下通知渠道：

* **Webhook**，用于服务器到服务器的投递和下游自动化
* **电子邮件**，用于正式的运营跟进和基于邮箱的工作流程
* **钉钉**、**企业微信**、**Slack** 和 **Microsoft Teams**，用于团队协作和快速感知

您可以配置一个或多个渠道。

### 首个上线场景

该通知框架的首个场景是**航司状态变更**。

当航司运营状态发生变化并可能影响搜索或预订可用性时，Atlas 会发送通知。

常见原因包括：

* 数据质量问题
* 系统问题或计划内维护
* 余额不足或 Look-to-Book 限制

### 通知内容

航司状态通知可包含以下业务字段：

* 航司名称和航司代码
* 当前状态
* 开始时间
* 原因
* 预计恢复时间（如有）
* 航司详情页面的链接

{% hint style="info" %}
Webhook 载荷字段在 [航司状态更新通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/airline-status-update-notification.md) 页面中单独说明。聊天和电子邮件投递可能会以渠道特定的格式呈现同一事件。
{% endhint %}

### 在 ATRIP 中配置通知

{% stepper %}
{% step %}

### 打开通知提醒

登录 ATRIP。

进入 **账户中心 → 个人设置 → 通知提醒**。
{% endstep %}

{% step %}

### 选择一个或多个渠道

选择您的团队想要使用的渠道：

* Webhook
* 电子邮件
* 钉钉
* 企业微信
* Slack
* Teams
  {% endstep %}

{% step %}

### 完成各渠道设置

打开目标渠道区域。

使用 **如何获取** 查看渠道特定的设置说明。
{% endstep %}

{% step %}

### 发送测试通知

设置完成后使用 **发送测试通知**。

确认测试消息到达正确的邮箱、群组或端点。
{% endstep %}
{% endstepper %}

### 渠道选择指导

根据团队的工作方式选择渠道：

* 当其他系统需要自动响应时，使用 **Webhook**
* 当运营或管理部门需要可审计的轨迹时，使用 **电子邮件**
* 当多名客服需要快速共享可见性时，使用聊天工具

### 常见问题

#### 是否需要配置所有渠道？

不需要。

仅配置您的团队使用的渠道。

#### 如何确认设置生效？

在 **通知提醒** 中使用 **发送测试通知**。

然后确认消息到达目标渠道。

#### 哪个页面记录了 webhook 结构？

使用 [航司状态更新通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/airline-status-update-notification.md) 查看当前 `airline.status` webhook 的载荷。

### 相关页面

* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [Webhook 注册与事件](/api-wen-dang/api-reference/webhook-and-incident-apis/webhook-registration-and-incidents.md)
* [航司状态更新通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/airline-status-update-notification.md)
