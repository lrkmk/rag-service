# 合作伙伴常见问题

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

在首次集成通话前，将本页面作为简短的预读材料使用。

它适用于业务、产品和技术利益相关者共同阅读。

### 1. 应使用哪种预订流程？

当 Atlas 是您的主要搜索来源时，使用 `search.do`。

当您已经知道行程或需要独立的实时价格检查时，使用 `getOffers.do`。

标准流程是：

1. `search.do`
2. `verify.do`
3. `order.do`
4. `pay.do`
5. `queryOrderDetails.do`

请参阅[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)。

### 2. 为什么搜索价格和预订价格可能不同？

搜索可能使用缓存数据。

验证或 Get Offer 在预订前检查实时票价和可用性。

使用最新的已验证或报价价格作为真相来源。

### 3. 如何保护价格完整性？

将刷新点保持在接近预订的时间。

避免在价格检查和订单创建之间长时间延迟。

将价格刷新视为必需的业务规则，而不仅仅是技术细节。

### 4. Atlas 是否支持票价家族、行李和座位？

是的，但支持取决于航司和流程。

票价家族可以在搜索中返回。

行李和座位查询应保持可选，除非它们对转化率是必需的。

请参阅[座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)和[行李](/api-wen-dang/product-guides/booking/optional-ancillaries/baggage.md)。

### 5. 哪些支付模式可用？

主要选项是：

* **Deposit（存款）**
* **VCC pass-through（VCC 直通）**

Atlas 不发行 VCC 卡。

使用 VCC 直通时，您提供卡详情。

请参阅[支付](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-payments.md)。

### 6. 出票是同步的吗？

不总是。

支付和最终出票可能在不同时间完成。

您的系统应在支付后轮询订单状态，直到最终状态确认。

### 7. `pnrCode` 是航司 PNR 吗？

不是。

`pnrCode` 是 Atlas 预订参考号。

航司 PNR 在出票后出现，应从订单查询中读取。

### 8. Webhook 足够用于状态跟踪吗？

不够。

Webhook 送达是尽力而为的。

将 webhook 作为有用的信号，而不是唯一的真相来源。

您的最终对账路径仍应包括订单查询，并在需要时与航司沟通。

### 9. 退款和改签如何处理？

退款行为取决于支付模式。

VCC 退款通常返回到原始卡。

Deposit 退款在 Atlas 收到航司资金后记入余额。

预订变更通常通过 ATRIP 服务请求处理，而不是通用的自助 API 流程。

请参阅[预订后](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-post-ticketing.md)。

### 10. UAT 和上线前应准备什么？

UAT 前：

* 沙箱集成端到端稳定
* 主要预订流程正常工作
* 标识符和身份验证处理正确
* 如果需要，webhook 处理已就绪

上线前：

* UAT 已批准
* 生产凭证已生成
* IP 白名单已就绪
* 端点已正确切换
* 首批实时订单可以密切监控

请参阅：

* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)
* [生产上线](/api-wen-dang/readme-1/production-go-live.md)

### 如果只先对齐 5 件事

从这些开始：

* 选择的预订流程
* 价格刷新规则
* 支付模式
* 轮询和最终状态规则
* 预订后归属

### 相关页面

* [集成前](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/before-integration.md)
* [启动检查清单](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/kickoff-checklist.md)
* [常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)
