# 邮件列表

**背景：**

一些航空公司会阻止使用来自在线旅行社和旅行公司的电子邮件的预订，因为他们希望推广自己的销售渠道。为了克服航空公司的这一限制并为客户提供独特的内容，Atlas使用他们自己的电子邮件服务，在与航空公司进行预订时，将原始邮件更改为Atlas邮件。

由于航空公司没有客户的电子邮件地址，客户将不会收到这封电子邮件。因此，Atlas已开发出一个功能，使客户的运营团队成员可以查看和处理这些邮件。

"电子邮件列表"可通过以下3种方法访问：

1. ATRIP
2. 电子邮件列表API
3. 电子邮件通知Webhook

**目标：**\
有这个列表的目的是让客户能够告知乘客航班时间的变更或航空公司做出的其他重要公告。

**电子邮件列表类别：**\
以下类别的电子邮件将显示在“电子邮件列表”中：

* 航班时间变更
* 收据
* 支付成功
* 验证
* 行程提醒
* 促销代码
* 旅行行程
* 广告
* PNR取消成功
* 付款到期
* 未识别的
* 重复的航班时间变更
* 未归属的取消

**ATRIP：**

![](/files/X9RUvCB4txefdWTSDah5)

这里可以管理所有的电子邮件，包括航班变动、行程等。所有航空公司发送到联系电子邮件地址的电子邮件都会显示在这里，包括广告。

电子邮件列表的位置是 ATRIP --> Bookings --> Email List&#x20;

**处理电子邮件列表：**

在电子邮件列表中收到的电子邮件可以“查看”，“下载”，然后“处理”。

**查看电子邮件：**

![](/files/PB8Zp0tdyjT6TgAPFirR)

点击“View”超链接。来自航空公司的电子邮件将在新标签页中打开，如下所示。客户随后可以根据其内部流程将电子邮件转发给乘客。

![](/files/C0trCMZq8d26AQqpIf0K)

**下载邮件**

![](/files/FF1dOyDaDQNli9DbHXRD)

点击“Download ”超链接。来自航空公司的电子邮件将下载到笔记本电脑/ PC 上。客户随后可以根据其内部流程将电子邮件转发给乘客。

**处理电子邮件**

电子邮件可以通过以下两种方式进行处理：

通过单击“**View**”，然后单击“**Handle**”按钮。

通过在摘要界面上单击一个或多个电子邮件，然后单击“批量处理”按钮。

“**View**”并单击“**Handle**”按钮

一旦单击“**View**”超链接，将在浏览器中显示带有电子邮件的以下界面。

单击屏幕右上角的“**Handle**”按钮

![](/files/QrQScAszqWDBhlYYJvyj)

单&#x51FB;**“Handle**”按钮后，将显示如下弹出窗口，其中包含下拉选项。

![](/files/ICvNYiXp0gQTtHsaZMv1)

选择适当的选项，然后单击“Confirm”。当您检查电子邮件列表摘要时，状态会变为“Processed”。

可用的选项包括：

* No Change （预订没有变化）
* Flight Change Confirmed （没有航班变动）
* Micro Schedule Change （航班变动很小）
* API Notified （已通过电子邮件列表API通知客户）
* Wait （稍后将通知客户）

**批量更新**

从电子邮件列表中选择一个或多个电子邮件。然后单击“批量处理”按钮。

![](/files/U5oFzxuaNRzmp8xtvfbV)

A pop-up window will be displayed as shown below:

![](/files/kvwnof8Bo04QevnFgIFM)

选择适当的选项，然后单击“Confirm”。当您检查电子邮件列表摘要时，状态会变为“已处理”。

**Email List API**

端点: <https://api-sg.atriptech.com/mail.do>

&#x20;&#x20;

**请求**

```
{
    "orderNo":null,
    "emailReceivingDateStart":"2023-11-01 00:00:00",
    "emailReceivingDateEnd":"2023-11-30 00:00:00",
    "createTimeStart":null,
    "createTimeEnd":null,
    "emailCategories": ["Travel Itinerary","Verification"],
    "pageIndex":1,
    "pageSize":100
}
```

![](/files/wSUZTEbkeAFn4MonSX02)

|                         |          |                                                                                                                                                                                                                                                                     |
| ----------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| orderNo                 | Optional | Order Number                                                                                                                                                                                                                                                        |
| emailReceivingDateStart | Optional | Receiving time Start.                                                                                                                                                                                                                                               |
| emailReceivingDateEnd   | Optional | <p>Receiving time End.</p><p>You can only query data for up to one month at a time.</p>                                                                                                                                                                             |
| createTimeStart         | Optional | Create time Start.                                                                                                                                                                                                                                                  |
| createTimeEnd           | Optional | <p>Create time End.</p><p>You can only query data for up to one month at a time.</p>                                                                                                                                                                                |
| emailCategory           | Optional | <p>Options:</p><ul><li>Schedule change</li><li>Receipt</li><li>Payment Success</li><li>Verification</li><li>Trip Reminder</li><li>Promo code</li><li>Travel Itinerary</li><li>Advertisement</li></ul><p>Multiple categories can be added, separated by a comma.</p> |
| pageIndex               | Required | Pagination                                                                                                                                                                                                                                                          |
| pageSize                | Required | <p>Number of records per page</p><p>maximum number=1000</p>                                                                                                                                                                                                         |

**Response**

