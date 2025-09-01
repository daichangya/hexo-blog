---
title: 可能是CAP理论的最好解释
id: 1504
date: 2024-10-31 22:01:59
author: daichangya
permalink: /archives/%E5%8F%AF%E8%83%BD%E6%98%AFcap%E7%90%86%E8%AE%BA%E7%9A%84%E6%9C%80%E5%A5%BD%E8%A7%A3%E9%87%8A/
tags: 
 - 分布式
---

一篇非常[精彩的解释CAP理论的文章](http://ksat.me/a-plain-english-introduction-to-cap-theorem/)，翻译水平有限，不准确之处请参考原文，还请见谅。

**Chapter 1: “Remembrance Inc” Your new venture :**

Last night when your spouse appreciated you on remembering her birthday and bringing her a gift, a strange Idea strikes you. People are so bad in remembering things. And you’re sooo good at it. So why not start a venture that will put your talent to use? The more you think about it, the more you like it. In fact you even come up with a news paper ad which explains your idea

**第一章：记忆公司**

昨晚当你的妻子感激你记得她生日还给她买了礼物时，你突然冒出一个想法。人们的记性总是很糟而你又是如此善于记忆，所以为什么不利用你的天赋干出一番事业呢？你越想越觉得这个点子不错。事实上你甚至想出一份新闻广告来解释你的想法。

Remembrance Inc! - Never forget,  even without remembering!

   Ever felt bad that you forget so much?  Don't worry. Help is just a phone away!

    When you need to remember something, just call 555--55-REMEM and tell us what you need to remember. For eg., call us and let us know of your boss's phone number, and forget to remember it. when you need to know it back.. call back the same number\[(555)--55-REMEM \] and we'll tell you what's your boss's phone number.

   Charges : only $0.1 per request

记忆公司！ - 不用记忆，从不忘记

您是否曾为健忘而感到沮丧？不用担心，只需一通电话。当您需要记住什么时，拨打555-55，告诉我们您想记住的东西。例如，来电让我们知道您老板的电话号，然后忘了这事。当您想要知道已忘了的东西时，拨打同样的号码，我们将告诉您老板的电话号。费用：每次仅需0.1美元。

So, your typical phone conversation will look like this:

·Customer : Hey, Can you store my neighbor’s birthday?

·You: Sure.. when is it?

·Customer : 2nd of jan

·You: (write it down against the customer’s page in your paper note book )Stored. Call us any time for knowing your neighbor’s birthday again!

·Customer : Thank you!

·You: No problem! We charged your credit card with $0.1

所以您的通话通常是这样的：

Ø客户：嗨！能记一下我邻居的生日吗？

Ø你：当然可以，他生日是什么时候？

Ø客户：1月2日

Ø你：(在笔记本上该客户的那一页记下)记好了！想知道他生日时随时打给我们！

Ø客户：谢谢！

Ø不客气，您的信用卡将支付0.1美元。

## Chapter 2 : You scale up:

Your venture gets funded by YCombinator. Your Idea is so simple, needs nothing but a paper notebook and phone, yet so effective that it spreads like wild fire. You start getting hundreds of call every day.

And there starts the problem. You see that more and more of your customers have to wait in the queue to speak to you. Most of them even hang up tired of the waiting tone. Besides when you were sick the other day and could not come to work you lost a whole day of business. Not to mention all those dissatisfied customers who wanted information on that day.  
You decide it’s time for you to scale up and bring in your wife to help you.

**第二章：公司扩张**

你拿到了YC的投资。这个点子是如此简单，只需纸笔和电话，但却像燎原之火一样发展迅猛。你每天逐渐有上百个来电。但问题也随之而来。你发现越来越多的客户要排队等你应答。他们都受够了等待。而且当你生病没法工作时，你将损失一整天的生意，更不用说那些客户的不满。于是你决定：是时候把你的妻子拉过来帮忙了。

Your start with a simple plan:

1.You and your wife both get an extension phone

2.Customers still dial (555)–55-REMEM and need to remember only one number

3.A pbx will route the a customers call to whoever is free and equally

你的计划很简单：

1.你和你妻子都有分机号

2.客户还是拨打原来的号码

3.交换机将把客户来电发给你们俩空闲的那位。

## Chapter 3 : You have your first “Bad Service” :

Two days after you implemented the new system, you get a call from your trusted customer Jhon. This is how it goes:

·Jhon: Hey

·You: Glad you called “Remembrance Inc!”. What can I do for you?

·Jhon: Can you tell me when is my flight to New Delhi?

·You: Sure.. 1 sec sir  
(You look up your notebook)  
(wow! there is no entry for “flight date” in Jhon’s page)!!!!!

·You: Sir, I think there is a mistake. You never told us about your flight to delhi

·Jhon: What! I just called you guys yesterday!(cuts the call!)

**第三章：第一次Bad Service**

就在扩张后两天，你接到了老客户Jhon的来电：

ØJhon：嗨！

Ø你：感谢致电记忆公司，有什么可以帮您？

ØJhon：能告诉我第一次飞新德里的时间吗？

Ø你：当然可以，请稍等(你翻阅你的笔记本，在Jhon那页却没发现航班这一项)。

Ø先生，抱歉，我想您没有告诉过我们您去新德里的航班信息。

ØJhon：什么！？我昨天就打给过你们！(挂断了)

How did that happen? Could Jhon be lying? You think about it for a second and the reason hits you! Could Jhon’s call yesterday reached your wife? You go to your wife’s desk and check her notebook. Sure enough it’s there. You tell this to your wife and she realizes the problem too.

What a terrible flaw in your distributed design! **Your distributed system is not consistent! There could always be a chance that a customer updates something which goes to either you or your wife and when the next call from the customer is routed to another person there will not be a consistent reply from Remembrance Inc!**

怎么可能发生这种事？Jhon在说谎吗？你一下子想到了原因！可能Jhon昨天打给了你的妻子。于是你到她桌上检查她的笔记本。没错，就是这个原因。你告诉了你妻子，她也意识到了这个问题。多么糟糕的问题！**你的分布式系统不是一致性的！****客户打给你或你妻子，再来电时却是另一个人接的，你的记忆公司没法给出一个一致性的答复！**

## Chapter 4: You fix the Consistency problem:

Well, your competitors may ignore a bad service, but not you. You think all night in the bed when your wife is sleeping and come up with a beautiful plan in the morning. You wake up your wife and tell her:

” Darling this is what we are going to do from now”

·Whenever any one of us get a call for an update(when the customer wants us to remember something) before completing the call we tell the other person

·This way both of us note down any updates

·When there is call for search(When the customer wants information he has already stored) we don’t need to talk with the other person. Since both of us have the latest updated information in both of our note books we can just refer to it..

**第四章：修复一致性问题**

你的竞争者可能会忽视这个问题，你却不会。你妻子入睡时你想了一整晚，终于在清晨时想出了一个美丽的方案。你叫醒她说：

“亲爱的，这是我们从今往后要做的事：”

Ø不论我俩谁接到客户要求记东西的电话，打完电话前我们要告诉另一个人

Ø这样我俩都能记下任何的更新

Ø当客户要求查找时，我们不用互相问，因为我俩的笔记本上都记录了所有更新。

There is only one problem though, you say, and that is an “update” request has to involve both of us and we cannot work in parallel during that time. For eg. when you get an update request and telling me to update too, i cannot take other calls. But that’s okay because most calls we get anyway are “search” (a customer updates once and asks many times) . Besides, we cannot give wrong information at any cost.

“Neat” your wife says, “but there is one more flaw in this system that you haven’t thought of. What if one of us doesn’t report to work on a particular day? On that day, then, we won’t be able to take “any” Update calls, because the other person cannot be updated! We will have **Availability problem , i.e, for eg., if an update request comes to me I will never be able to complete that call because even though I have written the update in my note book, I can never update you. So I can never complete the call!”**

但是还是有一个问题，客户要求记东西的来电需要我们俩人同时处理，所以那段时间就没法并行工作了。例如，当你接到保存或更新请求时也会告诉我，于是我就不能接听其他来电了。但是因为多数来电都是查找的，所以也没什么大问题(客户更新一次然后查找多次)。而且，我们要不惜一切代价避免记错东西。

“很好！”你的妻子说“但是还有个问题你没想到。要是我俩中的一个哪天不能来工作呢？在那天我们就不能一起接受更新的来电了，因为另一个人不能记下这个更新。所以我们会有**可用性问题！例如，我接到更新来电时就没法完成这个请求，****因为即使我在我的本子上记下了，我也没法告诉你。所以我没法完成这个来电”**

## Chapter 5: You come up with the greatest solution Ever:

You being to realize a little bit on why distributed system might not be as easy as you thought at first. Is it that difficult to come up with a solution that could be both **“Consistent and Available”**? Could be difficult for others, but not for you!! Then next morning you come up with a solution that your competitors cannot think of in their dreams! You wake your wife up eagerly again..

” look” , you tell her.. “This is what we can do to be consistent and available” . The plan is mostly similar to what I told you yesterday:

·i) Whenever any one of us get a call for an update(when the customer wants us to remember something) before completing the call, if the other person is available we tell the other person. This way both of us note down any updates

