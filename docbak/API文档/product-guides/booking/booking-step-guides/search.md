# 搜索

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此页面开始预订流程。

{% hint style="warning" %}
`Smart Search` (`smartSearch.do`) 即将弃用。

不要将其用于新集成。请优先使用标准 `search.do` 流程。
{% endhint %}

当您需要以下内容时从这里开始：

* 开始标准预订流程
* 在 `search.do` 和 `getOffers.do` 之间做选择
* 了解为下一步保留哪个标识符

### 常见问题

#### 何时应使用 `search.do`？

当 Atlas 是您的主要购物入口点时，使用 `search.do`。

保留返回的 `routingIdentifier` 用于 `verify.do`。

#### 何时应使用 `getOffers.do`？

当您已知道目标行程或需要独立价格检查时，使用 `getOffers.do`。

保留返回的 `OfferId` 用于订单流程。

#### `search.do` 适用什么请求限制？

`search.do` 默认使用 `10 QPS`。

超限请求返回 Atlas 错误代码 `429`。

在重试前遵守返回的 `retryAfter` 值。

### 搜索请求限制

Atlas 在滚动 1 秒窗口中计算 `search.do`。

除非 Atlas 为您的账户配置了不同的层级，否则使用 `10 QPS` 作为默认限制。

#### 什么计入

以下请求会计入：

* 成功的搜索
* 无结果的搜索
* 业务失败、航司失败和缓存命中的响应

以下请求不计入：

* 被请求限制治理拒绝的请求
* 认证、权限或验证失败

#### 如何避免 `429`

尽可能使用本地缓存。

合并重复搜索。

在重试前使用返回的 `retryAfter` 值退避。

### 此页面涵盖的内容

* 标准报价搜索
* 独立的获取报价查询
* 高级或智能搜索流程
* 报价轮询和请求跟进

### 主要 API

* `search.do`
* `getOffers.do`
* `smartSearch.do`

### 关键输出

* 用于标准验证流程的 `routingIdentifier`
* 用于获取报价订单流程的 `OfferId`
* 用于智能搜索跟进的 `requestId`
* 用于下游选择的报价数据

### 应保留哪个标识符？

保留与流程匹配的标识符：

* `routingIdentifier` 用于标准搜索 → 验证流程
* `OfferId` 用于获取报价 → 订单流程
* `requestId` 仅用于智能搜索跟进

不要跨流程混合使用标识符。

### 在以下情况下使用此部分

* 标准搜索到预订流程
* 无需标准搜索的独立报价查询
* 智能或异步搜索行为
* 智能搜索后的报价刷新

### 接下来是什么？

#### 标准流程

使用 `routingIdentifier` 调用[验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)。

#### 获取报价流程

继续使用[获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)，然后使用 `OfferId` 创建订单。

#### 智能搜索流程

仅对现有实现使用智能搜索跟进。

### 相关页面

* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [沙箱访问](/api-wen-dang/readme-1/making-requests.md)
* [预订 API](/api-wen-dang/api-reference/booking-apis.md)

### 完整 API 参考

在此查看端点级详情：

* [搜索](/api-wen-dang/api-reference/booking-apis/search.md)
* [智能搜索](/api-wen-dang/api-reference/booking-apis/smart-search.md)
* [获取报价](/api-wen-dang/api-reference/booking-apis/get-offer.md)
