# API 请求限制

{% hint style="info" %}
💬 **Need help?** If you're stuck, ask Eva in the Help Center for instant diagnostics.

<a href="https://resources.atriptech.com/?fallback=true" class="button primary" data-icon="comments">Ask Eva</a>
{% endhint %}

当您需要在一个位置查看请求限制规则时，使用此页面。

Atlas 对选定的预订前 API 应用请求限制治理。

超限请求返回 Atlas 错误代码 `429`。

### 受影响的 API

以下 API 受此策略约束：

* `search.do`
* `verify.do`
* `getOffers.do`
* `seatAvailability.do`
* `getLuggage.do`

以下 API 不受此策略约束：

* `order.do`
* `pay.do`

### 默认限制

#### 搜索资源

* `search.do` — `10 QPS`

Atlas 在滚动 1 秒窗口中计算搜索次数。

#### 履约资源

* `verify.do` + `getOffers.do` — 共享 `60 QPM`

Atlas 在滚动 60 秒窗口中计算履约次数。

#### 附加服务资源

* `seatAvailability.do` + `getLuggage.do` — 共享 `60 QPM`

Atlas 在滚动 60 秒窗口中计算附加服务次数。

### 共享池规则

`verify.do` 和 `getOffers.do` 共享一个履约池。

一个 API 的高流量会消耗另一个 API 的池。

`seatAvailability.do` 和 `getLuggage.do` 共享一个附加服务池。

一个 API 的高流量会消耗另一个 API 的池。

### 什么计入限制

以下请求会计入：

* 成功的请求
* 无结果的请求
* 业务失败和航司失败
* 缓存命中的响应

以下请求不计入：

* 已被请求限制治理拒绝的请求
* 认证失败
* 参数验证失败
* 权限或安全策略拒绝
* 幂等性阻止的重复请求（从未进入业务处理）

### `429` 响应

当请求超过当前限制时，Atlas 返回错误代码 `429`。

#### 响应示例

```json
{
  "code": 429,
  "message": "Rate limit exceeded. Please retry after the current window resets",
  "limitType": "SEARCH_QPS",
  "limit": 1,
  "retryAfter": 1
}
```

#### 字段含义

* `code` — 错误代码
* `message` — 错误摘要
* `limitType` — 当前限制桶
* `limit` — 当前配置的限制
* `retryAfter` — 重试前等待的秒数

### 如何处理 429

降低请求频率。

等待 `retryAfter` 后再重试。

不要立即并行重试。

尽可能使用缓存。

在到达 Atlas 之前合并重复请求。

### 按 API 的实践指导

#### 搜索

对重复的航线和日期查询使用本地缓存。

平滑每秒的突发流量。

#### 验证和获取报价

不要在紧密循环中重复检查同一行程。

在预订条件未改变时，重用新鲜的验证或报价上下文。

#### 座位和行李

除非预订上下文发生变化，否则不要重新查询附加服务。

在当前 `sessionId` 或 `OfferId` 仍然有效时重用它。

### 常见问题

#### `429` 是否意味着账户被封禁？

不是。

它仅表示当前请求频率超过了配置的限制。

#### 缓存命中的请求是否计入？

是的。

如果请求进入 Atlas 业务处理并返回结果，则会计入。

#### 可以请求更高的限制吗？

可以。

如果您的业务需要更高的吞吐量，请联系您的 Atlas 客户经理或业务团队。

### 相关页面

* [预订概述](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/82DaHlpWfsy0ANSplNI3)
* [错误代码](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/Jk40OgfAM5G1NDZxwAS1)
* [搜索](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/9K7uEnLGfEbpjGjni5gD)
* [获取报价](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/FSGess6buGE1P02WnVNu)
* [验证](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/Hg2lCO93wE6SPAXEYPOm)
* [座位](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/3ujCySdZ8OYYLfGI3iF3)
* [行李](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/Ftzqh42LAaE6QYzklv67)
