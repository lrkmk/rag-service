# 故障排除与支持

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当你需要故障排除材料、错误查询或支持资源时，使用本部分。

当你需要以下内容时，从这里开始：

* 排查失败的 API 调用
* 查看已知的集成问题或边缘情况
* 找到正确的支持或升级路径

### 常见问题

#### 当出现故障时，我应该从哪里开始？

当你有返回的状态码时，从[错误代码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)开始。

当问题涉及预期行为、设计决策或常见边缘情况时，使用[常见问题解答](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)。

#### 何时应使用支持资源？

当错误查询和常见问题解答无法解决问题时，或者当案例需要超出自助故障排除范围的运营跟进时，使用支持资源。

### 按症状开始排查

#### 请求被限流或返回 `429`

使用[429 vs 110](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/429-vs-110.md)区分限流与业务错误。

等待返回的 `retryAfter` 值后再重试。不要立即循环重试。

#### 搜索未返回预期结果或失败

使用[搜索错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/search-errors.md)检查请求验证、余额、航线限制和超时。

需要确认流程行为时，使用[搜索与预订常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-search-and-book.md)。

#### 支付、出票或订单状态异常

支付状态使用[支付错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/payment-errors.md)排查。

订单和出票问题使用[订单与出票常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-order.md)排查。

#### 退款、作废或出票后操作失败

使用[退款、查询与预订后错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/refund-query-and-post-booking-errors.md)选择正确处理路径。

### 本部分的页面

* [错误代码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [常见问题解答](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)
* [帮助中心](broken://spaces/DGvFJgcmYPDYk6hvtLpx/pages/Uz15LoKbrvyjsHXVzMDH)

### 本部分涵盖的内容

* 错误代码查询
* 集成常见问题解答
* 支持资源和帮助渠道

### 典型流程

{% stepper %}
{% step %}

### 检查错误或症状

从返回的错误代码或观察到的行为开始。
{% endstep %}

{% step %}

### 查看已知答案

使用常见问题解答确认预期行为和常见边缘情况。
{% endstep %}

{% step %}

### 必要时升级

当自助参考不足以解决问题时，使用支持资源。
{% endstep %}
{% endstepper %}

### 在需要以下内容时使用

* 调查失败的请求
* 检查常见的集成边缘情况
* 查找自助支持资源

### 后续步骤

从与症状匹配的页面开始，然后仅在自助指南不足以解决问题时升级。

### 相关页面

* [错误代码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [常见问题解答](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)
* [帮助中心](broken://spaces/DGvFJgcmYPDYk6hvtLpx/pages/Uz15LoKbrvyjsHXVzMDH)
