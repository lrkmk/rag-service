# 搜索与预订

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用本页面了解搜索响应、定价和预订时机问题。

当你需要以下内容时，从这里开始：

* 在 `search.do` 和 `getOffers.do` 之间选择
* 为下一步保留正确的标识符
* 了解为什么显示的价格在预订前发生变化
* 确认搜索、验证和订单之间的安全时机

### 常见问题

#### 每个预订步骤应保留哪个标识符？

为 `verify.do` 保留来自 `search.do` 的 `routingIdentifier`。

为标准流程中的 `order.do` 和座位查询保留来自 `verify.do` 的 `sessionId`。

为 Get Offer 订单流程保留来自 `getOffers.do` 的 `OfferId`。

#### 何时应使用 `search.do`，何时应使用 `getOffers.do`？

当 Atlas 是您的主要购物入口点时使用 `search.do`。

当您已经知道目标行程或需要独立价格检查时使用 `getOffers.do`。

#### 如何在 `search.do`、`getOffers.do` 和 `priceCompareSearch.do` 之间选择？

使用 `search.do` 进行标准预订。

当行程已知或需要独立价格检查时使用 `getOffers.do`。

使用 `priceCompareSearch.do` 进行售前航线覆盖和原始价格发现。

不要将 `priceCompareSearch.do` 用作生产预订的价格来源。

#### 为什么在 `search.do` 之后仍然需要 `verify.do`？

`search.do` 可能返回缓存定价。

`verify.do` 在创建订单前检查实时票价、库存和预订条件。

将验证响应视为预订前的当前真实来源。

### 用户可以切换显示货币吗？

不。\
定价以约定的合同货币返回。

### 为什么一些搜索结果中缺少税费明细？

许多低成本航空公司在预订期间或 PNR 中不提供税费拆分数据。\
Atlas 仅在航空公司提供时才能公开明细。

### `TransactionFeePerPax` 是什么意思？

这是 Atlas 按乘客收取的技术服务费。\
它与机票价格和税费分开。\
不可退款。

### 为什么缺少 `bookingclass` 或 `farebasis` 等字段？

许多低成本航空公司不返回这些值。\
在可用时使用 `cabin`。\
不要假设每个航空公司都存在 GDS 风格的票价数据。

### 搜索返回多少结果？

搜索默认返回所有可用报价。\
默认排序为最低票价优先。

### 何时应使用 `getOffers.do` 而不是 `search.do`？

当 Atlas 是您的主要购物入口点时使用 `search.do`。\
当您已经知道目标行程或需要独立价格检查时使用 `getOffers.do`。

`getOffers.do` 更适合外部购物引擎和最终价格验证流程。

### 为什么搜索和验证可能返回不同的价格？

搜索可能使用缓存数据。\
验证在创建订单前检查实时票价和可用性。

如果价格发生变化，将验证结果用作当前真实来源。\
对于 Get Offer 流程，在需要时刷新报价。

#### 搜索、验证和订单之间最安全的时机是什么？

搜索和验证之间最多允许 6 小时。

验证和订单之间最多允许 2 小时。

两种情况越短越安全。

### `seatCount` 是什么意思？

这是该票价的剩余座位数。\
Atlas 将实际最大值限制为 4，因为更大的低成本航空预订更容易失败。

### 搜索和验证之间可以等待多长时间？

最多允许 6 小时。\
时间越短越好，因为价格可能变化。

### Atlas 是否支持票价等级？

是的。\
当需要票价等级结果时，在搜索中启用 `includeMultipleFareFamily`。

可用性仍取决于航空公司的支持和当前库存。

### 可以在搜索期间过滤行李吗？

不。\
首先选择行程。

然后在行李在预订前重要时使用 `getLuggage.do` 查询行李选项。

请参阅[行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)。

### 支持哪些座位选择场景？

Atlas 支持支持 Atlas API 座位功能的航空公司的座位选择。

Atlas 支持 Atlas 发行的订单以及在预订流程中随机票购买的座位选择。

Atlas 不支持非 Atlas 发行的订单或出票后的座位选择。

请参阅[座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)了解当前支持范围。

### 可以仅使用航班信息调用 `seatAvailability.do` 吗？

不。

使用来自 `verify.do` 的有效 `sessionId` 或来自 `getOffers.do` 的 `OfferId`。

`seatAvailability.do` 不再支持独立模式。

如果您上游的座位请求仅包含航班数据，请先将其与缓存的 `sessionId` 匹配。

### 验证和订单之间可以等待多长时间？

最多允许 2 小时。\
时间越短越好，因为定价和可用性可能变化。

### 乘客数量可以在搜索和订单之间更改吗？

可以，只要仍有至少一名成人旅客。\
但在搜索、验证和订单之间保持相同的计数更安全。

验证后更改计数会增加失败风险，因为验证检查实时库存。

### `getOffers.do` 需要 `verify.do` 吗？

在标准的 Get Offer 流程中不需要。\
该路径围绕返回的 `OfferId` 构建，然后继续到 `order.do`。

在实现该路径时使用 Get Offer 指南和当前 API 参考。

#### 何时应刷新 Get Offer 结果？

当乘客数量、目标航班、预期票价或预订时机发生变化时刷新。

不要基于过时的报价假设创建订单。

### Atlas 是否对预订 API 应用请求限制？

是的。

Atlas 对选定的预订前 API 应用请求限制治理。

默认限制：

* `search.do` — `10 QPS`
* `verify.do` + `getOffers.do` — 共享 `60 QPM`
* `seatAvailability.do` + `getLuggage.do` — 共享 `60 QPM`

`order.do` 和 `pay.do` 不在此策略范围内。

### `429` 意味着什么？

意味着当前请求频率超出了配置的限制。

并不意味着账户被禁止。

也不意味着取消已经在进行中的订单。

### 如何处理 `429`？

读取返回的 `retryAfter` 值。

等待该延迟后重试。

减少突发流量并避免立即重试循环。

### `verify.do` 和 `getOffers.do` 是否单独计数？

不。

它们共享一个执行池。

默认共享限制为 `60 QPM`。

### `seatAvailability.do` 和 `getLuggage.do` 是否单独计数？

不。

它们共享一个附加服务池。

默认共享限制为 `60 QPM`。

### 缓存命中请求是否计入限制？

是的。

如果请求进入 Atlas 业务处理并返回结果，则计入池中。

使用 [API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)获取完整的限制模型。

### 相关页面

* [标识符](/api-wen-dang/product-guides/booking/booking-overview/identifiers.md)
* [搜索 vs 报价](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/search-vs-offer.md)
* [搜索](/api-wen-dang/product-guides/booking/booking-step-guides/search.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
