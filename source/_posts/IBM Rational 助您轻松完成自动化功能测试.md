---
title: IBM Rational 助您轻松完成自动化功能测试
id: 469
date: 2024-10-31 22:01:43
author: daichangya
excerpt: "简介： 本文将向读者介绍 IBM Rational Functional Tester 的强大的功能和良好的易用性，以及如何帮助测试人员轻松的完成自动化的功能测试。"
permalink: /archives/8650085/
categories:
 - java
tags: 
 - 测试
---


## 1 解析自动化测试的困惑

在软件工程领域，如果说有一种工作让人在痛苦中感受它的价值、在无休止的加班中体会它的苦涩、在技术的进步中体验它的快乐的话，那它一定是软件测试。计算机技术发展到今天，自动化测试工具的广泛应用使人们重新认识到测试的源动力：最优的质量成本，软件开发过程中的测试及各种质量保证活动，无疑是在追求软件质量成本和收益间的最佳平衡点。

谈到自动化测试，首先我们要明确什么情况下需要自动化。自动化测试的目的是通过自动执行测试脚本，使测试人员在更短的时间内能够更快地完成更多的软件测试，并提供以更高的频率执行测试的能力，从而有效降低测试成本、提高测试效率。从软件测试的成本来看，使用测试工具进行软件自动化测试的成本可以以下公式表示：

自动化测试的成本＝测试工具成本＋测试脚本的创建成本＋测试脚本的维护成本

既然自动化测试的目的在于降低测试成本、提高测试效率，因此，测试团队在选择自动化测试工具时，必须在提高测试效率的同时，尽量做到自动化测试的总体成本小于手工测试成本。因此，自动化测试工具的脚本自动化创建能力和可维护性，就成了衡量自动化测试工具的重要因素。

在实际的测试工作中，一般说来，我们选择自动化的功能测试工具无外乎要解决以下三个问题：

*   自动化的功能回归测试
*   大批量数据驱动的软件测试
*   整个软件测试生命周期的管理

在选择自动化测试工具解决这些问题的过程中，人们主要关心的问题是使用自动化测试工具创建测试脚本的能力、工具的易用性、测试脚本的编程和扩展能力、测试脚本的参数化技术以及作为软件开发重要环节的测试工作和其它软件生命周期管理工具的集成能力。

因此，摆脱自动化测试困惑的根本途径，就是理解自动化测试的本质，明确自己的自动化测试需求，选择合适的自动化测试工具，帮助测试团队提高效率、降低成本，最终实现软件开发过程的全过程质量保证。

## 2 IBM最新自动化功能测试解决方案：Rational Functional Tester

IBM Rational Functional Tester（简称RFT）是一款先进的、自动化的功能和回归测试工具，它适用于测试人员和GUI开发人员。使用它，测试新手可以简化复杂的测试任务，很快上手；测试专家能够通过选择工业标准化的脚本语言，实现各种高级定制功能。通过IBM的最新专利技术，例如基于Wizard的智能数据驱动的软件测试技术、提高测试脚本重用的ScriptAssurance技术等等，大大提高了脚本的易用性和可维护能力。同时，它第一次为Java和Web测试人员，提供了和开发人员同样的操作平台（Eclipse），并通过提供与IBM Rational整个测试生命周期软件的完美集成，真正实现了一个平台统一整个软件开发团队的能力。

## 3 使用IBM RFT轻松完成自动化功能测试

### 3.1 基于与开发人员同一开发平台的功能测试

IBM RFT的最大特色就是基于开发人员的同一开发平台（Eclipse），为Java和Web测试人员提供了自动化测试能力。如图一所示，使用RFT进行软件测试时，我们只要在开发人员工作的Eclipse环境中打开Functional Test透视图，就会马上拥有专业的自动化功能测试工具所拥有的全部功能。

##### 图一、IBM Rational Functional Test工作界面

![图一、IBM Rational Functional Test工作界面](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image003.jpg)


在RFT中实现测试脚本的过程和大部分的自动化测试工具一样，是基于录制的脚本生成技术。当我们完成测试用例后，只要在功能测试工具条上选择测试脚本录制按钮，就会启动测试用例的脚本实现过程。

