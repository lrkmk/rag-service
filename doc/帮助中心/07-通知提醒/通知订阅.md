# 通知订阅

我们在ATRIP Flight Deck上推出了一个新功能，允许客户自行配置并订阅电子邮件和Webhook通知。此更新将控制权交给我们的客户，使他们能够自定义接收重要通知的方式。

**位置**

ATRIP -> Profile -> My Profile -> Notification

**权限**

Admin

**Webhook 通知配置**

![](/files/ayjXynWiezj7AKxHSvFh)

在Webhook URL中输入或更新您的Webhook URL。

选择您希望通过Webhook接收的通知类型。单击“Confirm”以应用更改。

有关Webhook API文档，请参阅“API文档”部分。

**电子邮件通知**

![](/files/QrcwRZlsBkximcj8czwS)

您可以接收两种类型的电子邮件通知：

* 航空公司状态更改
* 余额不足警报

**航空公司状态更改**

通过单击“Follow”列中的“星号”来选择需要接收通知电子邮件的航空公司。然后转到 Profile -> My Profile -> Notification -> Email 选项卡，然后单击“Edit”按钮。

输入需要接收航空公司状态通知的电子邮件地址（最多10个）。

![](/files/LNY0AKBb0NnUBYLThlUH)

然后点击“Advanced Settings” ，会显示一个弹出窗口。

![](/files/438EEHmDxL1IgPhaaLhL)

在此窗口中列出了在“航空公司列表”屏幕上选择的航空公司。在此处可以确定发送电子邮件通知的时间间隔。客户可能只想在航空公司处于“非活动”状态10分钟后收到通知，因此他们会将此时间配置为“10分钟”。

完成配置后，在弹出窗口和主窗口中点击“Confirm”。

“航空公司状态更改”现已配置完成。

**余额不足警报**

“余额不足”电子邮件通知可配置为通知客户存款余额现在较低，他们需要做充值。

阈值金额已在运营台配置。ATRIP将监控阈值金额，当余额低于该金额时，将触发到本部分配置的电子邮件地址的电子邮件。

![](/files/G1gD06APLR3vW8iUNrmL)

在配置电子邮件地址（最多10个）后，点击“Confirm”。
