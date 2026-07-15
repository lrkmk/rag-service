# 常驻价格集成

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要为符合条件的西班牙国内预订提供居民票价支持时使用此页面。

### 何时使用此流程

仅在以下情况下使用居民票价流程：

* 乘客符合西班牙居民或家庭折扣计划的资格
* 航线为支持的西班牙国内航线
* 您能够在预订时收集所需的证明字段
* 航司支持居民票价处理

### 支持的航司

* `FR`
* `VY`

### 符合条件的乘客群体

此流程适用于以下地区的合法居民：

* 加那利群岛
* 巴利阿里群岛
* 休达
* 梅利利亚

需要提供居民身份证明，例如 `DNI` 或 `NIE`，具体取决于票价类型。

### 符合条件的航线

仅西班牙国内航线符合条件，且行程必须符合居民计划规则。

| 居民区域   | 允许的航线范围                       | 示例          |
| ------ | ----------------------------- | ----------- |
| 加那利群岛  | 西班牙任何机场 ↔ 加那利群岛任何机场           | `MAD → TFS` |
| 巴利阿里群岛 | 西班牙任何机场 ↔ 巴利阿里群岛任何机场          | `VLC → PMI` |
| 休达     | `JCU` ↔ `SVQ` / `XRY` / `AGP` | `JCU → AGP` |

### 折扣适用范围

居民定价可适用于：

* 基础运价
* 每位乘客每航段的第一件行李
* 婴儿费用
* 强制性座位选择费

政府税费**不**享受折扣。

### 折扣代码

在搜索请求中使用 `residentCode`。

| 折扣类型         | 居民代码   | 折扣    |
| ------------ | ------ | ----- |
| 家庭折扣         | `DSC2` | `5%`  |
| 大家庭折扣        | `DSC3` | `10%` |
| SARA 居民折扣    | `DSC1` | `75%` |
| SARA + 家庭折扣  | `DSC4` | `80%` |
| SARA + 大家庭折扣 | `DSC5` | `85%` |

### 集成流程

{% stepper %}
{% step %}

### 使用 `residentCode` 搜索

在搜索请求中传递 `residentCode` 以获取居民定价。

如果航线和旅客符合条件，搜索结果中将应用折扣价格。
{% endstep %}

{% step %}

### 验价并创建订单

通过验价和订单创建继续常规预订流程。

如果原始搜索使用了 `residentCode`，居民票价逻辑将在后续步骤中继续生效。
{% endstep %}

{% step %}

### 在预订或出票流程中发送 `residentInfo`

为每位相关乘客传递居民证明字段。
{% endstep %}

{% step %}

### 航司执行最终验证

航司在出票后检查居民资格。
{% endstep %}
{% endstepper %}

### 搜索请求示例

```json
{
  "tripType": "1",
  "adultNum": 1,
  "childNum": 0,
  "infantNum": 0,
  "fromCity": "SVQ",
  "toCity": "OVD",
  "fromDate": "20251103",
  "retDate": "20250603",
  "includeMultipleFareFamily": true,
  "currency": "",
  "requestSource": "",
  "residentCode": "DSC2"
}
```

### 必需的乘客证明字段

为每位符合条件的乘客传递 `residentInfo`。

| 字段                | 说明                               |
| ----------------- | -------------------------------- |
| `docType`         | 证件类型。支持的值包括 `D`、`E` 和 `U`        |
| `docNum`          | 当 `docType` 为 `D` 或 `E` 时必填      |
| `municipality`    | `DSC1`、`DSC4` 和 `DSC5` 必填        |
| `largeFamilyCert` | `DSC2`、`DSC3`、`DSC4` 和 `DSC5` 必填 |
| `community`       | `DSC2`、`DSC3`、`DSC4` 和 `DSC5` 必填 |

### 预订请求示例

```json
{
  "cid": "******",
  "sessionId": "5475cdb2-ce22-4e52-8c2f-8ef2e81e462c",
  "passengers": [
    {
      "name": "TEST/ONE",
      "passengerType": 0,
      "birthday": "19900101",
      "gender": "M",
      "cardNum": "00000000",
      "cardType": "PP",
      "cardIssuePlace": "SG",
      "cardExpired": "20301231",
      "nationality": "SG",
      "ancillaries": [],
      "residentInfo": {
        "docType": "D",
        "docNum": "99999999Z",
        "municipality": "",
        "largeFamilyCert": "06-9999-99",
        "community": "502973"
      }
    }
  ],
  "contact": {
    "name": "TEST/TEST",
    "address": null,
    "postcode": null,
    "email": "test@test.com",
    "mobile": "0086-13928109091"
  },
  "requestSource": ""
}
```

### 按折扣代码的字段要求

| 居民代码   | `docType` | `docNum`                    | `municipality` | `largeFamilyCert` | `community` |
| ------ | --------- | --------------------------- | -------------- | ----------------- | ----------- |
| `DSC2` | 必填        | 当 `docType` 为 `D` 或 `E` 时必填 | 非必填            | 必填                | 必填          |
| `DSC3` | 必填        | 当 `docType` 为 `D` 或 `E` 时必填 | 非必填            | 必填                | 必填          |
| `DSC1` | 必填        | 当 `docType` 为 `D` 或 `E` 时必填 | 必填             | 非必填               | 非必填         |
| `DSC4` | 必填        | 当 `docType` 为 `D` 或 `E` 时必填 | 必填             | 必填                | 必填          |
| `DSC5` | 必填        | 当 `docType` 为 `D` 或 `E` 时必填 | 必填             | 必填                | 必填          |

### 编码字段的参考文件

使用以下文件将名称映射为编码值。

#### 市镇代码

市镇代码为 6 位数字，由 `CPOR + CMUN + DC` 组成。

{% file src="/files/FTAwlwvZNW1pTZVdiw51" %}

#### 社区代码

{% file src="/files/P4YaS4RNy6icas3re3XF" %}

### 最终验证行为

Atlas 在履约过程中将居民票价详情传递给航司。

航司在出票后验证资格。\
如果验证失败：

* 预订不会自动取消
* 旅客可能会被要求在机场出示证明

请确保旅客准备好所需的原始证件。

### 相关页面

* [搜索](/api-wen-dang/product-guides/booking/booking-step-guides/search.md)
* [创建订单](/api-wen-dang/product-guides/booking/booking-step-guides/create-order.md)
* [支付与出票](/api-wen-dang/product-guides/booking/booking-step-guides/payment-and-ticketing.md)
* [特殊集成](/api-wen-dang/product-guides/extensions-and-integrations/special-integrations.md)
