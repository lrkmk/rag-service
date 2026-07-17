# 作废

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用本部分了解专用的作废生命周期。

在需要以下内容时从此处开始：

* 检查订单是否仍可作废
* 使用最新的 `voidOfferId` 提交作废请求
* 跟踪作废处理和结果

需要先了解工作流指南？

使用[作废工作流](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/B8hsI0GKlmcexaJt4Npx)。

### 常见问题

#### 标准的 Atlas API 作废流程是什么？

标准流程是 `voidQuotation.do` → `void.do` → `queryVoidOrders.do`。

首先请求报价。

然后使用最新的 `voidOfferId` 提交作废。

提交后，查询状态直到案件完成或被拒绝。

#### Atlas 会在截止日期后拒绝作废请求吗？

会。

如果返回的当日作废截止日期已过，`void.do` 会实时失败。

典型错误信息：

* `Void deadline exceeded. This ticket can no longer be voided`（超过作废截止日期。此票证无法再作废）

#### Atlas 支持部分乘客作废吗？

不支持。

Atlas 仅接受整单作废。

不要仅针对部分乘客提交作废。

#### 服务费固定时，是否仍需调用 `voidQuotation.do`？

需要。

每次 `void.do` 请求前都需要调用 `voidQuotation.do`。

#### 何时应使用作废而非退款？

当订单仍在航司作废窗口内时使用作废。

当作废窗口已过或案件需要走退款流程时使用退款。

### 当前作废覆盖范围

Atlas 作废目前支持四个地区的 23 家航司。

#### 美洲

* `AS`
* `DM`
* `F9`
* `G4`
* `PB`
* `SY`
* `TS`
* `Y4`

#### 欧洲

* `A3`
* `D8`
* `EI`
* `DY`
* `N0`
* `OA`
* `VF`
* `Z0`

#### 日本

* `ZG` — 仅限美国航线

#### 韩国

* `7C`
* `BX`
* `LJ`
* `RS`
* `TW`
* `ZE`

近期新增：

* `TS`
* `Y4`
* `EI`
* `VF`

覆盖范围因航司和航线而异。

如果预订超出此范围，Atlas 可能返回 `843`。

### 本部分涵盖内容

* 请求作废报价
* 提交作废请求
* 查询作废状态和结果

### 典型流程

{% stepper %}
{% step %}

### 作废报价

检查订单是否可作废。

获取最新金额、方式和 `voidOfferId`。
{% endstep %}

{% step %}

### 提交作废

使用最新的报价结果提交作废请求。

保留返回的 `voidCode` 用于后续跟进。
{% endstep %}

{% step %}

### 查询作废状态

跟踪进度，直到作废完成、被拒绝或以其他方式关闭。
{% endstep %}
{% endstepper %}

### 提交作废前应确认什么？

确认：

* 原始 `orderNo` 正确
* 订单仍在航司作废窗口内
* 返回的当日截止日期尚未过
* 使用的是最新的 `voidOfferId`
* 该案件应走作废流程，而非退款流程

作废处理通常比退款处理更严格。

窗口过期可能使订单不可作废，即使退款仍有可能。

如果截止日期已过，Atlas 会立即拒绝作废请求。

### 关键行为

* 作废使用专用端点
* 提交前应先进行报价
* `voidOfferId` 用于提交
* `voidCode` 用于状态跟进

### 主要 API

* `voidQuotation.do`
* `void.do`
* `queryVoidOrders.do`

### 请求模型

使用专用的作废流程，输入如下：

* `voidQuotation.do`：`orderNo`
* `void.do`：`orderNo` + `voidOfferId`
* `queryVoidOrders.do`：`voidCode`

{% hint style="warning" %}
作废应在订单级别处理。

不要将作废视为部分退款流程。

Atlas 仅接受整单作废。
{% endhint %}

### 端点说明

#### `voidQuotation.do`

使用报价获取最新的作废资格和金额。

预期响应回答：

* 订单是否可作废
* 适用的 `voidMethod`
* 下一步使用的 `voidOfferId`

首先读取的重要字段：

* `isVoidable`
* `voidOfferId`
* `expectedConfirmationDate`
* `expectedRefundDate`
* `voidWindow.sameDayDeadlineTime`
* `voidWindow.sameDayTimezone`

#### `void.do`

使用最新的 `voidOfferId` 提交作废。

