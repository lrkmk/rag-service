# Atlas API 文档更新

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此页面追踪 Atlas API 文档的最新更新，并更快地跳转到合适的指南。

当您需要最新的指南、修订后的故障排除内容或新增的入口点时，请将此页面作为**支持与参考**的更新动态。

{% hint style="success" %}
最新更新：Atlas VOID 覆盖范围现已涵盖四个地区的 23 家航司，新增支持 `TS`、`Y4`、`EI` 和 `VF`。
{% endhint %}

此页面突出显示新指南、主要的故障排除改进以及按使用场景推荐的后续阅读页面。

如果您需要以下内容，请从此处开始：

* 查找最新的 Atlas API 指南
* 查看沙箱、预订、支付或故障排除方面的变更
* 选择下一步要阅读的合适页面

### 常见问题

#### Atlas API 文档最近有什么变化？

最近的更新增加了预订流程标识符指南，明确了何时使用 `search.do` 与 `getOffers.do`，解释了 `429` 与 `110` 的区别，增加了 `202` vs `301` vs `308` 的决策指南，明确了 Verify 与 Create Order 的边界，增加了 `pay.do` 后的轮询指南，明确了 `401`、`402`、`404`、`406` 和 `615` 的支付状态恢复，记录了辅助服务 `productCode` 的时效性，增加了 Search vs Verify vs Get Offer 的重启指南，明确了预订输入错误 `307`、`327` 和 `410`，明确了辅助服务映射错误 `309` 和 `409`，记录了座位回退模式，明确了瞬态验证和订单失败 `205`、`299` 和 `304`，记录了 `318` 和 `608` 的重复预订处理，增加了选定预订前 API 的请求限制指南，发布了多渠道通知设置，更新了 ATRIP UAT 流程，优化了作废指南，并明确了座位可用性调用规则。

当您需要页面级别的详细信息时，请使用下面的变更日志。

#### 新集成团队应该从哪里开始？

从[快速入门](/api-wen-dang/readme-1/quick-start.md)开始。

然后使用[集成指南](/api-wen-dang/readme-1.md)、[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)和[错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)。

#### 我应该查看哪些页面了解请求限制指南？

从[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)、[搜索](/api-wen-dang/product-guides/booking/booking-step-guides/search.md)、[搜索与预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-search-and-book.md)和[错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)开始。

### 热门起点

#### 新集成

从[快速入门](/api-wen-dang/readme-1/quick-start.md)和[集成指南](/api-wen-dang/readme-1.md)开始。

#### 预订流程

从[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)和[搜索与预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-search-and-book.md)开始。

当您需要下一步的正确令牌时，请使用[标识符](/api-wen-dang/product-guides/booking/booking-overview/identifiers.md)。

当预订边界是主要问题时，请使用[验证 vs 创建订单](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/verify-vs-order.md)。

当主要问题是从何处重新开始时，请使用[从搜索 vs 验证 vs 获取报价重启](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/restart-point.md)。

当付费座位失败行为必须在预订前定义时，请使用[座位回退模式](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage/seat-fallback-modes.md)。

#### 故障排除

从[错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)和[常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)开始。

当请求频率或搜索并发是主要问题时，请使用[429 vs 110](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/429-vs-110.md)。

当您需要知道哪个更早的步骤必须被刷新时，请使用[202 vs 301 vs 308](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/202-vs-301-vs-308.md)。

当主要风险是重复或不必要的支付重试时，请使用[402 vs 404 vs 406 vs 615](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/402-vs-404-vs-406-vs-615.md)。

当订单输入或辅助服务映射是主要故障区域时，请使用[307 vs 327 vs 410](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/307-vs-327-vs-410.md)和[309 vs 409](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/309-vs-409.md)。

当主要问题是订单是否已过期或已支付时，请使用[401 vs 402 vs 404](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/401-vs-402-vs-404.md)。

### 最新的 Atlas API 文档更新

#### VOID 航司覆盖范围扩展

更新了 VOID 文档以显示当前支持的航司范围。

变更内容：

* 记录了覆盖美洲、欧洲、日本和韩国的 23 家支持 VOID 的航司
* 标记 `ZG` 仅支持美国航线
* 新增最新支持的航司：`TS`、`Y4`、`EI` 和 `VF`

