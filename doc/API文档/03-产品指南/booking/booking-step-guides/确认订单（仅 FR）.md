# 确认订单（仅 FR）

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

仅 FR 预订流程使用此页面。

此页面以"确认订单"为主要名称。

您也可能看到此步骤称为"订单提交"。

{% hint style="info" %}
大多数航司不使用此步骤。

对于标准预订流程，直接调用 `order.do`，然后调用 `pay.do`。

只有 FR 在这两个步骤之间插入 `orderCommit.do`。
{% endhint %}

### 主要 API

* `orderCommit.do`

### 此步骤的适用场景

仅在以下情况下使用"确认订单"：

* 航司是 FR
* 预订流程返回 FR 确认页面
* 用户必须在支付前完成 FR 确认

在以下情况下跳过此步骤：

* 航司不是 FR
* 订单可以直接从 `order.do` 进入 `pay.do`

如果您正在构建标准预订流程，请不要将"确认订单"添加为必需步骤。

### 在流程中的位置

#### 标准流程

* `verify.do`
* `order.do`
* `pay.do`

#### FR 流程

* `verify.do`
* `order.do`
* `orderCommit.do`
* 用户完成 FR 确认
* `pay.do`

### 注意事项

* 此步骤为航司特定
* FR 必须使用此步骤
* 支付必须等待 FR 确认完成
* "确认订单"和"订单提交"是同一个步骤

### 返回内容

Atlas 返回一个 `confirmationUrl`。

在以下模式中使用它：

* 弹窗模式
* iframe 模式

### 相关页面

* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [FR 集成](/api-wen-dang/product-guides/extensions-and-integrations/special-integrations/fr-integration.md)
* [预订 API](/api-wen-dang/api-reference/booking-apis.md)

### 完整 API 参考

在此处查看端点级别的详细信息：

* [确认订单](/api-wen-dang/api-reference/booking-apis/confirm-order.md)
