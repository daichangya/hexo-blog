---
title: 用 TableModel Free 框架简化 Swing 开发——JTable
id: 1140
date: 2024-10-31 22:01:49
author: daichangya
excerpt: "简介： 本文将介绍 TableModel Free（TMF) 框架，该框架利用 SWing JTable 消除了对 TableModel 的需要。通过将所有特定于表的数据移到编译好的代码之外，"
permalink: /archives/7690900/
tags: 
 - swing
---


“Java™ Desktop 的再介绍”强调了今年的 JavaOne 大会。对于那些抱怨 Swing 太慢、太难使用、界面太难看的开发人员来说，Swing 和 GUI 开发所做的更新努力，并没有带来什么受人欢迎的好消息。如果您最近没有用过 Swing，那么您会很高兴听到其中的许多问题已经得到解决。Swing 被重新设计，它能执行得更好，并能更好地利用 Java 2D API。Swing 的开发者在 1.4 版甚至最新发布的 5.0 版中提高了外观支持。Swing 从没像现在这么好过。

Swing 社区现在需要的是能够让 GUI 开发变成一个更加顺利、更加容易的过程的工具。而这正是本文的目标所在。

本文将介绍 TableModel Free（TMF）框架，这是一个 GUI 开发包，它解除了为每个 JTable 建立 TableModel 的需要（在这篇文章中，我将 TableModel 称为 *传统 TableModel*，以便将它们与我为该框架引入的新结构区分开来）；在处理过程中，能够使您的 JTable 具备更高的可配置性和可维护性。

如果以前曾经用过 JTable，那么您可能也同时被迫使用了 TableModel。您可能还注意到，每个 TableModel 中的所有代码，与其他 TableModel 中的代码几乎是一样的，在编译的 Java 类中，有差异的代码实际上是不存在的。本文将分析 TableModel/JTable 目前的设计方法，说明这种设计的不足，展示为什么它没有实现模型-视图-控制器（MVC）模式的真正目标。您将看到框架和构成 TMF 框架的代码 —— 我以前编写的代码与最常用的开放源代码项目的组合。使用该框架，开发人员可以把 TableModel 的大小从数百行代码减少到只有区区一行，并把重要的表信息放在外部 XML 文件中。在读完本文之后，只使用如下所示的一行代码，您就可以管理您的 JTable 数据：

```
TableUtilities.setViewToModel("tableconfig.xml", "My Table",
  myJTable, CollectionUtilities.observableList(myData));
```

##### TMF 框架中的开放源代码包