·ii) But if the other person is not available(doesn’t report to work) we send the other person an email about the update.

·iii) The next day when the other person comes to work after taking a day off, He first goes through all the emails, updates his note book accordingly.. before taking his first call.

**第五章：最棒的解决方法**

你有点儿意识到了为什么分布式系统不像你一开始想的那样简单。想出一个既一致又可用的方案很难吗？对其他人也许很难，但对你则不是！第二天早上，你想出了一个你的竞争者们做梦都想不到的解决方法。你再一次急切地叫醒了你妻子。

“看！“你跟她说，”这就是我们既一致又可用的做法，方案与我昨天告诉你的很像“：

Ø不论我俩谁接到客户要求记东西的电话，打完电话前我们要告诉另一个人，这样我俩都能记下任何的更新。

Ø但是如果另一个人请假不在，我们给他发一封更新的邮件。

Ø第二天他来工作时，在处理任何来电前先看一遍这些邮件，更新到他的本子上。

Genius! You wife says! I can’t find any flaws in this systems. Let’s put it to use.. Remembrance Inc! is now both **Consistent and available!**

天才啊！你的妻子说。这个方案想不到任何的问题的。咱们就这样来吧！记忆公司现在**既是一致的又是可用的！**

## Chapter 6: Your wife gets angry :

