# 出票完成通知

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要订单的最终出票结果时，请使用此 webhook。

当您需要以下操作时，请从这里开始：

* 检测出票已完成
* 存储机票号码和航司 PNR
* 触发出票后的客户或运营工作流程

### 常见问题

#### 何时应依赖此 webhook？

将此 webhook 用作出票完成的近实时信号。

当您需要最终核实时，请使用订单查询。

#### 此事件的主要业务含义是什么？

此事件表示 Atlas 已完成出票，且机票详情在负载中可用。

最重要的结果是订单可以从出票跟进状态转移到已出票处理状态。

### 触发条件

出票完成后，Atlas 发送 `order.ticketed`。

### 您应该做什么

当您收到此事件时：

* 将订单标记为已出票
* 存储机票号码和航司 PNR
* 更新面向旅客的行程详情
* 如有需要，触发预订确认消息

### 推荐的处理方式

按以下顺序处理事件：

1. 读取 `type` 并确认其为 `order.ticketed`。
2. 将 `data.orderNo` 与您的内部预订进行匹配。
3. 为每位旅客存储 `ticketNos` 和 `airlinePNRs`。
4. 在检查通过后，将订单更新为已出票状态。
5. 如果下游状态仍不清楚，请通过订单查询进行核对。

### 端点

POST 到您在 Atlas 注册的 webhook URL。

### 首先读取的字段

* `type`
* `data.orderNo`
* `data.orderStatus`
* `data.paxTicketInfos[].ticketNos`
* `data.paxTicketInfos[].airlinePNRs`

### 订单状态值

首先读取 `data.orderStatus`：

* `0`: 未支付
* `1`: 出票中
* `2`: 已出票
* `-3`: 已取消（因请求信息问题导致预订失败）

### 典型负载

```json
{
  "cid": "XXXXXXX",
  "data": {
    "orderNo": "TESTL20230922153224323",
    "orderStatus": 2,
    "paxTicketInfos": [
      {
        "name": "zhang/lisi",
        "passengerType": 1,
        "ticketNos": ["S30814"],
        "airlinePNRs": ["S30814"],
        "ancillaries": []
      }
    ]
  },
  "status": -1,
  "type": "order.ticketed"
}
```

### 注意事项

* `orderStatus=2` 表示已出票
* `status` 是内部字段，不应驱动业务逻辑
* 使用订单号和机票号码进行下游核对
* 如果您的系统需要额外的确认步骤，请使用订单查询

### 此事件的最佳用途

将此事件用于：

* 订单履行更新
* 旅客确认流程
* 中台或财务核对输入

### 此事件不应取代的内容

此事件不应取代：

* 用于最终状态检查的订单查询
* 您自己的预订到客户核对
* 当更广泛的订单状态仍不清楚时的事件跟进

{% tabs %}
{% tab title="模式" %}
**cid**

* **类型:** 字符串
* **必填:** 是
* **描述:** 用于跟踪请求的唯一客户端标识符。
* **默认值:** 无
* **示例:** `"XXXXXXX"`

**data**

* **类型:** Object
* **必填:** 是
* **描述:** 包含订单相关信息。
* **默认值:** 无
* **示例:**

```
{
  "orderNo": "TESTL20230922153224323",
  "orderStatus": 2,
  "paxTicketInfos": [ ... ]
}
```

**data.orderNo**

* **类型:** 字符串
* **必填:** 是
* **描述:** 与机票购买关联的唯一订单号。
* **默认值:** 无
* **示例:** `"TESTL20230922153224323"`

**data.orderStatus**

* **类型:** 整数
* **必填:** 是
* **描述:** 订单状态。
* **有效值:**
  * 0: 未支付
  * 1: 出票中
  * 2: 已出票
  * -3: 已取消（因请求信息问题导致预订失败）
* **默认值:** 无
* **示例:** `2`

**data.paxTicketInfos**

* **类型:** 对象数组
* **必填:** 是
* **描述:** 包含旅客及其关联机票信息的详情。
* **默认值:** 无

**data.paxTicketInfos\[]**

* **类型:** Object
* **必填:** 是
* **描述:** 单个旅客的机票详情。
* **示例:**

```
{
  "name": "zhang/lisi",
  "passengerType": 1,
  "birthday": "20160202",
  "gender": "F",
  "cardNum": "123458",
  "cardType": "PP",
  "cardIssuePlace": "CN",
  "cardExpired": "20400101",
  "nationality": "CN",
  "ticketNos": ["S30814"],
  "airlinePNRs": ["S30814"],
  "ancillaries": []
}
```

**data.paxTicketInfos\[].name**

* **类型:** 字符串
* **必填:** 是
* **描述:** 旅客姓名，采用标准航司格式（姓/名 中间名）。
* **默认值:** 无
* **示例:** `"zhang/lisi"`

**data.paxTicketInfos\[].passengerType**

