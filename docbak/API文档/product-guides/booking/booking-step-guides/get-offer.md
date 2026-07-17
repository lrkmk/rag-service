# 获取报价

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要独立的报价查询流程时，使用此页面。

{% hint style="info" %}
使用 OpenAPI 命名作为真实来源。

在文档和集成中使用 `getOffers.do`。
{% endhint %}

当您需要以下内容时从这里开始：

* 对已知行程进行定价（无需标准搜索流程）
* 在订单创建前获取新鲜的 `OfferId`
* 在预订前运行行李或座位查询

### 常见问题

#### 何时应使用 `getOffers.do`？

当您已知道目标行程或需要在预订前进行独立价格检查时，使用 `getOffers.do`。

当购物发生在 Atlas 外部且 Atlas 用作预订和定价层时，此流程非常合适。

不要将此页面作为履约特定 `getOfferPrice.do` 路径的真实来源。

当流程需要更广泛的展示规则和 5 分钟出票窗口时，使用[获取报价价格](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)。

#### 应从获取报价响应中保留什么？

保留 `OfferId`。

将其用作下游订单创建的关键标识符。

在预订前需要座位查询时，将同一 `OfferId` 用于 `seatAvailability.do`。

#### `getOffers.do` 适用什么请求限制？

`getOffers.do` 与 `verify.do` 共享一个 `60 QPM` 的履约池。

超限请求返回 Atlas 错误代码 `429`。

在重试前遵守返回的 `retryAfter` 值。

### 履约请求限制

Atlas 在滚动 60 秒窗口中一起计算 `getOffers.do` 和 `verify.do`。

默认共享限制为 `60 QPM`。

一个繁忙的 API 会消耗另一个的共享池。

#### 什么计入

以下请求会计入：

* 成功的响应
* 无结果的响应
* 业务失败、航司失败和缓存命中的响应

#### 如何减少限制压力

当预订上下文未发生变化时，重用新鲜的报价数据。

避免在短时间内对同一行程进行重复价格检查。

当返回 `429` 时，遵守 `retryAfter`。

### 主要 API

* `getOffers.do`

### 输入

* 准确的行程详情
* 请求要求时的旅客组合
* 当前 API 参考要求的任何字段

### 关键输出

* 最新可预订运价
* 库存状态
* 用于下游订单创建的 `OfferId`
* 用于获取报价路径中 `seatAvailability.do` 的 `OfferId`

### 接下来是什么？

#### 最小路径

继续使用[创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)，然后[支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)。

#### 带座位和行李的路径

在订单创建前使用[座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)和[行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)。

### 与标准搜索的区别

#### 标准搜索流程

当 Atlas 是您的主要购物入口点时，使用 `search.do`。

当您希望 Atlas 首先返回可用报价时，该流程最佳。

#### 获取报价流程

当您已知道目标行程时，使用 `getOffers.do`。

该流程更适合直接价格检查、独立验证和外部购物路径。

#### 实际区别

标准搜索流程通常通过 `verify.do` 继续。

获取报价流程围绕返回的 `OfferId` 设计，用于下游订单创建。

### 在以下情况下使用此部分

* 无需标准搜索的报价查询流程
* 订单创建前的辅助价格检查
* 出票前的最低价格验证
* 由您自己的航班数据源驱动的流程

### 常见场景

#### 使用自己的航班数据源

当航班选择发生在标准 Atlas 搜索流程外部时，使用 `getOffers.do`。

这让您直接获取最新可预订运价和 `OfferId`。

#### 在订单创建前运行最终价格检查

使用 `getOffers.do` 在创建订单前重新检查最新可预订价格。

这有助于减少报价和预订之间的运价漂移。

#### 出票前比较渠道

当您需要在将订单发送到出票前进行实时验证时，使用 `getOffers.do`。

当您为完成前的最新可用价格进行优化时，这很有用。

### 推荐的业务链

#### 最小链

当您只需要运价检索和出票时使用此路径：

1. 调用 `getOffers.do`
2. 保留返回的 `OfferId`
3. 调用 `order.do`
4. 调用 `pay.do`

#### 带座位和行李的链

当行李和座位追加销售是预订流程的一部分时使用此路径：

1. 调用 `getOffers.do`
2. 确认运价和目标航班
3. 如果需要，查询 `getLuggage.do` 或 `seatAvailability.do`
4. 使用 `order.do` 创建订单
5. 使用 `pay.do` 完成支付

#### 何时停止并重新检查

如果以下任何内容发生变化，停止并刷新报价：

* 目标航班
* 旅客组合
* 预期运价
* 改变预订计划的附加服务要求

### 最佳实践

当预订关键输入发生变化或预订延迟时，刷新报价。

不要基于过时的报价假设构建订单。

### 典型流程

{% stepper %}
{% step %}

### 获取报价

使用目标行程调用 `getOffers.do`。

保留返回的 `OfferId`。
{% endstep %}

{% step %}

### 座位和行李

查询 `getLuggage.do` 或 `seatAvailability.do`。

在报价匹配您的目标航班和价格后运行此步骤。

对于座位查询，传递返回的 `OfferId`。
{% endstep %}

{% step %}

### 创建订单

