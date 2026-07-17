# 作废通知

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要近实时的作废生命周期更新时，请使用此 webhook。

当您需要以下操作时，请从这里开始：

* 检测作废已成功提交
* 跟踪作废进度和最终结果
* 捕获拒绝或重试失败的原因

### 常见问题

#### 此 webhook 何时发送？

Atlas 在 `void.do` 成功后发送 `order.void`。

当作废状态发生变化时，Atlas 也会发送。

当自动处理在 10 次重试后仍然失败时，Atlas 再次发送。

#### 应以此取代作废查询吗？

不能。

将此 webhook 用作快速信号。

使用 `queryVoidOrders.do` 进行最终核对。

#### 首次作废结果预计多快返回？

在大多数情况下，Atlas 会在约 5 分钟内返回作废请求是否已被接受处理。

最终完成或拒绝仍可能需要更长时间。

将此 webhook 用于进度变更。

### 触发条件

Atlas 在以下场景发送 `order.void`：

* 作废成功提交
* 作废状态变更
* 10 次重试后自动失败

### 您应该做什么

当您收到此事件时：

* 匹配 `data.orderNo` 和 `data.voidCode`
* 使用 `data.voidStatus` 更新案件状态
* 存储 `data.message` 用于运营跟进

### 推荐的处理方式

按以下顺序处理事件：

1. 读取 `type` 并确认为 `order.void`。
2. 将 `data.orderNo` 与您的订单进行匹配。
3. 将 `data.voidCode` 与作废案件进行匹配。
4. 根据 `data.voidStatus` 更新内部状态。
5. 存储 `data.message` 用于审计和支持。
6. 如果案件仍处于开放状态，查询作废状态。

### 端点

POST 到您在 Atlas 注册的 webhook URL。

使用现有的 webhook 注册流程。

`order.void` 无需额外注册。

### 首先读取的字段

* `type`
* `data.orderNo`
* `data.voidCode`
* `data.voidStatus`
* `data.message`

### 作废状态值

* `0`: Atlas 处理中
* `1`: 航司处理中
* `2`: 已作废/已退款
* `3`: 航司作废中
* `4`: 已拒绝
* `5`: 已完成
* `6`: 已撤回

### 典型负载

```json
{
  "cid": "XXXXXXX",
  "type": "order.void",
  "status": -1,
  "data": {
    "orderNo": "TESTA20250512100600259",
    "voidCode": "202505-0012",
    "voidStatus": 2,
    "message": "Void successful and confirmed by the airline."
  }
}
```

### 重试失败行为

如果自动处理在 10 次重试后仍然失败，Atlas 会发送另一个 `order.void` 事件。

在这种情况下，预期 `data.voidStatus = 4`。

使用 `data.message` 安排手动跟进。

### 注意事项

* `status` 是内部字段，通常为 `-1`
* `message` 是描述性的，可能因案件而异
* 首次提交通常在约 5 分钟内给出反馈
* 如果退款完成状态仍不清楚，请使用作废查询

{% tabs %}
{% tab title="模式" %}
**cid**

* **类型:** 字符串
* **必填:** 是
* **描述:** 唯一客户端标识符。
* **示例:** `"XXXXXXX"`

**type**

* **类型:** 字符串
* **必填:** 是
* **描述:** 通知类型。始终为 `order.void`。
* **示例:** `"order.void"`

**status**

* **类型:** 整数
* **必填:** 是
* **描述:** 内部状态字段。`-1` 表示正常投递。
* **示例:** `-1`

**data**

* **类型:** Object
* **必填:** 是
* **描述:** 作废事件负载。

**data.orderNo**

* **类型:** 字符串
* **必填:** 是
* **描述:** Atlas 订单号。
* **示例:** `"TESTA20250512100600259"`

**data.voidCode**

* **类型:** 字符串
* **必填:** 是
* **描述:** `void.do` 返回的作废案件号。
* **示例:** `"202505-0012"`

**data.voidStatus**

* **类型:** 整数
* **必填:** 是
* **描述:** 当前作废处理状态。
* **有效值:**
  * `0`: Atlas 处理中
  * `1`: 航司处理中
  * `2`: 已作废/已退款
  * `3`: 航司作废中
  * `4`: 已拒绝
  * `5`: 已完成
  * `6`: 已撤回
* **示例:** `2`

**data.message**

* **类型:** 字符串
* **必填:** 否
* **描述:** 人类可读的状态或失败详情。
* **示例:** `"Void successful and confirmed by the airline."`
  {% endtab %}

{% tab title="示例" %}
**成功**

```json
{
  "cid": "XXXXXXX",
  "type": "order.void",
  "status": -1,
  "data": {
    "orderNo": "TESTA20250512100600259",
    "voidCode": "202505-0012",
    "voidStatus": 2,
    "message": "Void successful and confirmed by the airline."
  }
}
```

**重试失败**

```json
{
  "cid": "XXXXXXX",
  "type": "order.void",
  "status": -1,
  "data": {
    "orderNo": "TESTA20250512100600259",
    "voidCode": "202505-0012",
    "voidStatus": 4,
    "message": "Automatic void processing failed after 10 retries."
  }
}
```

{% endtab %}
{% endtabs %}

### 相关页面

* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [Webhook 注册与事件](/api-wen-dang/api-reference/webhook-and-incident-apis/webhook-registration-and-incidents.md)
* [作废](/api-wen-dang/api-reference/post-booking-apis/void.md)
* [作废工作流程](/api-wen-dang/product-guides/post-booking/void.md)
