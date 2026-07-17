# Atlas Pay

Atlas Pay 是 Atlas 的支付解决方案。

它帮助你在出票速度、支付成功率和资金管理之间取得平衡。

### 这页适合谁

* 需要选择默认支付方式的产品和运营团队
* 需要处理支付失败补救链路的客服和技术团队
* 需要对账和管理多币种资金的财务或结算团队

### 支持的支付方式

#### 预存款支付

预先充值账户余额，再通过余额完成支付。

适合追求稳定性和出票速度的场景。

主要特点：

* 支付路径更稳定
* 出票速度更快
* 账务和对账更清晰
* 适合高价值或时效敏感订单

#### VCC 透传支付

使用你提供的虚拟信用卡，直接向航司支付。

适合保留自有支付渠道、返点体系和财务管理方式的场景。

主要特点：

* 保留自有资金沉淀
* 支持按航司策略灵活支付
* 便于结合卡组织权益和财务对账

#### 混合支付重试

当 VCC 失败时，可切换至预存款继续完成支付。

适合挽回订单，降低取消率。

### 如何选择支付方式

#### 优先考虑预存款

适合这些场景：

* 追求更高支付成功率
* 追求更快出票
* 对稳定性要求高

#### 优先考虑 VCC

适合这些场景：

* 需要保留自有支付链路
* 需要使用客户自有卡产品
* 需要更灵活的资金管理

#### 同时启用两种方式

适合既要灵活性，也要兜底能力的团队。

推荐将 VCC 作为首选支付，再用预存款做失败兜底。

### 多币种能力

Atlas Pay 支持多币种账户和灵活结算。

支持的币种包括 `AED`、`AUD`、`CAD`、`CNH`、`DKK`、`EUR`、`GBP`、`HKD`、`IDR`、`ILS`、`JPY`、`MXN`、`NOK`、`NZD`、`PLN`、`RON`、`SEK`、`SGD`、`THB`、`USD`、`ZAR` 等。

{% hint style="info" %}
`THB` 仅可使用花旗银行进行充值。
{% endhint %}

最新支持情况，请以平台配置和账户能力为准。

### 支持范围

Atlas Pay 可覆盖大量低成本航空公司的支付场景。

最新支持航司列表，请查看：

[航司支持列表](https://www.atriptech.com/#/airline/list)

### 支付失败后的处理方式

#### 在 ATRIP 中处理

{% stepper %}
{% step %}

### 找到原订单

进入 **ATRIP → 我的订单**，定位支付失败的订单。
{% endstep %}

{% step %}

### 重新生单

如果原订单因航司支付失败被取消，先重新生成新订单。
{% endstep %}

{% step %}

### 切换支付方式

对新订单改用预存款支付，完成后续出票。
{% endstep %}
{% endstepper %}

#### 通过 API 处理

**场景 A：`pay.do` 调用失败**

如果订单尚未成功支付，可以直接重试，或改用余额支付。

```json
{
  "orderNo": "XXX",
  "supportCreditTransPayment": null,
  "creditCard": null
}
```

**场景 B：`pay.do` 成功，但航司侧支付失败**

这种情况下，系统可能自动取消原订单，并通过 Webhook 返回取消原因。

典型处理链路：

`取消订单 → 重新生单 → 改用余额支付`

重新生成订单：

```json
{
  "originalOrderNo": "{original order no}"
}
```

使用新订单改用余额支付：

```json
{
  "orderNo": "{new order no}",
  "supportCreditTransPayment": null,
  "creditCard": null
}
```

### 使用建议

* 上线前完整测试成功、失败和重试路径
* 对 `pay.do`、取消和重新生单做幂等保护
* 结合履约能力和航司表现选择默认支付方式
* 对账时结合订单状态和实际出票结果判断最终结果

### 继续阅读

* [支付解决方案](/chan-pin-jie-shao/atlas-chan-pin-jie-shao/zhi-fu-jie-jue-fang-an.md)
* [数据解决方案](/chan-pin-jie-shao/atlas-chan-pin-jie-shao/shu-ju-jie-jue-fang-an.md)
* [履约与售后](/chan-pin-jie-shao/atlas-chan-pin-jie-shao/l-yue-yu-shou-hou.md)

需要更完整的产品上下文，请参阅 [支付解决方案](/chan-pin-jie-shao/atlas-chan-pin-jie-shao/zhi-fu-jie-jue-fang-an.md)。
