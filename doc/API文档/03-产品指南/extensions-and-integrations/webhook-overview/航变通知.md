# 航变通知

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当已出票的行程发生变化时，请使用此 webhook。

### 触发条件

当航班航段发生变更或被取消时，Atlas 发送 `order.schedulechange`。

### 您应该做什么

当您收到此事件时：

* 比较 `previousSegs`、`revisedSegs` 和 `originalSegs`
* 确定变更是日程更新还是取消
* 通知受影响的旅客
* 根据需要创建内部改签、退款或支持工作流程

### 端点

POST 到您在 Atlas 注册的 webhook URL。

### 首先读取的字段

* `type`
* `data.orderNo`
* `data.scheduleChangeType`
* `data.previousSegs`
* `data.revisedSegs`
* `data.originalSegs`

### 日程变更类型

* `1`: 日程变更
* `2`: 航班取消

### 典型负载

```json
{
  "cid": "XXXXXXX",
  "notificationId": "20230917143240511TATVO",
  "status": 0,
  "type": "order.schedulechange",
  "data": {
    "orderNo": "ATXFQ20230720193244809",
    "scheduleChangeType": 1,
    "previousSegs": [],
    "revisedSegs": [],
    "originalSegs": []
  }
}
```

### 注意事项

* `status` 反映事件确认状态，而非预订成功状态
* 在取消场景中，`revisedSegs` 可能为空
* `originalSegs` 保留旅客预订的行程

{% tabs %}
{% tab title="模式" %}
**cid**

* **类型:** 字符串
* **必填:** 是
* **描述:** 用于跟踪请求的唯一客户端标识符。
* **默认值:** 无
* **示例:** `"XXXXXXX"`

**notificationId**

* **类型:** 字符串
* **必填:** 是
* **描述:** 通知事件的唯一标识符。
* **默认值:** 无
* **示例:** `"20230917143240511TATVO"`

**status**

* **类型:** 整数
* **必填:** 是
* **描述:** 事件状态。

  有效值：

  * 0: 未确认
  * 1: 已确认
* **默认值:** 无
* **示例:** `0`

**type**

* **类型:** 字符串
* **必填:** 是
* **描述:** 通知类型。对于日程变更，始终为 `order.schedulechange`。
* **默认值:** 无
* **示例:** `"order.schedulechange"`

**data**

* **类型:** Object
* **必填:** 是
* **描述:** 包含之前、原始和修改后的航班航段。
* **默认值:** 无
* **示例:**

  ```json
  {
    "orderNo": "ATXFQ20230720193244809",
    "previousSegs": [ ... ],
    "revisedSegs": [ ... ],
    "originalSegs": [ ... ],
    "scheduleChangeType": 1
  }
  ```

**data.orderNo**

* **类型:** 字符串
* **必填:** 是
* **描述:** 与航班预订关联的唯一订单号。
* **默认值:** 无
* **示例:** `"ATXFQ20230720193244809"`

**data.scheduleChangeType**

* **类型:** 整数
* **必填:** 是
* **描述:** 日程变更的类型。

  有效值：

  * 1: 日程变更
  * 2: 航班取消
* **默认值:** 无
* **示例:** `1`

**data.previousSegs**

* **类型:** 对象数组
* **必填:** 是
* **描述:** 包含此次日程变更前的航班航段详情。
* **默认值:** 无

**data.previousSegs\[]**

* **类型:** Object
* **必填:** 是
* **描述:** 此次日程变更前的单个航班航段详情。
* **示例:**

  ```json
  {
    "depAirport": "HKG",
    "arrAirport": "SGN",
    "depTime": "2023-07-24 19:50:00",
    "arrTime": "2023-07-24 21:30:00",
    "carrier": "VJ",
    "flightNumber": "VJ877",
    "depTerminal": "",
    "arrTerminal": "",
    "direction": 1
  }
  ```

**data.previousSegs\[].depAirport**

* **类型:** 字符串
* **必填:** 是
* **描述:** 出发机场代码（IATA）。
* **默认值:** 无
* **示例:** `"HKG"`

**data.previousSegs\[].arrAirport**

* **类型:** 字符串
* **必填:** 是
* **描述:** 到达机场代码（IATA）。
* **默认值:** 无
* **示例:** `"SGN"`

**data.previousSegs\[].depTime**

* **类型:** 字符串
* **必填:** 是
* **描述:** 出发时间，格式为 `YYYY-MM-DD HH:MM:SS`。
* **默认值:** 无
* **示例:** `"2023-07-24 19:50:00"`

**data.previousSegs\[].arrTime**

* **类型:** 字符串
* **必填:** 是
* **描述:** 到达时间，格式为 `YYYY-MM-DD HH:MM:SS`。
* **默认值:** 无
* **示例:** `"2023-07-24 21:30:00"`

**data.previousSegs\[].carrier**

* **类型:** 字符串
* **必填:** 是
* **描述:** 航司代码。
* **默认值:** 无
* **示例:** `"VJ"`

**data.previousSegs\[].flightNumber**

