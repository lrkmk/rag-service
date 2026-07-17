# 支付与出票

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此端点支付已有订单。

发送 `orderNo` 和选定的 `paymentMethod`。

支付成功并不总是意味着出票已经完成。

使用[查询订单](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/2yNUkts3yozduQUMF05n)确认最终出票状态。

## Payment

> \*\*Dependency:\*\*\
> \`Order\` function should be called in prior to this call.\
> \
> \> - Atlas provides the information from the search.do API response itself whether VCC can be accepted as a mode of payment for an order. Please read the "supportCreditTransPayment" field in the search.do and verify.do responses. When this field is equal to "0" (zero), it means that only "deposit" mode of payment can be used and when this field is equal to "1" (one), it means that both the "deposit" as well as the "VCC" mode of payment can be used.\
> \> - For VCC payments, the Test Cards to be used for testing in SANDBOX:\
> \> Visa:\
> \>    \&#9702; 4532015112830366\
> \>    \&#9702; 4916931584764308\
> \>    \&#9702; 4485275742308327\
> \>    \&#9702; 4556737586899855\
> \>    \&#9702; 4532644189324563\
> \> Mastercard:\
> \>    \&#9702; 5555555555554444\
> \>    \&#9702; 5105105105105100\
> \>    \&#9702; 5223456789012346\
> \>    \&#9702; 5301250070000191\
> \>    \&#9702; 5454545454545454\
> \> American Express:\
> \>    \&#9702; 378282246310005\
> \>    \&#9702; 371449635398431\
> \>    \&#9702; 340000000000009\
> \>    \&#9702; 370000000000002\
> \>    \&#9702; 375987654321001\
> \> Discover:\
> \>    \&#9702; 6011111111111117\
> \>    \&#9702; 6011000990139424\
> \>    \&#9702; 6011987612345678\
> \> JCB:\
> \>    \&#9702; 3566002020360505\
> \
> \*\*Endpoint:\*\*\
> <https://sandbox.atriptech.com/pay.do>

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/pay.do":{"post":{"summary":"Payment","deprecated":false,"description":"**Dependency:**\n`Order` function should be called in prior to this call.\n\n> - Atlas provides the information from the search.do API response itself whether VCC can be accepted as a mode of payment for an order. Please read the \"supportCreditTransPayment\" field in the search.do and verify.do responses. When this field is equal to \"0\" (zero), it means that only \"deposit\" mode of payment can be used and when this field is equal to \"1\" (one), it means that both the \"deposit\" as well as the \"VCC\" mode of payment can be used.\n> - For VCC payments, the Test Cards to be used for testing in SANDBOX:\n> Visa:\n>    &#9702; 4532015112830366\n>    &#9702; 4916931584764308\n>    &#9702; 4485275742308327\n>    &#9702; 4556737586899855\n>    &#9702; 4532644189324563\n> Mastercard:\n>    &#9702; 5555555555554444\n>    &#9702; 5105105105105100\n>    &#9702; 5223456789012346\n>    &#9702; 5301250070000191\n>    &#9702; 5454545454545454\n> American Express:\n>    &#9702; 378282246310005\n>    &#9702; 371449635398431\n>    &#9702; 340000000000009\n>    &#9702; 370000000000002\n>    &#9702; 375987654321001\n> Discover:\n>    &#9702; 6011111111111117\n>    &#9702; 6011000990139424\n>    &#9702; 6011987612345678\n> JCB:\n>    &#9702; 3566002020360505\n\n**Endpoint:**\nhttps://sandbox.atriptech.com/pay.do","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"Order number you want to do the payment."},"paymentMethod":{"description":"The payment method you want to use\n- 1: balance\n- 3: vcc passthough\n- 4: BYOA\n- 5: MoR","$ref":"#/components/schemas/PaymentMethod"},"creditCard":{"type":"object","properties":{"cardNumber":{"type":"string","description":"Credit card number that conforms to the Luhn algorithm."},"cardCVV":{"type":"string","description":"The Card Verification Value (CVV). For vcc passthrough, CVV is required. When using MoR, the CVV is mandatory if the card is being used for the first time, and for subsequent uses, it can be left as `null` (not empty string `\"\"`)."},"cardExpireMonth":{"type":"string","description":"The card expiry month as an integer with two digits(01-12), e.g. for February use 02."},"cardExpireYear":{"type":"string","description":"The card expiry year as an integer with two digits, e.g. for 2026 use 26."},"cardHolderLastName":{"type":"string","description":"Last name of the card holder"},"cardHolderFirstName":{"type":"string","description":"First name of the card holder"},"cardHolderCountry":{"type":"string","description":"The ISO 3166-1 alpha-2 code for the country of the billing address associated with the card.","nullable":true},"cardHolderProvince":{"type":"string","description":"The state/province of the billing address associated with the card. Only use tow-letter code, for example, use \"CA\" and not \"California\".","nullable":true},"cardHolderCity":{"type":"string","description":"The city of the billing address associated with the card.","nullable":true},"cardHolderPostCode":{"type":"string","description":"The postal code of the billing address associated with the card.","nullable":true},"cardHolderAddress":{"type":"string","description":"The first/second line of the billing address associated with the card.","nullable":true},"reusable":{"type":"boolean","description":"A flag used to indicate whether it is a single-use card or a multi-use card.\n-`true`: multiple-use card\n-`false`: single-use card\n\n**Explanation:**\nAtlas hopes that users can inform us of this information because Atlas is cautious when making payments for multiple cards.\nFor example, when encountering unknown errors in payment to the airline, Atlas will not easily attempt to retry, as this may result in multiple deductions.","default":false,"nullable":true},"paymentLimit":{"type":"integer","description":"Certain airlines may experience fare change after payment submission due to their inability to hold seat reservations. You can use this parameter to set a maximum acceptable payment amount(in vendor currency) threshold. This is the maximum amount which can be used to create the booking using a VCC. ","nullable":true},"threeDS":{"type":"object","properties":{"ip":{"type":"string","description":"The device IP of the end user. By default, the system will use the source IP of the current request."}},"required":["ip"],"description":"The information used for the 3DS verification. It is only required in the MoR payment scenario.","nullable":true}},"required":["cardNumber","cardExpireMonth","cardExpireYear","cardCVV","cardHolderLastName","cardHolderFirstName"],"description":"Credit card. It is necessary when using MoR(`paymentMethod`=`5`) or VCC passthrough(`paymentMethod`=`3`) payment.","nullable":true},"clientOrderNo":{"type":"string","description":"Order number at the customer side.","nullable":true},"requestSource":{"$ref":"#/components/schemas/RequestSource","nullable":true}},"required":["orderNo","paymentMethod"]}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"$ref":"#/components/schemas/PaymentResponseStatus","description":"- 400: Illegal request param. Description: Check and correct the request parameters according to the error message.\n- 401: Later than the payment deadline. Description: Payment for the booking was initiated later than the payment deadline.\n- 402: Order status does not support payment. Description: The order status maybe “ticketing” or “ticketed” where the payment has already been made. Check if the order status is unpaid\n- 403: Unsupported payment method. Description: The payment method is not supported for this order.\n- 404: The order is already paid. Description: Check if the order has been paid. If “yes”, do not send the payment request\n- 406: Payment operation is in progress. Description: The previous payment request is still in process. Wait for the airline PNR to be received in the PNR details response.\n- 407: Some mandatory element for the passenger has not been submitted.. Description: Check the information and correct the same and resubmit.\n- 408: Passenger can not board alone. Description: Create a new order and add an adult passenger with the child passenger\n- 409: Additional baggage does not match the flight segment. Description: Luggage purchased for each segment of a connecting flight must be the same.\n- 410: The contact information is not in the correct format.. Description: Check the contact information and confirm that it matches the required format.\n- 411: Some error happened with the payment gateway. Description: Some error happened with the payment gateway\n- 412: No available payment methods. Description: No available payment methods for this order\n- 413: Card is not supported. Description: For MoR, the brand of the card sent by customer is not supported by Atlas.\n- 414: Card mismatch. Description: The brand of the card sent during payment is inconsistent with the \"cardType\" sent when generating the order.\n- 415: order is not confirmed by user. Description: order is not confirmed by user"},"msg":{"$ref":"#/components/schemas/ResponseMessage","nullable":true},"orderNo":{"type":"string","description":"Echo the order number"},"paymentMethod":{"$ref":"#/components/schemas/PaymentMethod","description":"Payment method"}},"required":["orderNo","paymentMethod","status"]}}},"headers":{}}}}}},"components":{"schemas":{"PaymentMethod":{"type":"integer","enum":[1,3,4,5],"title":""},"RequestSource":{"type":"string","description":"The tag to identify which channel does this traffic come from. For example: SkyScanner,Google,Oganic search,etc…"},"PaymentResponseStatus":{"type":"integer","enum":[400,401,402,403,404,406,407,408,409,410,411,412,413,414,415]},"ResponseMessage":{"type":"string","description":"It serves as an additional description of the response result. Especially when the interface reports an error (`status` !=`0`), it is usually a human-readable error message. Note: Do not use this field in any programming scenarios. For example, do not judge whether the interface responds successfully based on this field. Instead, you should only determine it by checking whether the status is equal to`0`at any time."}}}}
```
