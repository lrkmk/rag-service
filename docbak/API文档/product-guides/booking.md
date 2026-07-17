# 预订

使用此部分获取 Atlas API 预订指导。

当您需要以下内容时从这里开始：

* 了解完整的预订领域
* 选择正确的预订流程
* 详细了解某一预订步骤
* 安全地添加可选座位或行李

### 主要预订部分

* [预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)
* [预订流程](/api-wen-dang/product-guides/booking/booking-flows.md)
* [预订步骤](/api-wen-dang/product-guides/booking/booking-step-guides.md)
* [可选附加服务](/api-wen-dang/product-guides/booking/optional-ancillaries.md)

### 常见问题

#### Atlas API 的标准预订流程是什么？

标准流程为 `search.do` → `verify.do` → `order.do` → `pay.do` → `queryOrderDetails.do`。

在最终出票确认前，持续调用 `queryOrderDetails.do`。

查看[标准预订](/api-wen-dang/product-guides/booking/booking-flows/standard-booking-flow.md)了解完整顺序。

#### 应从哪种预订路径开始？

Atlas 是主要搜索入口时，使用标准搜索路径。

已知目标行程时，使用获取报价路径。

需要更广报价范围且能立即支付时，使用履约路径。

使用[预订决策](/api-wen-dang/product-guides/booking/booking-overview/booking-decisions.md)选择正确路径。

#### 座位和行李应在何时添加？

座位和行李属于可选附加服务。

在支付前添加，并仅使用有效的 `sessionId` 或 `OfferId`。

使用[可选附加服务](/api-wen-dang/product-guides/booking/optional-ancillaries.md)确认支持的流程和时效规则。

### 后续步骤

选择路径后，打开[预订概述](/api-wen-dang/product-guides/booking/booking-overview.md)确认标识符、时效和请求限制。
