# Invoice管理

## **一、功能概述**

在 ATRIP 系统中，您可以通过【Invoice管理】模块统一查看、管理所有发票及账单报表，并根据业务需求灵活配置发票接收规则，实现高效对账与财务管理。

## **二、操作信息**

操作权限： Admin

操作路径：ATRIP -> 财务管理 -> Invoice管理

<figure><img src="/files/UFJ6LZgKChxOc4KtBedS" alt=""><figcaption></figcaption></figure>

## **三、发票配置说明**

点击【配置规则】后，将打开侧边滑窗，您可以根据实际需求进行如下设置：

<figure><img src="/files/rI9qO1GU7EAINQ6E6SJw" alt=""><figcaption></figcaption></figure>

## **四、账单字段说明**

### **1.账单核心字段**

| 字段                        | 说明                                                                                               | 样例                      |
| ------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------- |
| Order Type                | <p>订单类型： </p><p>Regular=出票 </p><p>Refund=退票 </p>                                                 | Regular                 |
| Airline                   | 航司二字码；若为往返航班，多个航司二字码以英文逗号分隔                                                                      | 6E,6E                   |
| Ticketed Time             | <p>支付时间（出票订单）/退款时间（退票订单） <br>时区：GMT+8 </p>                                                       | 2026/3/11 23:48         |
| Passenger Name            | 乘客姓名                                                                                             | TEST/TEST               |
| Ticket Number             | 票号                                                                                               | UBLUWP                  |
| Fare Price                | 票价                                                                                               | 341.07                  |
| Tax                       | 税费                                                                                               | 55.38                   |
| Total Fare                | 总价格                                                                                              | 396.45                  |
| Service Fee               | 技术服务费（出票）/退票服务费（退票）                                                                              | 6.88                    |
| CCY                       | 币种                                                                                               | CNY                     |
| Payment Method            | <p>支付方式： </p><p>balance payment：预存款支付 </p><p>credit card：信用卡 </p><p>paid in B2B account：托管付 </p> | balance payment         |
| Booking Number            | Atlas订单号                                                                                         | TESTA20260224174117189  |
| First Flight Date         | 第一程起飞日期                                                                                          | 20260412                |
| Second Flight Date        | 第二程起飞日期                                                                                          | 20260412                |
| Third Flight Date         | 第三程起飞日期                                                                                          | 20260412                |
| Fourth Flight Date        | 第四程起飞日期                                                                                          | 20260412                |
| First Flight Number       | 第一程航班号                                                                                           | 7C302                   |
| Second Flight Number      | 第二程航班号                                                                                           | 7C302                   |
| Third Flight Number       | 第三程航班号                                                                                           | 7C302                   |
| Fourth Flight Number      | 第四程航班号                                                                                           | 7C302                   |
| Trip Type                 | <p>行程类型： </p><p>OW=单程 </p><p>RT=往返 </p>                                                          | OW                      |
| Routing                   | 出发 - 到达城市                                                                                        | CJU-KWJ                 |
| Trip                      | 出发 - 到达机场                                                                                        | CJU-SEL                 |
| Airline PNR               | 航司订座记录编号（PNR）                                                                                    | YFPGJN                  |
| Ancillary Type & Name     | 附加服务类型及名称                                                                                        | SP\_SCI\_BAG\_1PC\_23KG |
| Ancillary Category        | 附加服务分类                                                                                           | StandardCheckInBaggage  |
| Ancillary Purchase Method | 附加服务搭售方式                                                                                         | Bundle                  |
| Billing Date              | 账单日期（GMT+8）                                                                                      | 2026-03-11              |

**重要说明**&#x20;

1）部分字段可能为空，属正常现象；&#x20;

2）本账单核心体现预存款金额变动：&#x20;

* 非“预存款支付（balance payment）” 场景下，票价、税费仅作参考，实际金额以信用卡账单或航司账单为准；&#x20;
* 非“预存款支付（balance payment）” 场景下，账户余额仅扣减出票 / 退票对应的技术服务费。&#x20;

3）账单中所有日期、时间类字段，均以 GMT+8 时区为准。&#x20;

### **2.账单汇总字段**

| 字段                                   | 说明                                                                                                                          | 样例                                 |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Agency Transaction Period（GMT+8）     | <p>账单周期 </p><p>时区说明：GMT+8 </p>                                                                                              | 2026/03/09-2026/03/11              |
| Agency Name                          | 客户名称                                                                                                                        | TEST Client                        |
| Agency Currency                      | 账单币种                                                                                                                        | CNY                                |
| Tax Invoice No.                      | 发票编号                                                                                                                        | TAX-INVOICE-202603TEST0011CNY-0005 |
| Credit Note No.                      | 贷项通知书编号                                                                                                                     | CREDIT-NOTE-202603TEST0011CNY-1005 |
| Agency Opening Balance               | 当期账单期初余额                                                                                                                    | 105                                |
| Usage                                | <p>当期账单支出总金额 </p><p>计算公式： Usage = Regular + Service Charge + Debit Note + Refund + Credit Note </p>                         | -195（=-180-20-30+30+5）             |
| <ul><li>Regular </li></ul>           | <p>出票金额总计 </p><p>说明：仅统计 “预存款支付” 方式的出票金额累计值 </p>                                                                             | -180                               |
| <ul><li>Service Charge </li></ul>    | <p>技术服务费总计 </p><p>说明：包含出票、退票对应的技术服务费 </p>                                                                                   | -20                                |
| <ul><li>Debit Note </li></ul>        | 补款金额总计                                                                                                                      | -30                                |
| <ul><li>Refund </li></ul>            | <p>退款金额总计 </p><p>说明：仅统计 “预存款支付” 方式的退款金额累计值  </p>                                                                            | 30                                 |
| <ul><li>Credit Note </li></ul>       | 赔款金额总计                                                                                                                      | 5                                  |
| Payment Received                     | 当期账单收入总金额                                                                                                                   | 300                                |
| <ul><li>TOP-UP </li></ul>            | <p>充值金额总计 </p><p>说明：充值为收入项之一，可能存在多行数据；若当期无调账，则该字段无数据 </p>                                                                   | 300                                |
| Adjustment Amount                    | 当期账单调账总金额                                                                                                                   | 50                                 |
| <ul><li>Commission Rebate </li></ul> | <p>返利金额总计 </p><p>说明：返利为调账项之一，可能存在多行数据；若当期无调账，该字段无数据 </p>                                                                    | 50                                 |
| Agency Closing Balance               | <p>当期账单期末余额 </p><p>计算公式：Agency Closing Balance = Agency Opening Balance + Usage + Payment received + Adjustment Amount </p> | 260（=105-195+300+50）               |
