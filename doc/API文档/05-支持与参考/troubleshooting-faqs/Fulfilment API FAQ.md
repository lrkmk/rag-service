# Fulfilment API FAQ

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

本页汇集了从商业评估到集成规划过程中关于 Fulfilment API 的常见问题。

当您需要以下信息时，从这里开始：

* 判断 Fulfilment API 是否适合您的预订模式
* 了解它如何与现有 Atlas 接口协作
* 向内部团队解释定价、支付路径和失败处理机制

### 简短回答

Fulfilment API **不会取代**标准 Atlas 预订流程。

它增加了一条独立的履约路径，适用于已经持有订单或运价、需要 Atlas 完成验价和出票的合作方。

您可以将其与现有 Atlas 接口并行使用。

### 何时评估 Fulfilment API

当以下任一情况适用时，建议评估 Fulfilment API：

* 您需要**临近起飞出票**，且不希望受缓存过期压力的限制
* 您处理**多人订单**，希望在出票前获得更准确的价格
* 您已拥有自己的运价来源，仅需 Atlas 完成履约
* 您需要在预存款（Deposit）和 VCC 直通之间提供**支付兜底**
* 您希望比完整的 `search.do` → `verify.do` → `order.do` 链路更简单的出票集成

### Fulfilment API vs. 现有接口 —— 一表看清

Fulfilment API 不会取代现有的 Atlas 接口。

它在标准预订流程之上增加了一条独立的履约路径。

| 维度          | 现有接口（`search.do` / `verify.do` / `order.do`）    | Fulfilment API       |
| ----------- | ----------------------------------------------- | -------------------- |
| 前置条件        | 必须先通过 Atlas 购物流程获取运价                            | 您已持有运价或订单上下文，直接传入    |
| 运价来源        | 必须来自 Atlas 运价上下文                                | 可来自 Atlas 或您自己的运价来源  |
| 临近起飞出票      | 受缓存过期压力限制                                       | 提交请求后无提前购买限制         |
| 多人定价准确性     | 依赖缓存，价格变动风险较高                                   | 实时验价，出票前准确性更高        |
| VCC 返利/航司佣金 | 通常在商业计算中单独处理                                    | 可直接在报价净价中体现          |
| 支付方式        | 预存款（Deposit）                                    | 预存款（Deposit）和 VCC 直通 |
| 提交后系统故障     | 您的预订编排可能中断                                      | 请求被接受后 Atlas 继续履约    |
| 集成工作量       | 需要完整的 `search.do` → `verify.do` → `order.do` 链路 | 独立接口，集成范围约 1 小时      |
| 定价模式        | 遵循标准商业模型                                        | 按使用量计费的交易费模式         |
| 可并行使用       | 是                                               | 是                    |

#### 保持不变的部分

现有的 `search.do`、`verify.do`、`order.do` 及相关流程将继续正常工作。

Fulfilment API 是额外增加的产品路径。

#### 变化的部分

Fulfilment API 从 `getOfferPrice.do` 开始。

它适用于您已知目标订单上下文、需要 Atlas 快速完成履约的场景。

同时，它在订单创建后严格执行 **5 分钟支付和出票窗口**。

#### 团队选择它的原因

团队通常基于以下一个或多个原因选择 Fulfilment API：

* 更好地支持临近起飞出票
* 出票前的实时运价验证
* 自带运价、由 Atlas 完成出票履约
* 通过预存款和 VCC 直通实现双支付路径
* 纯出票场景下更低的集成工作量

### FAQ

#### 我已经在使用 Atlas 现有接口，还需要 Fulfilment API 吗？

不需要。

它是可选的。

当您的业务存在标准流程无法很好解决的场景时使用。

典型触发因素包括：临近起飞出票、多人定价漂移、自供运价、或更强的容错需求。

#### Fulfilment API 会取代 `search.do`、`verify.do` 和 `order.do` 吗？

不会。

Fulfilment API 是一个独立的履约通道。

当 Atlas 是您主要的购物和预订层时，使用标准流程。

当您已持有运价或订单上下文、需要 Atlas 完成验价和出票时，使用 Fulfilment API。

#### 可以同时使用现有接口和 Fulfilment API 吗？

可以。

它们完全兼容。