保留返回的 `voidCode`。

使用该代码进行所有后续状态跟进。

即使服务费固定，也不要跳过报价。

如果返回的当日截止日期已过，Atlas 会实时拒绝请求。

#### `queryVoidOrders.do`

使用查询在提交后跟踪作废状态。

在大多数情况下，Atlas 会在约 5 分钟内返回作废请求是否已被接受处理。

最终完成或拒绝仍可能需要更长时间。

首先读取的重要字段：

* `voidCode`
* `voidStatus`
* `cancelReason`
* `actualRefundAmount`（可用时）

### 状态处理

需要关注的主要结果状态：

* 处理中
* 已退款或履约完成
* 已拒绝

如果作废被拒绝，首先检查 `cancelReason`。

如果作废窗口已过期，在适用时将案件移至退款流程。

### 集成说明

提交前使用最新的报价结果。

不要重复使用旧的 `voidOfferId`。

将作废窗口视为严格限制。

如果订单不再可作废，不要继续重试作废路径。

### Webhook 选项

Atlas 也可以将 `order.void` 发送到你注册的 webhook URL。

在 `void.do` 之后使用它获取近乎实时的状态更新。

Webhook 是提交后跟进进度的推荐方式。

首先读取这些字段：

* `data.orderNo`
* `data.voidCode`
* `data.voidStatus`
* `data.message`

无需额外注册 webhook。

使用通过 `updateWebhookURL.do` 注册的同一 URL。

当需要最终对账时，使用 `queryVoidOrders.do`。

阅读[作废通知](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/4aywYMVHUfvNZttgiHPn)。

### 相关页面

* [退款](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/4SLUBW4WrcN15Hl7KYDP)
* [作废通知](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/4aywYMVHUfvNZttgiHPn)
* [错误代码](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/Jk40OgfAM5G1NDZxwAS1)
* [预订后 API](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/8P9YQq692vHSOmVjquJF)

## POST /voidQuotation.do

