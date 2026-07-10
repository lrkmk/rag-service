# 多币种指南

1. **什么是多币种账户？**

我们现在为客户推出多币种账户功能，客户可以为每笔交易指定所需的结算货币。这项创新服务提供了几个关键优势：

以前，如果客户需要进行多种货币的交易，他们必须在Atlas开设多个账户，每种货币一个账户。而且，同一个电子邮件地址不能用于不同的账户。现在的更新是，只需一个账户就能处理多种货币，并且通过一个单一的API实现多币种选项。

* 灵活性与控制：客户可以根据市场情况和财务策略选择每笔交易的首选货币
* 成本效益的解决方案：Atlas提供多个国家的银行账户，使得支付更加快捷且具成本效益

2. **支持的货币**

阿联酋迪拉姆（AED）、澳大利亚元（AUD）、加拿大元（CAD）、英镑（GBP）、印度尼西亚盾（IDR）、墨西哥比索（MXN）、新西兰元（NZD）、离岸人民币（CNH）、丹麦克朗（DKK）、欧元（EUR）、港元（HKD）、新加坡元（SGD）、美元（USD）、瑞士法郎（CHF）、捷克克朗（CZK）、匈牙利福林（HUF）、以色列新谢克尔（ILS）、日元（JPY）、挪威克朗（NOK）、波兰兹罗提（PLN）、罗马尼亚列伊（RON）、瑞典克朗（SEK）、南非兰特（ZAR）、泰铢（THB\*）

**\*THB仅可使用花旗银行进行充值**

如何使用：请与您的客户经理联系，获取您希望存款的货币的银行账户信息，客户经理将为您在系统内设置相应货币。

**ATRIP**

允许客户在充值的时候指定充值币种，当切换充值币种后，会动态展示该币种对应的余额， 充值记录中提供充值货币筛选

![](/files/9UYEXRJCNQ9Qpcv8AdDz)

![](/files/mwyMmCB25T0kvOwwGwnA)

**Transaction Records**

页面增加币种筛选，帮助更快定位交易明细

![](/files/YZFeURtIZTd3smPR4Cab)

**Invoice Management**

发票管理中增加币种筛选，帮助准确定位需要下载的发票

![](/files/S2q2vJDNyvXZ4jwAqTkJ)

**Invoice and Reconciliation Statements**

发票周期内会生成多个币种的发票和账单

合同中的交易费用和出票后费用将转换为结算货币，并体现在发票和对账单中。

结算货币：人民币（CNY）

![](/files/E0orkFEFgQnxDKQbANMf)

![](/files/UgZGEjgVuZyG01wjv03O)

![](/files/sQmWR4UnofdZaXvEGm2k)

**结算币种：美金**

<figure><img src="/files/iN6VLjUbpaASSB8t688c" alt=""><figcaption></figcaption></figure>

![](/files/NrRhaF8lD6Fxh7aiUbyG)

![](/files/zZJZ5XgdaWOJyKp916yg)

**Emails**

**Invoices and Statements**

**发票邮件中，多个币种的账单邮件分开发送**

![](/files/T6EMFqtLQXKjcTy5Omvt)

![](/files/OcIPHy4iP8ZFFo5QHejQ)

**余额不足的告警邮件：特定币种对应的账户余额达到告警阈值时：邮件通知客户**

![](/files/UPZcAsr9Ahn9QtXt0t3t)

**API 更新**

**Search Request**

```
{
"tripType": "2",
"adultNum": 1,
"childNum": 0,
"infantNum": 0,
"fromCity": "KRK",
"toCity": "LTN",
"fromDate": "20240326",
"retDate": "20240423",
"airlines": ["W6"],
"currency": "GBP",
"displayCurrency": "PHP",
"requestSource": "Organic"
}
```

“currency” 不是必须的，默认情况下，系统将以客户设置的首个币种作为默认的报价和结算币种。

客户可以通过currency这个字段指定币种报价、出票、结算，客户需要在一开始询价（搜索）的时候指定币种

验价、生单、支付等其他接口的请求参数都没有变化，对应的响应内容里，相关的结算金额将以客户指定的币种展示。

* 技术服务费的转换

技术服务费用被转换为“结算货币”