后续阅读：

* [作废工作流](/api-wen-dang/product-guides/post-booking/void.md)
* [作废](/api-wen-dang/api-reference/post-booking-apis/void.md)
* [退款、查询与预订后错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/refund-query-and-post-booking-errors.md)

#### Fulfillment API 和 `getOfferPrice.do` 发布

发布了 `getOfferPrice.do` 流程的新履约指南，并更新了关键预订页面，包含其时间限制和请求限制规则。

变更内容：

* 新增[Fulfillment API](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)，用于新的面向履约的预订路径
* 新增[Get Offer vs Fulfillment API](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/get-offer-vs-get-offer-price.md)，明确何时使用 `getOffers.do` 与 `getOfferPrice.do`
* 在 API 参考下新增[获取报价价格](/api-wen-dang/api-reference/booking-apis/get-offer-price.md)
* 更新了[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)、[支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)、[查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)、[创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)、[订单与出票](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-order.md)和[API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)

后续阅读：

* [Fulfillment API](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)

#### 支付超时、瞬态失败和重复预订说明包

发布了三个新页面，用于支付截止恢复、瞬态预订阶段失败和重复预订处理。

变更内容：

* 新增[401 vs 402 vs 404](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/401-vs-402-vs-404.md)，区分已过期的支付窗口与不可支付或已支付的订单状态
* 新增[205 vs 299 vs 304](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/205-vs-299-vs-304.md)，明确何时应重试一次、从搜索重新开始或升级瞬态验证和订单失败
* 新增[318 vs 608 重复预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/318-vs-608-duplicate-booking.md)，明确在重试前如何确认现有预订状态

后续阅读：

* [支付错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/payment-errors.md)
* [验证、订单与出票错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/verify-order-and-ticketing-errors.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)

#### 输入验证和座位回退说明包

发布了三个新页面，用于订单输入故障排除、辅助服务映射和座位失败行为。

变更内容：

* 新增[307 vs 327 vs 410](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/307-vs-327-vs-410.md)，区分通用订单字段问题、预订要求不匹配和联系电话格式错误
* 新增[309 vs 409](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/309-vs-409.md)，区分过期的辅助服务代码与行李航段映射错误
* 新增[座位回退模式](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage/seat-fallback-modes.md)，解释 `STOP_TICKET`、`STOP_SEAT` 和 `SIMILAR_SEAT`

后续阅读：

* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)

#### 支付状态和辅助服务时效性说明包

发布了三个新页面，用于支付恢复、辅助服务复用安全性和流程重启决策。

变更内容：

* 新增[402 vs 404 vs 406 vs 615](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/402-vs-404-vs-406-vs-615.md)，明确何时应查询订单、等待或避免再次调用 `pay.do`
* 新增[行李与座位产品代码时效性](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage-and-seat-productcode-freshness.md)，解释辅助服务选择何时过期
* 新增[从搜索 vs 验证 vs 获取报价重启](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/restart-point.md)，解释必须重新运行的最早预订步骤

后续阅读：

* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)

#### 预订恢复和时机说明包

发布了三个新页面，用于预订阶段恢复决策和支付后跟进。

变更内容：

* 新增[202 vs 301 vs 308](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/202-vs-301-vs-308.md)，解释何时应刷新搜索、刷新验证或重建预订上下文
* 新增[验证 vs 创建订单](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/verify-vs-order.md)，明确预订创建前的验证边界
* 新增[轮询与出票时机](/api-wen-dang/product-guides/booking/booking-step-guides/query-order/post-payment-polling.md)，解释为什么支付成功并不总是意味着最终出票

后续阅读：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)

#### 预订流程说明包

发布了三个新页面，针对流程选择、标识符处理和请求压力故障排除等常见集成问题。

变更内容：

* 新增[标识符](/api-wen-dang/product-guides/booking/booking-overview/identifiers.md)，涵盖 `routingIdentifier`、`sessionId`、`OfferId`、`orderNo` 和新鲜标识符规则
* 新增[搜索 vs 获取报价](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/search-vs-offer.md)，明确何时使用 `search.do` 与 `getOffers.do`
* 新增[429 vs 110](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/429-vs-110.md)，区分请求限制治理与搜索并发压力

