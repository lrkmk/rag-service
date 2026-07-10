# 沙箱验证测试工具包

使用此页面在开发开始前验证您的沙箱设置。

此检查不需要任何自定义代码。

它确认您的凭证和网络可以完成核心预订流程。

当您需要以下内容时，从这里开始：

* 在编写集成代码之前验证沙箱访问
* 快速确认凭证和网络可达性
* 在环境更改后重新运行快速健康检查

### 常见问题

#### 何时应该运行测试工具包？

一旦沙箱凭证可用就立即运行。

在每次网络、IP 或环境更改后再次运行。

#### 通过的结果证明什么？

它证明在当前设置下，沙箱快乐路径可以运行。

它不能证明完全的生产就绪性或完整的边缘情况覆盖。

### 此检查的目标

将此测试工具包作为开发前的"通过/不通过"检查。

它帮助您在实施开始前发现访问和环境问题。

### 此工具验证的内容

测试工具包在沙箱中运行标准的快乐路径。

| 步骤   | 检查内容           |
| ---- | -------------- |
| `搜索` | 您的凭证有效，且返回航班结果 |
| `校验` | 价格确认有效，且创建了会话  |
| `下单` | 订单可以成功创建       |
| `支付` | 支付被接受          |

如果所有四个步骤都通过，您的沙箱环境已准备好进行集成工作。

### 此工具不验证的内容

此测试工具包 **不** 验证：

* 完整的 Webhook 处理
* 边缘情况或失败路径覆盖
* 生产定价或真实航司行为

将其用作快速入门检查，而不是完整的集成证明。

### 何时使用

运行此测试：

* 在您收到沙箱凭证后
* 在您开始编码之前
* 在网络或 IP 更改后
* 当您想要快速的环境健康检查时

### 下载测试工具包

使用以下文件：

* `Atlas_UAT_HappyPath.postman_collection.json`

{% file src="/files/a6bJ47SKAiO1VPSKYCqH" %}

* `Atlas_UAT_Environment.json`

{% file src="/files/kvUdumBofaVz3y7L7HMr" %}

将两个文件下载到同一个本地文件夹。

### 运行前准备

确保您已具备：

* 有效的沙箱凭证
* 到 Atlas 沙箱的出站网络访问
* 在本地运行 Newman 的能力
* 测试请求的未来旅行日期

### 如何运行

{% stepper %}
{% step %}

### 填写环境文件

打开 `Atlas_UAT_Environment.json`。

设置：

* `client_id`
* `client_secret`
* `currency`
* `from_date`

对于首次集成，Atlas 可能尚未配置结算货币。

将 `currency` 设置为 `USD` 用于沙箱测试，除非您的测试用例需要其他值。

在运行集合之前将 `from_date` 更新为未来的日期。
{% endstep %}

{% step %}

### 安装 Newman

安装 Newman 和 HTML 报告器。

{% code title="安装 Newman" %}

```bash
npm install -g newman newman-reporter-htmlextra
```

{% endcode %}
{% endstep %}

{% step %}

### 运行集合

使用环境文件运行快乐路径集合。

{% code title="运行测试工具包" %}

```bash
newman run Atlas_UAT_HappyPath.postman_collection.json -e Atlas_UAT_Environment.json --delay-request 10000 --reporters htmlextra --reporter-htmlextra-export report.html
```

{% endcode %}

如果命令失败，改用 `npx` 运行。

{% code title="使用 npx 的备用命令" %}

```bash
npx newman run Atlas_UAT_HappyPath.postman_collection.json -e Atlas_UAT_Environment.json --delay-request 10000 --reporters htmlextra --reporter-htmlextra-export report.html
```

{% endcode %}
{% endstep %}

{% step %}

### 查看结果

运行完成后打开 `report.html`。

预计运行时间约为 2 到 3 分钟。
{% endstep %}
{% endstepper %}

### 预期结果

当以下条件满足时，您的沙箱设置已准备就绪：

* `搜索` 通过
* `校验` 通过
* `下单` 通过
* `支付` 通过

您可以将其视为沙箱启动信号。

这些检查通过后，继续 API 集成。

### 通过和失败标准

当四个核心步骤成功时，视为运行通过：

* `搜索`
* `校验`
* `下单`
* `支付`

当这四个步骤中的任何一个失败时，视为运行失败。

### 已知行为

最终的检索步骤在轮询出票时可能会超时。

这是预期的行为。

出票是异步的。

最终检索步骤的超时不会影响沙箱环境验证。

{% hint style="info" %}
专注于四个核心步骤：`搜索`、`校验`、`下单` 和 `支付`。

最终的检索轮询步骤仅供参考。
{% endhint %}

### 常见失败原因

如果运行早期失败，首先检查以下项目：

* `client_id` 或 `client_secret` 缺失或错误
* 选择了错误的环境文件
* 出站网络访问被阻止
* 请求源 IP 在白名单设置后发生更改
* 集合或环境文件名在本地被更改
* Newman 已安装但报告器包缺失

#### 快速检查

使用以下顺序：

1. 确认环境文件中的凭证
2. 确认沙箱端点值
3. 确认您的网络可以访问 Atlas
4. 重新运行集合，不要编辑请求顺序
5. 打开 `report.html` 并检查第一个失败的请求

{% hint style="warning" %}
如果 `搜索` 失败，请先修复凭证或网络。

在快乐路径通过之前，不要继续集成工作。
{% endhint %}

### 如果运行失败

使用此恢复顺序：

1. 确认 `client_id` 和 `client_secret` 正确。
2. 确认 `from_date` 仍在未来。
3. 确认选择的环境文件是沙箱文件。
4. 确认您的网络和源 IP 可以访问 Atlas。
5. 重新运行集合并在 `report.html` 中检查第一个失败的请求。

### 此检查的产出

* 已验证的沙箱凭证
* 已验证的网络可达性
* 已确认的快乐路径执行基线

### 通过后做什么

测试工具包通过后：

* 开始 API 集成
* 保留相同的沙箱凭证用于开发
* 继续 [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)

### 相关页面

* [快速入门](/api-wen-dang/readme-1/quick-start.md)
* [沙箱访问](/api-wen-dang/readme-1/making-requests.md)
* [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)
* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)
