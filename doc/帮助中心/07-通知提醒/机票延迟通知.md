# 机票延迟通知

由于各种原因，机票可能会出现罕见的延迟。在这种情况下，订单将被发送到异常队列。客户可以选择通过以下一种或多种方法获得延迟通知：

电子邮件：客户在ATRIP中配置电子邮件地址。

钉钉：Atlas在客户钉钉群组中配置机器人，通知将发送到该群组。

Slack：Atlas在客户Slack群组中配置机器人，并将通知发送到该群组。

**电子邮件通知配置**

**谁将进行配置？**

客户需要添加需要接收这些通知的电子邮件地址。

**配置可以在何处进行？**

Atrip -> Profile -> My Profile -> Notification -> Email Notification

![](/files/5CUJX5laOuPkpPmHhWTN)

已添加的电子邮件地址将收到一封说明延迟原因的电子邮件。如果客户需要就该订单号与运营团队联系，则可以通过服务请求进行回复。

**机票发放延迟的不同原因是什么？**

导致机票发放延迟的原因可能是以下任何一种：

* 系统问题
* 售罄
* 等待航空公司确认
* 等待客户确认
* 航空公司系统问题
* 支付问题

**我在ATRIP中如何查看机票延迟通知？**

当您将鼠标悬停在预订状态上时，“机票延迟通知”将显示在“预订详情”屏幕中，如下截图所示：

![](/files/nFa0dCQ5Bav9FHqdxSvM)

**为何针对机票延迟通知创建服务请求？**

只有在延迟原因为“等待客户确认”时才会创建服务请求。客户需要在获得所需信息后回复响应。

**DingTalk群组消息配置**

**谁将进行配置？**

Atlas将在DingTalk群组聊天中进行配置。

**如何进行配置？**

**步骤1：向DingTalk群组添加机器人并获取URL中的关键参数**

位置：Group Settings -> Bot -> Add Robot -> Customize

![](/files/CwMsl5a6cucB6llDTUKQ)

向DingTalk群组添加机器人并获取URL中的关键参数。

在安全设置中勾选“添加签名”选项，并记下签名值。此值将是稍后URL中secret所对应的值。

在安全设置中，勾选签名复选框，并记下签名值，这将对应于稍后URL中的secret值。

![](/files/nGnCHKV1jGODUe1qNZFd)

点击“Complete”后，记下webhook中的access\_token。此值需要替换后续URL中的accessToken值。

**步骤2：在运营台为客户配置客户端**

位置: Client Library -> Details -> Operational Configuration -> Notification Configuration -> DingTalk.

输入URL。

URL示例：

<https://oapi.dingtalk.com/robot/send?accessToken=76360a316fe57e9f923398a69eae664ebf249994472beb1a6aa3be0ee5658e59&secret=SEC94508ffc75757d2365d389bc2cb2a10332b3a3fb082a06a1687f300c921fa144>

我们需要在上述示例中的access token和secret值的对应值替换。

accessToken字段的值应替换为通过配置机器人获得的DingTalk机器人webhook中的access\_token值。

secret字段的值应替换为先前配置机器人时记下的签名值（secret）。

一旦将这些值插入到URL中，新URL应配置在DingTalk输入字段中，如下所示：

![](/files/fi2U57M0c4jJqBY8NO9s)

**Slack群组消息配置**

**谁将进行配置？**

Atlas将在Slack群组聊天中进行配置。

**如何进行配置？**

**步骤1：配置Slack频道应用并获取webhook URL。**

选择频道。

右键单击“view channel details” 。

转到 Integrations → Apps → Add an App

按页面提示完成设置。

在最后一页后，显示的webhook URL是您需要的URL。

确保您具有将应用程序和集成添加到Slack频道的必要权限。一旦获得Webhook URL，您可以将其用于发送通知或消息至Slack频道作为您操作配置的一部分。

![](/files/CuQNF3QM2PoLh0cofdwN)

![](/files/9e4w8IbO0jlyffxhfWl5)

![](/files/2WBYAdynmQ4cpsTARcrb)

![](/files/eCDf43hSMSLD7YmYJPA1)

**步骤2：在运营台为客户配置**

位置: Client Library -> Details -> Operational Configuration -> Notification Configuration -> Slack

在Slack部分，输入您获取的Webhook URL。这将允许根据您的运营配置向指定的Slack频道发送通知。

![](/files/eIhix5bthBEEoHIgiz5d)
