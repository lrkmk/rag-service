# 启动检查清单

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

在首次集成通话中使用此页面。

其目标很简单。

在会议结束时，就主要流程、归属和发布路径达成一致。

{% hint style="info" %}
需要先给合作伙伴一份简短的预读材料？

请使用[合作伙伴常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/top-questions-for-partners.md)。
{% endhint %}

### 本次会议应达成的目标

在启动结束时，双方应就以下内容达成一致：

* 要实施的预订流程
* 预订前的价格刷新点
* 按业务场景的支付模式
* 出票状态处理模型
* 座位或行李是否必须在购买前支持
* 谁负责退款和改签跟进
* UAT 和上线前需要什么

### 推荐会议顺序

{% stepper %}
{% step %}

### 确认商业和产品契合度

明确 Atlas 是主要的搜索来源，还是最终的预订和定价层。
{% endstep %}

{% step %}

### 选择预订流程

决定标准搜索流程还是 Get Offer 流程是主要的实施路径。
{% endstep %}

{% step %}

### 确认支付和出票设计

对齐 Deposit 或 VCC 的使用、轮询逻辑和最终状态处理。
{% endstep %}

{% step %}

### 确认预订后归属

就退款、改签、航班时刻变更和紧急情况的处理方式达成一致。
{% endstep %}

{% step %}

### 确认发布路径

就沙箱范围、UAT 预期和上线前提条件达成一致。
{% endstep %}
{% endstepper %}

### 第一部分：业务和系统契合度

首先问这些问题：

* Atlas 是您的主要搜索来源吗？
* 或者您已经有自己的搜索工具？
* 您主要需要 Atlas 用于最终的可预订价格确认？
* 您需要为所有航司使用一种流程，还是按承运人选择性路由？

#### 需要记录的决定

记录以下其中一项作为 Atlas 的主要角色：

* 主要搜索和预订层
* 最终定价和预订层
* 多源系统中的选择性供应商

### 第二部分：预订流程

选择主要路径。

#### 标准搜索路径

当 Atlas 是您的主要搜索来源时使用此路径。

主要链路：

1. `search.do`
2. `verify.do`
3. `order.do`
4. `pay.do`
5. `queryOrderDetails.do`

#### Get Offer 路径

当目标行程已知时使用此路径。

主要链路：

1. `getOffers.do`
2. `order.do`
3. `pay.do`
4. `queryOrderDetails.do`

#### 需要解决的问题

* 哪条路径是默认的生产路径？
* 您何时在预订前刷新价格？
* 您的系统会阻止长时间延迟后的过时定价吗？
* 您将支持两种流程还是仅一种？

请参阅：

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [获取报价](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer.md)
* [验证](/api-wen-dang/product-guides/booking/booking-step-guides/verify.md)

### 第三部分：定价完整性

这通常是风险最高的主题。

就以下规则达成一致：

* 搜索结果不是最终的预订承诺
* 验证或 Get Offer 应在接近预订时间时使用
* 长时间延迟会增加失败和不匹配的风险
* 最新的已验证或报价价格是订单创建的真相来源

#### 需要解决的问题

* 必须刷新价格的最晚时间点是什么？
* 如果用户延迟后返回，会发生什么？
* 加价是在最终刷新前还是之后应用？
* 当价格变化时，向用户显示哪个值？

### 第四部分：票价内容和附加服务

尽早设定期望。

#### 需要解决的问题

* 您需要票价家族展示吗？
* 您需要预订前的行李追加销售吗？
* 您需要预订前的座位图吗？
* 您需要出票后的行李或座位销售吗？
* 附加服务查询可以在第一个版本中保持可选吗？

#### 重要规则

除非必需，否则不要将附加服务查询强制加入基本流程。

请参阅[座位与行李](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)。

### 第五部分：支付模式

在开始构建前确认主要支付路径。

#### 主要选项

* **Deposit（存款）**
* **VCC pass-through（VCC 直通）**

#### 需要解决的问题

* 哪种支付模式是默认模式？
* 支付模式会因航司而异吗？
* 客户是否提供 VCC 卡？
* 当特定订单无法使用 VCC 时，会发生什么？
* 退款预期如何向运营团队展示？

#### 重要规则

Atlas 不发行 VCC 卡。

请参阅[支付](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-payments.md)。

### 第六部分：出票和预订状态

将出票视为异步的。

#### 需要解决的问题

* 客户会在 `pay.do` 之后轮询吗？
* 哪个状态被视为最终成功？
* 客户何时向代理人或用户展示航司 PNR？
* 如何防止重复支付？
* 存储哪些标识符以供跟进？

#### 需要保留的最低标识符

* `routingIdentifier`
* `sessionId` 或 `OfferId`
* `orderNo`
* `pnrCode`
* 可用的航司 PNR

请参阅[查询订单](/api-wen-dang/product-guides/booking/booking-step-guides/query-order.md)。

### 第七部分：预订后操作

这部分通常范围不足。

#### 需要解决的问题

* 谁提交退款？
* 谁跟进延迟的退款？
* 如何请求变更？
* 谁监控航班时刻变更？
* 出发当天紧急情况的处理流程是什么？

#### 重要规则

* 退款路径取决于支付模式
* 变更处理通过 ATRIP 服务请求进行
* Webhook 不应该是唯一的对账来源

请参阅：

* [预订后](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-post-ticketing.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)

### 第八部分：交付计划

以交付预期结束启动会议。

#### 需要解决的问题

* 沙箱中首先包含哪些范围？
* UAT 开始前需要什么？
* 适用哪个 UAT 轨道？
* 谁准备证据？
* 生产上线前必须准备什么？

请参阅：

* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)
* [生产上线](/api-wen-dang/readme-1/production-go-live.md)

### 启动的最终输出

不要仅以开放讨论结束会议。

以书面决策日志结束，记录以下内容：

* 选择的预订流程
* 定价刷新规则
* 支付模式
* 轮询规则
* 附加服务范围
* 预订后归属
* UAT 负责人
* 上线前提条件

### 相关页面

* [集成前](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/before-integration.md)
* [合作伙伴常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/top-questions-for-partners.md)
* [常见问题](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [预订后概述](/api-wen-dang/product-guides/post-booking.md)
