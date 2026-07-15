# 作废

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当订单可能仍有资格作废时使用此部分。

当您需要以下内容时从这里开始：

* 判断应该使用**作废**还是**退款**
* 遵循标准的作废流程
* 确认保留哪些标识符用于后续跟进

### 常见问题

#### 标准的 Atlas API 作废流程是什么？

标准流程是 `voidQuotation.do` → `void.do` → `queryVoidOrders.do`。

先请求报价。

然后使用最新的 `voidOfferId` 提交作废。

提交后，使用 `orderNo` 查询状态。

当需要查询特定作废案件时，添加 `voidCode`。

#### 作废请求在提交前何时会失败？

当订单已超出作废窗口、`orderNo` 错误或报价不再有效时，作废可能失败。

先检查当前订单状态并请求新的报价。

#### Atlas 是否支持部分旅客作废？

不支持。

Atlas 仅接受整单作废。

不要为 Atlas 作废设计拆分订单或拆分 PNR 的变通方案。

#### 何时应该使用作废？

当订单仍在航司作废窗口内时使用**作废**。

在提交之前先进行报价。

#### 何时应该使用退款？

当作废窗口已过或案件不再符合专门的作废路径时，使用**退款**。

不要在窗口关闭后继续重试作废。

### 当前 VOID 覆盖范围

Atlas VOID 目前支持横跨四个地区的 23 家航司。

#### 美洲

* `AS`
* `DM`
* `F9`
* `G4`
* `PB`
* `SY`
* `TS`
* `Y4`

#### 欧洲

* `A3`
* `D8`
* `EI`
* `DY`
* `N0`
* `OA`
* `VF`
* `Z0`

#### 日本

* `ZG` — 仅限美国航线

#### 韩国

* `7C`
* `BX`
* `LJ`
* `RS`
* `TW`
* `ZE`

近期新增：

* `TS`
* `Y4`
* `EI`
* `VF`

如果预订超出此范围，Atlas 可能返回 `843`。

### 典型流程

{% stepper %}
{% step %}

### 检查作废资格

首先调用 `voidQuotation.do`。

确认订单仍可作废。
{% endstep %}

{% step %}

### 提交作废

使用报价响应中的最新 `voidOfferId`。

保留返回的 `voidCode`。
{% endstep %}

{% step %}

### 查询最终状态

使用带有 `orderNo` 的 `queryVoidOrders.do` 直到案件完成、被拒绝或以其他方式关闭。

当需要将结果缩小到特定作废案件时，添加 `voidCode`。
{% endstep %}
{% endstepper %}

### 在提交前应确认什么？

确认：

* 原始 `orderNo` 正确无误
* 订单仍在作废窗口内
* 返回的当日截止时间尚未过去
* 使用最新的 `voidOfferId`
* 案件不应转入退款流程
* 请求涵盖整张订单，而非仅部分旅客

### 哪些标识符重要？

在流程中保留以下值：

* `orderNo` 用于报价和查询
* `voidOfferId` 用于提交
* `voidCode` 用于可选的状态筛选

在提交前使用最新的报价结果。

不要重复使用旧的 `voidOfferId`。

将返回的截止时间视为严格限制。

截止时间过后，`void.do` 将立即被拒绝。

### 在以下情况使用此页面

* 作废资格检查
* 作废提交跟进
* 退款边界决策

### 此页面未涵盖的内容

此页面不列出完整的端点模式或字段级定义。

请使用 API 参考获取请求和响应详情。

### 后续步骤

打开下方的端点页面查看请求和响应详情。

然后将结果与当前订单状态进行核对。

### 完整 API 参考

在此查看端点级详细信息：

* [作废](/api-wen-dang/api-reference/post-booking-apis/void.md)

### 相关页面

* [退款](/api-wen-dang/product-guides/post-booking/refunds.md)
* [预订后操作](/api-wen-dang/product-guides/post-booking.md)
* [预订后 API](/api-wen-dang/api-reference/post-booking-apis.md)
* [退款、查询与预订后错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/refund-query-and-post-booking-errors.md)