> Void Quotation

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/voidQuotation.do":{"post":{"summary":"Void Quotation","deprecated":false,"description":"","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string","default":"gzip"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_ID>"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_SECRET>"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"Atlas original order number. You can choose to request either orderNo or both airlinePNR and carrier."}},"required":["orderNo"]}}},"required":true},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"type":"integer","description":"Status code\n0 : Success\n801：Order not found for void. Check the original main ticket order number.\n803：Void already submitted for this passenger or segment. Query void status instead.\n805：voidOfferId expired. Call refundQuotation.do again for a fresh ID, then resubmit.\n808：This ticket is non-voidable per airline policy.\n810：Invalid request parameters\n814：Void submission already in progress. Wait before retrying.\n815：Ticket not found. Verify ticket number and order number.\n816：Void already submitted for this order. Query void status instead of resubmitting.\n817：Void already submitted for this order. Query void status instead of resubmitting.\n818：Void already submitted for this order. Query void status instead of resubmitting.\n820：Ticket already used — cannot void a flown segment.\n822：Void deadline exceeded. This ticket can no longer be voided.\n824：Wrong orderNumber: use the main ticket order, not the ancillary order number.\n841：Void not support the payment method. Please contact the airline directly for resolution.\n843：Atlas does not currently support VOID service for the airline or route of this booking."},"msg":{"type":"string","description":"Error message\nThe ‘msg’ element is for description of the results. Please do not use this field to check the success or failure of the request. Only use the ‘status’ code to check the result.","nullable":true},"fastConfirmation":{"type":"integer","enum":[0,1],"description":"Fast confirmation depends on whether the airline supports auto fulfillment.\n0 for False, 1 for True."},"expectedConfirmationDate":{"type":"string","description":"Expected date of getting airline void confirmation. The format is yyyyMMdd."},"expectedRefundDate":{"type":"string","description":"Expected date of getting refund. The format is yyyyMMdd."},"voidOfferId":{"type":"string","description":"Void offer id for this quotation which can be used for the coming Void call."},"voidMethod":{"type":"string","enum":["CashBackToOriginalPayment","Voucher"],"description":"Void method: CashBackToOriginalPayment or Voucher.\nCashBackToOriginalPayment: Refund cash back to the original form of payment.\nVoucher: Refund in the form of a voucher."},"voidTickets":{"type":"array","items":{"type":"object","properties":{"lastName":{"type":"string","description":"Last name of the passenger who wants to void."},"firstName":{"type":"string","description":"First name of the passenger who wants to void."},"ticketNo":{"type":"string","description":"The PNR received from the airline in the retrieve PNR response."}}},"description":"The void calculation for each of the passengers whose void quote has been requested"},"voidFareAmount":{"type":"object","properties":{"currency":{"type":"string","description":"The refund calculation for flight fare and inflow ancillaries.\n3-letter ISO currency code."},"originalFareAmount":{"type":"number","description":"Original fare of the flight."},"estimatedRefundAmount":{"type":"number","description":"Estimated amount which can be got back for this refund of flight."}},"required":["currency","originalFareAmount","estimatedRefundAmount"],"description":"If voidMethod is CashBackToOriginalPayment, the voidFareAmount field is not null."},"voidPostTicketingServiceAmounts":{"type":"array","items":{"type":"object","properties":{"postTicketingOrderNo":{"type":"string","description":"Unique order number for the post-ticketing service."},"currency":{"type":"string","description":"Currency used for post-ticketing service calculations.\n3-letter ISO currency code."},"originalPostTicketingServiceAmount":{"type":"number","description":"The original amount charged for the post-ticketing service."},"estimatedRefundAmount":{"type":"number","description":"Estimated amount which can be got back for this refund of Ancillaries."}},"required":["postTicketingOrderNo","currency","originalPostTicketingServiceAmount","estimatedRefundAmount"]},"description":"The void calculation for Post-ticketing Servrice, including baggage etc. Each post-ticketing order will be present as an object."},"serviceFee":{"type":"object","properties":{"currency":{"type":"string","description":"Currency used for the service fee.\n3-letter ISO currency code."},"transactionFee":{"type":"integer","description":"Transaction Fee of void."}},"required":["currency","transactionFee"],"description":"Service fee of void."},"voidWindow":{"type":"object","properties":{"supportVoid":{"type":"boolean"},"allowVoid":{"type":"boolean"},"voidTimeAfterIssure":{"type":"string"},"voidTimeBeforeDepature":{"type":"string"},"sameDayDeadlineTime":{"type":"string"},"sameDayTimezone":{"type":"string"}},"required":["supportVoid","allowVoid","voidTimeAfterIssure","voidTimeBeforeDepature","sameDayDeadlineTime","sameDayTimezone"],"description":"Void Window"},"orderNo":{"type":"string","description":"Original order number"},"isVoidable":{"type":"boolean","description":"True : Voidable False: Non-Voidable \ntrue or false"}},"required":["fastConfirmation","expectedConfirmationDate","expectedRefundDate","voidOfferId","voidMethod","isVoidable","voidTickets","voidFareAmount","serviceFee","voidWindow","orderNo","status","msg"]}}},"headers":{}}}}}}}
```

## Make a Void

> Void quotation function should be called in prior of this call

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/void.do":{"post":{"summary":"Make a Void","deprecated":false,"description":"Void quotation function should be called in prior of this call","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string","default":"gzip"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_ID>"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_SECRET>"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"Atlas original order number. You can choose to request either orderNo or both airlinePNR and carrier."},"voidOfferId":{"type":"string","description":"Get this from the void quotation response. "}},"required":["orderNo","voidOfferId"]}}},"required":true},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"type":"integer","description":"Status code\n0 : Success,\n801：Order not found for void. Check the original main ticket order number.\n803：Void already submitted for this passenger or segment. Query void status instead.\n805：voidOfferId expired. Call refundQuotation.do again for a fresh ID, then resubmit.\n808：This ticket is non-voidable per airline policy.\n810：Invalid request parameters\n814：Void submission already in progress. Wait before retrying.\n815：Ticket not found. Verify ticket number and order number.\n816：Void already submitted for this order. Query void status instead of resubmitting.\n817：Void already submitted for this order. Query void status instead of resubmitting.\n818：Void already submitted for this order. Query void status instead of resubmitting.\n820：Ticket already used — cannot void a flown segment.\n822：Void deadline exceeded. This ticket can no longer be voided.\n824：Wrong orderNumber: use the main ticket order, not the ancillary order number.\n841：Void not support the payment method. Please contact the airline directly for resolution.\n843：Atlas does not currently support VOID service for the airline or route of this booking."},"msg":{"type":"string","description":"Error message\nThe ‘msg’ element is for description of the results. Please do not use this field to check the success or failure of the request. Only use the ‘status’ code to check the result.","nullable":true},"fastConfirmation":{"type":"integer","description":"Fast confirmation depends on whether the airline supports auto fulfillment.\n0 for False, 1 for True."},"expectedConfirmationDate":{"type":"string","description":"Expected date of getting airline void confirmation. The format is yyyyMMdd."},"expectedRefundDate":{"type":"string","description":"Expected date of getting refund. The format is yyyyMMdd."},"voidOfferId":{"type":"string","description":"Void offer id for this quotation which can be used for the coming void call."},"voidMethod":{"type":"string","description":"Voidmethod: CashBackToOriginalPayment or Voucher.\nCashBackToOriginalPayment: Refund cash back to the original form of payment.\nVoucher: Refund in the form of a voucher."},"voidTickets":{"type":"array","items":{"type":"object","properties":{"lastName":{"type":"string","description":"Last name of the passenger who wants to void."},"firstName":{"type":"string","description":"First name of the passenger who wants to void."},"ticketNo":{"type":"string","description":"The PNR received from the airline in the retrieve PNR response."}},"required":["lastName","firstName","ticketNo"]},"description":"The void calculation for each of the passengers whose void quote has been requested"},"voidFareAmount":{"type":"object","properties":{"currency":{"type":"string","description":"The void calculation for flight fare and inflow ancillaries.\n3-letter ISO currency code."},"originalFareAmount":{"type":"number","description":"Original fare of the flight."},"estimatedRefundAmount":{"type":"number","description":"Estimated amount which can be got back for this refund of flight."}},"required":["currency","originalFareAmount","estimatedRefundAmount"],"description":"If voidMethod is CashBackToOriginalPayment, the voidFareAmount field is not null."},"voidPostTicketingServiceAmounts":{"type":"array","items":{"type":"object","properties":{"postTicketingOrderNo":{"type":"string","description":"Unique order number for the post-ticketing service."},"currency":{"type":"string","description":"Currency used for post-ticketing service calculations.\n3-letter ISO currency code."},"originalPostTicketingServiceAmount":{"type":"number","description":"The original amount charged for the post-ticketing service."},"estimatedRefundAmount":{"type":"number","description":"Estimated amount which can be got back for this refund of Ancillaries."}},"required":["postTicketingOrderNo","currency","originalPostTicketingServiceAmount","estimatedRefundAmount"]}},"serviceFee":{"type":"object","properties":{"currency":{"type":"string","description":"Currency used for the service fee.\n3-letter ISO currency code."},"transactionFee":{"type":"number","description":"Transaction Fee of void."}},"required":["currency","transactionFee"],"description":"Service fee of void."},"orderNo":{"type":"string","description":"Original order number"},"isVoidable":{"type":"boolean","description":"True : Voidable False: Non-Voidable\ntrue or false"},"voidStatus":{"type":"integer","description":"The present status of the void.\nThe options are:\n0: Atlas Processing\n1: Airline Processing (Submitted to airline by Atlas)\n2: Refunded\n3: Airline Refunding\n4: Rejected\n5: Fullfillment Done\n6: Withdrew\nIf the ticket is paid by deposit: the status can be 0,1,2,3,4\nIf the ticket is paid by VCC pass through: the status can be 0,1,4,5,6\nWithdrew is only in the refund claim"},"voidCode":{"type":"string","description":"Void order number generated for this void request"},"cancelReason":{"type":"string","description":"The reason why the void was cancelled."}},"required":["status","msg","fastConfirmation","expectedConfirmationDate","expectedRefundDate","voidOfferId","voidMethod","voidTickets","voidFareAmount","serviceFee","orderNo","isVoidable","voidStatus","voidCode","cancelReason"]}}},"headers":{}}}}}}}
```

