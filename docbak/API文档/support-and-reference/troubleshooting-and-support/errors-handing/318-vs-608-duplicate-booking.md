# 318 vs 608 重复预订

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当 Atlas 提示可能存在重复预订时使用本页面，您需要确认是否已存在真实预订。

### 简要回答

`318` 是订单阶段的重复预订信号。

`608` 是出票阶段的重复预订信号。

两者都意味着在再次尝试前应检查现有预订状态。

### 常见问题

#### `318` 通常意味着什么？

意味着在订单创建期间，可能存在具有相同乘客和航班详细信息的预订。

#### `608` 通常意味着什么？

意味着在出票过程中发现了重复预订。

#### 我应该立即重试吗？

不。

首先检查预订是否已存在。

### 核心区别

#### `318` — 订单创建时的重复预订

**失败阶段**

`order.do`

**通常含义**

Atlas 认为相同的乘客和行程可能已存在订单。

**下一步操作**

在重试前检查现有订单。

#### `608` — 出票时的重复预订

**失败阶段**

出票或支付后执行

**通常含义**

在执行链的后期发现了重复预订。

**下一步操作**

不要盲目开始新的预订。

检查旅客是否已有确认的预订。

### 首先检查什么

当这些代码出现时，检查：

* 相同乘客和行程的订单是否已存在
* 较早的订单上支付是否已成功
* 航空公司 PNR 或票号是否已存在
* 先前的重试是否创建了第二次尝试

### 快速决策规则

在生产中使用此规则：

* `318` — 在另一个 `order.do` 之前搜索现有订单
* `608` — 在任何新的预订或支付操作前检查执行结果

### 常见错误

#### 将重复预订信号视为普通失败

不要这样做。

新的重试可能会创建真正的重复旅客预订。

#### 在未检查现有订单的情况下从头重试

不要这样做。

首先确认旅客是否已有有效预订。

#### 忽略支付或出票活动后的部分成功

不要这样做。

重复信号可能在业务处理已推进后发生。

### 最佳实践

使用乘客姓名、行程、旅行日期和任何现有的 `orderNo` 或航空公司 PNR 来对账当前状态，然后再进行另一个预订操作。

### 相关页面

* [查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)
* [轮询和出票时机](/api-wen-dang/product-guides/booking/booking-step-guides/query-order/post-payment-polling.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [错误代码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [验证、订单与出票错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/verify-order-and-ticketing-errors.md)