后续阅读：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [搜索与预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-search-and-book.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)

#### QPS 和 QPM 请求限制治理

发布了选定预订前 API 的新请求限制指南。

变更内容：

* 记录了 Atlas 错误码 `429` 在超限请求时的行为
* 新增 `verify.do` 和 `getOffers.do` 的共享池规则，以及 `seatAvailability.do` 和 `getLuggage.do` 的共享池规则
* 新增 `retryAfter`、请求节奏和减少重复搜索的重试指南

后续阅读：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [搜索与预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-search-and-book.md)

#### 多渠道通知发布

发布了新的 Atlas 通知设置指南，支持通过 Webhook、邮件、钉钉、企业微信、Slack 和 Teams 进行 ATRIP 投递。

变更内容：

* 新增多渠道通知的 ATRIP 设置指南
* 明确 Webhook 是通知模型中的一种投递选项
* 将航司状态更新链接到首个多渠道应用场景

后续阅读：

* [多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [航司状态更新通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/airline-status-update-notification.md)

#### 标准请求头清理

更新了沙箱访问指南，移除了一个不必要的标准请求头。

变更内容：

* 从标准请求头列表中移除了 `Accept: application/json`
* 保留了 `Accept-Encoding`、`Authorization` 和 `Content-Type` 的指南不变

后续阅读：

* [沙箱访问](/api-wen-dang/readme-1/making-requests.md)
* [快速入门](/api-wen-dang/readme-1/quick-start.md)

#### UAT 测试流程更新

更新了 UAT 文档以反映当前的 ATRIP 验证流程。

变更内容：

* UAT 现在从 **UAT 测试** 开始
* 合作伙伴必须选择目标功能范围后才能继续
* **航班预订** 是必需的核心功能
* **提交验证** 现在触发自动验证并直接返回失败原因

后续阅读：

* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)
* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [入门指南](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-general-information.md)

#### 作废工作流和通知更新

更新了作废文档以反映当前的预订后流程和 webhook 处理。

变更内容：

* 明确了标准流程：`voidQuotation.do` → `void.do` → `queryVoidOrders.do`
* 增加了对 `voidOfferId`、`voidCode` 和作废窗口检查的更强指南
* 扩展了 `order.void` webhook 覆盖范围、状态值和重试失败行为

后续阅读：

* [作废工作流](/api-wen-dang/product-guides/post-booking/void.md)
* [作废](/api-wen-dang/api-reference/post-booking-apis/void.md)
* [作废通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/void-notification.md)

#### SeatAvailability 调用规则更新

更新了座位选择指南以反映当前的 `seatAvailability.do` 调用规则。

变更内容：

* 独立模式不再可用
* `seatAvailability.do` 现在需要来自 `verify.do` 的 `sessionId` 或来自 `getOffers.do` 的 `OfferId`
* 仅查询航班座位报价的请求不受支持

后续阅读：

* [流入座位与行李](/api-wen-dang/api-reference/booking-apis/inflow-seat-and-baggage.md)
* [座位与行李](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)

#### MCP 辅助开发

当您希望在 Atlas API 集成过程中使用 GitBook MCP 时，请阅读 [MCP 辅助开发](/api-wen-dang/readme-1/integration-tools/mcp-assisted-development.md)。

适用于：

* 开始沙箱构建的团队
* 绘制预订流程的开发人员
* 希望更快找到实现问题答案的团队

后续阅读：

* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [API 参考](/api-wen-dang/api-reference.md)

#### 沙箱验证测试工具包

当您在开发前或环境变更后需要进行无代码沙箱验证运行时，请阅读[沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)。

适用于：

* 在编码前验证沙箱凭证
* 确认网络访问和核心预订流程就绪
* 在凭证或 IP 变更后重新检查沙箱健康状态的团队

后续阅读：

* [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)
* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)

#### 错误码改进

[错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md) 现在作为主要的故障排除入口点效果更好。

适用于：

* 处理高频集成失败的团队
* 定义安全重试行为的开发人员
* 检查可能根本原因的运维团队

后续阅读：

* [通用与访问错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/common-and-access-errors.md)
* [验证、订单与出票错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/verify-order-and-ticketing-errors.md)