如图二所示，在脚本录制的"选择脚本资产"对话框中，用户可以选择预定义好的公用测试对象图和公用测试数据池，也可以选择在脚本录制过程中生成私有测试对象图和数据池。测试对象图是IBM用来解决测试脚本在不同被测版本间，成功回放的关键技术，它为测试脚本的重用提供了重要保证；而测试数据池是IBM用来实现数据驱动的自动化功能测试的重要手段，使用智能化的数据驱动测试向导，测试脚本的参数化几乎变得易如反掌。

##### 图二、"选择脚本资产"对话框

![图二、选择脚本资产对话框](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image005.jpg)


如图三所示，在功能测试的录制监视窗口，测试员可以根据提示启动被测应用系统，执行测试用例中规定的测试步骤，实现测试脚本的录制。在测试脚本录制过程中，测试员可以根据需要插入验证点和数据驱动的测试脚本，验证点是在指令中比较实际结果和预期结果的测试点，自动化功能测试工具正是通过它实现对被测系统功能需求的验证。

##### 图三、测试脚本录制窗口

![图三、测试脚本录制窗口](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image007.jpg)

完成脚本录制过程以后，RFT会自动生成用工业标准语言Java描述的测试脚本，如下所示：

##### 

```
import resources.ThirdwithDatapoolHelper;
import com.rational.test.ft.*;
import com.rational.test.ft.object.interfaces.*;
import com.rational.test.ft.script.*;
import com.rational.test.ft.value.*;
import com.rational.test.ft.vp.*;
/**
 * Description   : Functional Test Script
 * @author ndejun
 */
public class ThirdwithDatapool extends ThirdwithDatapoolHelper
{
    /**
     * Script Name   : <b>ThirdwithDatapool</b>
     * Generated     : <b>2005-4-17 15:22:36</b>
     * Description   : Functional Test Script
     * Original Host : WinNT Version 5.1  Build 2600 (S)
     *
     * @since  2005/04/17
     * @author ndejun
     */
    public void testMain(Object[] args)
    {
         
        startApp("ClassicsJavaB");
         
        // Frame: ClassicsCD
        classicsJava(ANY,MAY_EXIT).close();
    }
}
```

基于Java的测试脚本，为高级测试软员提高了更强大的编程和定制能力，测试员甚至可以通过在Helper类中加入各种客户化脚本，实现各种高级测试功能。

### 3.2 使用RFT轻松实现数据驱动的软件测试

RFT具有基于向导（Wizards）的数据驱动的功能测试能力。在功能测试脚本的录制过程中，如图四所示，我们可以方便选择被测应用图形界面上的各种被测对象，进行参数化，通过生成新的数据池字段或从数据池中选择已存在数据字段，实现数据驱动的功能回归测试。

##### 图四、数据驱动的功能测试

![图四、数据驱动的功能测试](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image009.jpg)


在生成测试脚本的同时，RFT还能够帮助测试员在验证点中使用正则表达式或使用数据驱动的方法建立动态验证点。动态验证点用来处理普通验证点的期望值随着输入参数不同而发生变化的情况。在下面的例子中，如图五所示，订单总金额会随着购买商品数量的不同而变化，通过数据驱动的功能测试方法，测试员首先要对购买的商品数量和订单总金额进行参数化，然后编辑验证点中的期望值，将其用数据池中的对应订单总金额代替，这样验证点中的总金额就随着购买商品数量的不同而得出正确的总金额。通过简单操作、无需任何编程，测试员就可以很方便地实现动态验证点的功能。

##### 图五、生成动态验证点

![图五、生成动态验证点](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image011.jpg)


此外，测试员还可以通过在验证点中使用正则表达式，建立更加灵活的验证点，保证测试脚本的重用性。

##### 图六、正则表达式在验证点中的应用

![图六、正则表达式在验证点中的应用](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image013.jpg)


### 3.3 提供多种专利技术，提高脚本的可维护性

