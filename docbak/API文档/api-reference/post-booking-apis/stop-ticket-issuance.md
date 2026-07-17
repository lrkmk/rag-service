# 停止出票

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当订单流程支持停止出票时，使用 `stopTicket.do` 中止出票操作。

它用于预订后的运营处理，不属于标准预订步骤。

### 常见问题

#### 何时应使用 `stopTicket.do`？

仅当当前订单和流程支持停止出票时使用。

在调用前，先确认订单状态和业务处理目标。

#### 停止出票后应做什么？

查询订单以确认当前状态和可用的后续操作。

使用[查询订单](/api-wen-dang/api-reference/booking-apis/query-order.md)获取订单与出票进度。

#### 停止出票与作废是否相同？

不是。停止出票用于中止适用流程中的出票操作。

作废适用于符合航司作废条件的订单。使用[作废](/api-wen-dang/api-reference/post-booking-apis/void.md)处理作废流程。

### 相关指南

使用[订单维护](/api-wen-dang/product-guides/post-booking/order-maintenance.md)确认停止出票的适用边界。

## Stop Ticket Issuance

> \*\*Dependency:\*\*\
> \`Payment\` function should be called in prior to this call.\
> \
> \*\*Endpoint:\*\*\
> <https://sandbox.atriptech.com/stopTicket.do>

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/stopTicket.do":{"post":{"summary":"Stop Ticket Issuance","deprecated":false,"description":"**Dependency:**\n`Payment` function should be called in prior to this call.\n\n**Endpoint:**\nhttps://sandbox.atriptech.com/stopTicket.do","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"The order number of the ticket order you want to stop ticket issuance."}},"required":["orderNo"]}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"type":"integer","description":"-`0`: success\n-other: fail"},"msg":{"$ref":"#/components/schemas/ResponseMessage","nullable":true}},"required":["status"]}}},"headers":{}}}}}},"components":{"schemas":{"ResponseMessage":{"type":"string","description":"It serves as an additional description of the response result. Especially when the interface reports an error (`status` !=`0`), it is usually a human-readable error message. Note: Do not use this field in any programming scenarios. For example, do not judge whether the interface responds successfully based on this field. Instead, you should only determine it by checking whether the status is equal to`0`at any time."}}}}
```
