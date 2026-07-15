# Atlas API 文档 — 本地归档

来源：https://resources.atriptech.com/api-wen-dang

结构与英文版一致，只是路径前缀不同。共 123 篇文档，4 个一级分类。这是开发者/API集成文档，跟 [../帮助中心/](../帮助中心/README.md)（面向客服/运营场景的政策与操作说明）是两套不同性质的文档，分开存放、分开建库——检索时先判断问题是业务政策类还是技术集成类，再决定查哪一套。

## 集成指南

- [UAT 验证](01-集成指南/UAT 验证.md)
- [快速入门](01-集成指南/快速入门.md)
- [沙箱开发](01-集成指南/沙箱开发.md)
- [沙箱访问](01-集成指南/沙箱访问.md)
- [生产环境上线](01-集成指南/生产环境上线.md)

### sandbox-development

- [沙箱验证测试工具包](01-集成指南/sandbox-development/沙箱验证测试工具包.md)

### 集成工具

- [集成工具](01-集成指南/02-集成工具/集成工具.md)

#### integration-tools

- [Atlas AI 助手技能](01-集成指南/02-集成工具/integration-tools/Atlas AI 助手技能.md)
- [MCP 辅助开发](01-集成指南/02-集成工具/integration-tools/MCP 辅助开发.md)

## 产品指南

- [扩展与集成](03-产品指南/扩展与集成.md)
- [预订](03-产品指南/预订.md)
- [预订后服务](03-产品指南/预订后服务.md)

### booking

- [可选附加服务](03-产品指南/booking/可选附加服务.md)
- [预订概述](03-产品指南/booking/预订概述.md)
- [预订步骤指南](03-产品指南/booking/预订步骤指南.md)
- [预订流程](03-产品指南/booking/预订流程.md)

#### booking-flows

- [履约流程](03-产品指南/booking/booking-flows/履约流程.md)
- [标准预订流程](03-产品指南/booking/booking-flows/标准预订流程.md)
- [获取报价流程](03-产品指南/booking/booking-flows/获取报价流程.md)

#### booking-overview

- [API 请求限制](03-产品指南/booking/booking-overview/API 请求限制.md)
- [标识符](03-产品指南/booking/booking-overview/标识符.md)
- [预订决策](03-产品指南/booking/booking-overview/预订决策.md)

##### booking-decisions

- [搜索 vs 报价](03-产品指南/booking/booking-overview/booking-decisions/搜索 vs 报价.md)
- [获取报价 vs 获取报价价格](03-产品指南/booking/booking-overview/booking-decisions/获取报价 vs 获取报价价格.md)
- [重启点](03-产品指南/booking/booking-overview/booking-decisions/重启点.md)
- [验证 vs 下单](03-产品指南/booking/booking-overview/booking-decisions/验证 vs 下单.md)

#### booking-step-guides

- [创建订单](03-产品指南/booking/booking-step-guides/创建订单.md)
- [搜索](03-产品指南/booking/booking-step-guides/搜索.md)
- [支付与出票](03-产品指南/booking/booking-step-guides/支付与出票.md)
- [查询订单](03-产品指南/booking/booking-step-guides/查询订单.md)
- [确认订单（仅 FR）](03-产品指南/booking/booking-step-guides/确认订单（仅 FR）.md)
- [获取报价](03-产品指南/booking/booking-step-guides/获取报价.md)
- [获取报价价格](03-产品指南/booking/booking-step-guides/获取报价价格.md)
- [验证](03-产品指南/booking/booking-step-guides/验证.md)

##### payment-and-ticketing

- [混合支付指南](03-产品指南/booking/booking-step-guides/payment-and-ticketing/混合支付指南.md)

##### query-order

- [支付后轮询](03-产品指南/booking/booking-step-guides/query-order/支付后轮询.md)

#### optional-ancillaries

