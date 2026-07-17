# 快速入门

{% hint style="info" %}
💬 **需要帮助？** 如果遇到问题，请在帮助中心咨询 Eva，快速获取诊断建议。

<a href="https://www.atriptech.com/" class="button primary" data-icon="comments">咨询 Eva</a>
{% endhint %}

使用本指南从 Atlas 沙箱访问逐步推进到正式上线。

{% hint style="warning" %}
首次接入时，Atlas 中可能尚未配置结算币种。

在沙箱环境下，在账户设置完成前，请在 `Search` 请求中手动添加 `"currency":"USD"`。
{% endhint %}

如果您需要可导入的助手来获取工作流指导和故障排除，请使用 [Atlas AI 助手技能](/api-wen-dang/readme-1/integration-tools/atlas-ai-assistant-skill.md)。

{% hint style="warning" %}
所有 API 参考的端点示例均使用沙箱基础 URL。

当您迁移到生产环境时，请在 ATRIP 中 `我的资料` → `公司信息` 下获取生产 API 基础 URL。

生产环境为 `搜索` 使用一个基础 URL，为所有其他交易 API 使用另一个基础 URL。
{% endhint %}

<figure><img src="/files/dZ0h03mqkdgE3C8Fv8GC" alt=""><figcaption><p>从沙箱访问到上线的端到端集成流程</p></figcaption></figure>

当您需要以下内容时，从这里开始：

* 了解完整的 Atlas API 集成路径
* 了解进入下一阶段前需要完成什么
* 找到沙箱、UAT 或上线工作的正确页面

### 常见问题

#### 如何开始 Atlas API 集成？

从获取沙箱凭证和请求基础开始。

然后在沙箱中构建完整的预订流程，完成 UAT，并在获得批准和环境切换后进入生产环境。

#### 何时应该进入下一阶段？

仅当当前阶段稳定时再向前推进。

每个阶段都应产生下一个阶段所依赖的明确输出。

### 本指南的目标

使用本页面在实施开始前了解完整的集成路径。

用它来决定下一步应打开哪个页面以及必须先完成什么。

### 集成流程

{% stepper %}
{% step %}

### 沙箱访问

生成沙箱凭证并确认请求基础。
{% endstep %}

{% step %}

### 沙箱开发

在沙箱中构建并验证完整的集成。
{% endstep %}

{% step %}

### UAT 验证

沙箱开发稳定后完成所需的 UAT 流程。
{% endstep %}

{% step %}

### 生产上线

UAT 通过且您的账户切换为 `LIVE` 后，生成生产凭证并切换至生产端点进行上线。
{% endstep %}
{% endstepper %}

### 每个阶段的含义

#### 沙箱访问

获取沙箱凭证，确认请求头，并验证基本的请求处理。

#### 沙箱开发

在沙箱中构建并测试预订流程、支付路径、订单查询和 Webhook 处理。

#### UAT 验证

完成所需的 UAT 验证并获得生产就绪批准。

#### 生产上线

生成生产凭证，切换端点，运行冒烟测试，并监控首批生产流量。

### 完整流程说明

#### 1. 沙箱访问

这是集成的起点。

在 ATRIP 中生成您的沙箱客户端 ID 和客户端密钥。

在继续之前，确认：

* 标准请求头
* 请求格式
* 标识符处理
* gzip 处理

当沙箱请求可以成功发送时，您就可以进入下一阶段了。

使用 [沙箱访问](/api-wen-dang/readme-1/making-requests.md) 进行此设置。

#### 2. 沙箱开发

使用沙箱完成实际的集成工作。

此阶段通常包括：

* 沙箱环境设置
* 搜索、校验、下单和支付
* 订单查询和出票跟进
* Webhook 注册和事件处理
* 沙箱测试数据和故障模拟

目标不仅仅是成功调用 API。

目标是在沙箱中完成端到端的业务流程。