### 按使用场景开始

#### 新的 Atlas API 集成

从以下内容开始：

* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [MCP 辅助开发](/api-wen-dang/readme-1/integration-tools/mcp-assisted-development.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)

#### 沙箱验证

从以下内容开始：

* [沙箱访问](/api-wen-dang/readme-1/making-requests.md)
* [沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)
* [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)

#### 预订和支付流程

从以下内容开始：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [混合支付指南](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing/hybrid-payment-guide.md)

#### 故障排除与支持

从以下内容开始：

* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)

### 常见问题

#### Atlas API 文档最近有什么变化？

最近的更新新增了[标识符](/api-wen-dang/product-guides/booking/booking-overview/identifiers.md)、[搜索 vs 获取报价](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/search-vs-offer.md)、[429 vs 110](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/429-vs-110.md)、[202 vs 301 vs 308](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/202-vs-301-vs-308.md)、[验证 vs 创建订单](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/verify-vs-order.md)、[轮询与出票时机](/api-wen-dang/product-guides/booking/booking-step-guides/query-order/post-payment-polling.md)、[402 vs 404 vs 406 vs 615](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/402-vs-404-vs-406-vs-615.md)、[行李与座位产品代码时效性](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage-and-seat-productcode-freshness.md)、[从搜索 vs 验证 vs 获取报价重启](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/restart-point.md)、[307 vs 327 vs 410](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/307-vs-327-vs-410.md)、[309 vs 409](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/309-vs-409.md)、[座位回退模式](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage/seat-fallback-modes.md)、[401 vs 402 vs 404](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/401-vs-402-vs-404.md)、[205 vs 299 vs 304](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/205-vs-299-vs-304.md)和[318 vs 608 重复预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/318-vs-608-duplicate-booking.md)，为选定的预订前 API 增加了 QPS 和 QPM 请求限制指南，新增了[多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)用于 ATRIP 通知设置，将新的 ATRIP **UAT 测试**流程添加到[UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)，明确了**航班预订**是必需的，增加了自动验证指南，扩展了[作废工作流](/api-wen-dang/product-guides/post-booking/void.md)，更改了 `seatAvailability.do` 的调用规则，新增了[MCP 辅助开发](/api-wen-dang/readme-1/integration-tools/mcp-assisted-development.md)，发布了[沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)，并改进了[错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)作为故障排除入口点。

#### 沙箱集成应该先阅读哪个指南？

从[快速入门](/api-wen-dang/readme-1/quick-start.md)开始。然后使用[沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)在编码前确认就绪状态。

#### 预订、支付或故障排除应该从哪里开始？

使用[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)了解主要流程，使用[支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)了解支付和轮询，使用[错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)了解失败处理。

### 完整变更日志

{% updates format="full" %}
{% update date="2026-07-08" %}

## 扩展 VOID 航司覆盖范围

更新了 VOID 文档以反映当前支持的航司范围。

变更内容：

* 记录了覆盖四个地区的 23 家支持 VOID 的航司
* 将 `TS`、`Y4`、`EI` 和 `VF` 添加到支持的覆盖列表
* 明确了 `ZG` 支持仅限于美国航线

更新的页面：

* [作废工作流](/api-wen-dang/product-guides/post-booking/void.md)
* [作废](/api-wen-dang/api-reference/post-booking-apis/void.md)
* [Atlas API 文档更新](/api-wen-dang/readme.md)
  {% endupdate %}

{% update date="2026-07-06" %}

## 新增 Fulfillment API 和 `getOfferPrice.do`

发布了 `getOfferPrice.do` 的新履约预订路径，并更新了关键工作流页面，包含履约特定的时间限制和请求限制指南。

变更内容：

* 新增[Fulfillment API](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)，用于履约定位、5 分钟时间限制、重试规则和恢复指南
* 新增[Get Offer vs Fulfillment API](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/get-offer-vs-get-offer-price.md)，区分标准 Get Offer 与履约路径
* 在 API 参考下新增[获取报价价格](/api-wen-dang/api-reference/booking-apis/get-offer-price.md)
* 更新[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)，新增履约分支
* 更新[获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)，区分 `getOffers.do` 和 `getOfferPrice.do`
* 更新[创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)、[支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)和[查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)，用于 5 分钟履约处理
* 更新[订单与出票](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-order.md)，将标准的 30 分钟保留与履约流程分开
* 更新[API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)，记录独立的 `getOfferPrice.do` QPM 策略
  {% endupdate %}

