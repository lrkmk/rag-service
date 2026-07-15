# 欢迎来到Atlas帮助中心

> 在Atlas帮助中心，您可以获得关于常见问题的帮助！

## 热门分类

<table data-view="cards" data-full-width="false"><thead><tr><th align="center" valign="middle"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td align="center" valign="middle"><a href="/pages/iMVwyUPvJYtzngYUYJpV"><strong>ATRIP</strong></a></td><td><a href="/files/FOvul1DoOYrggsHRSvlc">/files/FOvul1DoOYrggsHRSvlc</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/jczEvPqWKsy8FCVKwKE9"><strong>售前票务</strong></a></td><td><a href="/files/9jIryZWcKyL6eK8jnHdK">/files/9jIryZWcKyL6eK8jnHdK</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/tbHU3U7t6lANa2BnKe01"><strong>支付</strong></a></td><td><a href="/files/VIB8YAZxP1lXSivlB91Z">/files/VIB8YAZxP1lXSivlB91Z</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/coONo5mxJ3SYWlDm2NKS"><strong>售后服务</strong></a></td><td><a href="/files/90eis317GcK9wgpzg6J5">/files/90eis317GcK9wgpzg6J5</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/btQLdlQUTL6rRa41ClQp"><strong>财务</strong></a></td><td><a href="/files/Bk9EfhAG81mbjzvQcmFc">/files/Bk9EfhAG81mbjzvQcmFc</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/wZDsRy1uMFhvfs04rien"><strong>账单管理</strong></a></td><td><a href="/files/kPLGIq6cqpL2XUl5EoDR">/files/kPLGIq6cqpL2XUl5EoDR</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/s9V8CY9V6mVtSQDvCvuF"><strong>通知提醒</strong></a></td><td><a href="/files/6bR9YW64Sub3243Uv9gv">/files/6bR9YW64Sub3243Uv9gv</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/VcvtYTZtyeslO1pMF2lm"><strong>安全与合规</strong></a></td><td><a href="/files/LON7tsNwsUCM1nn7THF1">/files/LON7tsNwsUCM1nn7THF1</a></td></tr><tr><td align="center" valign="middle"><a href="/pages/n7l93ADTcwq5nhINswAs"><strong>Atlas功能</strong></a></td><td><a href="/files/UqEQSCMRciRLaFwlsDfo">/files/UqEQSCMRciRLaFwlsDfo</a></td></tr></tbody></table>

***

## 常见问题

<details>

<summary>如何查询“管理我的订单”的邮箱地址？</summary>

您可以通过API响应和Atrip Flight Deck平台进行查询：

* 在API响应的返回字段：“airlineBookings→mmbEmail”中查询；&#x20;
* 登录Atrip Flight Deck，进入“管理订单→MMB登录邮箱”模块查询。&#x20;

</details>

<details>

<summary>如何查询为特定预订创建的凭证？</summary>

您可以通过API响应和Atrip Flight Deck平台进行查询：

* 在API响应的返回字段：“airlineBookings→extras”中查询；
* 登录Atrip Flight Deck，进入“管理订单→ 额外信息”模块。点击“View”按钮查看详情。&#x20;

</details>

<details>

<summary>如何查询日本航空公司（如HD、7G）的确认编号（除PNR外）？</summary>

您可以通过API响应和Atrip Flight Deck平台进行查询：

* 在API响应的返回字段：“airlineBookings→extras”中查询；&#x20;
* 登录Atrip Flight Deck，进入“管理订单→ 额外信息”模块。点击“View”按钮查看详情。  &#x20;

</details>

<details>

<summary>如何获取航班变更通知？</summary>

1. **航空公司通知：**&#x822A;空公司通常会将航班变更通知发送至联系邮箱，请定期检查您的收件箱；
2. **Atlas通知**：&#x20;

* 如果您使用的是Atlas邮箱，Atlas将在收到航空公司的航班变更邮件后通过Webhook发送航班变更通知；
* 登录Atrip Flight Deck，在事件管理（Incident Management）模块下的“航班变更（Schedule Change）— 邮箱通知（Email Notification）”类别里查看；&#x20;

3. **监控通知：**&#x41;tlas会在航班起飞前监测航班状态，一旦监测到航班时间变更，我们将：&#x20;

* 通过Webhook发送API通知。&#x20;
* 登录Atrip Flight Deck，在事件管理（Incident Management）模块下的“航班变更（Schedule Change）— API通知（API notification）”类别里查看； &#x20;

&#x20;

</details>

<details>

<summary>我如何确认PNR是否有航班变更？</summary>

1. **航空公司通知：**&#x822A;空公司通常会将航班变更通知发送至联系邮箱，请定期检查您的收件箱；
2. **Atlas邮件服务：**&#x5982;果您使用的是Atlas邮箱，可以在订单详情里的邮件列表（Email List ）模块中查收邮件；
3. **航空公司官网：**&#x5982;果没有收到变更邮件，请登录航空公司官方网站，进入“ 订单管理(MMB)”页面查看航班动态：

* 如果显示有航班时间变更，那就确认变更已经发生；
* 如果未显示任何变更，请检查即将起飞的航班状态；

4. **航班状态**： 对于临近起飞的航班，您可以在航空公司官网的“航班状态”模块查看：

* 如果航班状态显示为“已取消”或“起飞时间已更改”，说明发生了航班变更；
* 如果航班状态”正常“且起飞时间未更改，则未发生航班变更；&#x20;

5. **联系航空公司：**&#x5982;果仍然无法确定航班状态，建议您联系航空公司客服中心或在线客服。

&#x20;

</details>

#### [<mark style="color:blue;">**查看更多常见问题**</mark>](/bang-zhu-zhong-xin/chang-jian-wen-ti/gong-neng-he-nei-rong-xiang-guan.md) <mark style="color:blue;">**→**</mark>

***

## 无法寻找到您需要的内容？

<table data-card-size="large" data-view="cards"><thead><tr><th data-type="content-ref"></th><th></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td><a href="/pages/IaDTDoLMsngWctpgtJfE">/pages/IaDTDoLMsngWctpgtJfE</a></td><td>联系我们的支持团队获取更多帮助</td><td><a href="/files/fvWg1E5OsRfhNQLXNGsv">/files/fvWg1E5OsRfhNQLXNGsv</a></td></tr></tbody></table>
