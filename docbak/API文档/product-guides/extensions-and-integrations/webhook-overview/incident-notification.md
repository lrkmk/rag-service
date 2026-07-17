# 事件通知

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当 Atlas 检测到影响订单的运营事件时，请使用此 webhook。

### 触发条件

Atlas 在以下情况下发送事件通知：

* `email.schedulechange`
* `order.schedulechange`
* `abnormal.cancelled`

### 您应该做什么

当您收到此事件时：

* 识别事件类型
* 决定是否需要旅客采取行动
* 如有需要，通知受影响的客户
* 使用事件查询或订单查询进行跟进调查

对于履行流程中的订单，请持续轮询订单，直到出票结果最终确定。

### 端点

POST 到您在 Atlas 注册的 webhook URL。

### 首先读取的字段

* `type`
* `notificationId`
* `status`
* `data.orderNo`

然后根据 `type` 读取事件特定字段。

### 事件类型

#### `email.schedulechange`

Atlas 收到了航司的日程变更邮件。\
使用 `data.emailSubject` 和 `data.emailLink`。

#### `order.schedulechange`

Atlas 拥有结构化的日程变更数据。\
使用航段数组和 `scheduleChangeType`。

#### `abnormal.cancelled`

检测到意外取消。\
使用订单号和取消详情进行跟进。

### 注意事项

* `status` 是事件确认状态
* `emailLink` 是临时的，如需使用请尽快存储
* 在依赖这些事件之前，请先注册您的 webhook URL
* 不要将事件通知视为 `getOfferPrice.do` 的唯一超时信号

### 示例注册请求

```json
{
  "cid": "XXXXXXXX",
  "url": "https://xxx.com/xxxx"
}
```

{% tabs %}
{% tab title="模式" %}
**cid**

* **类型:** 字符串
* **必填:** 是
* **描述:** 用于跟踪请求的唯一客户端标识符。
* **示例:** `"xxxxxxxxxx"`

**type**

* **类型:** 字符串
* **必填:** 是
* **描述:** 事件类型。
* **有效值:**
  * email.schedulechange: 日程变更 - 邮件通知
  * abnormal.cancelled: 意外取消
  * order.schedulechange: 日程变更 - API 通知
* **示例:** `"email.schedulechange"`

**notificationId**

* **类型:** 字符串
* **必填:** 是
* **描述:** 通知事件的唯一标识符。
* **示例:** `"20230323113246035DNIDD"`

**status**

* **类型:** 整数
* **必填:** 是
* **描述:** 事件状态。
* **有效值:**
  * 0: 未确认
  * 1: 已确认
* **示例:** `0`

**data**

* **类型:** Object
* **必填:** 是
* **描述:** 包含与日程变更相关的邮件通知详情。

**data.orderNo**

* **类型:** 字符串
* **必填:** 是
* **描述:** 与航班预订关联的唯一订单号。
* **示例:** `"TESTS20230323103458265"`

**data.emailSubject**

* **类型:** 字符串
* **必填:** 是
* **描述:** 发送给客户的邮件通知主题行。
* **示例:** `"IMPORTANT: Flight delay notice. Confirmation Code KDK7QG"`

**data.emailLink**

* **类型:** 字符串（URL）
* **必填:** 是
* **描述:** 指向邮件详情页面的直接链接，用于获取更多信息。
* **示例:** `"https://theatlas/#/email-detail/4378270"`

> **提示**: 客户的服务器 URL 需要在 Atlas 注册才能通过 webhook 接收通知。

可以通过如下 API 完成注册：

```
{

    "cid": "XXXXXXXX",

    "url": "https://xxx.com/xxxx"

}
```

也可以通过 ATRIP 在"我的资料"菜单的"客户信息"选项卡中进行注册。

接收通知：

将收到三种类型的事件通知。它们是：

a. \[日程变更 - 邮件通知] 使用 Atlas 生成的邮件 ID 从航司收到的任何日程变更邮件通知。

示例：

```
{

    "cid":"xxxxxxxxxx",

    "type":"email.schedulechange",

    "notificationId":"20230323113246035DNIDD",

    "status":0,

    "data":{

        "orderNo":"TESTS20230323103458265",

        "emailSubject":"IMPORTANT: Flight delay notice. Confirmation Code KDK7QG",

        "emailLink":"https://theatlas/#/email-detail/4378270"

    }

}
```

请注意，邮件链接的有效期为 10 分钟。邮件中收到的数据需要存储在客户方。

b. \[日程变更 - API 通知]

结构化的日程变更通知。包含旧航班和新航班的信息。

示例：

