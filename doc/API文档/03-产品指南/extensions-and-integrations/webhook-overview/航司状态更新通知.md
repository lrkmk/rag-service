# 航司状态更新通知

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要对航司级别的可用性变更做出反应时，请使用此 webhook。

这是 Atlas 多渠道通知中的第一个实时场景。

使用[多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)配置跨 webhook、电子邮件和团队聊天的 ATRIP 投递。

### 触发条件

当航司在活跃、维护或停用状态之间转换时，Atlas 发送 `airline.status`。

常见原因包括数据质量问题、系统问题、余额不足、计划内维护以及搜索出票比限制。

### 您应该做什么

当您收到此事件时：

* 更新内部航司可用性标志
* 调整搜索缓存或路由行为
* 如有需要，对处于停用或维护状态的航司禁止预订流程

### 端点

POST 到您在 Atlas 注册的 webhook URL。

### 首先读取的字段

* `type`
* `data.airline`
* `data.airlineStatus`

### 航司状态值

* `Active`（活跃）
* `Maintenance`（维护）
* `Inactive`（停用）

### 典型负载

```json
{
  "data": {
    "airline": ["TO", "HV"],
    "airlineStatus": "Active"
  },
  "status": -1,
  "type": "airline.status"
}
```

{% hint style="info" %}
电子邮件和聊天投递可能会以业务字段（如航司、状态、开始时间、原因、预计恢复时间和详情链接）呈现此事件。这些显示字段是渠道特定的，不属于本页的 webhook 模式。
{% endhint %}

### 注意事项

* `status` 是内部字段，不应用于业务逻辑
* 此事件是运营性的，并非特定于订单
* 在恢复之前，将 `Maintenance` 和 `Inactive` 视为不可预订状态

{% tabs %}
{% tab title="模式" %}
**data**

* **类型:** Object
* **必填:** 是
* **描述:** 包含航司信息，包括航司代码及其状态。
* **默认值:** 无
* **示例:**

  ```json
  {
    "airline": ["TO", "HV"],
    "airlineStatus": "Active"
  }
  ```

**data.airline**

* **类型:** 字符串数组
* **必填:** 是
* **描述:** 与响应关联的航司代码列表。
* **默认值:** 无
* **示例:** `["TO", "HV"]`

**data.airlineStatus**

* **类型:** 字符串
* **必填:** 是
* **描述:** 指示航司的运营状态。
* **有效值:**
  * Active = 在线
  * Maintenance = 航司正在维护中
  * Inactive = 离线
* **默认值:** 无
* **示例:** `"Active"`

**status**

* **类型:** 整数
* **必填:** 是
* **描述:** 指示响应状态。仅供 Atlas 内部使用。
* **默认值:** 无
* **示例:** `-1`

**type**

* **类型:** 字符串
* **必填:** 是
* **描述:** 指定响应消息的类型。
* **有效值:**
  * airline.status
* **默认值:** 无
* **示例:** `"airline.status"`
  {% endtab %}

{% tab title="示例" %}

```json
{
  "data":{
     "airline":["TO","HV"],
     "airlineStatus":"Active"},
  "status":-1,
  "type":"airline.status"
}
```

{% endtab %}
{% endtabs %}

### 相关页面

* [多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [搜索错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/search-errors.md)
