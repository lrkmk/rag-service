# 获取报价 vs 获取报价价格

{% hint style="info" %}
💬 **Need help?** If you're stuck, ask Eva in the Help Center for instant diagnostics.

<a href="https://resources.atriptech.com/?fallback=true" class="button primary" data-icon="comments">Ask Eva</a>
{% endhint %}

当您需要在 `getOffers.do` 和 `getOfferPrice.do` 之间做选择时，使用此页面。

### 简要回答

对于标准独立定价路径，使用 `getOffers.do`。

对于具有更广泛可见性和严格 5 分钟出票窗口的获取报价价格路径，使用 `getOfferPrice.do`。

### 核心区别

#### `getOffers.do`

这是标准的 Atlas 获取报价路径。

当您在正常预订流程前需要独立价格检查时，它最合适。

#### `getOfferPrice.do`

这是获取报价价格路径。

当您需要 Atlas 接受更困难的履约场景并在更紧的操作时限内完成预订时，它最合适。

### 附加服务支持

两条路径都可以在 `order.do` 前支持可选附加服务。

在两条路径中，都使用返回的 `OfferId` 作为附加服务上下文。

区别在于操作时序，而不是附加服务可用性。

### 获取报价价格路径的变化

`getOfferPrice.do` 可以返回标准获取报价路径可能不显示的报价。

示例包括：

* 临近出发的航班
* 售罄风险场景
* 高于 `OW + OW` 的往返价格

### 时序差异

#### 标准获取报价路径

标准预订流程遵循正常订单时序。

它不应用履约特定的 5 分钟出票规则。

它仍然可以在 `order.do` 前添加可选座位或行李。

#### 获取报价价格路径

获取报价价格路径应用 5 分钟支付和出票窗口。

如果出票未及时完成，订单将自动取消。

它也可以在 `order.do` 前添加可选座位或行李，但附加服务步骤必须保持在更严格的履约时限内。

### 请求限制差异

#### 标准获取报价路径

`getOffers.do` 与 `verify.do` 共享标准履约限制池。

#### 获取报价价格路径

`getOfferPrice.do` 使用自己的请求限制策略。

不要假设限制与 `verify.do` 或 `getOffers.do` 共享。

### 恢复差异

#### 标准获取报价路径

重试决策通常关注新鲜的报价检索、过期的预订上下文或支付状态检查。

#### 获取报价价格路径

重试决策还必须尊重剩余的获取报价价格窗口。

在每次重试前，确认订单仍在安全操作窗口内。

### 决策指南

在以下情况下使用 `getOffers.do`：

* Atlas 是您的价格检查和预订层
* 您需要标准的独立报价流程
* 您可能希望在没有履约时序压力的情况下进行附加销售
* 正常订单时序可以接受

在以下情况下使用 `getOfferPrice.do`：

* 您需要具有履约路径的可选附加服务
* 您需要更广泛的展示规则
* 您需要快速履约路径
* 您的系统可以立即支付并主动监控

### 最佳实践

在没有业务规则的情况下，不要在这两个 API 之间切换流量。

将它们视为具有不同操作行为的独立产品路径。

### 相关页面

* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [获取报价价格](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)
* [可选附加服务](/api-wen-dang/product-guides/booking/optional-ancillaries.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)
