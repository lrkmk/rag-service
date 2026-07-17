# 验证 vs 下单

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要决定预订问题属于 `verify.do` 还是 `order.do` 时，使用此页面。

### 简要回答

使用 `verify.do` 验证当前预订上下文。

使用 `order.do` 创建实际预订。

`verify.do` 告诉您需要什么。

`order.do` 提交预订请求。

### 常见问题

#### `verify.do` 的主要职责是什么？

它刷新运价、航线和预订要求。

它返回订单创建所需的 `sessionId` 和 `bookingRequirement`。

#### `order.do` 的主要职责是什么？

它创建订单。

它使用已验证的上下文、旅客数据、联系数据和附加服务选择。

#### 在标准搜索流程中可以跳过 `verify.do` 吗？

不可以。

在标准搜索流程中，`order.do` 依赖于 `verify.do` 返回的 `sessionId`。

### 边界在哪里

#### `verify.do`

用于回答：

* 行程是否仍然有效
* 最新的运价是什么
* 需要哪些旅客和证件字段
* 订单应使用哪个 `sessionId`

#### `order.do`

用于回答：

* Atlas 现在可以创建预订吗
* 旅客数据是否满足预订要求
* 附加服务选择是否仍然匹配当前上下文
* 支付接下来应使用哪个 `orderNo`

### 每个步骤返回什么

#### `verify.do` 返回

* `sessionId`
* 最新的运价和航线上下文
* `bookingRequirement`
* 附加服务上下文

#### `order.do` 返回

* `orderNo`
* 订单状态
* 与当前请求关联的预订结果

### 验证阶段通常失败的原因

典型的验证阶段失败包括：

* 过期的 `routingIdentifier`
* 搜索后航班售罄
* 目标航班变更
* 运价系列售罄
* 临时验证超时

典型代码包括：

* `202`
* `205`
* `206`
* `207`
* `210`
* `299`

### 订单创建阶段通常失败的原因

典型的订单阶段失败包括：

* 过期的 `sessionId`
* 旅客数据缺失或无效
* 过期的附加服务 `productCode`
* 验证后价格变化
* 预订提交前航班售罄

典型代码包括：

* `301`
* `302`
* `307`
* `308`
* `309`
* `410`

### 决策指南

#### 在以下情况下再次使用 `verify.do`

* 当前 `sessionId` 已过期
* 预订延迟
* 您需要最新的 `bookingRequirement`
* 您需要再次获取当前运价上下文

#### 在以下情况下使用 `order.do`

* `sessionId` 仍然新鲜
* 旅客和联系数据完整
* 附加服务选择匹配当前上下文
* 您已准备好创建预订

### 常见错误

#### 将验证视为仅可选的检查

不要这样做。

在标准流程中，它是 `sessionId` 和 `bookingRequirement` 的真实来源。

#### 基于过期的验证数据构建订单

不要这样做。

当预订关键输入发生变化或预订延迟时，刷新验证。

#### 期望 `order.do` 为您决定缺失的字段要求

不要这样做。

首先读取 `bookingRequirement`。

### 最佳实践

在 `order.do` 之前立即确认：

* `sessionId` 仍然有效
* `bookingRequirement` 是最新的
* 旅客数据匹配所需字段
* 附加服务映射匹配当前验证上下文

### 相关页面

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [标识符](/api-wen-dang/product-guides/booking/booking-overview/identifiers.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [202 vs 301 vs 308](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/202-vs-301-vs-308.md)
* [验证、订单和出票错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/verify-order-and-ticketing-errors.md)
