# 座位

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用此端点进行流入座位查询。

{% hint style="warning" %}
`seatAvailability.do` 不再支持独立模式。

仅使用 `verify.do` 的有效 `sessionId` 或 `getOffers.do` 的 `OfferId` 进行调用。

不要仅使用航班数据调用它。
{% endhint %}

{% hint style="warning" %}
`seatAvailability.do` 与 `getLuggage.do` 共享一个 `60 QPM` 的辅助服务池。

超出限制的请求返回 `HTTP 429 Too Many Requests`。

请等待返回的 `retryAfter` 值后再重试。
{% endhint %}

### SeatAvailability 调用规则

仅在有效的预订链中使用 `seatAvailability.do`。

支持的请求上下文：

* `verify.do` 返回的 `sessionId`
* `getOffers.do` 返回的 `OfferId`

不支持的请求上下文：

* 仅航班信息

### 区域处理

#### 全球客户

保持当前流程。

像以前一样使用 `sessionId` 或 `OfferId`。

#### 中国 OTA 场景

某些上游座位请求仅包含航班信息。

对于这种情况，保留 `verify.do` 返回的 `sessionId`。

当座位请求到达时，将航班与缓存的 `sessionId` 进行匹配。

如果匹配成功，使用该 `sessionId` 调用 `seatAvailability.do`。

如果不存在匹配，则将其视为纯询价请求。

Atlas 不支持这种情况。

### 变更原因

此规则确保座位定价和履约与实际预订链保持一致。

同时也减少了无效的航司侧查询。

有关共享规则和计数详情，请使用 [API 请求限制](/api-wen-dang/product-guides/booking/booking-overview/api-request-limits.md)。

## Seat Availability

> \*\*Dependency:\*\*\
> Verify or getOffer function should be called in prior to this call.\
> \
> \> In a booking process, please call the 'seatAvailability' API to get seat availability information after price verification via 'verify' or 'getOffer'.\
> \> Steps:\
> \> 1. API sequence\
> \>    \* Search - Verify- seatAvailability - Order - Pay\
> \>    \* getOffer - seatAvailability - Order - Pay\
> \> 2. Pass 'offerId' in 'seatAvailability' requests:\
> \>    \* From 'verify': Use sessionId directly.\
> \>    From 'getOffer': Use its offerId.\
> \> 3. In the Order step, use the productCode to add specific seat to the ticket order.\
> \
> \*\*Endpoint:\*\*\
> <https://sandbox.atriptech.com/seatAvailability.do>