* **类型:** 整数
* **必填:** 是
* **描述:** 旅客类型。

  有效值：

  * `0` = 成人
  * `1` = 儿童
  * `2` = 婴儿
* **默认值:** 无
* **示例:** `1`

**data.paxTicketInfos\[].birthday**

* **类型:** 字符串
* **必填:** 是
* **描述:** 旅客出生日期，格式为 `YYYYMMDD`。
* **默认值:** 无
* **示例:** `"20160202"`

**data.paxTicketInfos\[].gender**

* **类型:** 字符串
* **必填:** 是
* **描述:** 旅客性别。\
  有效值：
  * `M` 表示男性
  * `F` 表示女性
* **默认值:** 无
* **示例:** `"F"`

**data.paxTicketInfos\[].cardNum**

* **类型:** 字符串
* **必填:** 是
* **描述:** 身份证件号码（护照或身份证）。
* **默认值:** 无
* **示例:** `"123458"`

**data.paxTicketInfos\[].cardType**

* **类型:** 字符串
* **必填:** 是
* **描述:** 身份证件类型。
* **有效值:**
  * PP - 护照
  * GA - 港澳通行证（中国大陆居民）
  * TW - 台湾通行证（中国大陆居民）
  * TB - 台胞证（台湾居民）
  * HY - 国际海员证
* **默认值:** 无
* **示例:** `"PP"`

**data.paxTicketInfos\[].cardIssuePlace**

* **类型:** 字符串
* **必填:** 是
* **描述:** 签发身份证件的国家或机构。
* **默认值:** 无
* **示例:** `"CN"`

**data.paxTicketInfos\[].cardExpired**

* **类型:** 字符串
* **必填:** 是
* **描述:** 身份证件过期日期，格式为 `YYYYMMDD`。必须是有效的未来日期。
* **默认值:** 无
* **示例:** `"20400101"`

**data.paxTicketInfos\[].nationality**

* **类型:** 字符串
* **必填:** 是
* **描述:** 旅客国籍，使用国家代码（ISO 3166-1 alpha-2）。
* **默认值:** 无
* **示例:** `"CN"`

**data.paxTicketInfos\[].ticketNos**

* **类型:** 字符串数组
* **必填:** 是
* **描述:** 与该旅客关联的已出票机票号码列表。
* **默认值:** 无
* **示例:** `["S30814"]`

**data.paxTicketInfos\[].airlinePNRs**

* **类型:** 字符串数组
* **必填:** 是
* **描述:** 旅客姓名记录（PNR）代码列表。
* **默认值:** 无
* **示例:** `["S30814"]`

**data.paxTicketInfos\[].ancillaries**

* **类型:** 数组
* **必填:** 是
* **描述:** 与该旅客关联的辅助服务列表（例如，额外行李、座位选择）。
* **默认值:** `[]`
* **示例:** `[]`

**status**

* **类型:** 整数
* **必填:** 是
* **描述:** 指示响应状态。
* **默认值:** 无
* **示例:** `-1`

**type**

* **类型:** 字符串
* **必填:** 是
* **描述:** 指定响应消息的类型。
* **默认值:** 无
* **示例:** `"order.ticketed"`
  {% endtab %}

{% tab title="示例" %}

```json
{
  "cid": "XXXXXXX",
  "data": {
    "orderNo": "TESTL20230922153224323",
    "orderStatus": 2,
    "paxTicketInfos": [
      {
        "airlinePNRs": [
          "S30814"
        ],
        "ancillaries": [],
        "birthday": "20160202",
        "cardExpired": "20400101",
        "cardIssuePlace": "CN",
        "cardNum": "123458",
        "cardType": "PP",
        "gender": "F",
        "name": "zhang/lisi",
        "nationality": "CN",
        "passengerType": 1,
        "ticketNos": [
          "S30814"
        ]
      },
      {
        "airlinePNRs": [
          "S30814"
        ],
        "ancillaries": [],
        "birthday": "19920202",
        "cardExpired": "20400101",
        "cardIssuePlace": "CN",
        "cardNum": "123457",
        "cardType": "PP",
        "gender": "F",
        "name": "li/si",
        "nationality": "CN",
        "passengerType": 0,
        "ticketNos": [
          "S30814"
        ]
      },
      {
        "airlinePNRs": [
          "S30814"
        ],
        "ancillaries": [],
        "birthday": "19910101",
        "cardExpired": "20400101",
        "cardIssuePlace": "CN",
        "cardNum": "123456",
        "cardType": "PP",
        "gender": "M",
        "name": "zhang/san",
        "nationality": "CN",
        "passengerType": 0,
        "ticketNos": [
          "S30814"
        ]
      }
    ]
  },
  "status": -1,
  "type": "order.ticketed"
}
```

{% endtab %}
{% endtabs %}

### 相关页面

* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [事件查询](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-query.md)