```
{

  "cid": "xxxxxxxxxx",

  "data": {

    "orderNo": "XCEWF20221203094515954",

    "previousSegs": [

      {

        "arrAirport": "DPS",

        "arrTerminal": "",

        "arrTime": "2023-01-24 10:35:00",

        "carrier": "IU",

        "codeShare": false,

        "depAirport": "CGK",

        "depTerminal": "",

        "depTime": "2023-01-24 07:45:00",

        "flightNumber": "IU740"

      },

      {

        "arrAirport": "CGK",

        "arrTerminal": "",

        "arrTime": "2023-04-24 16:05:00",

        "carrier": "IU",

        "codeShare": false,

        "depAirport": "DPS",

        "depTerminal": "",

        "depTime": "2023-04-24 15:15:00",

        "flightNumber": "IU759"

      }

    ],

    "revisedSegs": [

      {

        "arrAirport": "CGK",

        "arrTerminal": "",

        "arrTime": "2023-04-24 16:05:00",

        "carrier": "IU",

        "codeShare": false,

        "depAirport": "DPS",

        "depTerminal": "",

        "depTime": "2023-04-24 15:15:00",

        "flightNumber": "IU743"

      }

    ],

    "scheduleChangeType": 1

  },

  "notificationId": "20230424050252711WZDMB",

  "status": 0,

  "type": "order.schedulechange"

}
```

c. \[意外取消]

这些是由我们的客户、航司或旅客自身进行的取消操作。此信息将发送给客户以进行确认，并在必要时通知客户。

示例：

```
{

  "cid": "xxxxxxxxxx",

  "data": {

    "orderNo": "RQWUV20230617185232880",

    "vendorRefundInformation": "FULLY"

  },

  "notificationId": "20230906014000568DRLNX",

  "status": 0,

  "type": "abnormal.cancelled"

}
```

{% endtab %}

{% tab title="示例" %}
**日程变更 - 邮件通知**

```json
{
    "cid":"xxxxxxxxxx",
    "type":"email.schedulechange",
    "notificationId":"20230323113246035DNIDD",
    "status":0,
    "data":{
        "orderNo":"TESTS20230323103458265",
        "emailSubject":"IMPORTANT: Flight delay notice. Confirmation Code KDK7QG",
        "emailLink":"https://theatlas/#/email-detail/4378270"
    }
}
```

> **提示**: 客户的服务器 URL 需要在 Atlas 注册才能通过 webhook 接收通知。

可以通过如下 API 完成注册：

```json
{

    "cid": "XXXXXXXX",

    "url": "https://xxx.com/xxxx"

}
```

也可以通过 ATRIP 在"我的资料"菜单的"客户信息"选项卡中进行注册。

接收通知：

将收到三种类型的事件通知。它们是：

a. \[日程变更 - 邮件通知] 使用 Atlas 生成的邮件 ID 从航司收到的任何日程变更邮件通知。

示例：

```json
{

    "cid":"xxxxxxxxxx",

    "type":"email.schedulechange",

    "notificationId":"20230323113246035DNIDD",

    "status":0,

    "data":{

        "orderNo":"TESTS20230323103458265",

        "emailSubject":"IMPORTANT: Flight delay notice. Confirmation Code KDK7QG",

        "emailLink":"https://theatlas/#/email-detail/4378270"

    }

}
```

请注意，邮件链接的有效期为 10 分钟。邮件中收到的数据需要存储在客户方。

b. \[日程变更 - API 通知]

结构化的日程变更通知。包含旧航班和新航班的信息。

示例：

```
{

  "cid": "xxxxxxxxxx",

  "data": {

    "orderNo": "XCEWF20221203094515954",

    "previousSegs": [

      {

        "arrAirport": "DPS",

        "arrTerminal": "",

        "arrTime": "2023-01-24 10:35:00",

        "carrier": "IU",

        "codeShare": false,

        "depAirport": "CGK",

        "depTerminal": "",

        "depTime": "2023-01-24 07:45:00",

        "flightNumber": "IU740"

      },

      {

        "arrAirport": "CGK",

        "arrTerminal": "",

        "arrTime": "2023-04-24 16:05:00",

        "carrier": "IU",

        "codeShare": false,

        "depAirport": "DPS",

        "depTerminal": "",

        "depTime": "2023-04-24 15:15:00",

        "flightNumber": "IU759"

      }

    ],

    "revisedSegs": [

      {

        "arrAirport": "CGK",

        "arrTerminal": "",

        "arrTime": "2023-04-24 16:05:00",

        "carrier": "IU",

        "codeShare": false,

        "depAirport": "DPS",

        "depTerminal": "",

        "depTime": "2023-04-24 15:15:00",

        "flightNumber": "IU743"

      }

    ],

    "scheduleChangeType": 1

  },

  "notificationId": "20230424050252711WZDMB",

  "status": 0,

  "type": "order.schedulechange"

}
```

c. \[意外取消]

这些是由我们的客户、航司或旅客自身进行的取消操作。此信息将发送给客户以进行确认，并在必要时通知客户。

示例：

```
{

  "cid": "xxxxxxxxxx",

  "data": {

    "orderNo": "RQWUV20230617185232880",

    "vendorRefundInformation": "FULLY"

  },

  "notificationId": "20230906014000568DRLNX",

  "status": 0,

  "type": "abnormal.cancelled"

}
```

{% endtab %}
{% endtabs %}

### 相关页面

* [Webhook 注册与事件](/api-wen-dang/api-reference/webhook-and-incident-apis/webhook-registration-and-incidents.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [事件查询](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-query.md)
* [日程变更通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/schedule-change-notification.md)
* [电子邮件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/email-notification.md)