使用返回的 `OfferId` 和所需预订数据调用 `order.do`。
{% endstep %}

{% step %}

### 支付和出票

调用 `pay.do` 完成出票。
{% endstep %}
{% endstepper %}

### 何时使用附加服务查询

#### 使用 `getLuggage.do`

用于在预订前显示行李价格和行李选项。

在确认目标报价后运行。

#### 使用 `seatAvailability.do`

用于在预订前显示座位可用性和付费座位选择。

在此流程中使用返回的 `OfferId` 作为请求上下文。

不要仅使用航班数据调用它。

#### 将附加服务视为推荐

当您的预订产品支持座位和行李追加销售时，包括附加服务查询。

最短技术路径仍然是 `getOffers.do` → `order.do` → `pay.do`。

### 实施指导

#### 最佳适配

此流程适合已经控制搜索逻辑的合作伙伴。

它也适用于在预订前需要进行最终 Atlas 侧价格检查的流程。

#### 保留的数据

保留用于 `getOffers.do` 的准确行程上下文。

保留返回的 `OfferId` 直到订单创建完成。

#### 建议验证

在 `order.do` 之前确认：

* 航班与预期行程匹配
* 运价与预期销售逻辑匹配
* 旅客组合仍然正确
* 附加服务选择在需要时已完成

### 操作说明

#### 真实来源

使用 OpenAPI 架构作为请求字段和响应字段的真实来源。

#### 命名

在实现材料、支持回复和面向客户的指导中使用 `getOffers.do`。

#### 错误处理

如果订单或支付步骤因运价或可用性变化而失败，从新鲜的报价查询重新开始。

使用最新返回的数据，而不是使用过时的假设重试。

### 常见问题

#### `getOffers.do` 是否替代 `search.do`？

不是。

当 Atlas 是主要购物入口点时，使用 `search.do`。

当您已知道目标行程或需要独立价格检查时，使用 `getOffers.do`。

#### 在此流程中是否仍需要 `verify.do`？

在此页面描述的标准获取报价路径中不需要。

该流程以 `OfferId` 和下游订单创建为中心。

#### 附加服务查询是强制性的吗？

当您的产品包括附加销售时，强烈建议进行座位和行李查询。

在 `order.do` 前使用 `getLuggage.do` 或 `seatAvailability.do` 以提高转化率和旅客清晰度。

#### 何时应刷新报价？

当任何预订关键输入发生变化时，刷新报价。

典型触发因素：

* 旅客数量变化
* 目标航班变化
* 预期运价变化
* 预订延迟且当前定价可能过时

#### 可以使用获取报价与我自己的搜索引擎吗？

可以。

这是此流程的主要用例之一。

保持您的行程映射与 OpenAPI 中定义的请求字段一致。

### 失败处理

#### 如果 `getOffers.do` 失败

首先检查请求完整性。

然后确认行程数据、旅客数据以及 OpenAPI 中定义的任何必填字段。

如果问题是临时的，使用受控退避重试。

#### 如果在获取报价后 `order.do` 失败

不要假设返回的报价仍然有效。

如果失败指向运价、库存或预订状态漂移，再次调用 `getOffers.do` 并从新鲜数据重建订单请求。

#### 如果 `pay.do` 失败

检查订单是否已支付或仍在处理中。

不要盲目发送重复支付。

在重试前，必要时查询订单状态。

#### 何时不立即重试

当问题可能由以下原因引起时，避免即时重试：

* 过时的运价数据
* 不支持的支付方式
* 无效的旅客或联系数据
* 航司侧限制

首先修复根本原因。

### 日志记录和支持指导

#### 在日志中保留这些值

捕获故障排除所需的最小字段：

* 请求时间戳
* 行程摘要
* 旅客组合
* `OfferId`
* 订单创建后的 `orderNo`
* 支付方式类型
* 最终响应状态和消息

#### 保持请求链路清晰

将获取报价请求和下游订单请求记录为一个业务链。

这使得运价漂移和状态不匹配更容易追踪。

#### 升级准备

升级时提供：

* API 名称
* 请求时间
* 关键标识符，如 `OfferId` 或 `orderNo`
* 响应代码
* 响应消息

这可以加速支持审核。

### 说明

* 此流程不从标准 `search.do` 路径开始。
* 使用当前 API 参考作为必填字段的真实来源。
* 使用 OpenAPI 命名作为接口名称的真实来源。
* 在实现材料中使用 `getOffers.do` 作为官方接口名称。

### 相关页面

* [搜索](/api-wen-dang/product-guides/booking/booking-step-guides/search.md)
* [获取报价价格](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)
* [获取报价 vs 获取报价价格](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/get-offer-vs-get-offer-price.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)
* [行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)

### 完整 API 参考

在此查看端点级详情：

* [获取报价](/api-wen-dang/api-reference/booking-apis/get-offer.md)
* [座位](/api-wen-dang/api-reference/booking-apis/inflow-seat-and-baggage.md)
* [行李](/api-wen-dang/api-reference/booking-apis/baggage.md)
* [创建订单](/api-wen-dang/api-reference/booking-apis/create-order.md)
* [支付与出票](/api-wen-dang/api-reference/booking-apis/payment-and-ticketing.md)
