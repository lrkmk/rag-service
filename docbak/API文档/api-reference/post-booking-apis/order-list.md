# 订单列表

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用 `orderList.do` 查询订单集合，支持预订后的运营核对和订单跟进。

它适用于列表级查询，而非单笔订单的出票状态确认。

### 常见问题

#### 何时应使用 `orderList.do`？

当需要查询多个订单并进行运营跟进时使用。

使用它支持订单核对和预订后处理。

#### 如何查询单笔订单的出票状态？

使用[查询订单](/api-wen-dang/api-reference/booking-apis/query-order.md)获取单笔订单状态、出票进度和订单详情。

不要使用列表查询替代支付后的订单状态跟进。

#### 查询订单后应做什么？

根据订单状态选择适用的预订后操作。

退款、作废和订单维护流程请参阅[预订后操作](/api-wen-dang/product-guides/post-booking.md)。

### 相关指南

使用[订单维护](/api-wen-dang/product-guides/post-booking/order-maintenance.md)了解运营查询与其他维护操作的边界。

## Order List

> \*\*Dependency:\*\*\
> No preceding function needs to be called before 'orderList' API.\
> \
> \*\*Endpoint:\*\*\
> <https://sandbox.atriptech.com/orderList.do>

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/orderList.do":{"post":{"summary":"Order List","deprecated":false,"description":"**Dependency:**\nNo preceding function needs to be called before 'orderList' API.\n\n**Endpoint:**\nhttps://sandbox.atriptech.com/orderList.do","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"orderNo":{"type":"string","description":"Atlas order number. Accurate matching","nullable":true},"airlinePNRs":{"type":"array","items":{"type":"string"},"description":"The airline PNR(not Atlas's).  If the airline pnr of the order contains any of the given values, it will be returned.","nullable":true},"paxName":{"type":"string","description":"The name of the passenger(last name/first name). If the passenger in the order includes the given value, it will be returned.","nullable":true},"contactEmail":{"type":"string","description":"Accurate matching，match based on the contact email provided by the customer","nullable":true},"fromCity":{"type":"string","description":"IATA code of the departure city","nullable":true},"toCity":{"type":"string","description":"IATA code of the arrival city","nullable":true},"depDate":{"type":"string","description":"Date of departure. The format is:`yyyyMMdd`","nullable":true},"createTimeRangeFrom":{"type":"string","description":"The start time of order creation. This is in UTC. The format is:`yyyy-MM-dd'T'HH:mm:ss'Z'`.","nullable":true},"createTimeRangeTo":{"type":"string","description":"The end time of order creation. This is in UTC. The format is`yyyy-MM-dd'T'HH:mm:ss'Z'`","nullable":true},"orderStatus":{"type":"array","items":{"$ref":"#/components/schemas/OrderStatus"},"description":"If the status of the order matches any of the given values, it will be returned","nullable":true},"airlines":{"type":"array","items":{"type":"string"},"description":"If the airlines of the order contains any of the given values, it will be returned","nullable":true},"page":{"type":"string","description":"Start from: 1","default":"1","nullable":true},"pageSize":{"type":"string","description":"Number of records to be displayed on each page. ","default":"20","maxLength":100,"nullable":true}},"description":"A series of conditions for matching orders"}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"type":"integer"},"msg":{"$ref":"#/components/schemas/ResponseMessage","nullable":true},"page":{"type":"string"},"pageSize":{"type":"string"},"totalRecords":{"type":"string"},"orders":{"type":"array","items":{"type":"object","properties":{"orderNo":{"type":"string","description":"Atlas order number"},"pnrCode":{"type":"string","description":"Atlas internal reference code"},"airlinePNRs":{"type":"array","items":{"type":"string"},"description":"Airline PNRs in the order","nullable":true},"orderStatus":{"$ref":"#/components/schemas/OrderStatus","description":"Order status"},"depDate":{"type":"string","description":"Date of departure. The format is:`YYYYMMDD`"},"airlines":{"type":"array","items":{"type":"string"},"description":"The IATA codes of all airlines in the order"},"orderCreateTimestamp":{"type":"string","description":"The time of order creation. This is in UTC. Format:`yyyy-MM-dd'T'HH:mm:ss'Z'`"},"paymentTimestamp":{"type":"string","description":"The time payment was made. This is in UTC. Format:`yyyy-MM-dd'T'HH:mm:ss'Z'`"},"paxNames":{"type":"array","items":{"type":"string"},"description":"The names of all passengers in the order"},"contactEmail":{"type":"string","description":"Contact email provided by the customer"},"fromCity":{"type":"string","description":"IATA code of departure city"},"toCity":{"type":"string","description":"IATA code of arrival city"},"errorCode":{"type":"string","description":"The error code returned for a cancelled order. This will only be displayed for cancelled orders.","nullable":true},"errorMessage":{"type":"string","description":"The error description.","nullable":true}},"required":["orderNo","pnrCode","orderStatus","depDate","airlines","orderCreateTimestamp","paymentTimestamp","paxNames","contactEmail","fromCity","toCity"]}}},"required":["status","page","pageSize","totalRecords","orders"]}}},"headers":{}}}}}},"components":{"schemas":{"OrderStatus":{"type":"integer","enum":[0,1,2,-3]},"ResponseMessage":{"type":"string","description":"It serves as an additional description of the response result. Especially when the interface reports an error (`status` !=`0`), it is usually a human-readable error message. Note: Do not use this field in any programming scenarios. For example, do not judge whether the interface responds successfully based on this field. Instead, you should only determine it by checking whether the status is equal to`0`at any time."}}}}
```
