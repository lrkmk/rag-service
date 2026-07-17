# 搜索 vs 报价

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要在 `search.do` 和 `getOffers.do` 之间做选择时，使用此页面。

### 简要回答

当 Atlas 是您的主要购物入口点时，使用 `search.do`。

当目标行程已知或需要独立价格检查时，使用 `getOffers.do`。

### 常见问题

#### 何时应使用 `search.do`？

当您希望 Atlas 首先返回可用报价时，使用 `search.do`。

这是标准的 Atlas 预订流程。

#### 何时应使用 `getOffers.do`？

当购物发生在 Atlas 外部或您已知道目标行程时，使用 `getOffers.do`。

这也是进行最终独立价格检查的正确路径。

#### 每个流程返回哪个标识符？

`search.do` 返回 `routingIdentifier`。

`getOffers.do` 返回 `OfferId`。

#### `getOffers.do` 是否仍需要 `verify.do`？

在此站点的标准获取报价流程中不需要。

该流程以 `OfferId` 为中心，然后继续到 `order.do`。

### 核心区别

#### `search.do`

用于报价发现。

Atlas 返回航线和日期的可用选项。

然后标准路径继续到 `verify.do`。

#### `getOffers.do`

用于针对性价格检索。

Atlas 返回已知行程的当前报价上下文。

然后流程继续使用 `OfferId`。

### 应选择哪个流程？

#### 选择 `search.do` 当

* Atlas 是您的主要搜索层
* 用户需要可用报价列表
* 您需要标准的搜索 → 验证 → 订单路径

#### 选择 `getOffers.do` 当

* 您自己的系统已经选择了航班
* 您需要在订单创建前进行独立价格检查
* 您希望 Atlas 作为定价和预订层，而不是搜索层

### 接下来是什么？

#### 在 `search.do` 之后

1. 保留 `routingIdentifier`
2. 调用 `verify.do`
3. 保留 `sessionId`
4. 调用 `order.do`

#### 在 `getOffers.do` 之后

1. 保留 `OfferId`
2. 可选地查询座位或行李
3. 调用 `order.do`

### 座位和行李的差异

#### 标准搜索流程

使用来自 `verify.do` 的 `sessionId` 进行 `seatAvailability.do`。

#### 获取报价流程

使用来自 `getOffers.do` 的 `OfferId` 进行 `seatAvailability.do`。

在两个流程中，仅在目标行程确认后查询行李。

### 时序和刷新规则

#### 搜索流程

`routingIdentifier` 最长有效 6 小时。

`sessionId` 最长有效 2 小时。

#### 获取报价流程

当行程、旅客组合、预期运价或预订时序发生变化时，刷新报价。

不要基于过时的报价假设构建订单。

### 常见错误

#### 跨流程混淆标识符

不要将 `OfferId` 当作 `routingIdentifier` 使用。

不要将 `routingIdentifier` 当作 `OfferId` 使用。

#### 跳过正确的下一步

不要在 `verify.do` 之前从标准搜索流程调用 `order.do`。

不要将 `verify.do` 添加到标准获取报价路径，除非您的实现特别需要。

### 按用例推荐页面

#### 需要标准搜索和预订

使用[搜索](/api-wen-dang/product-guides/booking/booking-step-guides/search.md)。

#### 需要独立价格检索

使用[获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)。

#### 需要完整的预订序列

使用[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)。

### 相关页面

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [标识符](/api-wen-dang/product-guides/booking/booking-overview/identifiers.md)
* [搜索](/api-wen-dang/product-guides/booking/booking-step-guides/search.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
