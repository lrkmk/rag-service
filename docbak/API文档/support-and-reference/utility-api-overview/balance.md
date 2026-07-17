# 余额

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用本页查询当前账户余额。

### 主要 API

* `balance.do`

### 何时使用

* 在支付前做财务检查
* 对账余额
* 确认余额不足相关问题

### 关键入参

请传入：

* `currency`

使用您要查询的余额账户对应的结算币种。

### 响应会返回什么

响应通常包括：

* 账户余额金额
* 结算币种

### 最佳实践

* 在高频支付前先查询余额
* 确认币种账户正确
* 将返回金额仅用于运营检查
* 以响应中的 `status` 作为成功判断依据

### 注意事项

* 余额按币种区分
* 余额不足可能阻塞 Deposit 支付
* `msg` 仅作说明，不应作为程序判断依据

### 完整 API 参考

完整端点结构和示例请查看：

[余额](/api-wen-dang/api-reference/utility-apis/balance.md)
