# 航班数据源

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

当您需要 Atlas 将运价数据投递到自有存储时使用此页面。

{% hint style="info" %}
当您的产品需要快速本地查询、批量定价数据或 AI 就绪的运价存储时，使用 `Flight Data Feed`。

当您的产品需要实时验价、预订、支付和出票时，使用 `Transaction API`。
{% endhint %}

当您需要以下内容时从这里开始：

* 构建本地航班存储以实现快速搜索和排序
* 在 Data Feed、Transaction API 或两者之间进行选择
* 了解何时批量运价投递比实时预订 API 更合适

### 常见问题

#### Flight Data Feed 会取代 Transaction API 吗？

不会。

使用 Data Feed 进行本地展示、比较和分析。

使用 Transaction API 进行实时验价、订单创建、支付和出票。

#### 何时应使用 Flight Data Feed？

当您的产品需要低延迟本地查询、批量运价存储或大规模运价检索以用于 AI、元搜索或打包流程时使用。

### 概览

* 投递模式：全量推送 + 增量推送
* 最短增量间隔：`2 分钟`
* 吞吐量：每小时可达 `5,000,000` 个航班
* 典型全量推送：约 `500k` 个航班，耗时 `7 分钟`
* 传输方式：`SFTP`
* 文件格式：`CSV`、`JSON`、`XML`

### 这是什么

`Atlas Flight Data Feed` 是 Atlas 航班基础设施的数据投递层。

它将全量数据集和增量更新推送到您的服务器。

使用它来构建本地航班知识库。

这不是预订 API。

它是对实时预订流程的补充。

### 在 Atlas 中的定位

* `Layer 1` — Data Feed，用于本地数据存储和快速检索
* `Layer 2` — Transaction API，用于实时验价、下单和支付
* `Layer 3` — Agentic Fulfillment，用于预订后自动化操作

### 选择合适的产品路径

{% tabs %}
{% tab title="使用 Data Feed" %}
当您需要以下内容时选择此路径：

* 本地运价存储
* 低延迟搜索和比较
* 批量分析或打包逻辑
* 基于结构化运价数据的 AI 检索
  {% endtab %}

{% tab title="使用 Transaction API" %}
当您需要以下内容时选择此路径：

* 实时价格确认
* 实时订单创建
* 支付和出票
* 预订状态跟进
  {% endtab %}

{% tab title="同时使用两者" %}
当您需要以下内容时选择此路径：

* 从自有数据库进行本地展示
* 降低搜索阶段的 API 压力
* 结算前进行实时验价
* 快速搜索配合实时预订完成
  {% endtab %}
  {% endtabs %}

### 核心能力

#### 全量和增量投递

Atlas 支持两种投递模式：

* 全量推送，用于首次设置或数据回填
* 增量推送，用于价格和可用性的变更
* 更新间隔短至 `2 分钟`

使用全量推送确保完整性。

使用增量推送确保时效性。

{% hint style="success" %}
这种模式为您同时提供覆盖率和时效性。

全量投递保障完整性。

增量投递保持本地价格最新。
{% endhint %}

#### 规模

当前投递容量支持：

* 每小时最多 `5,000,000` 个航班
* 每天约传输 `14.4 GB` 数据
* 支持 `10+` 个客户数据源并行

`500k` 个航班的典型全量推送约需 `7 分钟`。

#### 格式与映射

Atlas 可以投递：

* `CSV`、`JSON` 或 `XML`
* 自定义字段名称和字段顺序
* `GZ` 或 `ZIP` 压缩

#### 安全传输

Atlas 使用 `SFTP` 进行加密文件投递。

传输成功率超过 `99.9%`。

Atlas 可在传输完成后验证文件。

#### 可配置范围

您可以配置：

* 航司覆盖范围
* 航线或区域范围
* 全量和增量频率
* 格式、压缩和文件命名

### 您会收到什么

具体数据取决于您的配置。

典型字段包括：

* 航司、航班号、机场和旅行日期
* 基础运价、税费、手续费、总价和币种
* 舱位、票价系列和剩余座位数
* 成人、儿童和婴儿定价（如配置）
* 行李额度及规则摘要（如配置）
* 生成时间、有效性和时效性标记

<details>

<summary>这对产品和工程为什么重要</summary>

使用航班基本信息进行搜索和展示。

