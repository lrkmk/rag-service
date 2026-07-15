# 预订后操作

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用本页面解决退款、航班时刻变更和运营跟进问题。

{% hint style="info" %}
通过 ATRIP 中的 Eva 提交服务请求。
{% endhint %}

### 我们会收到航班时刻变更通知吗？

会的，但不总是通过单一渠道。 航司可能直接通知预订联系人。 Atlas webhook 和事件流程也应进行配置。

### Atlas 保证 webhook 送达吗？

不保证。 Webhook 送达是尽力而为的。

使用航司邮件、事件流程和订单查询进行最终确认。

### 预订后操作应如何处理？

根据操作类型使用 Atlas API 和 ATRIP：

* 退款和取消
* 附加服务追加
* 变更的服务请求
* 事件跟进

### 你们提供紧急售后支持吗？

对于出发前 24 小时内的紧急情况，尽可能使用航司的"管理我的预订"流程。

### 应在哪里查看退款和取消政策？

始终使用航司的最新政策作为真相来源。

### 退款需要多长时间？

Atlas 通常在 4 小时内向航司提交退款请求。 最终确认和资金返还仍取决于航司。

Atlas 收到资金后，进行对账和余额记入。

### Atlas 的作废处理如何工作？

使用专用的作废流程：

* `voidQuotation.do`
* `void.do`
* `queryVoidOrders.do`

首先请求报价。

然后使用最新的 `voidOfferId` 提交作废。

跟踪状态直到案件关闭。

请参阅[作废](/api-wen-dang/product-guides/post-booking/void.md)。

### Atlas 支持部分乘客作废吗？

不支持。 Atlas 仅接受整单作废。

不要仅为部分乘客提交作废。

### 如果在截止日期后提交作废会怎样？

Atlas 实时拒绝请求。 典型消息：

* `Void deadline exceeded. This ticket can no longer be voided（超过作废截止时间。此机票无法再作废）`

如果作废窗口已过，重新检查案件是否应转为退款。

### 作废费用固定时，还需要作废报价吗？

需要。 在 `void.do` 之前仍需要 `voidQuotation.do`。

### 多久能获得作废结果？

在大多数情况下，Atlas 大约在 5 分钟内返回作废请求是否已被接受处理。 最终完成或拒绝仍可能需要更长时间。

使用 webhook 获取进度更新。 使用作废查询进行最终对账。

### 应如何请求预订变更？

通过 ATRIP 中的 Eva 提交服务请求，进行姓名更正、航班变更或类似的预订后操作。

### 预订变更是否通过 API 支持？

不作为通用的自助 API 流程。 使用 ATRIP 中的 Eva 提交服务请求。

### 非自愿变更如何处理？

对于航司航班时刻变更或类似的非自愿情况，使用 ATRIP 中的退款流程。 这是免费处理的。

### 出票后可以添加行李或座位吗？

当航司和订单支持时，行李可以在出票后添加。 出票后不支持座位选择。

请参阅[座位](/api-wen-dang/product-guides/booking/optional-ancillaries/seats-and-baggage.md)了解当前的座位选择支持范围。

### 如果预订或服务失败怎么办？

如果 Atlas 导致错误的预订或出票，Atlas 将在适用时补偿替代机票。 退款延迟仍取决于航司处理。

### 为运营团队提供哪些支持或培训？

Atlas 在 UAT 完成后提供上线指导。 其中包括 ATRIP 流程指导和后续问答。

### 退款处理因支付模式有何不同？

#### Deposit（存款）

* Atlas 跟踪通过 Atlas 发起的退款
* 如果乘客或代理直接向航司退款，在需要时通过 ATRIP 通知 Atlas
* Atlas 在收到航司资金后记入您的 Atlas 余额

#### VCC

退款资金通常返回到原始 VCC 账户。 不要为 VCC 退款使用 ATRIP 的"代理和乘客发起退款"流程。

### ATRIP 中有哪些退款发起选项？

#### Atlas 发起的退款

使用以下任一方式：

* **退款**按钮
* 通过 Eva 提交的**取消与退款**服务请求

#### 代理或乘客发起的退款

使用以下任一方式：

* 通过 Eva 提交的**代理与乘客发起退款**服务请求
* 退款模块中的批量上传

### 应如何处理退款跟进？

在退款提交后至少等待 21 天再进行跟进。 然后通过 Eva 在现有服务请求中跟进，或在 ATRIP 中创建新的退款跟进请求。

### 相关页面

* [退款](/api-wen-dang/product-guides/post-booking/refunds.md)
* [预订后](/api-wen-dang/product-guides/post-booking.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)