- [座位](03-产品指南/booking/optional-ancillaries/座位.md)
- [行李](03-产品指南/booking/optional-ancillaries/行李.md)
- [行李与座位产品代码时效性](03-产品指南/booking/optional-ancillaries/行李与座位产品代码时效性.md)

##### seats-and-baggage

- [座位回退模式](03-产品指南/booking/optional-ancillaries/seats-and-baggage/座位回退模式.md)

### extensions-and-integrations

- [Webhook 概述](03-产品指南/extensions-and-integrations/Webhook 概述.md)
- [多渠道通知](03-产品指南/extensions-and-integrations/多渠道通知.md)
- [特殊集成](03-产品指南/extensions-and-integrations/特殊集成.md)
- [航班数据源](03-产品指南/extensions-and-integrations/航班数据源.md)

#### special-integrations

- [FR 集成](03-产品指南/extensions-and-integrations/special-integrations/FR 集成.md)
- [常驻价格集成](03-产品指南/extensions-and-integrations/special-integrations/常驻价格集成.md)

#### webhook-overview

- [事件查询](03-产品指南/extensions-and-integrations/webhook-overview/事件查询.md)
- [事件通知](03-产品指南/extensions-and-integrations/webhook-overview/事件通知.md)
- [作废通知](03-产品指南/extensions-and-integrations/webhook-overview/作废通知.md)
- [出票完成通知](03-产品指南/extensions-and-integrations/webhook-overview/出票完成通知.md)
- [航变通知](03-产品指南/extensions-and-integrations/webhook-overview/航变通知.md)
- [航司状态更新通知](03-产品指南/extensions-and-integrations/webhook-overview/航司状态更新通知.md)
- [邮件通知](03-产品指南/extensions-and-integrations/webhook-overview/邮件通知.md)

### post-booking

- [PNR 认领与提取](03-产品指南/post-booking/PNR 认领与提取.md)
- [作废](03-产品指南/post-booking/作废.md)
- [出票后附加服务](03-产品指南/post-booking/出票后附加服务.md)
- [订单维护](03-产品指南/post-booking/订单维护.md)
- [退款](03-产品指南/post-booking/退款.md)

## API参考

- [Webhook 与事件 API](04-API参考/Webhook 与事件 API.md)
- [工具 API](04-API参考/工具 API.md)
- [预订 API](04-API参考/预订 API.md)
- [预订后 API](04-API参考/预订后 API.md)

### booking-apis

- [创建订单](04-API参考/booking-apis/创建订单.md)
- [座位](04-API参考/booking-apis/座位.md)
- [搜索](04-API参考/booking-apis/搜索.md)
- [支付与出票](04-API参考/booking-apis/支付与出票.md)
- [智能搜索](04-API参考/booking-apis/智能搜索.md)
- [查询订单](04-API参考/booking-apis/查询订单.md)
- [比价搜索](04-API参考/booking-apis/比价搜索.md)
- [确认订单](04-API参考/booking-apis/确认订单.md)
- [获取报价](04-API参考/booking-apis/获取报价.md)
- [获取报价价格](04-API参考/booking-apis/获取报价价格.md)
- [行李](04-API参考/booking-apis/行李.md)
- [验证](04-API参考/booking-apis/验证.md)

### post-booking-apis

- [PNR 认领](04-API参考/post-booking-apis/PNR 认领.md)
- [作废](04-API参考/post-booking-apis/作废.md)
- [停止出票](04-API参考/post-booking-apis/停止出票.md)
- [出票后附加服务](04-API参考/post-booking-apis/出票后附加服务.md)
- [提取 PNR](04-API参考/post-booking-apis/提取 PNR.md)
- [订单列表](04-API参考/post-booking-apis/订单列表.md)
- [退款](04-API参考/post-booking-apis/退款.md)
- [重新生成订单](04-API参考/post-booking-apis/重新生成订单.md)

### utility-apis

