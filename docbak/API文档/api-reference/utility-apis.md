# 工具 API

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

{% hint style="warning" %}
本网站中的 API 参考端点示例均使用 **沙箱** 基础 URL。

生产流量请使用 ATRIP 中 **My Profile** → **Company Information** 显示的生产 API 基础 URL。

生产环境使用 **两个** API 基础 URL：

* 一个用于 `search` 流量
* 一个用于其他所有交易类 API

不要将生产流量发送到沙箱端点。
{% endhint %}

使用工具 API 完成集成后的运营、财务和数据操作。

这些端点不属于核心预订交易流程。

### 常见问题

#### 如何查询账户余额？

使用[余额](/api-wen-dang/api-reference/utility-apis/balance.md)端点获取余额信息。

将结果用于财务核对和运营检查。

#### 如何获取航线或订单相关数据？

使用[航线导出](/api-wen-dang/api-reference/utility-apis/route-export.md)获取航线数据。

使用[邮件查询](/api-wen-dang/api-reference/utility-apis/email-query.md)检索关联邮件记录。

### 按任务选择端点

* [余额](/api-wen-dang/api-reference/utility-apis/balance.md) — 查询账户余额。
* [航线导出](/api-wen-dang/api-reference/utility-apis/route-export.md) — 导出航线数据。
* [邮件查询](/api-wen-dang/api-reference/utility-apis/email-query.md) — 查询订单关联邮件。
* [ATRIP 令牌](/api-wen-dang/api-reference/utility-apis/atrip-token.md) — 生成下游流程所需令牌。