许多合作方保留标准流程用于 Atlas 来源的购物，同时使用 Fulfilment API 处理独立履约场景。

#### Fulfilment API 在什么情况下比标准流程更合适？

当您需要以下能力时，它通常是更好的选择：

* 临近起飞出票
* 出票前更高的多人定价准确性
* 在自有运价之上使用 Atlas 出票能力
* 预存款和 VCC 直通之间的支付兜底
* 提交请求后仍能继续运行的履约

#### 为什么 Fulfilment API 更适合临近起飞出票？

标准流程更依赖缓存的定价上下文。

Fulfilment API 在更接近履约的时间点执行实时运价验证。

这消除了标准流程在请求提交后的缓存过期压力。

使得 Fulfilment API 更适合临近起飞预订场景，请求提交后无提前购买限制。

#### 为什么 Fulfilment API 更适合多人订单？

多人订单更容易受到价格漂移的影响。

Fulfilment API 在出票前再次验证运价。

与依赖缓存的流程相比，这降低了后期价格变动的风险。

#### 我可以自带运价来源吗？

可以。

Fulfilment API 支持已在 Atlas 之外获取运价的合作方。

当您需要 Atlas 的履约和出票能力、但不想将购物层迁移到 Atlas 时使用。

#### Fulfilment API 支持哪些支付方式？

Fulfilment API 支持预存款（Deposit）和 VCC 直通（VCC pass-through）两种支付方式。

这为您提供了两条可操作的支付路径。

当其中一条路径不可用时，只要当前订单状态允许，您可以切换到另一条。

#### 如果我自己的系统在提交请求后发生故障会怎样？

履约请求被接受后，Atlas 会在 Atlas 端继续执行履约流程。

后续合作方侧的不稳定不会阻止已提交的履约任务继续推进。

您仍应通过订单查询或 Webhook 监控最终订单状态。

#### 定价模式是按使用量计费的吗？

是的。

Fulfilment API 采用按预订计费的交易费模式。

定价基于使用量，并可随用量层级调整。

您只需为成功的使用付费。

#### 所谓的"1 小时集成"在实践中意味着什么？

这意味着集成范围比完整的全链路流程小得多。

您无需从头重建搜索、验价和订单编排。

在高层面上，您只需要：

1. 以要求的请求格式发送现有运价或订单上下文
2. 处理运价验证结果
3. 处理出票结果或失败后续处理

对于已经持有所需订单上下文的团队，集成通常可以在大约 1 小时内完成。

#### 为什么 Fulfilment API 的定价可以更有竞争力？

Fulfilment API 的定价可以将返利直接包含在净价中。

这可以减少 VCC 返利和航司佣金场景下单独的返利计算工作。

具体的商业结果仍取决于您签约的定价模型。

#### 如果出票失败会怎样？

Fulfilment API 支持失败告警和快速诊断。

出票失败时，失败消息会标识主要原因类别，以便您的团队更快行动。

请使用订单查询作为最终状态的真实来源。

#### 失败告警的发送速度有多快？

失败告警会在出票失败确认后的 6 分钟内发出。

请使用 `queryOrderDetails.do` 作为最终订单状态的真实来源。

当您需要合同承诺时，请使用为您账户约定的 SLA。

#### Fulfilment API 支持哪些航司？

Fulfilment API 由 Atlas 100+ 条直连官方航司线路提供支持，并持续扩展。

覆盖范围与现有 Atlas 航司出票能力基本一致。

如果航司范围是上线障碍，请在解决方案评审期间确认具体的航司列表。

#### Fulfilment API 对 AI 代理工作流有用吗？

是的。

它为 AI 代理系统提供面向履约的统一接口，而非各个航司独立的出票规则。

当您的自动化层需要标准状态处理和错误管理时，这降低了编排复杂度。

### 相关页面

* [Fulfilment API](/api-wen-dang/product-guides/booking/booking-flows/fulfillment-flow.md)
* [Get Offer Price](/api-wen-dang/product-guides/booking/booking-step-guides/get-offer-price.md)
* [Get Offer vs Fulfilment API](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions/get-offer-vs-get-offer-price.md)
* [订单与出票](/api-wen-dang/support-and-reference/troubleshooting-and-support/faqs/atlas-api-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
