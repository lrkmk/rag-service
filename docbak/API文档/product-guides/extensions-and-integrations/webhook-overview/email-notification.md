# 邮件通知

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要处理与订单关联的航司邮件活动时，请使用此 webhook。

### 触发条件

当 Atlas 邮件捕获收到与订单相关的航司邮件时，Atlas 发送 `email.all`。

### 您应该做什么

当您收到此事件时：

* 存储 `orderNo` 和 `uniqueCode`
* 按 `emailCategory` 对邮件进行分类
* 如需完整正文，请快速获取或归档邮件内容
* 在需要时将事件路由到支持、日程变更或预订后工作流程

### 端点

POST 到您在 Atlas 注册的 webhook URL。

### 首先读取的字段

* `type`
* `data.orderNo`
* `data.emailCategory`
* `data.emailSubject`
* `data.emailLink`
* `data.createTime`

### 典型负载

```json
{
  "cid": "XXXXX",
  "data": {
    "orderNo": "XXXXXX",
    "emailCategory": "Payment Success",
    "emailSubject": "easyJet booking reference: XXXXX",
    "emailLink": "http://example.com/email.eml",
    "createTime": "2024-01-05 10:54:26"
  },
  "notificationId": "20240105105430470MJMOR",
  "status": -1,
  "type": "email.all"
}
```

### 注意事项

* `emailLink` 是临时的，很快就会过期
* 如果您需要长期访问，请在您这边存储邮件负载
* `status` 是内部字段，应在业务逻辑中忽略

{% tabs %}
{% tab title="模式" %}
**`cid`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 唯一客户端标识符。
* **默认值:** 无
* **示例:** `"XXXXX"`

**`notificationId`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 通知事件的唯一标识符。
* **默认值:** 无
* **示例:** `"20240105105430470MJMOR"`

**`status`**

* **类型:** 整数
* **必填:** 是
* **描述:** 在此类通知中，状态始终 = -1。这是一个内部字段，应忽略。
* **默认值:** 无
* **示例:** `-1`

**`type`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 通知类型。
* **默认值:** 无
* **示例:** `"email.all"`

**`data`**

* **类型:** Object
* **必填:** 是
* **描述:** 包含邮件相关的详细信息。
* **默认值:** 无
* **示例:** `{ ... }`

**`data.orderNo`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 与邮件关联的订单号。
* **默认值:** 无
* **示例:** `"XXXXXX"`

**`data.emailReceivingDate`**

* **类型:** 字符串
* **必填:** 是
* **描述:** Atlas 收到邮件的日期和时间（UTC）。格式：`YYYY-MM-DD HH:mm:ss`。
* **默认值:** 无
* **示例:** `"2024-01-05 10:54:21"`

**`data.uniqueCode`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 用于标识邮件的唯一代码。
* **默认值:** 无
* **示例:** `"e4afbecfd5727817ff73a71a94a2a64d"`

**`data.emailCategory`**

* **类型:** 字符串
* **必填:** 是
* **描述:** Atlas 邮件类别。Atlas 会对邮件进行分类，但不保证分类的准确性。
* **有效值:**
  * Schedule change（日程变更）
  * Receipt（收据）
  * Payment Success（支付成功）
  * Verification（验证）
  * Trip Reminder（行程提醒）
  * Promo code（促销代码）
  * Travel Itinerary（旅行行程）
  * Advertisement（广告）
  * PNR Cancellation Success（PNR 取消成功）
  * Payment Due（待付款）
  * Unidentified（未识别）
  * Duplicated Schedule Change（重复的日程变更）
  * Unaccounted Cancellation（意外取消）
* **默认值:** 无
* **示例:** `"Payment Success"`

**`data.from`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 发件人的电子邮件地址。
* **默认值:** 无
* **示例:** `"donotreply@easyjet.com"`

**`data.to`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 收件人的电子邮件地址。
* **默认值:** 无
* **示例:** `"NSDLZCQTGJTEYXOMFOD@gorn.top"`

**`data.emailSubject`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 邮件的主题。
* **默认值:** 无
* **示例:** `"easyJet booking reference: XXXXX"`

**`data.emailLink`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 用于访问邮件内容的 URL 链接。邮件链接仅有效 10 分钟。
* **默认值:** 无
* **示例:** `"http://order-oss-sg.oss-ap-southeast-1.aliyuncs.com/...eml?Expires=1704426870..."`

**`data.createTime`**

* **类型:** 字符串
* **必填:** 是
* **描述:** 创建时间是 Atlas 在邮件列表中创建此邮件记录的时间。通常晚于接收时间。格式：`YYYY-MM-DD HH:mm:ss`。
* **默认值:** 无
* **示例:** `"2024-01-05 10:54:26"`
  {% endtab %}

{% tab title="示例" %}

```json
{
    "cid":"XXXXX",
    "data":{
        "orderNo":"XXXXXX",
        "emailReceivingDate":"2024-01-05 10:54:21",
        "uniqueCode":"e4afbecfd5727817ff73a71a94a2a64d",
        "emailCategory":"Payment Success",
        "from":"donotreply@easyjet.com",
        "to":"NSDLZCQTGJTEYXOMFOD@gorn.top",
        "emailSubject":"easyJet booking reference: XXXXX",
        "emailLink":"http://order-oss-sg.oss-ap-southeast-1.aliyuncs.com/2024/01/e4afbecfd5727817ff73a71a94a2a64d.eml?Expires=1704426870&OSSAccessKeyId=LTAI5tDmTE9iwtNdsqxVXuom&Signature=zF8aNNsGgY8n2jhsW7V1gmPLw8c%3D",
        "createTime":"2024-01-05 10:54:26"
    },
    "notificationId":"20240105105430470MJMOR",
    "status":-1,
    "type":"email.all"
}
```

{% endtab %}
{% endtabs %}

### 相关页面

* [邮件查询](/api-wen-dang/support-and-reference/utility-api-overview/email-query.md)
* [事件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-notification.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