* **类型:** 字符串
* **必填:** 是
* **描述:** 航司分配的航班号。
* **默认值:** 无
* **示例:** `"VJ877"`

**data.previousSegs\[].depTerminal**

* **类型:** 字符串
* **必填:** 否
* **描述:** 出发航站楼信息。
* **默认值:** `""`
* **示例:** `""`

**data.previousSegs\[].arrTerminal**

* **类型:** 字符串
* **必填:** 否
* **描述:** 到达航站楼信息。
* **默认值:** `""`
* **示例:** `""`

**data.previousSegs\[].direction**

* **类型:** 整数
* **必填:** 是
* **描述:** 1 表示去程航段，2 表示回程航段。
* **默认值:** 无
* **示例:** `1`

**data.revisedSegs**

* **类型:** 对象数组
* **必填:** 是
* **描述:** 包含日程变更后的航班航段详情。如果 `data.scheduleChangeType` 指示航班取消，此节点应为空数组（即没有受保护的航班）。
* **默认值:** 无

**data.revisedSegs\[]**

* **类型:** Object
* **必填:** 是
* **描述:** 日程变更后的单个航班航段详情。
* **示例:**

  ```json
  {
    "depAirport": "SGN",
    "arrAirport": "HKG",
    "depTime": "2023-10-19 15:10:00",
    "arrTime": "2023-10-19 18:50:00",
    "carrier": "VJ",
    "flightNumber": "VJ876",
    "codeShare": false,
    "depTerminal": "",
    "arrTerminal": "",
    "direction": 1
  }
  ```

**data.originalSegs**

* **类型:** 对象数组
* **必填:** 是
* **描述:** 包含任何日程变更前的原始航班航段详情。出票后可能会发生多次日程变更，此节点用于显示旅客预订机票时的航班航段详情。
* **默认值:** 无

**data.originalSegs\[]**

* **类型:** Object
* **必填:** 是
* **描述:** 旅客预订机票时的单个航班航段详情。
* **示例:**

  ```json
  {
    "depAirport": "HKG",
    "arrAirport": "SGN",
    "depTime": "2023-07-24 19:50:00",
    "arrTime": "2023-07-24 21:30:00",
    "carrier": "VJ",
    "flightNumber": "VJ877",
    "codeShare": false,
    "depTerminal": "",
    "arrTerminal": "",
    "direction": 1
  }
  ```

{% endtab %}

{% tab title="示例" %}

```json
{
    "cid": "XXXXXXX",
    "notificationId": "20230917143240511TATVO",
    "status": 0,
    "type": "order.schedulechange",
    "data": {
        "orderNo": "ATXFQ20230720193244809",
        "scheduleChangeType": 1,
        "previousSegs": [
            {
                "arrAirport": "SGN",
                "arrTerminal": "",
                "arrTime": "2023-07-24 21:30:00",
                "carrier": "VJ",
                "codeShare": false,
                "depAirport": "HKG",
                "depTerminal": "",
                "depTime": "2023-07-24 19:50:00",
                "flightNumber": "VJ877",
                "direction": 1
            },
            {
                "arrAirport": "HKG",
                "arrTerminal": "",
                "arrTime": "2023-10-18 18:50:00",
                "carrier": "VJ",
                "codeShare": false,
                "depAirport": "SGN",
                "depTerminal": "",
                "depTime": "2023-10-18 14:55:00",
                "flightNumber": "VJ876",
                "direction": 1
            }
        ],
        "revisedSegs": [
            {
                "arrAirport": "SGN",
                "arrTerminal": "",
                "arrTime": "2023-07-24 21:30:00",
                "carrier": "VJ",
                "codeShare": false,
                "depAirport": "HKG",
                "depTerminal": "",
                "depTime": "2023-07-24 19:50:00",
                "flightNumber": "VJ877",
                "direction": 1
            },
            {
                "arrAirport": "HKG",
                "arrTerminal": "",
                "arrTime": "2023-10-19 18:50:00",
                "carrier": "VJ",
                "codeShare": false,
                "depAirport": "SGN",
                "depTerminal": "",
                "depTime": "2023-10-19 15:10:00",
                "flightNumber": "VJ876",
                "direction": 1
            }
        ],
        "originalSegs": [
            {
                "arrAirport": "SGN",
                "arrTerminal": "",
                "arrTime": "2023-07-24 21:30:00",
                "carrier": "VJ",
                "codeShare": false,
                "depAirport": "HKG",
                "depTerminal": "",
                "depTime": "2023-07-24 19:50:00",
                "flightNumber": "VJ877",
                "direction": 1
            },
            {
                "arrAirport": "HKG",
                "arrTerminal": "",
                "arrTime": "2023-10-18 18:50:00",
                "carrier": "VJ",
                "codeShare": false,
                "depAirport": "SGN",
                "depTerminal": "",
                "depTime": "2023-10-18 14:55:00",
                "flightNumber": "VJ876",
                "direction": 1
            }
        ]
    }
}
```

{% endtab %}
{% endtabs %}

### 相关页面

* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [事件通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-notification.md)
* [事件查询](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/incident-query.md)
