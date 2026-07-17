# 集成前

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

在启动、解决方案评审或集成规划前使用此页面。

它涵盖了团队在开发开始前通常需要解答的问题。

{% hint style="info" %}
需要适合会议使用的版本？

请使用[启动检查清单](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/kickoff-checklist.md)。
{% endhint %}

当您需要以下内容时，从这里开始：

* 选择合适的预订和定价流程
* 确认支付、出票和退款设计
* 定义在 UAT 和上线前必须准备就绪的内容

### 启动前应决定什么？

首先确定以下要点：

* 将使用的搜索流程
* 预订前何时刷新价格
* 将支持的支付模式
* 如何跟踪出票完成情况
* 行李和座位选择是否需要在购买前完成
* 谁负责退款和改签跟进
* Webhook 是辅助性的还是设计中的核心

如果这些要点未确定，启动通常会变得缓慢且重复。

### 快速对齐检查清单

在第一次解决方案评审中使用此检查清单：

* Atlas 是主要的搜索来源，还是仅作为最终定价来源
* 选择 `search.do` 或 `getOffers.do` 作为核心流程
* 在 `order.do` 之前定义价格刷新点
* 支付模式由航司和商业模式决定
* 在 `pay.do` 之后实施订单轮询
* Webhook 不被视为唯一的真相来源
* 预订后变更通过 ATRIP 服务请求处理
* UAT 负责人和证据格式已达成一致

### 常见问题

#### 在 Atlas API 启动前应决定什么？

首先决定搜索流程、价格刷新点、支付模式、出票确认路径、附加服务范围和预订后归属。

如果这些要点未确定，实施和启动都会变慢。

### 定价完整性

航班预订的主要风险是价格过时或可用性过时。

使用以下规则：

* 在标准流程中，在 `order.do` 之前使用 `verify.do`
* 当您需要独立的实时价格检查时，使用 `getOffers.do`
* 将最新的验证或报价结果视为当前的真相来源
* 避免在定价和预订之间长时间延迟

不要将搜索结果视为最终的预订承诺。

### 如何获取沙箱凭证？

在 ATRIP 中的 `Profile` → `My Profile` → `Company Information` 下生成。

使用：

* `x-atlas-client-id`
* `x-atlas-client-secret`

在每个沙箱请求中使用它们。

请参阅[沙箱访问](/api-wen-dang/readme-1/making-requests.md)。

### 是否有用于首次测试的 Postman 集合？

有的。

使用[快速入门](/api-wen-dang/readme-1/quick-start.md)中的集合进行首次端到端测试。

在准备好进行正式验证时，稍后使用 UAT 指南。

### 应使用哪种预订流程？

当 Atlas 是您的主要搜索入口时，使用 `search.do`。

当您已经知道行程或需要独立的价格检查时，使用 `getOffers.do`。

在标准搜索流程中，在 `order.do` 之前使用 `verify.do`。

请参阅：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)

#### 如何在预订前保护定价完整性？

不要将搜索结果视为最终的预订承诺。

在接近预订时间时使用 `verify.do` 或 `getOffers.do` 刷新价格，然后立即创建订单，避免不必要的延迟。

### 为什么搜索和验证可能返回不同的价格？

搜索可能使用缓存数据。

验证在订单创建前检查实时票价和可用性。

如果价格发生变化，使用最新的验证结果。

### 最安全的定价模式是什么？

在定价完整性最重要时使用此模式：

1. 搜索或获取目标报价
2. 在接近预订时间时刷新价格
3. 立即创建订单
4. 立即支付，避免不必要的延迟

这减少了由缓存时效、库存变动或航司更新引起的不匹配。

### 步骤之间可以等待多长时间？

当前指南是：

* 搜索 → 验证：最长 2 小时
* 验证 → 订单：最长 30 分钟

时间越短越安全。

### 预订状态和出票

出票并不总是即时的。

为异步流程设计：

* 支付可以在最终出票详情出现之前成功
* 航司 PNR 可以在订单创建后出现
* 票号仅在出票完成后返回
* 需要轮询以进行最终确认

围绕 `queryOrderDetails.do` 构建您的状态处理。

### Atlas 是否支持票价家族？

是的。