让我们简要了解一下我用来协助构建 TMF 框架的两个开放源代码包。通过组合开放源代码包，并加入一些创新，您可以开发出非常强大的程序。请参阅 [参考资料](#artrelatedtopics)中这些代码包的链接。

*Apache Jakarta Commons Collections*  
最知名也最常用的开放源代码项目，可能就是 Apache 保护下的那些项目。Apache Jakarta 项目包含许多特定于 Java 的扩展和包，其中之一就是 Commons 项目。它的目标，正如在 Web 站点上所说那样，是“建立并维护可重用的 Java 组件”。其中列出了太多组件，而本文使用的只是 Jakarta Commons Collections 框架，它提供了大量对 Java Collections 框架的扩展。

*Castor*  
Castor 是一个被广泛采用的 XML 解析工具，虽然已经有了许多 XML 解析器，但是 Castor 的强大使得它非常流行。使用 Castor，可以非常容易地在简单的 XML 文档中建立复杂的 Java 对象。它把从 XML 到 Java 对象的许多繁重的转换工作从 XML 文件中提出取来，把复杂的转换工作放到一个映射文件中，该映射文件充当着 Java 与 XML 的中介。由于有一些非常能干的开发人员处理了映射文件，所以即使是最困难的转换，也可以在 XML 中进行，XML 文件非常便于阅读和更新。所以，Castor 工具在解析用作配置文件的 XML 文件（由最终用户更新，所以必须易于阅读）时，最为强大。

## JTable 和 TableModel 存在的 MVC 问题

MVC 已经成为非常流行的 UI 设计模式，因为它把业务逻辑清晰地从数据的视图中分离了出来。Struts 是 MVC 在 Web 上应用的一个非常好的例子。最初，Swing 最大的一个卖点是它采用了 MVC，将视图从模型中分离了出来，代码背后的想法是：代码的模块化程度足够高，所以，不用修改模型中的任何代码，就可以分离出视图。我想，任何用过 JTables 和 TableModels 的人都会发笑，告诉您这是绝对不可能的。使用 MVC 设计模式的理想情况是，在开发人员用 JList 或 JComboBox 替换 JTable 时，可以不用修改表示数据的模式中的代码。但是，在 Swing 中做不到这点。Swing 使得把 JTable、 JList 和 JComboBox 热交换到应用程序中成为不可能，即使所有这三个组件都是用来为相同的数据模型提供视图。对于 Swing 中的 MVC 设计，这是一个严重的不足。如果您想为 JTable 交换 JList，就必须重写视图背后的全部代码，才能实现该交换。

JTable/TableModel 的另一个 MVC 缺陷是：模型变化的时候，视图不会更新自身。开发人员必须保持对模型的引用，并调用一个函数，这样模型才会告诉视图对自身进行更新；但是，理想的情况应当是：不需要任何额外的代码，就能实现自动更新。

最后，JTable 和 TableModel 组件设计的问题是，它们彼此之间缠杂得过于密切。如果您修改了 JTable 中的代码，那么您需要确保您没有破坏负责处理的 TableModel，反之亦然。对于一个被认为是在模块化基础上建立的设计模式来说，目前的实现显然是一种存在过多依赖关系的设计。

TMF 框架更好地遵循了 MVC 的目标，它把 JTable 中视图和模型的工作更加清晰地分离开来。虽然它还没有达到让组件能够热切换的更高目标，但是它已经在正确方向上迈出了一步。

## 框架简介

让我们来检视 TMF 框架，看看它是如何让传统 TableModel 过时的。设计该框架的第一部分是学习 JTable 的使用 —— 开发人员如何使用它，它显示了什么内容，以便了理解哪些东西可以内化、通用化，哪些应当保留可配置状态，以便开发人员配置。对于 TableModel，也要进行同样的思考，我必须确定哪些东西可以从代码中移出，哪些必须留在代码中。一旦找出这些问题，接下来要做的就是确定能够让代码足够通用的最佳技术，以便所有人都能使用它，但是，还要让代码具备足够的可配置性，这也是为了让每个人都能使用它。

该框架分成三个基本部分：一个能够处理任何类型数据的通用 TableModel、一个外部 XML 文件（负责对不同表中不同的表内容进行配置），以及模型与视图之间的桥。

请单击 **Code**图标（或者参阅 [下载部分](#artdownload)），下载在本文中讨论的源代码、第三方 JAR 文件和 Javadoc。在本文中，您可以在 src 文件夹中找到文中介绍的所有源代码。特定于 TMF 的代码位于 `com.ibm.j2x.swing.table` 包中。

### com.ibm.j2x.swing.table.BeanTableModel

BeanTableModel 是框架的第一部分。它充当的是通用 TableModel ，您可以用它来处理任何类型的数据。我知道，您可能会说，“您怎么这么肯定它适用于所有的数据呢？”确实，很明显，我不能这么肯定，而且实际上，我确信有一些它不适用的例子。但是从我使用 JTables 的经验来说，我愿意打赌（即使看起来我有点抬杠），实际使用中的 JTables，99% 都是用来显示数据对象列表（也就是说，JavaBeans 组件的 ArrayList）。基于这个假设，我建立了一个通用表模型，它可以显示任何数据对象列表，它就是 *BeanTableModel*。

BeanTableModel 大量使用了 Java 的内省机制，来检查 bean 中的字段，显示正确的数据。它还使用了来自 Jakarta Commons Collections 框架（请参阅 [侧栏](#sidebar1)，以了解更多信息）的两个类来辅助设计。

在我深入研究代码之前，请让我解释来自类的几个概念。因为我可以在 bean 上使用内省机制，所以我需要了解 bean 本身的信息，主要是了解字段的名称是什么。我可以通过普通的内省机制来完成这项工作：我可以检查 bean ，找出其字段。但是，对于表来说，这还不够好，因为多数开发人员想让他们的表按照指定顺序显示字段。除此之外，还有一项表需要的信息，我无法通过内省机制从 bean 中获得，即列名消息。所以，为了获得正确显示，对于表中的每个列，您需要两条信息：列名和将要显示的 bean 中的字段。我用键-值对的格式表示该信息，其中，将列名用作键，字段作为值。

正因为如此，我在这里使用了来自 Collections 框架的适合这项工作的两个类。 `BeanMap` 用作实用工具类，负责处理内省机制，它接手了内省机制的所有繁琐工作。普通的内省机制开发需要大量的 `try` / `catch` 块，对于表来说，这是没有必要的。 `BeanMap` 把 bean 作为输入，像处理 HashMap 那样来处理它，在这里，键是 bean 中的字段（例如， `firstName` ），值是 get 方法（例如， `getFirstName()` ）的结果。BeanTableModel 广泛地运用 `BeanMap` ，消除了操作内省机制的麻烦，也使得访问 bean 中的信息更加容易。

`LinkedMap` 是另外一个在 BeanTableModel 中全面应用的类。我们还是回到为列名-字段映射所进行的键-值数据设置，对于数据对象来说，很明显应当选择 HashMap。但是，HashPap 没有保留插入的顺序，对于表来说，这是非常重要的一部分，开发人员希望在每次显示表的时候，都能以指定的顺序显示列。这样，插入的顺序就必须保留。解决方案是 `LinkedMap` ，它是 `LinkedList` 与 `HashMap` 的组合，它既保留了列，也保留了列的顺序信息。参见清单 1，可以查看我是如何用 `LinkedMap` 和 `BeanMap` 来设置表的信息的。

##### 清单1\. 用 LinkedMap 和 BeanMap 设置表信息

```
protected List mapValues = new ArrayList();
protected LinkedMap columnInfo = new LinkedMap(); 
 
protected void initializeValues(Collection values)
{
   List listValues = new ArrayList(values);
   mapValues.clear();
   for (Iterator i=listValues.iterator(); i.hasNext();)
   {
      mapValues.add(new BeanMap(i.next()));
   }
}
```

在 BeanTableModel 中比较有趣的检查代码实际上是通用 TableModel 的那一部分，这部分代码扩展了 `AbstractTableModel` 。将清单 2 中的代码与您通常用来建立传统 TableModel 的代码进行比较，您可以看到一些类似之处。

##### 清单 2\. BeanTableModel 中的通用 TableModel 代码

```
/**
 * Returns the number of BeanMaps, therefore the number of JavaBeans
 */   
public int getRowCount()
{
   return mapValues.size();
}
/**
 * Returns the number of key-value pairings in the column LinkedMap
 */   
public int getColumnCount()
{
   return columnInfo.size();
}
 
/**
 * Gets the key from the LinkedMap at the specified index (and a
 * good example of why a LinkedMap is needed instead of a HashMap)
 */  
public String getColumnName(int col)
{
   return columnInfo.get(col).toString();
}
/**
 * Gets the class of the column.  A lot of developers wonder what
 * this is even used for.  It is used by the JTable to use custom
 * cell renderers, some of which are built into JTables already
 * (Boolean, Integer, String for example).  If you  write a custom cell
 * renderer it would get loaded by the JTable for use in display  if that
 * specified class were returned here.
 * The function uses the BeanMap to get the actual value out of the
 * JavaBean and determine its class.  However, because the BeanMap
 * autoboxes things -- it converts the primitives to Objects for you
 * (e.g. ints to Integers) -- the code needs to unautobox it, since the
 * function must return a Class Object.  Thus, it recognizes any primitives
 * and converts them to their respective Object class.
 */  
public Class getColumnClass(int col)
{
   BeanMap map = (BeanMap)mapValues.get(0);
   Class c = map.getType(columnInfo.getValue(col).toString());
   if (c == null)
      return Object.class;
   else if (c.isPrimitive())
      return ClassUtilities.convertPrimitiveToObject(c);
   else
      return c;
}
/**
 * The BeanTableModel automatically returns false, and if you
 * need to make an editable table, you'll have to subclass
 * BeanTableModel and override this function.
 */   
public boolean isCellEditable(int row, int col)
{
   return false;
}
/**
 * The function that returns the value that you see in the JTable.  It gets
 * the BeanMap wrapping the JavaBean based on the row, it uses the
 * column number to get the field from the column information LinkedMap,
 * and then uses the field to retrieve the value out of the BeanMap. 
 */
public Object getValueAt(int row, int col)
{
   BeanMap map = (BeanMap)mapValues.get(row);
   return map.get(columnInfo.getValue(col));
}
/**
 * The opposite function of the getValueAt -- it duplicates the work of the
 * getValueAt, but instead puts the Object value into the BeanMap instead
 * of retrieving its value.
 */
public void setValueAt(Object value, int row, int col)
{
   BeanMap map = (BeanMap)mapValues.get(row);
   map.put(columnInfo.getValue(col), value);
   super.fireTableRowsUpdated(row, row);
}
 
/**
 * The BeanTableModel implements the CollectionListener interface
 * (1 of the 3 parts of the framework) and thus listens for changes in the
 * data it is modeling and automatically updates the JTable and the
 * model when a change occurs to the data.
 */ 
public void collectionChanged(CollectionEvent e)
{
   initializeValues((Collection)e.getSource());
   super.fireTableDataChanged();
}
```

正如您所看到的，BeanTableModel 的整个 TableModel 足够通用化，可以在任何表中使用。它充分利用了内省机制，省去了所有特定于 bean 的编码工作，在传统的 TableModel 中，这类编码工作绝对是必需的 —— 同时也是完全冗余的。BeanTableModel 还可以在 TMF 框架之外使用，虽然在外面使用会丧失一些威力和灵活性。

看过这段代码之后，您会提出两个问题。首先，BeanTableModel 从哪里获得列名-字段与键-值配对的信息？第二，到底什么是 `ObservableCollection` ？这些问题会将我们引入框架的接下来的两个部分。这些问题的答案以及更多的内容，将在本文后面接下来的章节中出现。

### Castor XML 解析器

保存必需的列名-字段信息的最合理的位置位于 Java 类之外，这样，不需要再重新编译 Java 代码，就可以修改这个信息。因为关于列名和字段的信息是 TMF 框架中惟一明确与表有关的信息，这意味着整个表格都可以在外部进行配置。

显然，该解决方案会自然而然把 XML 作为配置文件的语言选择。配置文件必须为多种表模型保存信息；您还需要能够用这个文件指定每个列中的数据。配置文件还应当尽可能地易于阅读，因为开发人员之外的人员有可能要修改它。

这些问题的最佳解决方案是 Castor XML 解析器（有关的更多信息，请参阅 [侧栏](#sidebar1)）。查看 Castor 实际使用的最佳方法就是查看如何在框架中使用它。

让我们来考虑一下配置文件的目的：保存表模型和表中列的信息。 XML 文件应当尽可能简单地显示这些信息。TMF 框架中的 XML 文件用清单 3 所示的格式来保存表模型信息。

##### 清单3\. TMF 配置文件示例

```
<model>
   <className>demo.hr.TableModelFreeExample</className>
   <name>Hire</name>
   <column>
      <name>First Name</name>
      <field>firstName</field>
   </column>
   <column>
      <name>Last Name</name>
      <field>lastName</field>
   </column>
</model>
```

与这个目的相反的目标是，开发人员必须处理的 Java 对象应当像 XML 文件一样容易理解。通过 Castor XML 解析器用来存储列信息的三个 Java 对象，就可以看到这一点，这三个对象是： `TableData` （存储文件中的所有表模型）、 `TableModelData` （存储特定于表模型的信息）和 `TableModelColumnData` （存储列信息）。这三个类提供了 Java 开发人员所需的所有包装器，以便得到有关 TableModel 的所有必要信息。

将所有这些包装在一起所缺少的一个环节就是 *映射文件*，它是一个 XML 文件，Castor 用它把简单的 XML 映射到简单的 Java 对象中。在完美的世界中，映射文件也应当很简单，但事实要比这复杂得多。良好的映射文件要使别的一切东西都保持简单；所以一般来说，映射文件越复杂，配置文件和 Java 对象就越容易处理。映射文件所做的工作顾名思义就是把 XML 对象映射到 Java 对象。清单 4 显示了 TMF 框架使用的映射文件。

##### 清单 4\. TMF 框架使用的 Castor 映射文件

```
<?xml version="1.0"?>
<mapping>
   <description>A mapping file for externalized table models</description>
  
   <class name="com.ibm.j2x.swing.table.TableData">
      <map-to xml="data"/>
      <field name="tableModelData" collection="arraylist" type=
        "com.ibm.j2x.swing.table.TableModelData">
         <bind-xml name="tableModelData"/>
      </field>
   </class>
  
   <class name="com.ibm.j2x.swing.table.TableModelData">
      <map-to xml="model"/>
      <field name="className" type="string">
         <bind-xml name="className"/>
      </field>
      <field name="name" type="string">
         <bind-xml name="name"/>
      </field>
      <field name="columns" collection="arraylist" type=
        "com.ibm.j2x.swing.table.TableModelColumnData">
         <bind-xml name="columns"/>
      </field>
   </class>
  
   <class name="com.ibm.j2x.swing.table.TableModelColumnData">
      <map-to xml="column"/>
      <field name="name" type="string">
         <bind-xml name="name"/>
      </field>
      <field name="field" type="string">
         <bind-xml name="field"/>
      </field>    
   </class>
  
</mapping>
```

仅仅通过观察这段代码，您就可以看出，映射文件清晰地勾划出了每个用来存储表模型信息的类，定义了类的类型，并将 XML 文件中的名称连接到了 Java 对象中的字段。请保持相同的名称，这样会让事情简单、更好管理一些，但是没必要保持名称相同。从 [参考资料](#artrelatedtopics)中，可以了解有关 Castor XML 映射的更多信息。

到现在为止，列名和字段信息都已外部化，可以读入包含列信息的 Java 对象中，并且可以很容易地把信息发送给 BeanTableModel，并用它来设置列。

### ObservableCollection

TMF 框架的最后一个关键部分，就是 `ObservableCollection` 。您们当中的某些人可能熟悉 `ObservableCollection` 的概念，它是 Java Collections 框架的一个成员，在被修改的时候，它会抛出事件，从而允许其侦听器根据这些事件执行操作。虽然从来没有将它引入 Java 语言的正式发行版中，但在 Internet 上，这个概念已经有了一些第三方实现。就本文而言，我使用了自己的 `ObservableCollection` 实现，因为框架只需要一些最基本的功能。我的实现使用了一个称为 `collectionChanged()` 的方法，每次发生修改时， `ObservableCollection` 都会在自己的侦听器上调用该方法。也可以将该用法称为 Collection 类的 *Decorator*（有关 Collections 的 Decorator 更多信息，请参阅 Collections 框架的站点），只需要增加几行代码，您就可以在普通的 Collection 类中创建 Collection 类的 Observable 实例。 清单 5 显示了 ObservableCollection 用法的示例。（这只是一个示例，没有包含在 j2x.zip 中。）

##### 清单 5\. ObservableCollection 用法示例

```
// convert a normal list to an ObservableList
ObservableList oList = CollectionUtilities.observableList(list);
// A listener could then register for events from this list by calling
oList.addCollectionListener(this);
// trigger event
oList.add(new Integer(3));
// listener receives event
public void collectionChanged(CollectionEvent e)
{
   // event received here
}
```

`ObservableCollection` 有许多 TMF 框架之外的应用程序。如果您决定采用 TMF 框架，您会发现，在开发代码期间， `ObservableCollection` 框架有许多实际的用途。

但是，它在 TMF 框架中的用途，重点在于它能更好地定义视图和模型之间的关系，当数据发生变化时，可以自动更新视图。您可以回想一下，这正是传统 TableModel 的最大限制，因为每当数据发生变化时，都必须用表模型的引用来更新视图。而在 TMF 框架中使用 ObservableCollection 时，当数据发生变化时，视图会自动更新，不需要维护一个到模型的引用。在 BeanTableModel 的 `collectionChanged()` 方法的实现中，您可以看到这一点。

### TableUtilities

在该框架中执行的最后一步操作，是将所有内容集成到一些实用方法中，让 TMF 框架使用起来简单明了。这些实用方法可以在 `com.ibm.j2x.swing.table.TableUtilities` 类中找到，该类提供了您将需要的所有辅助函数：

*   `getColumnInfo()` ：该实用方法用 Castor XML 文件解析指定的文件，并返回指定表模型的所有列信息，返回的形式是 BeanTableModel 所需的 `LinkedMap` 。当开发人员选择从 BeanTableModel 中派生子类时，这个方法很重要。
*   `getTableModel()` ：该实用方法是建立在上面的 `getColumnInfo()` 方法之上，它获得列的信息，然后把信息传递给 BeanTableModel，返回已经设置好所有信息的 BeanTableModel。
*   `setViewToModel()` ：该实用方法是最重要的函数，也是 TMF 框架的主要吸引人的地方。它也是建立在 `getTableModel()` 方法之上，也有一个到 JTable 的引用（JTable 中有这个表的模型），以及一个到数据（要在表中显示）的引用。它对 JTable 上的 TableModel 进行设置，并把数据传递给 TableModel，结果是：只需一行代码，就为 JTable 完成了 TableModel 的设置。TMF 框架在该方法上得到了最佳印证，TableModel 将永远地被下面这个简单的方法所代替：  
      
    
    ```
    TableUtilities.setViewToModel("table_config.xml", "Table", myJTable, myList);
    ```
    

## TMF 框架实战

每篇关于 GUI 编程的文章都需要一个示例，本文当然也不例外。该示例的目的是指出使用 TMF 框架代替传统 TableModel 设计的主要优势所在。示例中的应用程序将在屏幕上显示多个表，并且可以添加或删除表，表中可以包含不同类型的信息（ `String` 类型、 `int` 类型、 `Boolean` 类型和 `BigDecimal` 类型），而且最重要的是，其中还包含可配置的列信息，必须定期更改它们。

示例应用程序的代码从 `J2X` 包中分离了出来，您可以 HR 文件夹的 src 目录中找到源代码。还可以双击 build/lib 文件中编译好的 JAR 文件，通过 JRE 运行应用程序。

在示例应用程序中，有两个类可以相互交换，一个叫作 `TableModelFreeExample` ，另一个叫作 `TableModelExample` 。这两个类在应用程序中做的是同样的事，使应用程序产生的行为也相同。但是，它们的设计不同，一个使用的是 TMF 框架，另外一个则使用传统的 TableModel。您从它们身上注意到的第一件事可能是 TMF 类 `TableModelFreeExample` ，该类由 63 行代码构成，而在传统 TableModel 版本 `TableModelExample` 中，它长达 285 行。

### Evil HR Director 应用程序

我要使用的示例应用程序是 Evil HR Director 应用程序，它允许人力资源总监（可能很可怕，戴着眼镜）在 JTable 中查看潜在雇员的列表，然后从表中选出雇佣的人。新雇佣的员工的资料会转移到当前雇员使用的两个 JTable 中；其中一个表包含个人信息，另外一个表包含财务信息。在当前雇员表中，总监可以随意选择解雇谁。您可以在图 1 中看到该应用程序的 UI。

##### 图 1\. Evil HR Director 应用程序

![Evil HR Director](https://www.ibm.com/developerworks/cn/java/j-tabmod/hrdirector.jpg)


为了进一步证明 TMF 框架的简单性，请看清单 6。这个清单只包含三行必需的代码，就可以创建 Evil HR Director 应用程序中包含的三个表的模型。这些代码可以在 `TableModelFreeExample` 中找到。

##### 清单 6.在 Evil HR Director 应用程序中创建模型所需要的代码

```
TableUtilities.setViewToModel("demo/hr/resources/evil_hr_table.xml",
  "Hire", hireTable, candidates);   
TableUtilities.setViewToModel("demo/hr/resources/evil_hr_table.xml",
  "Personal", personalTable, employees);
TableUtilities.setViewToModel("demo/hr/resources/evil_hr_table.xml",
  "Financial", financialTable, employees);
```

为了进行比较， `TableModelExample` 中包含用传统 TableModel 方法为三个表格创建模型所需要的代码。请查看示例包中的代码。不过，我不想在这里列出所有代码，因为它足足有 205 行！

### 演示 TMF 框架的灵活性

TMF 框架的巨大优势之一，是它能更加容易地基于 JTable 的应用程序在其发布之后进行修改。为了证实这一点，让我们来看两个可能的场景，这两个场景在使用 Evil HR Director 应用程序中每天都可能出现。在每个场景中，您都会看到框架是如何让应用程序更加容易地适应不断变化的用户需求。

**场景 1：**公司的策略发生变化，规定在公司的应用程序中查看私人的婚姻信息是非法的。

*   **TMF**：最终用户需要从 XML 配置文件中删除 `<name>Married?</name><field>married</field>` 。
*   **传统 TableModel**：开发人员必须深入研究 Java 代码，修改 `getColumnName(）` ，让它无法返回列名“Married?”；修改 `getColumnCount()` ，让它返回的结果比以前返回的结果少一列；修改 `getValueAt()` ，不让它返回 `isMarried()` 。然后开发人员必须重新编译 Java 代码，并重新部署应用程序。

**场景 2：**公司策略发生变化，公司觉得有必要在潜在雇员表中包含居住地所在的州的信息。

*   **TMF：**: 最终用户需要将 `<name>State</name><field>state</field>` 添加到 XML 配置文件中。
*   **传统 TableModel**：开发人员必须深入研究 Java 代码，修改 `getColumnName()` ，添加一个叫作 “State” 新列；修改 `getColumnCount()` ，让它返回的列数加 1 ；修改 `getValueAt()` ，让它返回 `getState()` 。然后开发人员必须重新编译 Java 代码，并重新部署应用程序。

您可以看到，当应用程序中的表发生变化时（尤其在碰到一个总是朝令夕改的老板时，更改更加频繁），编辑 XML 文件要比重新部署整个应用程序容易得多。

## 使用代码

在您飞奔过去删除所有 TableModel 代码之前，我想我还得占用您一分钟解释一下 j2x.zip 文件的内容，以及您怎样才能在您自己的项目中使用它。（请记住，特定于 TMF 的代码可以在 `com.ibm.j2x.swing.table` 包中找到；您还会在 J2X 包中找到我在以前的文章“Go state-of-the-art with IFrame.”中介绍的其他代码，请参阅 [参考资料](#artrelatedtopics)，其中有这篇文章的链接。）

j2x.zip 文件包含两上文件夹：

*   **src**—— 包含本文中使用的源代码。在 src 文件夹中，还有两个文件夹：一个是 HR，包含构成 Evil HR Director 应用程序的源代码；另一个是 J2X，包含 J2X 项目中使用的所有源代码。
*   **build**—— 包含 Evil HR Director 应用程序和 J2X 项目编译后的类文件。该文件夹中的 lib 文件夹则包含 HR 应用程序和 J2X 项目的 JAR 文件。

lib.zip 文件包含以下文件夹：

*   **lib**—— 包含所有的第三方 JAR 文件，运行应用程序或者任何使用 J2X 项目的项目，需要使用这些文件。在这个文件夹中，您还会找到第三方项目的许可。

docs.zip 文件包含下列文件夹：

*   **docs**—— 包含 J2X 项目的所有 JavaDoc 信息。

要在应用程序中使用 J2X 包，则需要把 `CLASSPATH` 指向 build/lib 文件夹中的 j2x.jar 以及 lib 文件中包含的所有三个第三方 JAR 文件。第三方包的许可条款允许您重新发布本文包含的所有包，但是如果有兴趣对这些包做些修改，请阅读许可条款。

## 结束语

使用 TableModel Free 框架，就不用再编写传统 TableModel 了。TMF 框架改进了 JTable 和 TableModel 模型之间的 MVC 关系，更清楚地分离了它们。在日后的发布中，您甚至可以在不修改任何模型代码的情况下，对组件进行热交换。框架还允许您在模型发生变化时，自动更新视图，从而消除传统 TableModel 设计中所必需的视图和模型之间的通信。

TMF 框架还会极大地减少开发 GUI 所需的时间，特别是在处理 JTable 时。几年以前，我处理的一个应用程序中有 150 多个 JTable，每个表都来自同一个原始表模型，该应用程序可以作为示例。使用 TMF 框架，我们只用 150 行代码就能解决问题；但是不幸的是，当时还没有 TMF，所以我们最后编写了 15,000 行额外的代码，才生成必需的表模型。这不但增加了开发时间，还增加了测试和调试的时间。

与使用传统 TableModel 相比，使用 TMF 框架使您到了一个更加容易配置所有 JTable 的时代。请想像这样一个 POS 应用程序：该应用程序被销售给了 5 个不同的客户，每个客户都有一套特定的信息，所以每个用户都想有一组显示在 GUI 上的特定的列。如果没有 TMF 框架，您就必须为每个客户都生成一组特定的 TableModel —— 由此，也就生成了一组特定的应用程序。而使用可配置的 XML 文件，每个客户都可以使用相同的应用程序，客户所在地的业务分析师可以根据需要修改 XML 文件。请想像一下，这节约了多少开发和支持成本！

TableModel Free 框架解决了 Swing 开发人员社区的特定需求：减少了处理 JTable 时的开发时间和维护开销，提高了它们对终端用户的易用性。Swing 桌面正在回归，使用像 TMF 框架这样的工具，开发人员会发现可以更容易地使用 Swing 和开发 GUI 应用程序。您要做的第一步就是用 TMF 框架的一行代码代替您所有的 TableModel，把所有 TableModel 都永远地抛到虚拟空间的黑洞中去吧。

* * *

#### 下载资源

*   [(j2x.zip)](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=49092&filename=j2x.zip&method=http&locale=zh_CN)
*   [(lib.zip)](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=49092&filename=lib.zip&method=http&locale=zh_CN)
*   [(docs.zip)](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=49092&filename=docs.zip&method=http&locale=zh_CN)

* * *

#### [相关主题](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=49092&filename=docs.zip&method=http&locale=zh_CN)

*   [您可以参阅本文在 developerWorks 全球站点上的](http://www.ibm.com/developerworks/apps/download/index.jsp?contentid=49092&filename=docs.zip&method=http&locale=zh_CN) [英文原文](http://www.ibm.com/developerworks/java/library/j-tabmod/?S_TACT=105AGX52&S_CMP=cn-a-j)。
*   请单击 **Code**图标（或者参阅 [下载部分](#download)），下载在本文中讨论的源代码、第三方 JAR 文件和 Javadoc。
*   [The Jakarta Commons Collections](http://jakarta.apache.org/commons/collections/)提供了 Java Collections 之外的其他功能。
*   [Castor](http://www.castor.org/)是一个强大的 XML 解析器。
*   如果对 XML 感兴趣，请访问 [*developerWorks*XML zone](https://www.ibm.com/developerworks/cn/xml) ，那里有大量优秀的内容，既适合初学者，也适合专家。
*   Michael Abernethy 的“ [Go state-of-the-art with IFrame](http://www.ibm.com/developerworks/java/library/j-iframe/?S_TACT=105AGX52&S_CMP=cn-a-j),”（ *developerWorks*，2004 年 3 月）中对 IFrame 进行了介绍，它是 J2X 项目的另外一个组件。它允许您创建定制设计的应用程序窗口。
*   Malcolm Davis 撰写的“ [Struts, an open-source MVC implementation](http://www.ibm.com/developerworks/java/library/j-struts/?S_TACT=105AGX52&S_CMP=cn-a-j)，”（ *developerWorks*，2001 年 2 月）提供了在 Web 应用程序中使用的 MVC。
*   Mitch Goldstein 撰写的“ [Swing model filtering](http://www.ibm.com/developerworks/java/library/j-filters/?S_TACT=105AGX52&S_CMP=cn-a-j)，”（ *developerWorks*，2001 年 2 月）提供了用于 TableModel 设计的 TMF 框架的替代方案。
*   Brett Spell 撰写的“ [Rendering cells in Swing's JTable component](http://www.ibm.com/developerworks/java/library/j-jtable/?S_TACT=105AGX52&S_CMP=cn-a-j)，”（ *developerWorks*，2000 年 11 月）通过提供关于绘制单元格的技巧，添加了一项 JTable 功能。
*   在 [*developerWorks*Java 技术专区](https://www.ibm.com/developerworks/cn/java/) 中，可以找到 Java 编程各个方面的文章。
*   参阅 [Developer Bookstore](http://devworks.krcinfo.com/)，以获得技术书籍的完整清单，其中包括数百本 [Java 相关主题](http://devworks.krcinfo.com/WebForms/ProductList.aspx?Search=Category&id=1200)的书籍。