使用IBM Rational Functional Test工具进行Java和Web应用系统测试时，标准Java的测试脚本语言，为测试脚本的可重用性和脚本能力提供了第一层保证。此外，通过维护"测试对象图"，IBM为测试员提供了不用任何编程就可以实现测试脚本在不同的被测系统版本间的重用能力。"测试对象图"分为两种，一种是公用"测试对象图"，它可以为项目中的所有测试脚本使用；另一种是私有"测试对象图"，它只被某一个管理的测试脚本所使用。在软件开发的不同版本间，开发员会跟据系统需求的变化，修改被测系统和用于构建被测系统的各种对象，所以测试脚本在不同的版本间进行回归测试时经常会失败。因此，通过维护公用"测试对象图"，如图七所示，测试员可以根据被测应用系统中对象的改变，更新测试对象的属性值及对应权重，这样在不修改测试脚本的前提下，就能使原本会失败的测试脚本回放成功。同时，为了方便测试员对测试对象图的修改和维护能力，RFT还提供了强大的查询和查询定制能力，帮助测试脚本维护人员快速找到变化的测试对象，进行修改和维护工作。

##### 图七、测试对象图的维护

![图七、测试对象图的维护](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image015.jpg)


其次，IBM提供的ScriptAssurance专利技术，使测试员能够从总体上改变工具对测试对象变更的容忍度，在很大程度上提高了脚本的可重用性。ScriptAssurance技术主要使用以下两个参数：脚本回放时，工具所容忍被测对象差异的最大门值和用于识别被测对象的属性权重。使用这种技术，测试员可以通过Eclipse的首选项设定脚本回放的容错级别，即门值，如图八和图九所示：

##### 图八、IBM专利技术：ScriptAssurance容错级别设定

![图八、IBM专利技术：ScriptAssurance容错级别设定](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image017.jpg)


点击高级，能够看到各种具体的可接受的识别门值。

##### 图八、ScriptAssurance门值设定

![图八、ScriptAssurance门值设定](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image019.jpg)


其次，测试员可以根据被测对象实际更改情况，在测试对象图中（如图七所示）修改用于回放时识别被测对象的属性及其权重。在测试脚本回访时，测试对象的识别分数将由以下公式计算得出：

##### 

```
int score = 0;
for ( int i = 0; i < property.length; ++i )
score += (100 - match(property[i])) * weight;
```

其中，match()将根据属性的符合程度返回0～100之间的值，完全符合返回100，完全不符合返回0。

测试脚本回放成功与否则取决于：识别得分 < 识别门值。通过这一技术，如图十所示，通过设置恰当的ScriptAssurance门值和为用于识别对象的属性设置合适的权重，即使在两个回归测试的版本间测试对象有多个属性不同，对象仍有可能被正确识别，脚本仍有可能回放成功。这为测试脚本的重用提供了最大程度的灵活性。

##### 图十、ScriptAssrance技术保证脚本的重用

![图十、ScriptAssrance技术保证脚本的重用](https://www.ibm.com/developerworks/cn/rational/r-func-test/images/image021.gif)


### 3.4 与其它生命周期管理软件的完美集成

IBM Rational的自动化功能测试工具基于Eclipse平台，提供了和需求管理工具（RequisitePro）、建模工具、代码级测试工具和变更及配置管理工具（ClearQuest和ClearCase）的完美集成，这使得系统测试人员能够和整个软件开发团队在同一个软件平台上，实现系统功能测试，完成测试脚本的配置管理和缺陷追踪。

## 4 小结

如果一种软件工具能够在提供强健的自动化测试脚本录制和自动化测试能力的同时，很好地解决测试脚本的可维护性、大批量数据驱动的软件测试和整个软件开发生命周期的集成问题，它无疑为降低软件测试的质量成本提供了重要保证，而IBM Rational Functional Tester正是这样的工具，它的出现必将使我们的测试生活变得更加美好！

## 5 参考资料

*   IBM Rational Functional Tester工具帮助
*   Evaluating Automated Functional Testing Tools by Carey Schwaber and Mike Gilpin
