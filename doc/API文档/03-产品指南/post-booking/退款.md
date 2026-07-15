# 退款

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此部分处理完整的退款生命周期。

当您需要以下内容时从这里开始：

* 判断应该使用**退款**还是**作废**
* 遵循标准的退款流程
* 确认保留哪些标识符用于后续跟进

### 常见问题

#### 标准的 Atlas API 退款流程是什么？

标准流程是 `refundQuotation.do` → `refund.do` → `queryRefundOrders.do`。

在提交之前先进行报价。

#### 退款请求在提交前何时会失败？

当出票未完成、退款报价已过期、订单号错误或行程不完整时，退款请求可能失败。

先检查当前订单状态和退款条件。

#### 何时应该使用退款而不是作废？

当情况超出作废窗口或需要退款流程时使用退款。

当订单仍有资格使用专门的作废流程时，使用[作废](/api-wen-dang/product-guides/post-booking/void.md)。

### 典型流程

{% stepper %}
{% step %}

### 检查退款资格

首先调用 `refundQuotation.do`。

确认最新的可退款金额和条件。
{% endstep %}

{% step %}

### 提交退款

当流程需要基于报价提交时，使用最新的 `refundOfferId`。

保留返回的 `refundCode`。
{% endstep %}

{% step %}

### 查询最终状态

使用 `queryRefundOrders.do` 直到案件完成、被拒绝或以其他方式关闭。
{% endstep %}
{% endstepper %}

### 在提交退款前应确认什么？

确认：

* 原始 `orderNo` 正确无误
* 出票已完成（如需要）
* 退款请求中的行程信息完整
* 最新的 `refundOfferId` 或报价结果仍然有效

退款路径和对账时机也可能取决于支付方式。

### 在以下情况使用此页面

* 自愿退款
* 非自愿退款
* 退款状态跟进

### 此页面未涵盖的内容

此页面不列出完整的端点模式或字段级定义。

请使用 API 参考获取请求和响应详情。

### 完整 API 参考

在此查看端点级详细信息：

* [退款](/api-wen-dang/api-reference/post-booking-apis/refunds.md)

### 相关页面

* [作废](/api-wen-dang/product-guides/post-booking/void.md)
* [财务](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-finance.md)
* [预订后操作](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-post-ticketing.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [预订后 API](/api-wen-dang/api-reference/post-booking-apis.md)