```json
{"openapi":"3.0.1","info":{"title":"Default module","version":"1.0.0"},"security":[],"paths":{"/seatAvailability.do":{"post":{"summary":"Seat Availability","deprecated":false,"description":"**Dependency:**\nVerify or getOffer function should be called in prior to this call.\n\n> In a booking process, please call the 'seatAvailability' API to get seat availability information after price verification via 'verify' or 'getOffer'.\n> Steps:\n> 1. API sequence\n>    * Search - Verify- seatAvailability - Order - Pay\n>    * getOffer - seatAvailability - Order - Pay\n> 2. Pass 'offerId' in 'seatAvailability' requests:\n>    * From 'verify': Use sessionId directly.\n>    From 'getOffer': Use its offerId.\n> 3. In the Order step, use the productCode to add specific seat to the ticket order.\n\n**Endpoint:**\nhttps://sandbox.atriptech.com/seatAvailability.do","tags":[],"parameters":[{"name":"Accept","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Content-Type","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"Accept-Encoding","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-id","in":"header","description":"","required":true,"schema":{"type":"string"}},{"name":"x-atlas-client-secret","in":"header","description":"","required":true,"schema":{"type":"string"}}],"requestBody":{"content":{"application/json":{"schema":{"type":"object","properties":{"sessionId":{"type":"string","description":"The`sessionId`returned by price verification api(`verify.do`). Only required in **Non-independent mode**."},"offerId":{"type":"string","description":"The`offerID`returned by get offer api(`getOffers.do`). Only required in **Non-independent mode**."},"carrier":{"type":"string","description":"The IATA code of MSC(known as Most Significant Carrier) of the itinerary."},"outboundSegments":{"type":"array","items":{"properties":{"flightNumber":{"type":"string"},"segmentIndex":{"type":"integer"},"depAirport":{"type":"string"},"arrAirport":{"type":"string"},"cabinClass":{"type":"string"},"depTime":{"type":"string"}},"$ref":"#/components/schemas/SeatMapFlight"},"description":"Outbound segments. All segments of the itinerary must be specified. Segments should be arranged in the order of takeoff.","minItems":1},"inboundSegments":{"type":"array","items":{"$ref":"#/components/schemas/SeatMapFlight"},"description":"Inbound segments. All segments of the itinerary must be specified. Segments should be arranged in the order of takeoff.","minItems":1,"nullable":true}},"required":["carrier","outboundSegments","sessionId","offerId"]}}}},"responses":{"200":{"description":"","content":{"application/json":{"schema":{"type":"object","properties":{"status":{"$ref":"#/components/schemas/SeatAvailabilityResponseStatus","description":"- 214: Session ID invalid or expired.\n- 215: Segment index missing.\n- 216: Seat selection failed.\n- 217: Unknown error.\n- 218: The airline don’t support seat selection currently.\n- 219: The route don’t support seat selection currently.\n- 220: illegal request parameter.\n- 221: Fare family is empty and not configured with lowest price fare family.\n- 223: The ratio of seat quotation requests to payment orders has exceeded the allowed threshold."},"msg":{"$ref":"#/components/schemas/ResponseMessage","nullable":true},"cabins":{"type":"array","items":{"type":"object","properties":{"segmentIndex":{"type":"integer","description":"The segment index to which the cabin belongs"},"cabin":{"properties":{"deck":{"type":"string","description":"Main deck or upper deck above that, which is found on some large aircraft.","enum":["Main","Upper deck"],"default":"Main","nullable":true},"cabinClass":{"$ref":"#/components/schemas/CabinClass","description":"Service grade of the fare","nullable":true},"cabinLayout":{"properties":{"columns":{"type":"array","items":{"properties":{"designator":{"type":"string","description":"A letter used to uniquely identify the seat position in the column.\n**Typical values:** A,B,C,D,E,F"},"characteristics":{"type":"string","description":"characteristics of column:\n-`A`: column by the aisle\n-`M`: middle column\n-`W`: column by the window","nullable":true}},"required":["designator"],"type":"object"},"description":"Contains columns and seat information for seat display purposes. Returns the characteristics for each column. Provided in the order from left to right."},"rows":{"properties":{"first":{"type":"integer","description":"First-row number Row starting row position for columns A,B,C,D,E,F"},"last":{"type":"integer","description":"Last row number Row ending row position for columns A,B,C,D,E,F"}},"required":["first","last"],"description":"Contains rows and seat information for seat display purposes Returns the starting end row position for each column","type":"object"},"exitRowPositions":{"type":"array","items":{"type":"object","properties":{"first":{"type":"integer","description":"Exit seat starting row position"},"last":{"type":"integer","description":"Exit seat ending row position"}},"required":["first","last"]},"description":"Return the position of exit rows, if applicable. The row number generally starts from 1 and increases from the front to the tail of the aircraft, that is, the seats close to the cockpit (nose) have the smallest row numbers, and the closer to the tail, the larger the row numbers.","nullable":true}},"required":["columns","rows"],"description":"Used to describe the seat layout of the cabin.","type":"object"},"rows":{"type":"array","items":{"properties":{"number":{"type":"integer","description":"Seat row number","minimum":1},"seats":{"type":"array","items":{"type":"object","properties":{"column":{"type":"string","description":"The column where the seat is located"},"seatStatus":{"type":"string","description":"A flag used to indicate whether a seat is free or occupied.\n- F: Free\n- O: Occupied","enum":["F","O"]},"seatCharacteristics":{"type":"array","items":{"type":"string"},"description":"A list contains seat characteristics, typical values(but not limited to):\n-`A`: Aisle seat\n-`E`: Exit and emergency exit\n-`I`: Seat suitable for adult with an infant\n-`IE`: Seat not suitable for child\n-`L`: Leg space seat\n-`U`: Seat suitable for unaccompanied minors\n-`V`: Seat to be left vacant or offered last\n-`W`: Window seat\n\nFor more information, please refer to: [EDIFACT Standards for Seat Characteristics (9825)](https://support.travelport.com/webhelp/GWS/Content/XML_Select_Web_Service/Codes/edifact_standards_for_seating.htm).","nullable":true},"price":{"type":"number","description":"The total price of the seat, including taxes"},"currency":{"type":"string","description":"Currency of the price."},"vendorPrice":{"type":"number","description":"The total price in vendor's currency of the seat, including taxes","nullable":true},"vendorCurrency":{"type":"string","description":"Vendor's currency","nullable":true},"productCode":{"type":"string","description":"A code used to uniquely identify this seat, which needs to be used when submitting a seat selection request."},"displayCurrency":{"type":"number","description":"Display currency","nullable":true},"displayPrice":{"type":"number","description":"The total price in display currency of the seat, including taxes","nullable":true}},"required":["column","seatStatus","price","currency","productCode"]},"description":"A list of seats that make up this row"}},"required":["number","seats"],"type":"object"},"description":"A list of rows in this cabin. A cabin row has one or more seats."}},"required":["cabinLayout","rows"],"description":"An object used to describe the seat layout within a cabin.","type":"object"}},"required":["segmentIndex","cabin"]},"description":"An array containing all cabins and the seat layouts within them.","nullable":true}},"required":["status"]}}},"headers":{}}}}}},"components":{"schemas":{"SeatMapFlight":{"type":"object","properties":{"segmentIndex":{"type":"integer","description":"This is the segment number, which starts from 1 and increments in the order of takeoff of each segment.","minimum":1},"flightNumber":{"type":"string","description":"Marketing flight number(with airline code prefix)."},"depAirport":{"type":"string","description":"3-letter iata code for the airport at which the segment is scheduled to depart."},"arrAirport":{"type":"string","description":"3-letter iata code for the arrival airport at which the segment is scheduled to arrive."},"depTime":{"type":"string","description":"The datetime at which the segment is scheduled to depart, in the departure airport timezone. The format is`YYYYMMDD`."},"cabinClass":{"$ref":"#/components/schemas/CabinClass","description":"Cabin class.\n- 1: economy\n- 2: business\n- 3: first\n- 4: premium economy"}},"required":["flightNumber","segmentIndex","depAirport","arrAirport","cabinClass","depTime"]},"CabinClass":{"type":"integer","enum":[1,2,3,4],"title":""},"SeatAvailabilityResponseStatus":{"type":"integer","enum":[214,215,216,217,218,219,220,221,223]},"ResponseMessage":{"type":"string","description":"It serves as an additional description of the response result. Especially when the interface reports an error (`status` !=`0`), it is usually a human-readable error message. Note: Do not use this field in any programming scenarios. For example, do not judge whether the interface responds successfully based on this field. Instead, you should only determine it by checking whether the status is equal to`0`at any time."}}}}
```
