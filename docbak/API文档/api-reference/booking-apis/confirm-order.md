# 确认订单

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

在指南和链接中使用 `确认订单` 作为主要名称。

此 API 映射到 `orderCommit.do`。

旧版资料可能称之为 `Order Commit`（订单提交）。

## Order Commit

> This API is only required in the FR integration process. After create an order and before payment, you need to call this API to obtain the link of the FR order confirmation page and display it to users. Users should confirm the order through this page, and finally customer pay to Atlas.\
> \
> \*\*Endpoint:\*\*\
> <https://sandbox.atriptech.com/orderCommit.do>

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/orderCommit.do":{"post":{"summary":"Order Commit","deprecated":false,"description":"This API is only required in the FR integration process. After create an order and before payment, you need to call this API to obtain the link of the FR order confirmation page and display it to users. Users should confirm the order through this page, and finally customer pay to Atlas.\n\n**Endpoint:**\nhttps://sandbox.atriptech.com/orderCommit.do","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string","default":"gzip"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_ID>"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_SECRET>"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"Order number"},"redirectUri":{"type":"string","description":"The redirect localtion to which when users confirm an order on the \nFR's confirmation page. If you choose to display the confirmation page in `Popup` mode, please specify this.","nullable":true},"iframe":{"type":"string","description":"If you want to display the FR's order confirmation page in `iframe` mode, please specify `iframe=true`, and in this case, the `redirectUri` will be ignored.","nullable":true},"timeout":{"type":"integer","default":8000,"description":"Maximum response time of the API in milliseconds.","nullable":true}},"required":["orderNo"]}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"$ref":"#/components/schemas/OrderCommitResponseStatus","description":"- 307: illegal booking request param\n- 800: order not exists\n- 316: timed out\n- 317: airline error"},"msg":{"$ref":"#/components/schemas/ResponseMessage","nullable":true},"confirmationUrl":{"type":"string","description":"The FR order confirmation page link."}},"required":["status","confirmationUrl"]}}},"headers":{}}}}}},"components":{"schemas":{"OrderCommitResponseStatus":{"type":"integer","enum":[307,800,316,317]},"ResponseMessage":{"type":"string","description":"It serves as an additional description of the response result. Especially when the interface reports an error (`status` !=`0`), it is usually a human-readable error message. Note: Do not use this field in any programming scenarios. For example, do not judge whether the interface responds successfully based on this field. Instead, you should only determine it by checking whether the status is equal to`0`at any time."}}}}
```