{% update date="2026-07-05" %}

## 新增标识符、流程选择和限流指南

发布了十五个新的支持页面，用于常见的预订流程集成问题。

变更内容：

* 新增[标识符](/api-wen-dang/product-guides/booking/booking-overview/identifiers.md)，涵盖 `routingIdentifier`、`sessionId`、`OfferId`、`orderNo` 和刷新规则
* 新增[搜索 vs 获取报价](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/search-vs-offer.md)，明确何时使用 `search.do` 以及何时使用 `getOffers.do`
* 新增[429 vs 110](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/429-vs-110.md)，解释请求限制治理与搜索并发压力
* 新增[202 vs 301 vs 308](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/202-vs-301-vs-308.md)，解释哪个更早的步骤必须被刷新
* 新增[验证 vs 创建订单](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/verify-vs-order.md)，明确订单创建前的验证边界
* 新增[轮询与出票时机](/api-wen-dang/product-guides/booking/booking-step-guides/query-order/post-payment-polling.md)，解释支付后跟进和安全轮询行为
* 新增[402 vs 404 vs 406 vs 615](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/402-vs-404-vs-406-vs-615.md)，明确支付状态恢复和重复支付风险
* 新增[行李与座位产品代码时效性](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage-and-seat-productcode-freshness.md)，解释辅助服务选择何时过期
* 新增[从搜索 vs 验证 vs 获取报价重启](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/restart-point.md)，解释在过期上下文或价格漂移后必须重新运行哪个预订步骤
* 新增[307 vs 327 vs 410](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/307-vs-327-vs-410.md)，明确创建订单时的乘客、证件和联系信息输入错误
* 新增[309 vs 409](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/309-vs-409.md)，明确过期的辅助服务代码与行李航段映射错误
* 新增[座位回退模式](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage/seat-fallback-modes.md)，解释 `STOP_TICKET`、`STOP_SEAT` 和 `SIMILAR_SEAT`
* 新增[401 vs 402 vs 404](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/401-vs-402-vs-404.md)，明确支付截止过期与不可支付或已支付的订单
* 新增[205 vs 299 vs 304](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/205-vs-299-vs-304.md)，明确瞬态验证和订单失败
* 新增[318 vs 608 重复预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/318-vs-608-duplicate-booking.md)，明确另一次重试前的重复预订处理

更新的页面：