当您需要票价家族结果时，在搜索中启用 `includeMultipleFareFamily`。

支持仍取决于航司和库存。

### 可以在搜索期间过滤行李吗？

不可以。

先选择行程。

然后在预订前查询行李和座位选项，以增强转化率和乘客清晰度。

请参阅[行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)。

### 附加服务和票价内容

尽早确认您的产品是否需要：

* 票价家族展示
* 预订前的行李追加销售
* 预订前的座位图
* 出票后的行李或座位销售

将行李和座位查询视为预订流程中推荐的商业功能。

### 支持哪些支付方式？

主要选项是：

* **Deposit（存款）**
* **VCC pass-through（VCC 直通）**

支持仍取决于航司和出票渠道。

请参阅[支付](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-payments.md)。

### 如何在存款和 VCC 之间做选择？

当您想要更简单的支付路径和 Atlas 余额结算时，使用 **Deposit（存款）**。

当您的业务需要直接向航司扣款时，使用 **VCC pass-through（VCC 直通）**。

在构建最终支付路径前，仍需按航司和订单确认支持情况。

#### 我们的系统应存储哪些值以供后续跟进？

存储 `routingIdentifier`、`sessionId` 或 `OfferId`、`orderNo`、`pnrCode`、可用的航司 PNR，以及所使用的支付方式。

这些值使出票、退款和支持跟进更加容易。

### Atlas 是否发行 VCC 卡？

不发行。

Atlas 仅支持 VCC 直通。

您在 `pay.do` 中提供卡详情。

### 支付后需要轮询吗？

需要。

支付和出票不总是同时发生。

使用 `queryOrderDetails.do` 直到出票达到最终状态。

Webhook 有帮助，但不应该是您唯一的确认路径。

请参阅[查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)。

### 我们的系统应存储哪些值以供后续跟进？

在您的预订链中保留这些值：

* `routingIdentifier`
* `sessionId` 或 `OfferId`
* `orderNo`
* `pnrCode`
* 可用的航司 PNR
* 使用的支付方式

### `pnrCode` 是航司 PNR 吗？

不是。

`pnrCode` 是 Atlas 预订参考号。

航司 PNR 在出票后出现，可以从订单查询中读取。

### 支付和退款模式

在上线前对齐退款预期。

退款路径取决于支付模式：

* VCC 退款通常返回到原始卡
* Deposit 退款在 Atlas 收到航司资金后记入余额

不要将一种退款路径描述为通用的。

### 退款资金到哪里去了？

对于 **VCC**，退款资金通常返回到原始卡。

对于 **Deposit**，Atlas 在收到航司资金后记入您的余额。

请参阅[预订后](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-post-ticketing.md)。

### 预订变更是否通过 API 处理？

不是作为通用的自助服务流程。

对于姓名更正、航班变更和类似请求，请使用 ATRIP 中的服务请求。

### 预订后归属

确认上线后谁负责以下任务：

* 退款发起
* 退款跟进
* 航班时刻变更监控
* 出发当天的紧急处理
* 手动变更请求

如果归属不明确，运营问题通常会在首批实时订单后出现。

### Webhook 是保证送达的吗？

不是。

Webhook 送达是尽力而为的。

使用航司邮件、事件流程和订单查询进行最终对账。

请参阅[Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)。

#### 何时应开始 UAT 并为上线做准备？

仅在沙箱流程端到端稳定后开始 UAT。

仅在 UAT 批准、生产凭证、IP 白名单和首批订单监控准备就绪后，才能进入上线。

### 何时应开始 UAT？

仅在沙箱流程端到端稳定后开始 UAT。

准备：

* 所需的用例订单详情
* 每个场景的证据
* 需要时的 webhook 证据
* 相关的订单号或请求 ID

请参阅[UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)。

### 上线前应确认什么？

确认所有以下内容：

* 沙箱流程稳定
* UAT 已批准
* 生产凭证已生成
* 生产 IP 白名单已就绪
* 端点已正确切换
* 首批实时订单可以监控

请参阅[生产上线](/api-wen-dang/readme-1/production-go-live.md)。

### 相关页面

* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [启动检查清单](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/kickoff-checklist.md)
* [常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [预订后概述](/api-wen-dang/product-guides/post-booking.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
