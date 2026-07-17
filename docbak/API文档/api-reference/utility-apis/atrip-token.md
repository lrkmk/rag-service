# ATRIP 令牌

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

在指南和链接中使用 `ATRIP 令牌` 作为主要名称。

此 API 映射到 `getAtripToken.do`。

旧版资料可能称之为 `getAtripToken`。

## getAtripToken

> \*\*Dependency\*\*\
> No preceding function needs to be carried out.

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/getAtripToken.do":{"post":{"summary":"getAtripToken","deprecated":false,"description":"**Dependency**\nNo preceding function needs to be carried out.","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string","default":"gzip"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_ID>"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string","default":"<YOUR_CLIENT_SECRET>"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"Order number. It can be an order for ticketing, or an order for add bags. The format of each kind of order is different."},"userName":{"type":"string","description":"This is to identifier the operator's name in client's system, Atlas will grant access to this operator and track his/her actions in Atlas customer service portal."},"role":{"type":"string","description":"This is to identify the operator's role. Atlas will grant access to this operator according to the role assigned. Here are the acceptable options:\n\nCustomer service : Access to manage orders and request post ticketing services\n\nFinance : Access to manage the balance and check statements\n\nDeveloper : Access to manage the system configurations\n\nAdmin : Full access"}},"required":["role","userName","orderNo"]}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"url":{"type":"string","description":"A url with token to access to Atlas customer service portal.\n\n"},"status":{"type":"integer","description":"0: success\n\n2: System error\n\n3: unauthorized access"},"msg":{"type":"string","description":"Error message.\n\nThe 'msg' element is for description of the results. Please DO NOT use this field to check the success or failure of the request. Only use the 'status' code to check the result.","nullable":true}},"required":["url","status"]}}},"headers":{}}}}}}}
```
