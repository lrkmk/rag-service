# 支付后轮询

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当支付成功但出票尚未完成时使用此页面。

这不是一个独立的预订步骤。

标准流程仍然以通过 `queryOrderDetails.do` 进行订单跟进结束。

### 简要说明

`pay.do` 成功并不总是意味着出票已完成。

持续轮询 `queryOrderDetails.do` 直到最终出票状态得到确认。

将此页面视为"查询订单"步骤的跟进指导。

使用 webhook 作为补充，而不是唯一的确认方式。

### 常见问题

#### 何时开始轮询？

在 `pay.do` 返回且订单进入支付后跟进阶段时开始。

#### 何时停止轮询？

当订单达到最终出票结果或其他已确认的终态时停止。

#### Webhook 应取代轮询吗？

不。

Webhook 有帮助，但订单查询应保持为您的首要状态来源。

### 支付成功不保证的内容

支付成功并不总是保证：

* 航司 PNR 已可用
* 票号已签发
* 出票已完成

将支付和最终出票视为独立的里程碑。

### 主要状态来源

使用 `queryOrderDetails.do` 作为支付后的主要事实来源。

至少检查：

* `orderStatus`
* `ticketStatus`
* 航司 PNR 详情
* 票号（如可用）

### 推荐的轮询模式

使用受控的轮询循环。

一个实用的模式是：

1. 在 `pay.do` 后调用 `queryOrderDetails.do`
2. 在出票仍在进行中时，以退避方式继续轮询
3. 仅在最终结果确认后停止

#### 建议的节奏

以短间隔开始。

如果出票仍在进行中，则拉长间隔。

不要以紧密循环的方式频繁调用订单查询端点。

### 何时不重试支付

不要因为票号尚未出现就重试 `pay.do`。

先检查订单状态。

以下情况尤其重要：

* `402`
* `404`
* `406`
* `615`

### 常见时间场景

#### 支付成功且出票仍在进行中

继续轮询。

这是正常情况。

#### 支付正在进行中

不要发送另一笔支付请求。

等待并再次查询订单。

#### 支付成功但 PNR 仍缺失

不要重试支付。

改为监控订单状态。

#### 出票延迟超过预期

保持订单在跟进中。

如果状态停滞或重复出现错误，请附带订单上下文升级处理。

### 常见错误

#### 在收到第一个成功的支付响应后停止

不要这样做。

订单可能仍在出票中。

#### 在首次支付仍在处理时重试支付

不要这样做。

这会带来重复支付的风险。

#### 将 webhook 作为唯一的完成信号

不要这样做。

持续轮询直到最终订单状态得到确认。

### 最佳实践

在整个跟进链中记录以下值：

* `orderNo`
* 支付请求时间
* 最新 `orderStatus`
* 最新 `ticketStatus`
* 航司 PNR（如可用）
* 最终票号（如可用）

### 相关页面

* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [支付错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/payment-errors.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