* [Atlas API 文档更新](/api-wen-dang/readme.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
  {% endupdate %}

{% update date="2026-07-03" %}

## 新增 QPS 和 QPM 请求限制指南

更新了预订、故障排除和常见问题页面，记录选定预订前 API 的请求限制治理。

变更内容：

* 新增 Atlas 错误码 `429` 指南，附带 `retryAfter`
* 记录了搜索、履约和辅助服务资源池的默认限制
* 明确了 `verify.do` 和 `getOffers.do` 共享一个履约池
* 明确了 `seatAvailability.do` 和 `getLuggage.do` 共享一个辅助服务池
* 确认 `order.do` 和 `pay.do` 不在本次请求限制策略范围内

更新的页面：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [搜索](/api-wen-dang/product-guides/booking/booking-step-guides/search.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)
* [行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)
* [错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)
* [搜索错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/search-errors.md)
* [验证、订单与出票错误](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing/verify-order-and-ticketing-errors.md)
* [搜索与预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-search-and-book.md)
  {% endupdate %}

{% update date="2026-06-30" %}

## 新增多渠道通知设置指南

发布了[多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)，支持通过 Webhook、邮件、钉钉、企业微信、Slack 和 Teams 进行 ATRIP 投递。

变更内容：

* 新增渠道选择、ATRIP 设置和测试通知的指南
* 在 [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)中明确 Webhook 是更广泛通知模型中的一种投递选项
* 更新[航司状态更新通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/airline-status-update-notification.md)，将航司状态定位为首个多渠道应用场景

更新的页面：

* [多渠道通知](/api-wen-dang/product-guides/extensions-and-integrations/multi-channel-notifications.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
* [航司状态更新通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/airline-status-update-notification.md)
  {% endupdate %}

{% update date="2026-06-29" %}

## 从标准请求头中移除了 `Accept: application/json`

更新了沙箱访问指南，使标准请求头与当前使用保持一致。

变更内容：

* 从标准请求头列表中移除了 `Accept: application/json`
* 其余标准请求头指南保持不变

更新的页面：

* [沙箱访问](/api-wen-dang/readme-1/making-requests.md)
  {% endupdate %}

{% update date="2026-06-29" %}

## 更新 UAT 验证以适应 ATRIP UAT 测试

更新了 UAT 指南以反映最新的 ATRIP 流程。

变更内容：

* UAT 现在从 **UAT 测试** 开始
* 合作伙伴选择目标功能范围后才能继续
* **航班预订** 现被记录为必需的核心功能
* **确认并继续** 和 **提交验证** 现已成为文档流程的一部分
* 失败案例现在直接指向 ATRIP 失败原因

更新的页面：

* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)
* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [入门指南](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-general-information.md)
  {% endupdate %}

{% update date="2026-06-10" %}

## 扩展作废工作流和 webhook 指南

更新了作废文档以反映当前的预订后流程。

变更内容：

* 明确了标准的 `voidQuotation.do` → `void.do` → `queryVoidOrders.do` 顺序
* 新增 `voidOfferId`、`voidCode` 和严格作废窗口处理的指南
* 扩展了 `order.void` webhook 触发规则、状态值和重试失败行为

更新的页面：

* [作废工作流](/api-wen-dang/product-guides/post-booking/void.md)
* [作废](/api-wen-dang/api-reference/post-booking-apis/void.md)
* [作废通知](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview/void-notification.md)
  {% endupdate %}

{% update date="2026-06-09" %}

## 更新 SeatAvailability 调用规则

更新了座位选择文档以反映最新的 `seatAvailability.do` 要求。

变更内容：

* 独立模式不再可用
* 使用 `verify.do` 的 `sessionId` 或 `getOffers.do` 的 `OfferId`
* 仅查询航班座位报价的请求不受支持

更新的页面：

* [流入座位与行李](/api-wen-dang/api-reference/booking-apis/inflow-seat-and-baggage.md)
* [座位与行李](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [搜索与预订](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-search-and-book.md)
  {% endupdate %}

{% update date="2026-04-15" %}

## 新增 MCP 辅助开发

发布了[MCP 辅助开发](/api-wen-dang/readme-1/integration-tools/mcp-assisted-development.md)，面向在 Atlas API 集成过程中使用 GitBook MCP 的团队。

当您需要以下内容时使用它：

* 在编码前找到正确的工作流
* 了解下一步需要使用哪个标识符或 API
* 从开发问题跳转到正确的参考或故障排除页面

该指南还包含了生产安全开发的提示模式和用法边界。
{% endupdate %}

{% update date="2026-04-09" %}

## 新增沙箱验证测试工具包

发布了[沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)，用于无代码沙箱验证运行。

当您需要以下内容时使用它：

* 在开发前确认凭证和网络访问
* 使用 Newman 运行核心沙箱成功路径
* 一次性验证 `搜索`、`验证`、`下单` 和 `支付`
* 在环境变更后快速检查沙箱就绪状态

该页面还解释了出票轮询期间预期的最终检索超时。
{% endupdate %}

{% update date="2026-04-08" %}

## 改进错误码落地页面

更新了[错误码](/api-wen-dang/support-and-reference/troubleshooting-and-support/errors-handing.md)，新增：

* 重试策略指南
* 高频错误码快速决策表
* 重试时应避免的高风险错误
* 基于模式的常见集成问题检查

这使该页面作为主要的故障排除入口点更加有用。
{% endupdate %}

{% update date="2026-04-03" %}

## 新增混合支付指南

在**支付与出票**下发布了[混合支付指南](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing/hybrid-payment-guide.md)。

当您需要以下内容时使用它：

* 从 VCC 直通切换为押金
* 决定是复用还是重新生成订单
* 处理 ATRIP 和 API 流程中的混合支付回退
  {% endupdate %}
  {% endupdates %}