```
{
"records": [
{
"orderNo": "OPQRN20230520100137937",
"emailReceivingDate": "2023-11-02 07:29:28",
"uniqueCode": "d08a419d46bb93b8fd9e7ac3ea29a227",
"emailCategory": "Travel Itinerary",
"from": "
infoEticket@lionair.co.id
",
"to": "
bearrpemvgwqyafo@nwt.ttjipiao.top
",
"emailSubject": "Lion Group Reservation to PANGKALANBUUN, INDONESIA, November 02 for MS CATHERINE DEWOLFF",
"emailLink": "
http://order-oss-sg.oss-ap-southeast-1.aliyuncs.com/2023/11/d08a419d46bb93b8fd9e7ac3ea29a227.eml?Expires=1706010036&OSSAccessKeyId=LTAI5tDmTE9iwtNdsqxVXuom&Signature=9%2Bwzk6GcZRcnUIx8w5rbBHCirjI%3D
",
"createTime": "2023-11-02 07:29:32"
},
{
"orderNo": "OPQRN20230520100137937",
"emailReceivingDate": "2023-11-02 07:31:06",
"uniqueCode": "4c5f214942b33659ad21d54366af32fa",
"emailCategory": "Travel Itinerary",
"from": "
infoEticket@lionair.co.id
",
"to": "
bearrpemvgwqyafo@nwt.ttjipiao.top
",
"emailSubject": "Lion Group Reservation to PANGKALANBUUN, INDONESIA, November 03 for MS CATHERINE DEWOLFF",
"emailLink": "
http://order-oss-sg.oss-ap-southeast-1.aliyuncs.com/2023/11/4c5f214942b33659ad21d54366af32fa.eml?Expires=1706010036&OSSAccessKeyId=LTAI5tDmTE9iwtNdsqxVXuom&Signature=RWgF9%2BQcrUi7bv%2FA9Q29Zf%2BkZqM%3D
",
"createTime": "2023-11-02 07:31:09"
}
],
"hasNext": false,
"status": 0,
"msg": "success"
}
```

|                         |          |                                                                                                                                                                                                       |
| ----------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| orderNo                 | Required | Order Number                                                                                                                                                                                          |
| emailReceivingDate      | Required | The time at which the email has been received from the airline.                                                                                                                                       |
| uniqueCode              | Required | Unique Code of the email                                                                                                                                                                              |
| emailCategory           | Required | <p>Options:</p><ul><li>Schedule change</li><li>Receipt</li><li>Payment Success</li><li>Verification</li><li>Trip Reminder</li><li>Promo code</li><li>Travel Itinerary</li><li>Advertisement</li></ul> |
| from                    | Required | Email “from” address                                                                                                                                                                                  |
| to                      | Required | Email “to” address                                                                                                                                                                                    |
| emailSubject            | Required | Email “Subject”                                                                                                                                                                                       |
| emailLink               | Required | Email Link. Email Link is only valid for 10 mins.                                                                                                                                                     |
| createTime              | Required | <p>Create time End.</p><p>You can only query data for up to one month at a time</p>                                                                                                                   |
| emailNotificationStatus | Optional | <p>Notification Status</p><p>0=Notification not sent successfully</p><p>1=Notification sent successfully</p>                                                                                          |

客户可以下载“emailLink”。

已下载的电子邮件在打开后会显示航空公司发送的原始邮件。

![](/files/prJTHf4jEIiro5O3S1ND)

**Email Notification via Webhook**

The customer server URL needs to be configured in ATRIP to receive the webhook notifications.

**Webhook Notification**

```
{
"cid":"pxmhg93103",
"data":{
"orderNo":"AEQTO20230711142920543",
"emailReceivingDate":"2023-08-04 15:58:52",
"uniqueCode":"017e7e70d729f6392144953bae1a68
68",
"emailCategory":"Unidentified",
"
from":"brb@blueribbonbags.com
",
"
to":"dioneblebp@msbzt.com
",
"emailSubject":"Change to the time of your flydubai flight: Booking reference: 7RGWPY",
"emailLink":"http://order-oss-sg.oss-ap-southeast-1.aliyuncs.com/2023/08/42e157e7f9f60e2ccda3693b19d2659a.eml?Expires=1691139906&OSSAccessKeyId=LTAI5tDmTE9iwtNdsqxVXuom&Signature=r69CnS7lt1rc8f4nZRrdxufI7Fk%3D",
"createTime":"2023-08-04 15:58:56"
},
"notificationId":"20230804160506282JUWFJ",
"status": -1,
"type":"email.all"
}
```

|                    |                                                                                                                                                                                                                                                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| orderNo            | Order Number                                                                                                                                                                                                                                                                                                    |
| emailReceivingDate | <p>The time Atlas received the airline's email. </p><p>Format: yyyy-MM-dd HH:mm:ss UTC+08:00</p>                                                                                                                                                                                                                |
| uniqueCode         | Unique Code of the email                                                                                                                                                                                                                                                                                        |
| emailCategory      | <p>Atlas email categories. Atlas categorizes emails but does not guarantee accuracy in classification.</p><p>Options:</p><ul><li>Schedule change</li><li>Receipt</li><li>Payment Success</li><li>Verification</li><li>Trip Reminder</li><li>Promo code</li><li>Travel Itinerary</li><li>Advertisement</li></ul> |
| from               | Email “from” address                                                                                                                                                                                                                                                                                            |
| to                 | Email “to” address                                                                                                                                                                                                                                                                                              |
| emailSubject       | Email “Subject”                                                                                                                                                                                                                                                                                                 |
| emailLink          | Email Link. Email Link is only valid for 10 mins.                                                                                                                                                                                                                                                               |
| createTime         | The time when Atlas created this email record in the Email list. Generally, it will be later than the receiving time.                                                                                                                                                                                           |
| notificationId     | Unique Code of the notification                                                                                                                                                                                                                                                                                 |
| status             | Always equal to -1, internal field                                                                                                                                                                                                                                                                              |
| type               | Notification type. When type=email.all, the notification is the Email Notification.                                                                                                                                                                                                                             |