使用价格和舱位字段进行排序、筛选和打包。

使用时效性标记控制缓存逻辑和数据可信度。

</details>

### 典型投递流程

{% stepper %}
{% step %}

### 生成数据集

Atlas 构建全量数据集或增量差异数据。
{% endstep %}

{% step %}

### 转换文件

Atlas 应用目标格式、字段映射和压缩。
{% endstep %}

{% step %}

### 通过 SFTP 投递

Atlas 通过加密通道将文件推送到您的服务器。
{% endstep %}

{% step %}

### 加载到数据库

您的系统解析文件并更新本地存储。
{% endstep %}
{% endstepper %}

### 典型使用场景

{% tabs %}
{% tab title="AI 旅行助手" %}
将数据源用作本地航班知识库。

这支持快速检索和复杂推理，无需高频实时调用。
{% endtab %}

{% tab title="元搜索" %}
使用数据源实现广泛覆盖和快速结果展示。

增量投递在控制运行时查询成本的同时，保持缓存的高时效性。
{% endtab %}

{% tab title="动态打包" %}
使用数据源进行大规模本地组合定价。

这在需要预计算航班和酒店组合时效果尤佳。
{% endtab %}
{% endtabs %}

### 何时使用 Data Feed

当您需要以下内容时使用 Data Feed：

* 快速本地搜索和比较
* 大规模本地定价、打包和分析
* 基于结构化运价数据的 AI 检索

### Data Feed 和 Transaction API

使用 `Data Feed` 进行展示、比较和本地计算。

使用 `Transaction API` 进行验价、下单、支付和出票。

当您需要快速搜索和实时预订时，两者同时使用。

{% tabs %}
{% tab title="展示阶段" %}
使用 `Data Feed`。

从本地数据库读取数据。

这为您提供低延迟和较低的 API 依赖。
{% endtab %}

{% tab title="结算阶段" %}
使用 `Transaction API`。

在创建订单前验证最新的运价和库存。
{% endtab %}

{% tab title="最佳实践链路" %}
推荐顺序：

1. 从本地数据源搜索
2. 让用户选择行程
3. 实时验价
4. 创建订单
5. 支付和出票
   {% endtab %}
   {% endtabs %}

### 最佳适用对象

本产品适用于：

* AI 旅行助手和元搜索产品
* 动态打包和数据分析团队
* 希望快速展示并配合 Atlas 预订的 OTA

### 下一步是什么？

如果您在本地搜索后需要实时预订，请继续阅读 [预订概述](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/82DaHlpWfsy0ANSplNI3)。

如果您仍在评估接入和产品适配性，请使用 [快速开始](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/rHs9a1GaRY814fF0fIkT)。

### 集成选项

#### 标准配置

当标准格式足够时使用此路径。

典型配置需要 `1-3 天`。

您提供 SFTP 访问权限。

Atlas 配置数据源。

#### 自定义配置

当您需要自定义映射或规则时使用此路径。

典型配置约需 `2 周`。

Atlas 对齐字段、测试输出，然后切换到生产环境。

### 服务保障

Atlas `7x24` 小时监控数据质量和传输健康。

数据准确率超过 `99.9%`。

故障恢复目标低于 `30 分钟`。

### 常见问题

#### 这会取代 Transaction API 吗？

不会。

使用 Data Feed 进行本地数据访问。

使用 Transaction API 完成预订。

#### 数据有多新？

增量投递可每 `2 分钟` 运行一次。

端到端延迟保持在分钟级别。

#### 如果投递失败怎么办？

Atlas 自动重试临时性故障。

持续性故障会触发告警并跟进支持。

### 团队为何选择此模式

* 本地读取带来更快的搜索速度
* 降低展示阶段的 API 成本
* 更好地支持批量比较和排序
* 更适合 AI 和分析工作负载
* 展示与预订之间的职责分离更清晰

{% hint style="warning" %}
Data Feed 不是最终的预订数据权威来源。

在创建订单和支付前，请始终使用实时交易调用。
{% endhint %}

### 相关页面

* [预订概述](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/82DaHlpWfsy0ANSplNI3)
* [快速入门](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/MkEt9qjU24ig50fQ8be2)
* [快速开始](broken://spaces/6LsKtmbJhZxgxraY5mHB/pages/rHs9a1GaRY814fF0fIkT)
