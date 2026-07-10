# 混合支付指南

### **ATLAS 混合支付解决方案**

Atlas混合支付解决方案是一套创新系统，支持您在需要重试预订时使用不同的支付方式。目前我们提供两种支付方式（预存款和VCC透传），如果VCC透传支付失败，客户可以选择使用预存款模式来重试预订，确保更顺畅且可靠的支付流程。借助Atlas混合支付解决方案，即使遇到支付挑战，我们也为您提供无缝且无忧的体验。

以下是如何在ATRIP上使用不同支付方式重试失败的VCC透传订单的方法：

#### **通过ATRIP界面操作：**

1.登录 ATRIP Flight Deck，进入「我的订单」并找到对应订单。

2.使用「重新生单」功能，快速创建与原订单信息完全一致的新订单。

3.订单生成后，在对应的 ATRIP 页面点击「支付」按钮，即可通过预付款完成支付。

详细操作方法可点击查看：[如何重新生单？](/bang-zhu-zhong-xin/re-men-fen-lei/shou-qian-piao-wu/ru-he-chong-xin-sheng-dan.md)

<figure><img src="/files/pl5MmOaj1NsNG7bYbM4z" alt=""><figcaption></figcaption></figure>

#### **通过API操作：**

**场景A：**&#x41;tlas支付（pay.do）失败无论失败原因是什么，只要订单未成功支付，客户可以采取以下行动：

1. 重试

或者

2. 切换到预付款支付或换卡支付

![](/files/TC6C8IQLJSprU79mc9GD)

**场景B：**&#x41;tlas支付（pay.do）成功，但航空公司支付失败。

取消订单 → 重新生成订单 → 使用预付款支付或换卡支付

* 如果由于卡片问题无法完成支付，系统将自动取消订单，并通过Webhooks通知客户取消原因，通知内容如下：

![](/files/sq3SlOrlwxufcUnd1pHl)

客户随后可以采取以下行动：

1. 重新生成订单（regenerateOrder.do）：

![](/files/bVhKYHrzmYrwvPdI0Ds5)

2. 使用预付款支付或换卡支付 (pay.do)：

![](/files/3acpMJCRuO1EKkbHWpRO)