在开发过程中使用以下页面：

* [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)
* [MCP 辅助开发](/api-wen-dang/readme-1/integration-tools/mcp-assisted-development.md)
* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [Webhook 概述](/api-wen-dang/product-guides/extensions-and-integrations/webhook-overview.md)

在此阶段，请保留以下标识符以备后续步骤使用：

* 搜索：`routingIdentifier`
* 校验：`sessionId`
* 下单：`orderNo`

仅在沙箱流程稳定且可重复后，再进入 UAT 阶段。

#### 3. UAT 验证

UAT 是上线前的验证阶段。

使用此阶段来证明您的集成已为上线做好准备。

在 ATRIP 的 **UAT 测试** 中运行 UAT。

选择所需的功能范围，务必完成 **机票预订**。

然后点击 **确认并继续**，填写用例订单详情，并使用 **提交验证** 进行自动验证。

此阶段的主要输出是 UAT 批准。

使用 [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md) 了解验证步骤。

#### 4. 生产上线

当沙箱工作完成且您准备好进入生产环境时，开始此阶段。

然后：

* 完成所需的 UAT 工作
* 等待您的客户经理将账户切换为 `LIVE`
* 生成生产凭证
* 替换沙箱端点
* 运行受控的冒烟测试
* 监控首批生产订单和 Webhook
* 在生产环境中上线

至此完成从测试集成到生产运营的迁移。

使用 [生产上线](/api-wen-dang/readme-1/production-go-live.md) 获取上线检查清单。

### 在预订流程中应保留什么？

在整个主流程中保留以下标识符：

* `routingIdentifier`
* `sessionId`
* `orderNo`

如果您使用 Get Offer 路径，请使用 `OfferId` 代替 `sessionId`。

### 每个阶段的产出

* 沙箱访问 → 沙箱客户端 ID 和客户端密钥
* 沙箱开发 → 稳定的沙箱预订和 Webhook 流程
* UAT 验证 → 批准的验证结果
* 生产上线 → 生产就绪环境

### 何时进入下一阶段

使用以下退出检查：

* 当经过身份验证的沙箱请求可靠工作时，即可通过沙箱访问阶段。
* 当完整的沙箱流程稳定且可重复时，即可通过沙箱开发阶段。
* 当所需范围获得批准时，即可通过 UAT 验证阶段。
* 当生产冒烟测试通过且首批生产流量已监控时，即可通过生产上线阶段。

### 推荐的起始路径

1. 使用 [沙箱访问](/api-wen-dang/readme-1/making-requests.md) 获取凭证并确认请求基础。
2. 运行 [沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md) 进行快速的无代码健康检查。
3. 使用 [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md) 实现完整流程。
4. 沙箱流程稳定后进入 [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)。
5. 最后完成 [生产上线](/api-wen-dang/readme-1/production-go-live.md)。

如果您在实施过程中需要工作流查询、端点发现或故障排除的可选帮助，请使用 [集成工具](/api-wen-dang/readme-1/integration-tools.md)。

### 首次端到端测试资源

如果您想先进行无代码环境检查，请使用 [沙箱验证测试工具包](/api-wen-dang/readme-1/sandbox-development/sandbox-validation-test-kit.md)。

然后在沙箱开发过程中使用此 Postman 集合：

{% file src="/files/Hxsk2y9vLwn4uU8dvFHq" %}

### 下一步

如果您是全新开始，请继续 [沙箱访问](/api-wen-dang/readme-1/making-requests.md)。

如果沙箱访问已经完成，请继续 [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)。

### 相关页面

* [沙箱访问](/api-wen-dang/readme-1/making-requests.md)
* [沙箱开发](/api-wen-dang/readme-1/sandbox-development.md)
* [UAT 验证](/api-wen-dang/readme-1/uat-submission-guide.md)
* [生产上线](/api-wen-dang/readme-1/production-go-live.md)