## Query Void Status

> No preceding function needs to be carried out.

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/queryVoidOrders.do":{"post":{"summary":"Query Void Status","deprecated":false,"description":"No preceding function needs to be carried out.","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string","default":"gzip"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_ID>"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_SECRET>"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"Atlas original order number. "},"voidCode":{"type":"string","description":"The code of the void transaction received in the void.do response."}},"required":["orderNo"]}}},"required":true},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"voidOrders":{"type":"array","items":{"type":"object","properties":{"orderNo":{"type":"string","description":"The original order number"},"voidCode":{"type":"string","description":"The void order number generated for this void request"},"expectedConfirmationDate":{"type":"string","description":"Expected date to receive airline void confirmation. Format: yyyyMMdd."},"expectedRefundDate":{"type":"string","description":"Expected date to receive the refund. Format: yyyyMMdd.","nullable":true},"voidTickets":{"type":"array","items":{"type":"object","properties":{"lastName":{"type":"string","description":"Last name of the passenger for whom the void is requested"},"firstName":{"type":"string","description":"First name of the passenger for whom the void is requested"},"ticketNo":{"type":"string","description":"The PNR received from the airline retrieve PNR response."}},"required":["lastName","firstName","ticketNo"]},"description":"Void calculation for each passenger requesting a void quotation"},"voidFareAmount":{"type":"object","properties":{"currency":{"type":"string","description":"Currency used for flight fare and onboard ancillary service void calculations.\n3-letter ISO currency code."},"originalFareAmount":{"type":"number","description":"The original fare amount of the flight."},"estimatedRefundAmount":{"type":"number","description":"Estimated amount recoverable from this flight refund."}},"required":["currency","originalFareAmount","estimatedRefundAmount"],"description":"If voidMethod is CashBackToOriginalPayment, the voidFareAmount field is not empty."},"voidPostTicketingServiceAmounts":{"type":"array","items":{"type":"object","properties":{"postTicketingOrderNo":{"type":"string","description":"The unique order number for the post-ticketing service."},"currency":{"type":"string","description":"Currency used for post-ticketing service calculations.\n3-letter ISO currency code."},"originalPostTicketingServiceAmount":{"type":"number","description":"The original charged amount for the post-ticketing service."},"estimatedRefundAmount":{"type":"number","description":"Estimated amount recoverable from this ancillary service refund."}},"required":["postTicketingOrderNo","currency","originalPostTicketingServiceAmount","estimatedRefundAmount"]},"description":"List of void amounts for post-ticketing services"},"serviceFee":{"type":"object","properties":{"currency":{"type":"string","description":"Currency used for the service fee.\n3-letter ISO currency code."},"transactionFee":{"type":"integer","description":"Transaction fee for the void."}},"required":["currency","transactionFee"],"description":"Service fee for the void."},"voidStatus":{"type":"integer","description":"Current status of the void.\nOptions:\n0: Atlas processing\n1: Airline processing (submitted to airline by Atlas)\n2: Refunded\n3: Airline refunding\n4: Rejected\n5: Fulfillment completed\n6: Cancelled\nIf ticket is paid via deposit: status may be 0,1,2,3,4\nIf ticket is paid via VCC direct payment: status may be 0,1,4,5,6\nCancelled status only exists in refund applications"},"cancelReason":{"type":"string","description":"Reason why the void was cancelled."},"voidOfferId":{"type":"string","description":"The void offer ID for this quotation, which can be used for subsequent void calls."},"voidMethod":{"type":"string","description":"Void method: CashBackToOriginalPayment or Voucher","enum":["CashBackToOriginalPayment","Voucher"]}},"required":["orderNo","voidCode","expectedConfirmationDate","voidStatus","voidMethod"]},"description":"List of void orders"},"status":{"type":"integer","description":"API status code.\n0 : Success\n801: No voidable orders found. Please check the original main ticket order number.\n803: Passenger or segment has already submitted a void request. Please check the void status.\n805: voidOfferId has expired. Please call refundQuotation.do again to get a new ID and resubmit.\n808: This ticket cannot be voided according to airline policy.\n810: Invalid request parameters.\n814: Void submission is already in process, please try again later.\n815: Ticket not found. Please verify the ticket number and order number.\n816: This order has already submitted a void request. Please check the void status, do not resubmit.\n817: This order has already submitted a void request. Please check the void status, do not resubmit.\n818: This order has already submitted a void request. Please check the void status, do not resubmit.\n820: Ticket already used - cannot void flown segments.\n822: Void deadline has passed. This ticket can no longer be voided.\n824: Wrong order number: Please use the main ticket order number, not the ancillary service order number.\n841: Void is not supported for this payment method. Please contact the airline directly for processing.\n843: Atlas currently does not support void service for this airline or route."},"msg":{"type":"string","description":"Error message","nullable":true}},"required":["voidOrders","status","msg"],"description":"Void order query response"}}},"headers":{}}}}}}}
```