Everything goes well for a while. Your system is consistent. Your system works well even when one of you doesn’t report to work. But what if Both of you report to work and one of you doesn’t update the other person? Remember all those days you’ve been waking your wife up early with your Greatest-idea-ever-bullshit? * What if your wife decides to take calls but is too angry with you and decides not to update you for a day? Your idea totally breaks! Your idea so far is good for consistency and availability but is not Partition Tolerant!*  
You can decide to be partition tolerant by deciding not to take any calls until you patch up with your wife.. Then your system will not be “available” during that time…

**第六章：妻子的愤怒**

一切都很顺利。你的系统是一致的，当你俩中的一人不能工作时也能运行良好。但是假如你们都来工作了，但是却没把更新告诉另一个人呢？想想你吵醒你妻子，说你那些所谓的伟大的点子。**要是哪天她接电话却很生气而不告诉你去更新呢？**你的方法完全毁了。到目前为止，你的方法是一致而可用的，但却不是**分区容忍的。****你可以在与你妻子和好前不接听任何来电，于是你的系统在那段时间又是不可用的了…**

## Chapter 7: Conclusion :

So Let’s look at CAP Theorem now. Its states that, when you are designing a distributed system you can get cannot achieve all three of Consistency, Availability and Partition tolerance. You can pick only two of:

·Consistency: You customers, once they have updated information with you, will always get the most updated information when they call subsequently. No matter how quickly they call back

·Availability: Remembrance Inc will always be available for calls until any one of you(you or your wife) report to work.

·Partition Tolerance: Remembrance Inc will work even if there is a communication loss between you and your wife!

**第六章：总结**

让我们现在看一下CAP理论。它说：当你设计分布式系统时，你只能实现一致性、可用性和分区容忍中的两者：

Ø一致性：你的客户再次来电时总能查到他们刚来电更新的信息，不论相隔多短

Ø可用性：不论你和你妻子谁来工作，记忆公司总能接听来电，处理客户请求

Ø分区容忍：即便你和你妻子失联，记忆公司依然能正常运转

## Bonus : Eventual Consistency with a run around clerk :

Here is another food for thought. You can have a run around clerk, who will update other’s notebook when one of your’s or your wife’s note books is updated. The greatest benefit of this is that, he can work in background and one of your or your wife’s “update” doesn’t have to block, waiting for the other one to update. This is how many NoSql systems work, one node updates itself locally and a background process synchronizes all other nodes accordingly… The only problem is that you will lose consistency of some time. For eg., a customer’s call reaches your wife first and before the clerk has a chance to update your notebook , the customer’ calls back and it reaches you. Then he won’t get a consistent reply.. But that said, this is not at all a bad idea if such cases are limited. For eg., assuming a customer won’t forget things so quickly that he calls back in 5 minutes.

**奖励：最终一致性和东奔西跑的员工**

你可以雇一个员工负责当一个本子上内容更新时去更新另一个本子。最大的好处就是，他能在后台工作，你或你妻子更新时不用等待另一个完成更新。这就是许多NoSQL数据库系统的工作方式。一个结点进行本地更新，后台进程将更新内容同步到其他所有结点。唯一的问题是：你将会失去一定时间的一致性。例如，客户先打给你妻子，在负责更新的员工未完成更新你的本子时，客户打给了你。那么他就无法得到一个一致性的回复。但即便如此，在某些情况下倒也不算是个坏主意。例如，一个客户不会忘东西忘得这么快，一般五分钟左右才会再次来电。

That’s CAP and eventual consistency for you in simple english :)

这就是给您的CAP理论和最终一致性的极简解释：）