- [ATRIP 令牌](04-API参考/utility-apis/ATRIP 令牌.md)
- [余额](04-API参考/utility-apis/余额.md)
- [航线导出](04-API参考/utility-apis/航线导出.md)
- [邮件查询](04-API参考/utility-apis/邮件查询.md)

### webhook-and-incident-apis

- [Webhook 注册与事件](04-API参考/webhook-and-incident-apis/Webhook 注册与事件.md)

## 支持与参考

- [参考数据与沙箱](05-支持与参考/参考数据与沙箱.md)
- [故障排除与支持](05-支持与参考/故障排除与支持.md)
- [运营工具](05-支持与参考/运营工具.md)

### errors-handing

- [202 vs 301 vs 308](05-支持与参考/errors-handing/202 vs 301 vs 308.md)
- [205 vs 299 vs 304](05-支持与参考/errors-handing/205 vs 299 vs 304.md)
- [307 vs 327 vs 410](05-支持与参考/errors-handing/307 vs 327 vs 410.md)
- [309 vs 409](05-支持与参考/errors-handing/309 vs 409.md)
- [318 vs 608 重复预订](05-支持与参考/errors-handing/318 vs 608 重复预订.md)
- [401 vs 402 vs 404](05-支持与参考/errors-handing/401 vs 402 vs 404.md)
- [402 vs 404 vs 406 vs 615](05-支持与参考/errors-handing/402 vs 404 vs 406 vs 615.md)
- [429 vs 110](05-支持与参考/errors-handing/429 vs 110.md)
- [搜索错误](05-支持与参考/errors-handing/搜索错误.md)
- [支付错误](05-支持与参考/errors-handing/支付错误.md)
- [退款、查询与预订后错误](05-支持与参考/errors-handing/退款、查询与预订后错误.md)
- [通用与访问错误](05-支持与参考/errors-handing/通用与访问错误.md)
- [错误码](05-支持与参考/errors-handing/错误码.md)
- [验证、订单与出票错误](05-支持与参考/errors-handing/验证、订单与出票错误.md)

### integration-reference

- [参考数据](05-支持与参考/integration-reference/参考数据.md)
- [沙箱测试数据](05-支持与参考/integration-reference/沙箱测试数据.md)

#### reference-data

- [区域设置参考](05-支持与参考/integration-reference/reference-data/区域设置参考.md)

#### sandbox-test-data

- [沙箱测试卡号](05-支持与参考/integration-reference/sandbox-test-data/沙箱测试卡号.md)
- [沙箱测试航线](05-支持与参考/integration-reference/sandbox-test-data/沙箱测试航线.md)

### troubleshooting-faqs

- [Atlas API 常见问题](05-支持与参考/troubleshooting-faqs/Atlas API 常见问题.md)
- [入门指南](05-支持与参考/troubleshooting-faqs/入门指南.md)
- [合作伙伴常见问题](05-支持与参考/troubleshooting-faqs/合作伙伴常见问题.md)
- [启动检查清单](05-支持与参考/troubleshooting-faqs/启动检查清单.md)
- [搜索与预订](05-支持与参考/troubleshooting-faqs/搜索与预订.md)
- [支付](05-支持与参考/troubleshooting-faqs/支付.md)
- [订单与出票](05-支持与参考/troubleshooting-faqs/订单与出票.md)
- [财务](05-支持与参考/troubleshooting-faqs/财务.md)
- [集成前](05-支持与参考/troubleshooting-faqs/集成前.md)
- [预订后服务](05-支持与参考/troubleshooting-faqs/预订后服务.md)

### utility-api-overview

- [ATRIP 令牌](05-支持与参考/utility-api-overview/ATRIP 令牌.md)
- [余额](05-支持与参考/utility-api-overview/余额.md)
- [航线导出](05-支持与参考/utility-api-overview/航线导出.md)
- [邮件查询](05-支持与参考/utility-api-overview/邮件查询.md)

