# 入门指南

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用本页面了解商业、接入、性能和支持基础知识。

当你需要以下内容时，从这里开始：

* 确认如何获取沙箱访问权限
* 在开发前了解 Atlas 支持什么
* 查找有关定价、性能和升级的基本指南

### 常见问题

#### 如何开始使用 Atlas API？

首先确认商业适配性、NDA 步骤和沙箱访问权限。

然后生成沙箱凭证，运行首次测试，并仅在端到端流程稳定后进入 UAT。

### 我们可以通过 Atlas 销售哪些航空公司的机票？

Atlas 连接 150 多家航空公司。\
您可以在[航空公司列表](https://www.atriptech.com/#/airline/list)和 ATRIP 中查看当前列表。

#### 签约前可以测试吗？

是的。

提交[入门表单](https://atlaslovestravel.com/get-started/)。

Atlas 将审核您的公司，完成 NDA 步骤，然后发放测试凭证。

### 签约前可以测试吗？

是的。提交[入门表单](https://atlaslovestravel.com/get-started/)。\
Atlas 将审核您的公司，完成 NDA 步骤，然后发放测试凭证。

#### 在哪里获取沙箱凭证？

在 ATRIP 的 `Profile` -> `My Profile` -> `Company Information` 下生成。

在每个沙箱调用中使用 `x-atlas-client-id` 和 `x-atlas-client-secret`。

### 在哪里获取沙箱凭证？

在 ATRIP 的 `Profile` -> `My Profile` -> `Company Information` 下生成。\
在每个沙箱调用中使用 `x-atlas-client-id` 和 `x-atlas-client-secret`。

#### 是否有用于首次测试的 Postman 集合？

是的。

使用[快速入门](/api-wen-dang/readme-1/quick-start.md)中的 Postman 集合。

当您准备进行正式验证时，稍后使用 UAT 指南。

### 是否有用于首次测试的 Postman 集合？

是的。\
使用[快速入门](/api-wen-dang/readme-1/quick-start.md)中的 Postman 集合。

当您准备进行正式验证时，使用 UAT 指南。

#### 如何开始 UAT？

仅在沙箱流程端到端稳定后开始 UAT。

在 ATRIP 中打开 **UAT Testing**，选择所需的功能范围，并至少完成**航班预订**。

然后点击 **Confirm and Continue**，填写案例订单详情，使用 **Submit Verification** 进行自动验证。

### 如何开始 UAT？

仅在沙箱流程端到端稳定后开始 UAT。\
在 ATRIP 中打开 **UAT Testing**，选择所需的功能范围，并至少完成**航班预订**。

然后点击 **Confirm and Continue**，填写案例订单详情，使用 **Submit Verification** 进行自动验证。

### 航空公司的功能总是相同的吗？

不。功能取决于每家航空公司支持的内容。\
Atlas 按航空公司和流程公开支持的功能。

### Atlas 如何定价？

定价取决于市场、货币和商业条款。\
使用[联系表单](https://atlaslovestravel.com/contact/)获取当地定价详情。

#### 我们应该预期什么样的性能？

典型响应时间因 API 和航空公司条件而异。

将下面的超时和响应时间指南作为运营预期，而非每个请求的硬性保证。

### Atlas 是否支持促销票价或促销代码？

支持一般的促销票价。\
促销代码支持正在规划中，但尚未普遍可用。

### L2B 比率是什么？

查看率与预订率在您的商业协议中定义。

### Atlas 是否使用缓存？

是的。Atlas 为搜索流量使用共享缓存池。\
也可以支持客户特定缓存。

### API 失败时应该怎么做？

使用支持渠道获取即时帮助。\
Atlas 还计划提供一个用于预订、出票和预订后操作的回退门户。

### Atlas 是否提供票价保证？

是的，在**存款**模式下完成支付后。\
出票通常在 10 分钟内完成。\
极少数情况下可能需要长达 1 小时。

票价保证**不**适用于 VCC 直通支付。

### 标准的超时限制是多少？

* `search.do`：不固定
* `realTimeSearch.do`：`120s`
* `verify.do`：`15s`
* `order.do`：正常预订 `15s`，实时预订 `120s`
* `pay.do`：不固定

### 典型的响应时间是多少？

* `search.do`：98% 的响应在 `500ms` 以下
* `verify.do`：95% 的响应约 `8s`
* `order.do`：95% 的响应约 `14s`
* `pay.do`：95% 的响应约 `2s`

#### 如何升级未解决的问题？

通过 **<customerfeedback@atlaslovestravel.com>** 升级未解决的服务问题。

Atlas 可能首先要求您在 ATRIP 中打开或引用一个服务请求。

### 如何升级未解决的问题？

升级可以发送至 **<customerfeedback@atlaslovestravel.com>**。

用于与以下相关的未解决服务问题：

* 机票订单
* 预订后操作
* 退款

Atlas 可能首先要求您在 ATRIP 中打开或引用一个服务请求。
