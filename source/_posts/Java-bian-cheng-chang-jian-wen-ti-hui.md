---
title: Java编程：常见问题汇总
id: 1044
date: 2024-10-31 22:01:48
author: daichangya
excerpt: 该页面收集了一些不好的代码，对于初学者来说看起来似乎并不那么糟糕。初学者经常在语言语法上挣扎。他们对标准JDK类库以及如何最好地利用它也不了解。实际上，我已经从日常初级代码中收集了所有示例。我已经修改了原始代码，为它提供了示例字符，从而突出了问题所在。SonarQube可以很容易地发现许多这些问题。我强烈推荐此工具。
permalink: /archives/Java-bian-cheng-chang-jian-wen-ti-hui/
categories:
- java
---

Java反模式
=======

该页面收集了一些不好的代码，对于初学者来说看起来似乎并不那么糟糕。初学者经常在语言语法上挣扎。他们对标准JDK类库以及如何最好地利用它也不了解。实际上，我已经从日常初级代码中收集了所有示例。我已经修改了原始代码，为它提供了示例字符，从而突出了问题所在。[SonarQube](http://www.sonarsource.com/)可以很容易地发现许多这些问题。我强烈推荐此工具。

其中一些可能看起来像微优化，不带概要分析的过早优化或恒定因子优化。但是，在成千上万个这样的小地方浪费的性能和内存很快就会累积起来，并将使应用程序变得越来越困难。当我说应用程序时，我指的是在应用程序服务器上运行的服务器端应用程序。那就是我的生计。在桌面GUI应用程序上，情况可能没有那么糟。但是，运行客户端Java应用程序的唯一相关平台是什么？安卓 具有非常有限的资源（内存！）的嵌入式平台。在这里，即使恒​​定因子优化也能很快获得回报。就像遍历数组而不是列表一样。

如果您对如何友好地绘制图感兴趣，请查看 [JDK Performance Wiki](https://wiki.openjdk.java.net/display/HotSpot/PerformanceTechniques)。

最后，您的应用程序的很多性能取决于代码的整体质量。顺便说一句，您永远不要低估内存占用的重要性。我不能那么强调。我看到太多的应用程序具有疯狂的垃圾回收开销和内存不足错误。尽管垃圾回收非常快，但是大多数服务器端代码的可伸缩性主要受制于并限制了_每个请求/事务的内存使用量_和_请求/事务持续时间_。将这些参数中的任何一个提高一个常数都将直接为您带来更高的吞吐量。如果系数是10，则意味着要支持100或1000个用户，这可能对您的客户有所不同。

比较以下情况（假设年轻一代为100MB）：
| Scenario   | thread pool | tx duration | => max\. tx / s | mem / tx | => garbage / min | GC / min |
|------------|-------------|-------------|-----------------|----------|------------------|----------|
| base       | 30          | 100 ms      | 300             | 50 KB    | 900 MB           | 9        |
| slower     | 30          | 1000 ms     | 30              | 50 KB    | 90 MB            | 0\.9     |
| more mem   | 30          | 100 ms      | 300             | 500 KB   | 9 GB             | 90       |
| excess mem | 30          | 100 ms      | 300             | 5 MB     | 90 GB            | 900      |


在_较慢的_情况下，事务持续时间要长10倍。这也立即将每秒最大事务数减少了10倍（线程池有限，CPU资源有限）。在 _更多内存的_情况下，每个事务使用10倍的内存。这直接将垃圾收集的数量提高到每秒超过一个，从而导致不可忽略的开销。使用更多的内存，例如在场景 _多余的内存中_这将导致每秒15次收集，而每个收集只剩下66ms，这显然是不够的。系统将崩溃。同样，66ms低于100ms的事务持续时间，因此许多正在运行的事务仍将保留在内存中，从而阻止了它的收集，并导致该内存传播给较早的一代。这意味着较早的几代人将开始成长，并且需要较早的大量（慢速）收藏。该方案中的应用程序将不再执行。我认为，与仅慢速代码相比，这清楚地表明了过多的内存消耗是多么糟糕。当您分配过多的内存时，所有超快速代码都无法为您提供帮助。

*   [字符串串联](#0)
*   [失去StringBuffer性能](#1)
*   [测试字符串是否相等](#2)
*   [将数字转换为字符串](#3)
*   [解析和转换数字](#4)
*   [不利用不可变对象](#5)
*   [XML解析器用于sissies](#6)
*   [用String操作组装XML](#7)
*   [XML编码陷阱](#8)
*   [字符不是整数](#9)
*   [假设char代表一个字符](#10)
*   [平台相关的文件名](#11)
*   [未定义的编码](#12)
*   [无缓冲流](#13)
*   [InputStreamReader，OutputStreamWriter上的未缓冲操作](#14)
*   [使用PrintWriter进行文件I / O](#15)
*   [无限堆](#16)
*   [无限时间](#17)
*   [假设便宜的计时器呼叫](#18)
*   [抓住一切：我不知道正确的运行时异常](#19)
*   [异常很烦人](#20)
*   [重新包装RuntimeException](#21)
*   [没有正确传播异常](#22)
*   [愚蠢的异常消息](#23)
*   [捕捉日志](#24)
*   [不完整的异常处理](#25)
*   [永远不会发生的例外](#26)
*   [瞬态陷阱](#27)
*   [过度杀伤初始化](#28)
*   [日志实例：静态还是非静态？](#29)
*   [选择错误的类加载器](#30)
*   [使用反射不良](#31)
*   [同步过度杀伤力](#32)
*   [列表类型错误](#33)
*   [HashMap大小陷阱](#34)
*   [Hashtable，HashMap和HashSet被高估了](#35)
*   [清单被高估](#36)
*   [对象数组非常灵活](#37)
*   [物体过早分解](#38)
*   [修改二传手](#39)
*   [不必要的日历](#40)
*   [依赖默认的时区](#41)
*   [时区“转换”](#42)
*   [使用Calendar.getInstance（）](#43)
*   [危险日历操作](#44)
*   [调用Date.setTime（）](#45)
*   [假设SimpleDateFormat是线程安全的](#46)
*   [具有全局Configuration / Parameters / Constants类](#47)
*   [没有注意到溢出](#48)
*   [将==与float或double一起使用](#49)
*   [将钱存入浮点变量](#50)
*   [在finally块中不释放资源](#51)
*   [滥用finalize（）](#52)
*   [不由自主地重置Thread.interrupted](#53)
*   [来自静态初始值设定项的生成线程](#54)
*   [取消了保持状态的计时器任务](#55)
*   [拥有对ClassLoader和无法刷新的缓存的强大引用](#56)
*   [嵌套同步语句](#57)
*   [通过RandomAccessFile进行随机文件访问](#58)

### 字符串串联
```
String s = "";
for (Person p : persons) {
    s += ", " + p.getName();
}
s = s.substring(2); //remove first comma
```
这是真正的内存浪费。循环中字符串的重复连接会导致大量垃圾和数组复制。而且，必须将生成的字符串固定为多余的逗号，这很丑陋。令人惊讶的是，2016年仍然有人相信编译器会以某种方式对其进行优化。Java 8中甚至没有！一些白痴甚至以执行时间为基准，以“证明”还可以。不，产生大量不必要的垃圾不是很好。如果您仍然不相信我，那么我也不能帮助您的无知。
```
StringBuilder sb = new StringBuilder(persons.size() \* 16); // well estimated buffer
for (Person p : persons) {
    if (sb.length() > 0) sb.append(", "); // the JIT optimizes the if away out of the loop (peeling)
    sb.append(p.getName);
}
```
### 失去StringBuffer性能
```
StringBuffer sb = new StringBuffer();
sb.append("Name: ");
sb.append(name + '\\n');
sb.append("!");
...
String s = sb.toString();
```
这看起来像优化的代码，但还不是最佳的。那么，如果您未能正确地进行优化，为什么要首先进行优化呢？一路走！最明显的错误是第3行中的字符串连接。在第4行中，添加a `char`比添加String快。另外一个主要的遗漏是缓冲区缺少长度初始化，这可能导致不必要的调整大小（数组复制）。在JDK 1.5及更高版本中 `StringBuilder`，`StringBuffer`应该使用而不是：因为它只是一个局部变量，所以隐式同步是多余的。实际上，使用简单的String串联可以编译成几乎完美的字节码：仅缺少长度初始化。
```
StringBuilder sb = new StringBuilder(100);
sb.append("Name: ");
sb.append(name);
sb.append("\\n!");
String s = sb.toString();

String s = "Name: " + name + "\\n!";
```
### 测试字符串是否相等
```
if (name.compareTo("John") == 0) ...
if (name == "John") ...
if (name.equals("John")) ...
if ("".equals(name)) ...
```
以上比较均无误-但它们也不是很好。该`compareTo`方法过大且过于冗长。在`==`为对象的身份运营商的测试，可能不是你想要的。该`equals`方法是可行的方法，但是如果`name`是，则反转常量和变量将为您提供额外的安全性`null`。
```
if ("John".equals(name)) ...
if (name.length() == 0) ...
if (name.isEmpty()) ...
```
### 将数字转换为字符串
```
"" + set.size()
new Integer(set.size()).toString() 
```
方法的返回类型`Set.size()`为`int`。需要转换为`String`。实际上，这两个示例可以进行转换。但是第一种方法会导致串联操作的代价（转换为`(new StringBuilder()).append(i).toString())`）。第二个创建中间的Integer包装器。正确的方法是其中之一
```
Integer.toString(set.size())
```
### 解析和转换数字
```
int v = Integer.valueOf(str).intValue();
int w = Long.valueOf(Double.valueOf(str).longValue).intValue();
```
了解如何使用API​​而不分配不必要的对象。
```
int v = Integer.parseInt(str);
int w = (int) Double.parseDouble(str);
```
### 不利用不可变对象
```
zero = new Integer(0);
return Boolean.valueOf("true");
```
`Integer`以及`Boolean`是不可改变的。因此，创建代表相同值的多个对象没有任何意义。这些类具有针对常用实例的内置缓存。对于布尔型，甚至只有两个可能的实例。程序员可以利用以下优势：
```
zero = Integer.valueOf(0);
return Boolean.TRUE;
```
### XML解析器用于sissies
```
int start = xml.indexOf("<name>") + "<name>".length();
int end = xml.indexOf("</name>");
String name = xml.substring(start, end);
```
这种幼稚的XML解析仅适用于最简单的XML文档。但是，如果a）name元素在文档中不是唯一的，b）name的内容不仅是字符数据c）name的文本数据包含转义字符d）将该文本数据指定为CDATA部分e，它将失败。 ）文档使用XML名称空间。XML对于字符串操作来说太复杂了。诸如Xerces之类的XML解析器是一个超过一兆字节的jar文件，这是有原因的！与JDOM等效的是：
```
SAXBuilder builder = new SAXBuilder(false);
Document doc = doc = builder.build(new StringReader(xml));
String name = doc.getRootElement().getChild("name").getText();
```
### 用String操作组装XML
```
String name = ...
String attribute = ...
String xml = "<root>"
            +"<name att=\\""+ attribute +"\\">"+ name +"</name>"
            +"</root>";
```
许多初学者很想通过使用String操作（他们非常了解而且很容易）来产生如上所示的XML输出。确实，这是非常简单且几乎精美的代码。但是，它有一个严重的缺点：它无法转义保留的字符。因此，如果变量名称或属性包含任何保留字符<，>，＆，“或”，则此代码将生成无效的XML。此外，一旦XML使用名称空间，字符串操作可能很快就会变得讨厌并且难以维护。 XML应该在DOM中组装，JDom库对此非常有用。
```
Element root = new Element("root");
root.setAttribute("att", attribute);
root.setText(name);
Document doc = new Documet();
doc.setRootElement(root);
XmlOutputter out = new XmlOutputter(Format.getPrettyFormat());
String xml = out.outputString(root);
```
### XML编码陷阱
```
String xml = FileUtils.readTextFile("my.xml");
```
读取XML文件并将其存储在String中是一个非常糟糕的主意。XML在XML标头中指定其编码。但是在读取文件时，您必须事先知道编码！另外，将XML文件存储在字符串中会浪费内存。所有XML解析器都接受InputStream作为解析源，并且它们自己会正确计算出编码。因此，您可以向他们提供InputStream而不是将整个文件临时存储在内存中。当使用多字节编码（例如UTF-8）时，字节顺序（大端，小端）是另一个陷阱。XML文件可能在开头指定了字节顺序的字节顺序标记。XML解析器可以正确处理它们。

### 字符不是整数
```
int i = in.read();
char c = (char) i;
```
上面的代码假定您可以从数字创建字符。从技术上讲，这已经是错误的：int是有符号的，而char是无符号的。字符只是16位UTF-16编码的Unicode。请注意，Unicode定义的代码点数量超出了16位所能容纳的范围（Unicode 9.0的编码点为271792个，而65536个16位数字）。诸如流行表情符号之类的代码点已经远远超出了[BMP](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane)，甚至在Java中也由多个char表示！无论如何，在Java中，请使用Reader / Writer或CharsetEncoder / CharsetDecoder在字符及其字节表示形式之间进行转换（请参见下文）。

### 假设char代表一个字符
```
"\\uD83D\\uDC31".length() == 2
```
转义序列将 UTF-16中的Unicode代码点[0x1F431](http://www.isthisthingon.org/unicode/index.phtml?glyph=1F431)表示为2个字符。因此，即使这只是屏幕（🐱）上的单个猫脸符号，length（）方法仍返回2。

### 平台相关的文件名
```
File tmp = new File("C:\\\\Temp\\\\1.tmp");
File exp = new File("export-2013-02-01T12:30.txt");
File f = new File(path +'/'+ filename);
```
绝对不要在文件系统中使用硬编码路径。不同的平台具有不同的约定，并且您永远不能确定在随机系统上实际是否可以使用硬编码路径。使用API​​调用来创建临时文件。请注意，不同的文件系统对产生有效文件名的限制不同。这里的exp文件包含一个冒号，在Windows文件系统上是非法的。在文件系统中构造绝对路径或相对路径时，请注意依赖于平台的分隔符。
```
File tmp = File.createTempFile("myapp","tmp");
File exp = new File("export-2013-02-01\_1230.txt");

File f = new File(path + File.separatorChar + filename);
// or even better
File dir = new File(path);
File f = new File(dir, filename);
```
### 未定义的编码
```
Reader r = new FileReader(file);
Writer w = new FileWriter(file);
Reader r = new InputStreamReader(inputStream);
Writer w = new OutputStreamWriter(outputStream);
String s = new String(byteArray); // byteArray is a byte\[\]
byte\[\] a = string.getBytes();
```
以上各行在默认平台编码之间进行转换，`byte`并`char`使用默认平台编码。该代码的行为根据其所运行的平台而有所不同。如果数据从一个平台流到另一个平台，这将是有害的。完全依靠默认平台编码被认为是不好的做法。转换应始终以定义的编码执行。
```
Reader r = new InputStreamReader(new FileInputStream(file), "ISO-8859-1");
Writer w = new OutputStreamWriter(new FileOutputStream(file), "ISO-8859-1");
Reader r = new InputStreamReader(inputStream, StandardCharsets.UTF\_8);
Writer w = new OutputStreamWriter(outputStream, StandardCharsets.UTF\_8);
String s = new String(byteArray, "ASCII");
byte\[\] a = string.getBytes("ASCII");
```
### 无缓冲流
```
InputStream in = new FileInputStream(file);
int b;
while ((b = in.read()) != -1) {
   ...
}
```
上面的代码逐字节读取文件。`read()`流上的每个调用都会导致对文件系统的本机实现的本机（JNI）调用。根据实现的不同，这可能导致对操作系统的系统调用。JNI调用昂贵，而syscall也是如此。通过将流包装到中，可以大大减少本地调用的次数`BufferedInputStream`。`/dev/zero`使用上述代码从中读取1 MB的数据在笔记本电脑上花费了大约1秒钟。使用下面的固定代码，它可以减少到60毫秒！这样可以节省94％。当然，这也适用于输出流。这不仅适用于文件系统，而且适用于套接字。
```
InputStream in = new BufferedInputStream(new FileInputStream(file));

### InputStreamReader，OutputStreamWriter上的未缓冲操作

Writer w = new OutputStreamWriter(os, StandardCharsets.UTF\_8);
while (...) {
  // many small (<8kB) writes
  w.write("something");
}

Reader r = new InputStreamReader(in,  StandardCharsets.UTF\_8);
while (...) {
  // not reading into a buffer (char\[\], etc.)
  int c = r.read();
}
```
如图[所示，](/weblog/posting.php?posting=671)因为从char到字节的转换并不容易，所以OutputStreamWriter每次调用write（）方法都会使用内存。始终缓冲那些写操作：
```
Writer w = new BufferedWriter(new OutputStreamWriter(os, StandardCharsets.UTF\_8));
Reader r = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF\_8));
```
为了读写文本文件，正确的流链变为：
```
Writer w = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(f), StandardCharsets.UTF\_8));
Reader r = new BufferedReader(new InputStreamReader(new FileInputStream(f), StandardCharsets.UTF\_8));
```
### 使用PrintWriter进行文件I / O
```
PrintWriter w = new PrintWriter(new File("out.txt"), "UTF-8");
w.println("hello world");
```
PrintWriter从不抛出IOException。即使磁盘已满。即使在磁盘已满后继续调用println（）一百万次。即使在您打电话时也没有`close()`。您需要显式调用 `checkError()`以测试问题。然后您仍然没有得到一个异常，该异常可以告诉您到底发生了什么。您得到的只是一个布尔型说法，即在写入过程中的某个时刻出现问题， _文件现在已损坏_。问题就在这里。静默的文件损坏不是任何人想要的。要么生成一个完整的文件，要么根本不生成任何文件，然后出错。PrintWriter是为网络I / O（而非文件I / O）而发明的。例如，它由Servlet使用。另一个不错的应用程序是日志记录，当您真的不在乎日志记录是否产生I / O错误时。例如，它在JDBC API中使用。如何避免写入损坏的文件：
```
File f = new File("out.txt");
Writer w = null;
try {
  w = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(f), StandardCharsets.UTF\_8));
  w.append("hello world"); 
  ...
  w.close();
  w = null;
} finally {
  if (w != null) {
    // there was an exception and f is corrupt
    try { w.close(); } catch (IOException e) { }
    f.delete();
  }
}
```
### 无限堆
```
byte\[\] pdf = toPdf(file);
```
在这里，一种方法从某些输入创建PDF文件，然后将二进制PDF数据作为字节数组返回。此代码假定生成的文件足够小以适合可用的堆内存。如果此代码不能100％确定，则很容易出现内存不足的情况。特别是如果此代码在服务器端运行，通常意味着许多并行线程。批量数据绝不能使用字节数组进行处理。应该使用流，并且应该将数据假脱机到磁盘或数据库中。
```
File pdf = toPdf(file);
```
一种类似的反模式是缓冲来自“不受信任”（安全术语）源的流输入。例如缓冲到达网络套接字的数据。如果应用程序不知道将要到达多少数据，则必须确保它关注数据的大小。如果缓冲的数据量超过合理的限制，则应向调用者发出错误条件（异常）的信号，而不是通过使应用程序进入内存不足的情况来驱动应用程序。

### 无限时间
```
Socket socket = ...
socket.connect(remote);
InputStream in = socket.getInputStream();
int i = in.read();
```
上面的代码有两个使用未指定超时的阻塞调用。想象一下，如果超时是无限的。这可能导致应用程序永久挂起。通常，首先设置无限超时是一个非常愚蠢的想法。无限长。即使到太阳变成红色巨人（爆炸）时，它仍然是通往无限的一种轻松方式。一般的程序员去世，享年72我们根本**没有**在现实世界中，我们要等待那么长时间。无限超时只是荒谬的事情。使用小时，天，周，月，1年，10年。但不是无限。要连接到远程计算机，我个人发现有20秒的超时时间。人类甚至没有患者耐心，因此会取消手术。尽管可以对采用超时参数的connect（）方法进行很好的覆盖，但对于read（）则没有这种要求。但是您可以在每个阻塞调用之前修改Socket的套接字超时。（不仅是一次！您可以为不同的情况设置不同的超时。）套接字将在该超时之后阻止调用时引发异常。通过网络进行通信的框架还应该提供API，以控制这些超时并使用合理的默认值。无限是不明智的-太疯狂了，让您发疯。
```
Socket socket = ...
socket.connect(remote, 20000); // fail after 20s
InputStream in = socket.getInputStream();
socket.setSoTimeout(15000);
int i = in.read();
```
不幸的是，文件系统API（FileInputStream，FileChannel，FileDescriptor，File）无法提供设置文件操作超时的方法。真是不幸 因为这些是Java应用程序中最常见的阻塞调用：写stdout / stderr和从stdin读取是文件操作，而写日志文件是常见的。标准输入/输出流上的操作直接取决于Java VM之外的其他进程。如果他们决定永远阻止，那么在我们的应用程序中将对这些流进行读/写操作。磁盘I / O是系统上所有进程竞争的有限资源。不能保证对文件的简单读写是快速的。可能会导致未指定的等待时间。今天，远程文件系统也无处不在。磁盘可以位于SAN / NAS上，也可以通过网络安装文件系统（NFS，AFS，CIFS / Samba）。因此，文件系统调用实际上可能是网络调用：太糟糕了，以至于我们在这里没有网络API的功能！因此，如果操作系统确定写入超时为60秒，则您将无法执行。不能假定任何磁盘/文件操作是快速的，甚至是远程的，都是失败的。应用程序可以通过假设文件操作需要几秒钟来帮助用户。因此，最好避免或异步完成（在后台）。解决此问题的方法是：适当的缓冲和排队/异步处理。甚至是远程的。应用程序可以通过假设文件操作需要几秒钟来帮助用户。因此，最好避免或异步完成（在后台）。解决此问题的方法是：适当的缓冲和排队/异步处理。甚至是远程的。应用程序可以通过假设文件操作需要几秒钟来帮助用户。因此，最好避免或异步完成（在后台）。解决此问题的方法是：适当的缓冲和排队/异步处理。

### 假设便宜的计时器呼叫
```
for (...) {
  long t = System.currentTimeMillis();
  long t = System.nanoTime();
  Date d = new Date();
  Calendar c = new GregorianCalendar();
}
```
创建新的日期或日历会执行系统调用以获取当前时间。在Unix / Linux上，这是系统调用`gettimeofday`，被认为“非常便宜”。好吧，仅比其他系统调用便宜！因为它通常不需要从用户空间切换到内核空间，而是实现为对内存映射页面的读取。仍在呼叫`gettimeofday`与正常的代码执行相比，它是昂贵的。呼叫的确切代价在很大程度上取决于体系结构和配置（现代x86系统具有可由OS使用的众多计时器：HPET，TSC，RTC，ACPI，时钟芯片等）。在我的Linux-2.6.37-rc7系统上，计时器调用似乎也在系统上同步。这意味着所有线程/进程共享每毫秒约800个调用的总可用带宽。因此，我的双核运行2个线程，每个线程每毫秒可以进行约400次调用。（感谢J. Davies的提示）最后但并非最不重要的一点是，此计时器的分辨率不是无限的。充其量最好是毫秒，但它可能是25到50毫秒左右的较大抖动。现代Linux系统可以在System.currentTimeMillis中轻松实现完整的ms分辨率。但这并非总是如此。System.nanoTime当然不会具有其完整的理论分辨率：1ns = 10\-9 s对应于1GHz。因此，在具有3GHz的CPU上，这将允许约3条指令来执行调用，这显然是不够的。我测量了800ns至1000000ns（1ms）之间的较大抖动。清楚地每100纳秒调用gettimeofday是浪费的。

大多数时候，您不需要当前时间。将其缓存在循环之外是微不足道的。这样，您只需访问一次计时器。如果确实需要其他对象，您仍然可以决定克隆Date实例。与计时器访问相比，克隆非常便宜（我的系统中为50）。
```
Date d = new Date();
for (E entity : entities) {
  entity.doSomething();
  entity.setUpdated((Date) d.clone());
}
```
如果循环运行超过几毫秒，则可能无法选择缓存时间。在这种情况下，您可以设置一个计时器，以使用当前时间定期更新时间戳变量（使用中断）。将其设置为所需的确切粒度。粒度越大越好。在我的系统上，此循环比每次创建一个新的Date快200倍。
```
private volatile long time;

Timer timer = new Timer(true);
try {
  time = System.currentTimeMillis();
  timer.scheduleAtFixedRate(new TimerTask() {
    public void run() {
      time = System.currentTimeMillis();
    }
  }, 0L, 10L); // granularity 10ms
  for (E entity : entities) {
     entity.doSomething();
     entity.setUpdated(new Date(time));
  }
} finally {
  timer.cancel();
}
```
### 抓住一切：我不知道正确的运行时异常
```
Query q = ...
Person p;
try {
    p = (Person) q.getSingleResult();
} catch(Exception e) {
    p = null;
}
```
这是一个J2EE EJB3查询的示例。当a）结果不是唯一的，b）没有结果c）当由于数据库故障而无法执行查询时，getSingleResult会引发运行时异常。上面的代码捕获了任何异常。一个典型的万能块。使用 `null`结果可能是b情况下正确的事情），而不是情况下）或c）。通常，不应捕获过多的异常。正确的异常处理是
```
Query q = ...
Person p;
try {
    p = (Person) q.getSingleResult();
} catch(NoResultException e) {
    p = null;
}
```
### 异常很烦人
```
try {
    doStuff();
} catch(Exception e) {
    log.fatal("Could not do stuff");
}
doMoreStuff();
```
这小段代码有两个问题。首先，如果这确实是一个致命状况，则该方法应该中止并以适当的异常通知致命状况（为什么它首先被捕获了？）在出现致命状况之后，您几乎永远无法继续。其次，由于失败原因丢失，因此很难调试该代码。异常对象包含有关错误发生的位置以及导致错误的原因的详细信息。各个子类实际上可能携带许多额外的信息，调用者可以使用这些信息来适当地处理这种情况。它不仅仅是一个简单的错误代码（在C语言中非常流行。只需查看Linux内核。在任何地方都返回-EINVAL ...）。如果捕获高级异常，则至少记录消息和堆栈跟踪。您不应将例外视为必要的邪恶。它们是错误处理的好工具。
```
try {
    doStuff();
} catch(Exception e) {
    throw new MyRuntimeException(e.getMessage(), e);
}
```
### 重新包装RuntimeException
```
try {
  doStuff();
} catch(Exception e) {
  throw new RuntimeException(e);
}
```
有时您真的想将任何检查到的异常重新抛出为RuntimeException。上面的代码没有考虑到，但是RuntimeException扩展了Exception。RuntimeException不需要在这里捕获。此外，异常的消息也无法正确传播。更好的方法是分别捕获RuntimeException而不包装它。更好的办法是单独捕获所有检查的异常（即使它们很多）。
```
try {
  doStuff();
} catch(RuntimeException e) {
  throw e;
} catch(Exception e) {
  throw new RuntimeException(e.getMessage(), e);
}

try {
  doStuff();
} catch(IOException e) {
  throw new RuntimeException(e.getMessage(), e);
} catch(NamingException e) {
  throw new RuntimeException(e.getMessage(), e);
}
```
### 没有正确传播异常
```
try {
} catch(ParseException e) {
  throw new RuntimeException();
  throw new RuntimeException(e.toString());
  throw new RuntimeException(e.getMessage());
  throw new RuntimeException(e);
}
```
该代码只是以不同的方式将解析错误包装到运行时异常中。它们都没有为呼叫者提供真正好的信息。第一个只会丢失所有信息。第二种方法可以执行任何操作，具体取决于toString（）产生什么信息。默认的toString（）实现列出了完全限定的异常名称，后跟消息。嵌套许多异常将产生笨拙且冗长的字符串，不适合用户。第三只保留消息，总比没有好。最后一个保留原因，但将运行时异常的消息设置为其原因的toString（）（请参见上文）。最有用，最易读的版本是在运行时异常中仅传播原因消息，并将原始异常作为原因传递：
```
try {
} catch(ParseException e) {
  throw new RuntimeException(e.getMessage(), e);
}
```
### 愚蠢的异常消息
```
try {
} catch (ParseException e) {
  throw new RuntimeException("\*\*\*\* --> OMFG something scary happened !!!!11! <---");
}
```
这个异常是没有用的。它不会给呼叫者任何指示原因。相反，它包含ASCII艺术和情感用语，对任何人都没有帮助。添加有用的信息或简单地传递原始异常的消息。不要在原始消息前添加自定义“操作失败，因为：”字符串。这没用。并将该字符串添加到常量池中，该常量池将在大型应用程序中充满无用的字符串。字符串是已编译应用程序中的顶级空间使用者。
```
try {
} catch (ParseException e) {
  // for code so it gets access to some context
  throw new MyException(input, e);
  // for humans
  throw new RuntimeException(input +": "+ e.getMessage(), e);
  // or simply
  throw new RuntimeException(e.getMessage(), e);
}
```
### 捕捉日志
```
try {
    ...
} catch(ExceptionA e) {
    log.error(e.getMessage(), e);
    throw e;
} catch(ExceptionB e) {
    log.error(e.getMessage(), e);
    throw e;
}
```
此代码仅捕获异常以写出一条日志语句，然后重新引发相同的异常。真傻 让调用者决定消息是否对日志记录很重要并删除整个try / catch子句。仅当您知道呼叫者未记录它时，它才有用。如果不是由您控制的框架调用该方法，就是这种情况。如果您因为调用者没有足够的信息来记录日志，那么您的异常类是不合适的：将所有必需的信息一起传递给异常。那就是他们的目的！

### 不完整的异常处理
```
try {
    is = new FileInputStream(inFile);
    os = new FileOutputStream(outFile);
} finally {
    try {
        is.close();
        os.close();
    } catch(IOException e) {
        /\* we can't do anything \*/
    }
}
```
如果未关闭流，则底层操作系统无法释放本机资源。这位程序员想要关闭两个流时要小心。所以他把结束语放在了一个`finally`条款中。但是，如果`is.close()`抛出IOException，则 `os.close`甚至不会执行。两个close语句必须包装在它们自己的try / catch子句中。此外，如果创建输入流引发异常（因为未找到文件），`os`则为null并`os.close()`引发`NullPointerException`。为了使它不那么冗长，我删除了一些换行符。
```
try {
    is = new FileInputStream(inFile);
    os = new FileOutputStream(outFile);
} finally {
    try { if (is != null) is.close(); } catch(IOException e) {/\* we can't do anything \*/}
    try { if (os != null) os.close(); } catch(IOException e) {/\* we can't do anything \*/}
}
```
### 永远不会发生的例外
```
try {
  ... do risky stuff ...
} catch(SomeException e) {
  // never happens
}
... do some more ...
```
在这里，开发人员在try / catch块中执行一些代码。他不想将被调用的方法之一声明的异常抛出他的烦恼。由于开发人员很聪明，他知道在他的特定情况下永远不会抛出异常，因此他只是插入一个空的catch块。他甚至在空白的catch区域中添加了一个不错的注释-但它们是著名的遗言...问题是：他如何确定？如果被调用方法的实现发生变化怎么办？如果在某些特殊情况下仍然抛出异常，但他只是没有想到该怎么办？在这种情况下，try / catch之后的代码可能会做错事情。该异常将完全不被注意到。通过在这种情况下抛出运行时异常，可以使代码更加可靠。这就像断言一样，并遵循“
```
try {
  ... do risky stuff ...
} catch(SomeException e) {
  // never happens hopefully
  throw new IllegalStateException(e.getMessage(), e); // crash early, passing all information
}
... do some more ...
```
### 瞬态陷阱
```
public class A implements Serializable {
    private String someState;
    private transient Log log = LogFactory.getLog(getClass());
    
    public void f() {
        log.debug("enter f");
        ...
    }
}
```
日志对象不可序列化。程序员知道这一点，并正确地将该`log`字段声明为瞬态，因此不进行序列化。但是，此变量的初始化发生在类的初始化程序中。反序列化时，不执行初始化程序和构造函数！这`log`将使反序列化的对象具有null 变量，该变量随后导致`NullPointerException`in `f()`。经验法则：切勿将类初始化与瞬态变量一起使用。您可以在此处通过使用静态变量或通过使用局部变量来解决这种情况：
```
public class A implements Serializable {
    private String someState;
    private static final Log log = LogFactory.getLog(A.class);
    
    public void f() {
        log.debug("enter f");
        ...
    }
}

public class A implements Serializable {
    private String someState;
    
    public void f() {
        Log log = LogFactory.getLog(getClass());
        log.debug("enter f");
        ...
    }
}
```
### 过度杀伤初始化
```
public class B {
    private int count = 0;
    private String name = null;
    private boolean important = false;
}
```
这位程序员曾经使用C语言进行编程。因此，他自然希望确保每个变量都已正确初始化。但是，这里没有必要。Java语言规范保证成员变量会自动使用某些值初始化：0，null，false。通过显式声明它们，程序员使类初始化程序在构造函数之前执行。这是不必要的过度杀伤，应该避免。
```
public class B {
    private int count;
    private String name;
    private boolean important;
}
```
### 日志实例：静态还是非静态？

本节已经过编辑，在实际不建议将日志实例存储在静态变量中之前。原来我错了。Mea culpa。我道歉。  
将织补日志实例存储在静态的final变量中并感到高兴。
```
private static final Log log = LogFactory.getLog(MyClass.class);
```
原因如下：

*   自动线程安全。但仅包含最终关键字！
*   可用于静态和非静态代码。
*   可序列化类没有问题。
*   初始化只需花费一次：getLog（）可能不像您想象的那样便宜。
*   无论如何，没人会卸载Log类加载器。

### 选择错误的类加载器
```
Class clazz = Class.forName(name);
Class clazz = getClass().getClassLoader().loadClass(name);
```
该代码使用加载当前类的类加载器。getClass（）可能会返回意外的内容，例如子类或动态代理。超出您的控制范围。动态加载其他类时，这几乎不是您想要的。尤其是在诸如应用程序服务器，Servlet引擎或Java Webstart之类的托管环境中，这无疑是错误的。取决于运行的环境，此代码的行为将有很大不同。环境使用上下文类加载器为应用程序提供应用于检索“自己的”类的类加载器。
```
ClassLoader cl = Thread.currentThread().getContextClassLoader();
if (cl == null) cl = MyClass.class.getClassLoader(); // fallback
Class clazz = cl.loadClass(name);
```
### 使用反射不良
```
Class beanClass = ...
if (beanClass.newInstance() instanceof TestBean) ...
```
这位程序员正在努力使用反射API。他需要一种检查继承的方法，但没有找到一种方法。因此，他只是创建一个新实例并使用`instanceof`他习惯的运算符。创建您不知道的类的实例很危险。您永远都不知道该类做什么。它可能非常昂贵。否则默认构造函数可能甚至不存在。然后，此if语句将引发异常。进行此检查的正确方法是使用`Class.isAssignableFrom(Class)` 方法。它的语义是颠倒的`instanceof`。
```
Class beanClass = ...
if (TestBean.class.isAssignableFrom(beanClass)) ...
```
### 同步过度杀伤力
```
Collection l = new Vector();
for (...) {
   l.add(object);
}
```
`Vector`是同步的`ArrayList`。并且`Hashtable`是同步的`HashMap`。只有明确需要同步时，才应使用两个类。但是，如果将这些集合用作本地临时变量，则同步将完全被淘汰，从而大大降低性能。我测算了25％的罚款。
```
Collection l = new ArrayList();
for (...) {
   l.add(object);
}
```
### 列表类型错误

没有示例代码。初级开发人员通常很难选择正确的列表类型。他们通常会选择从非常随意 `Vector`，`ArrayList`和`LinkedList`。但是需要考虑性能！当通过索引添加，迭代或访问对象时，实现的行为有很大不同。在此列表中，我将忽略Vector，因为它的行为类似于ArrayList，只是速度较慢。注意：n是列表的大小，而不是操作数！我在这里避免使用O（）表示法，因为它不能给出正在发生的事情的有用图像。该表列出了列表操作的成本。
|        | 数组列表                  | 链表    |
|--------|-----------------------|-------|
| 添加（追加） | const或〜log（n）（如果增长）   | const |
| 插入（中间） | 线性或〜n \* log（n）（如果增长） | 线性的   |
| 删除（中）  | 线性（始终执行完整复制）          | 线性的   |
| 重复     | 线性的                   | 线性的   |
| 通过索引获取 | const                 | 线性的   |


ArrayList的插入性能取决于它在插入期间是否必须增大，或者是否合理设置了初始大小。增长呈指数增长（因数2），因此增长成本是对数的。但是，指数增长可能会使用比实际需要更多的内存。突然需要调整列表大小也使响应时间变慢，并且如果列表很大，可能会导致大量垃圾回收。遍历列表同样便宜。但是，在链接列表中，对索引列表元素的访问非常慢。  
内存注意事项：LinkedList将每个元素包装到包装对象中。ArrayList每次需要增长时都会分配一个全新的数组，并在每个remove（）上执行数组复制。所有标准Collection都不能重用其Iterator对象，这可能导致Iterator流失，尤其是在递归迭代大型树结构时。  
我个人几乎从不使用LinkedList。仅当您想在列表中间插入对象时，这才有意义。但是，由于无法访问包装对象，因此无法缩放并且具有线性成本，因为必须首先遍历列表，直到找到插入位置。那么，LinkedList类的确切含义是什么？我建议仅使用ArrayLists。

### HashMap大小陷阱
```
Map map = new HashMap(collection.size());
for (Object o : collection) {
  map.put(o.key, o.value);
}
```
该开发人员有良好的意愿，并希望确保不需要调整HashMap的大小。因此，他将其初始大小设置为要放入其中的元素数量。不幸的是，HashMap实现并不完全像这样。它将内部阈值设置为 `threshold = (int)(capacity * loadFactor)`。因此，在将集合的75％插入地图后，它将调整大小。因此，以上代码将始终导致额外的垃圾。
```
Map map = new HashMap(1 + (int) (collection.size() / 0.75));
```
### Hashtable，HashMap和HashSet被高估了

这些课程非常受欢迎。因为它们对于开发人员来说具有很大的可用性。不幸的是，它们的效率也非常差。当您有100个或更多条目时，哈希表将变得很有用。但是不只是一些要素。在典型的代码中，此类集合包含大约10个条目-适合CPU缓存行！Hashtable和HashMap将每个键/值对包装到Entry包装器对象中。Entry对象非常大。它不仅保存对键和值的引用，还存储哈希码和对哈希存储桶下一个Entry的正向引用。当您使用内存分析器查看堆转储时，您会为它们在大型应用程序（如应用程序服务器）中浪费多少空间而感到震惊。  
在使用任何这些类之前，请三思。IdentityHashMap可能是一个可行的选择。但请注意，它有意破坏Map界面。通过实现开放的哈希表（无存储桶），不需要Entry包装器并使用简单的Object \[\]作为其后端，可以提高内存效率。代替HashSet，简单的ArrayList可以做得很好（可以使用contains（Object）），只要它很小并且查找很少。  
对于仅包含少量条目的Set来说，整个哈希处理是多余的，并且HashMap后端加上包装器对象所浪费的内存只是胡说八道。只需使用ArrayList甚至是数组即可。  
实际上，在标准JDK中没有有效的Map和Set实现真是可惜！

### 清单被高估

List的实现也很受欢迎。但是，甚至列表通常也没有必要。简单数组也可以。我并不是说您根本不应该使用列表。他们很棒。但是知道何时使用数组。以下是应该使用数组而不是列表的指示符：

*   列表的大小固定。例如：星期几。一组常数。
*   该列表经常被遍历（10,000次）。
*   该列表包含数字的包装对象（没有原始类型的列表）。

让我用代码说明一下：
```
List<Integer> codes = new ArrayList<Integer>();
codes.add(Integer.valueOf(10));
codes.add(Integer.valueOf(20));
codes.add(Integer.valueOf(30));
codes.add(Integer.valueOf(40));

versus

int\[\] codes = { 10, 20, 30, 40 };

// horribly slow and a memory waster if l has a few thousand elements (try it yourself!)
List<Mergeable> l = ...;
for (int i=0; i < l.size()-1; i++) {
    Mergeable one = l.get(i);
    Iterator<Mergeable> j = l.iterator(i+1); // memory allocation!
    while (j.hasNext()) {
        Mergeable other = l.next();
        if (one.canMergeWith(other)) {
            one.merge(other);
            other.remove();
        }
    }
}

versus

// quite fast and no memory allocation
Mergeable\[\] l = ...;
for (int i=0; i < l.length-1; i++) {
    Mergeable one = l\[i\];
    for (int j=i+1; j < l.length; j++) {
        Mergeable other = l\[j\];
        if (one.canMergeWith(other)) {
            one.merge(other);
            l\[j\] = null;
        }
    }
}
```
您将保存一个额外的列表对象（包装一个数组），包装对象以及可能的许多迭代器实例。甚至Sun也意识到了这一点。这就是为什么 [Collections.sort（）](http://java.sun.com/j2se/1.5.0/docs/api/java/util/Collections.html#sort(java.util.List)) 实际上将列表复制到数组中并对数组执行排序的原因。  

### 对象数组非常灵活
```
/\*\*
 \* @returns \[1\]: Location, \[2\]: Customer, \[3\]: Incident
 \*/
Object\[\] getDetails(int id) {...
```
即使有文档记录，这种从方法传回值的方法也是丑陋且容易出错的。您应该真正声明一个将对象结合在一起的小类。这类似于`struct`C中的a 。
```
Details getDetails(int id) {...}

private class Details {
    public Location location;
    public Customer customer;
    public Incident incident;
}
```
### 物体过早分解
```
public void notify(Person p) {
    ...
    sendMail(p.getName(), p.getFirstName(), p.getEmail());
    ...
}

class PhoneBook {
    String lookup(String employeeId) {
        Employee emp = ...
        return emp.getPhone();
    }
}
```
在第一个示例中，分解对象只是将其状态传递给方法是很痛苦的。在第二个示例中，此方法的使用非常有限。如果总体设计允许，它可以通过对象本身。
```
public void notify(Person p) {
    ...
    sendMail(p);
    ...
}

class EmployeeDirectory {
    Employee lookup(String employeeId) {
        Employee emp = ...
        return emp;
    }
}
```
### 修改二传手
```
private String name;

public void setName(String name) {
    this.name = name.trim();
}

public void String getName() {
    return this.name;
}
```
这个可怜的开发人员在用户输入的名称的开头或结尾出现空格。他认为自己很聪明，只是删除了bean的setter方法内部的空格。但是，一个修改数据而不只是保存数据的bean有多奇怪？现在，getter返回的数据与setter设置的数据不同！如果这是在EJB3实体Bean中完成的，则从数据库中进行简单的读取实际上会修改数据：对于每个INSERT，将有一个UPDATE语句。更不用说调试这些副作用有多困难了！通常，bean不应修改其数据。它是一个数据容器，而不是业务逻辑。在有意义的地方进行微调：在发生输入的控制器中或在不需要空格的逻辑中。
```
person.setName(textInput.getText().trim());
```
### 不必要的日历
```
Calendar cal = new GregorianCalender(TimeZone.getTimeZone("Europe/Zurich"));
cal.setTime(date);
cal.add(Calendar.HOUR\_OF\_DAY, 8);
date = cal.getTime();
```
开发人员的一个典型错误，他们对日期，时间，日历和时区感到困惑。要将8小时添加到日期，则不需要日历。任何相关的时区也不是。（想想如果您不理解这一点！）但是，如果我们想增加天数（而不是小时数），我们将需要一个日历，因为我们不确定一天的时长（在DST更改的日子，可能会有23或25小时）。
```
date = new Date(date.getTime() + 8L \* 3600L \* 1000L); // add 8 hrs

Calendar cal = new GregorianCalender(TimeZone.getTimeZone("Europe/Zurich"));
SimpleDateFormat df = new SimpleDateFormat("dd.MM.yyyy HH:mm");
df.setCalendar(cal);
```
在这里，Calendar对象是完全不必要的。DateFormat对象已经包含一个Calendar实例。再用一次。
```
SimpleDateFormat df = new SimpleDateFormat("dd.MM.yyyy HH:mm");
df.setTimeZone(TimeZone.getTimeZone("Europe/Zurich"));
```
### 依赖默认的时区
```
Calendar cal = new GregorianCalendar();
cal.setTime(date);
cal.set(Calendar.HOUR\_OF\_DAY, 0);
cal.set(Calendar.MINUTE, 0);
cal.set(Calendar.SECOND, 0);
Date startOfDay = cal.getTime();
```
开发人员想要计算一天的开始时间（0h00）。首先，他显然错过了日历的毫秒字段。但是，真正的大错误不是设置Calendar对象的TimeZone。日历将因此使用默认时区。在桌面应用程序中，这可能很好，但是在服务器端代码中，这几乎不是您想要的：在上海，与伦敦相比，0h00的时刻与现在截然不同。开发人员需要检查哪个时区与此计算相关。
```
Calendar cal = new GregorianCalendar(user.getTimeZone());
cal.setTime(date);
cal.set(Calendar.HOUR\_OF\_DAY, 0);
cal.set(Calendar.MINUTE, 0);
cal.set(Calendar.SECOND, 0);
cal.set(Calendar.MILLISECOND, 0);
Date startOfDay = cal.getTime();
```
### 时区“转换”
```
public static Date convertTz(Date date, TimeZone tz) {
  Calendar cal = Calendar.getInstance();
  cal.setTimeZone(TimeZone.getTimeZone("UTC"));
  cal.setTime(date);
  cal.setTimeZone(tz);
  return cal.getTime();
}
```
如果您认为此方法有帮助，请阅读[有关time](datetime.php)的 [文章](datetime.php)。该开发人员尚未阅读本文，并拼命尝试“固定”其约会的时区。实际上，该方法不执行任何操作。返回的日期将与输入没有任何不同的值。因为日期不包含时区信息。它始终是UTC。Calendar的getTime / setTime方法始终在UTC与Calendar的实际时区之间进行转换。

### 使用Calendar.getInstance（）
```
Calendar c = Calendar.getInstance();
c.set(2009, Calendar.JANUARY, 15);
```
此代码假定使用公历。但是，如果返回的Calendar子类是佛教，儒略，希伯来语，伊斯兰，伊朗或Discordian日历，该怎么办？在这些年份中，2009年具有非常不同的含义。而且一个月称为一月不存在。Calendar.getInstance（）使用当前的默认语言环境选择适当的实现。这取决于可用的Java实现。因此Calendar.getInstance（）的实用程序非常有限，应避免使用它，因为其结果定义不明确。
```
Calendar c = new GregorianCalendar(timeZone);
c.set(2009, Calendar.JANUARY, 15);
```
### 危险日历操作
```
GregorianCalender cal = new GregorianCalender(TimeZone.getTimeZone("Europe/Zurich"));
cal.set(Calendar.SECOND, 0);
cal.set(Calendar.MILLISECOND, 0);
if (cal.before(other)) doSomething();

cal.setTimeZone(TimeZone.getTimeZone("GMT"));
cal.set(Calendar.HOUR\_OF\_DAY, 23);
Date d = cal.getTime();
```
此代码以一定方式处理Calendar对象，这些方法必然会产生未定义的结果。日历对象具有复杂的内部状态：日期，小时，年等的各个字段，历元值（如日期）后的毫秒数和时区。根据您所做的更改，这些字段中的某些是无效的，并且仅当您调用某些方法时才从其他值重新计算：

*   `set()` 自历元值和相关字段以来的毫秒数无效（更改DATE显然会使DAY\_OF\_WEEK无效）
*   `setTimeZone()` 使所有字段均无效，从纪元值开始执行的毫秒数
*   `get(), getTime(), getTimeInMillis(), add(), roll()` 从字段重新计算自纪元以来的毫秒数
*   `get(), add()` 还会重新计算自纪元以来的毫秒数内的无效字段

当您更改与字段`set()`，然后dependend领域没有得到更新，直到你打电话 `get()`，`getTime()`，`getTimeInMillis()`，`add()`，或`roll()`。上面代码调用的第一段，`set()`后跟`before()`。根据API文档，不能保证before（）会看到修改后的时间值。

第二段通过调用`setTimeZone()` 和`set()`，使历元值后的所有字段和毫秒无效，从而完全丢失日历的数据。另请参见[错误4827490](http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=4827490)

日历对象应始终根据以下简单规则进行操作：

*   在构造函数中已经初始化了TimeZone（如果需要，还可以初始化Locale）
*   通话后将通话`set()`添加到`getTimeInMillis()`
*   通话后将通话`setTimeZone()`添加到`get()`
```
GregorianCalender cal = new GregorianCalender(TimeZone.getTimeZone("Europe/Zurich"));
cal.set(Calendar.SECOND, 0);
cal.set(Calendar.MILLISECOND, 0);
cal.getTimeInMillis();
if (cal.before(other)) doSomething();

cal.setTimeZone(TimeZone.getTimeZone("GMT"));
cal.get(Calendar.DATE);
cal.set(Calendar.HOUR\_OF\_DAY, 23);
Date d = cal.getTime();
```
### 调用Date.setTime（）
```
account.changePassword(oldPass, newPass);
Date lastmod = account.getLastModified();
lastmod.setTime(System.currentTimeMillis());
```
上面的代码更新了帐户实体的最后修改日期。程序员希望保持保守，并避免创建新`Date`对象。相反，她使用的 `setTime`方法来修改现有`Date`实例。

实际上，这没有错。但我只是不推荐这种做法。日期对象通常会粗心传递。可以将同一Date实例传递给许多对象，这些对象不会在其设置器中进行复制。日期通常像图元一样使用。因此，如果您修改Date实例，则使用该实例的其他对象可能会出现异常情况。当然，如果您编写的代码严格遵循经典的OO原理（我认为这很不方便），那么如果对象将其固有的Date实例暴露给外界，那将是不干净的设计。但是，常规的日常Java做法是仅复制Date引用，而不用setter克隆对象。因此，每个程序员都应将Date视为不可变的，并且不应修改现有实例。仅出于特殊情况下的性能原因，才应这样做。即使那样简单的使用`long` 可能同样好。
```
account.changePassword(oldPass, newPass);
account.setLastModified(new Date());
```
### 假设SimpleDateFormat是线程安全的
```
public class Constants {
    public static final SimpleDateFormat date = new SimpleDateFormat("dd.MM.yyyy");
}
```
上面的代码有几种缺陷。坏了，因为它与任何数量的线程共享一个SimpleDateFormat的静态实例。SimpleDateFormat不是线程安全的。如果多个线程同时使用此对象，则结果是不确定的。您可能会发现从输出陌生`format`和`parse`甚至例外。不幸的是，这个错误很常见！

是的，共享SimpleDateFormat需要正确的同步。是的，需要付出一定的代价（缓存刷新，锁争用等）。是的，创建SimpleDateFormat也不是免费的（模式解析，对象分配）。但是，简单地忽略线程安全性不是解决方案，而是破解代码的肯定方法。

当然，此代码也没有考虑时区。然后定义一个名为“ Constants”的类，它发出另一个反模式的尖叫（请参阅下一节）。

### 具有全局Configuration / Parameters / Constants类
```
public interface Constants {
    String version = "1.0";
    String dateFormat = "dd.MM.yyyy";
    String configFile = ".apprc";
    int maxNameLength = 32;
    String someQuery = "SELECT \* FROM ...";
}
```
在大型项目中经常见到：一个类或接口，包含在整个应用程序中使用的各种常量。为什么这样不好？因为这些常量彼此无关。此类是他们唯一的共同点。对该类的引用将再次污染应用程序的许多不相关组件。您要稍后提取一个组件并在其他应用程序中使用它吗？还是在服务器和远程客户端之间共享一些类？您可能还需要提供常量类！此类在其他不相关的组件之间引入了依赖关系。这抑制了重用和松耦合，并让混乱。

而是将常量放在它们所属的位置。在任何情况下，均不得跨组件边界使用常量。仅当组件是需要显式依赖的库时才允许这样做。

### 没有注意到溢出
```
public int getFileSize(File f) {
  long l = f.length();
  return (int) l;
}
```
无论出于何种原因，该开发人员都将确定文件大小的调用包装到返回`int`而不是的方法中`long`。此代码不支持大于2 GB的文件，在这种情况下只会返回错误的长度。将值强制转换为较小大小类型的代码必须首先检查可能的溢出并引发异常。
```
public int getFileSize(File f) {
  long l = f.length();
  if (l > Integer.MAX\_VALUE) throw new IllegalStateException("int overflow");
  return (int) l;
}
```
以下是溢出错误的另一个版本。请注意第一个println语句中缺少的括号。
```
long a = System.currentTimeMillis();
long b = a + 100;
System.out.println((int) b-a);
System.out.println((int) (b-a)); 
```
最后，是我在代码审查过程中连根拔起的真正瑰宝。请注意程序员是如何尝试小心的，但随后由于假设一个int可能变得大于其最大值而严重失败。
```
int a = l.size();
a = a + 100;
if (a > Integer.MAX\_VALUE)
    throw new ArithmeticException("int overflow");
```
### 将==与float或double一起使用
```
for (float f = 10f; f!=0; f-=0.1) {
  System.out.println(f);
}
```
上面的代码无法正常工作。它导致无限循环。因为0.1是一个 [无限的二进制十进制数](http://www.binaryconvert.com/result_float.html?decimal=048046049)，所以`f`永远不会完全为0。通常，您永远不要将浮点或双精度值与相等运算符==进行比较。始终使用小于或大于。在这种情况下，应更改Java编译器以发出警告。甚至使Java语言规范中的浮点类型的==非法操作成为可能。拥有此功能真的没有任何意义。
```
for (float f = 10f; f>0; f-=0.1) {
  System.out.println(f);
}
```
### 将钱存入浮点变量
```
float total = 0.0f;
for (OrderLine line : lines) {
  total += line.price \* line.count;
}

double a = 1.14 \* 75; // 85.5 represented as 85.4999...
System.out.println(Math.round(a)); // surprising output: 85
System.out.println(10.0/3); // surprising output: 3.333333333333333**5** (precision lost twice during division and on conversion to decimal)

BigDecimal d = new BigDecimal(1.14); // precision has already been lost
```
我已经看到许多开发人员编写了这样的循环。包括我早年的我自己。当此代码将100条订单行相加，每行包含一个0.30 $项时，得出的总和将精确计算为29.999971。开发人员注意到异常行为，并将float更改为更精确的double值，仅得到结果30.000001192092896。当然，由于人（十进制格式）和计算机（二进制格式）在数字表示上的差异，有些令人惊讶的结果。当您增加零用钱或计算增值税时，它总是以其最令人讨厌的形式出现。

对于固有的_不精确_ 值（例如测量值），发明了浮点数的二进制表示形式。完美的工程！但是当您需要精确的数学运算时无法使用。像银行。或数数时。

在某些业务案例中，您不能失去精确度。在十进制和二进制之间进行转换时，以及在舍入方式不明确或不明确的点上进行舍入时，您将失去精度。为了避免精度下降，您必须使用定点或整数运算。这不仅适用于货币价值，而且在业务应用程序中经常引起烦恼，因此是一个很好的例子。在第二个示例中，程序的一个毫无戒心的用户只会说计算机的计算器坏了。对于程序员来说，这当然是很尴尬的。

因此，_永远不要_以浮点数据类型（浮点数，双精度数）存储金额。请注意，不仅任何计算都是不精确的。即使是简单的整数乘法也可能产生不精确的结果。仅以二进制表示形式（浮点数，双精度）_存储_值的事实 可能已经导致了舍入！ _您根本无法将0.3作为精确值存储在float或double中_。因为float和double是[二进制IEEE754](http://en.wikipedia.org/wiki/Binary64)类型。另请参阅[此处](http://0.30000000000000004.com/)。您可以在[此处尝试](http://www.binaryconvert.com/result_float.html?decimal=049046049052)各种数字及其 [二进制表示形式](http://www.binaryconvert.com/result_float.html?decimal=049046049052)。如果您在财务代码库中看到浮动或双精度，则该代码很可能会产生不精确的结果。相反，应该选择字符串或定点表示形式。文本表示形式必须采用定义明确的格式，并且_不得_与区域设置特定格式的用户输入/输出混淆。两种表示形式都必须定义所存储的精度（小数点前后的位数）。

为了进行计算，[BigDecimal](http://java.sun.com/j2se/1.5.0/docs/api/java/math/BigDecimal.html)类 提供了一种出色的工具。可以使用该类，以便在操作中意外丢失精度时引发运行时异常。这对于消除细微的数字错误非常有用，并使开发人员可以更正计算结果。
```
BigDecimal total = BigDecimal.ZERO;
for (OrderLine line : lines) {
  BigDecimal price = new BigDecimal(line.price);
  BigDecimal count = new BigDecimal(line.count);
  total = total.add(price.multiply(count)); // BigDecimal is immutable!
}
total = total.setScale(2, RoundingMode.HALF\_UP);

BigDecimal a = (new BigDecimal("1.14")).multiply(new BigDecimal(75)); // 85.5 exact
a = a.setScale(0, RoundingMode.HALF\_UP); // 86
System.out.println(a); // correct output: 86

BigDecimal a = new BigDecimal("1.14");
```
### 在finally块中不释放资源
```
public void save(File f) throws IOException {
  OutputStream out = new BufferedOutputStream(new FileOutputStream(f));
  out.write(...);
  out.close();
}

public void load(File f) throws IOException {
  InputStream in = new BufferedInputStream(new FileInputStream(f));
  in.read(...);
  in.close();
}
```
上面的代码打开输出流到文件，在操作系统中分配文件句柄。文件句柄是一种稀有资源，需要通过在FileOutputStream上调用close来正确释放（当然，与FileInputStream相同）。为了确保即使发生异常（在写操作期间文件系统可能已满），也必须在finally块中进行关闭。在此，流还被包装到缓冲流中。这意味着到我们到达磁盘时，并非所有数据都已被写入磁盘。`close()`呼叫。close调用本身会将缓冲区中的待处理数据刷新到磁盘，因此自身可能会失败并出现IOException。如果关闭失败，则磁盘上的文件不完整（被截断），因此很可能已损坏。因此，在这种情况下，该方法应传播IOException。对于FileInputStream，我们可以从close（）调用中安全地忽略潜在的IOException。我们已经读取了所需的所有数据，并且如果底层的close（）仍然失败，我们将无能为力。甚至不值得记录它。

在一个完美的世界`BufferedOutputStream.close()`中将正确实施。但是可悲的是，它有一个无法[修复的错误](http://bugs.sun.com/view_bug.do?bug_id=6335274)：它从隐式刷新中丢失了任何IOException，并以静默方式截断了文件。因此，在这里，我们在关闭之前使用显式刷新给出适当的解决方法。

确切地说，下面的更正代码可能会在一个很小的情况下泄漏：分配文件流但随后分配缓冲的流神秘地失败（例如，内存不足）。作为一个务实的人，我认为在这种病态的情况下，我们可以安全地依靠垃圾收集器来清理垃圾。处理它是不值得的麻烦。
```
// code for your cookbook
public void save() throws IOException {
  File f = ...
  OutputStream out = new BufferedOutputStream(new FileOutputStream(f));
  try {
    out.write(...);
    out.flush(); // don't lose exception by implicit flush on close
  } finally {
    out.close();
  }
}

public void load(File f) throws IOException {
  InputStream in = new BufferedInputStream(new FileInputStream(f));
  try {
    in.read(...);
  } finally {
    try { in.close(); } catch (IOException e) { }
  }
}
```
让我也为您提供另一种普遍使用的菜谱：数据库访问。同样，这是实用的方法。是的，rs.close（）可能会因神秘的错误而失败，除非它们仅出现在您关于量子力学的大学讲座中，而不是出现在《真实世界》（tm）中。而且只有变态者才会写出尝试/最终级联，即没有错误中微子无法逃脱。原谅我的嘲讽。一劳永逸的方法是处理SQL对象：
```
Car getCar(DataSource ds, String plate) throws SQLException {
  Car car = null;
  Connection c = null;
  PreparedStatement s = null;
  ResultSet rs = null;
  try {
    c = ds.getConnection();
    s = c.prepareStatement("select make, color from cars where plate=?");
    s.setString(1, plate);
    rs = s.executeQuery();
    if (rs.next()) {
       car = new Car();
       car.make = rs.getString(1);
       car.color = rs.getString(2);
    }
  } finally {
    if (rs != null) try { rs.close(); } catch (SQLException e) { }
    if (s != null) try { s.close(); } catch (SQLException e) { }
    if (c != null) try { c.close(); } catch (SQLException e) { }
  }
  return car;
}
```
话虽如此，不要错过下一段。

### 滥用finalize（）
```
public class FileBackedCache {
   private File backingStore;
   
   ...
   
   protected void finalize() throws IOException {
      if (backingStore != null) {
        backingStore.close();
        backingStore = null;
      }
   }
}
```
此类使用该`finalize`方法来释放文件句柄。问题是您不知道何时调用该方法。该方法由垃圾收集器调用。如果您用完了文件句柄，则希望此方法尽快被调用。但是GC可能只会在堆快用完时才调用该方法，这是非常不同的情况。从GC到完成定稿，可能需要几毫秒到几天的时间。垃圾收集器仅管理内存。它做得很好。但是，不得滥用它来管理除此之外的任何其他资源。**GC不是通用的资源管理机制！**在这方面，我发现Sun的finalize方法的API Doc非常令人误解。它实际上建议使用此方法关闭I / O资源-如果您问我，请完全废话。再次：I / O 与内存_无关_！

更好的代码提供了一个公共关闭方法，必须由定义良好的生命周期管理（例如JBoss MBeans）调用。
```
public class FileBackedCache {
   private File backingStore;
   
   ...
   
   public void close() throws IOException {
      if (backingStore != null) {
        backingStore.close();
        backingStore = null;
      }
   }
}
```
JDK 1.7（Java 7）引入了[AutoClosable](http://download.java.net/jdk7/docs/api/java/lang/AutoCloseable.html)接口。`close`当变量（不是对象）超出try-with-resource块的范围时，它启用对方法的自动调用。它与终结器有很大不同。它的执行时间在编译时已明确定义。
```
try (Writer w = new FileWriter(f)) { // implements Closable
  w.write("abc");
  // w goes out of scope here: w.close() is called automatically in ANY case
} catch (IOException e) {
  throw new RuntimeException(e.getMessage(), e);
}
```
### 不由自主地重置Thread.interrupted
```
try {
	Thread.sleep(1000);
} catch (InterruptedException e) {
	// ok
}

or 

while (true) {
	if (Thread.interrupted()) break;
}
```
上面的代码重置线程的中断标志。随后的读者将不知道该线程已被中断。如果您需要传递有关中断的信息，请像这样重写代码。
```
try {
	Thread.sleep(1000);
} catch (InterruptedException e) {
	Thread.currentThread().interrupt();
}

or 

while (true) {
	if (Thread.currentThread().isInterrupted()) break;
}
```
### 来自静态初始值设定项的生成线程
```
class Cache {
	private static final Timer evictor = new Timer();
}
```
java.util.Timer在其构造函数中增加了一个新线程。因此，以上代码在其静态初始化程序中产生了一个新线程。新线程将从其父级继承一些属性：上下文类加载器，可继承的ThreadLocals和一些安全属性（访问权限）。因此，很少希望以不受控制的方式设置这些属性。例如，这可能会阻止类加载器的GC。

静态初始化程序由首先加载类的线程（在任何给定的ClassLoader中）执行，该线程可以是例如来自Web服务器线程池的完全随机的线程。如果要控制这些线程属性，则必须在静态方法中启动线程，并控制谁在调用该方法。
```
class Cache {
    private static Timer evictor;

	public static setupEvictor() {
		evictor = new Timer();
	}
}
```
### 取消了保持状态的计时器任务
```
final MyClass callback = this;
TimerTask task = new TimerTask() {
	public void run() {
		callback.timeout();
	}
};
timer.schedule(task, 300000L);

try {
	doSomething();
} finally {
	task.cancel();
}
```
上面的代码使用计时器在doSomething（）上强制超时。TimerTask包含一个对外部类的（隐式）实例引用。因此，只要TimerTask存在，就不会对MyClass的实例进行GC处理。不幸的是，Timer可能会一直取消被取消的TimerTasks，直到它们的预定超时时间结束！这会使程序有5分钟的时间悬空地引用MyClass实例，在此期间它无法被收集！这是暂时的内存泄漏。更好的TimerTask会覆盖cancel（）方法，并在那里引用无效。它需要更多的代码。
```
TimerTask task = new Job(this);
timer.schedule(task, 300000L);

try {
	doSomething();
} finally {
	task.cancel();
}


static class Job extends TimerTask {
	private volatile MyClass callback;

	public Job(MyClass callback) {
		this.callback = callback;
	}

	public boolean cancel() {
		callback = null;
		return super.cancel();
	}

	public void run() {
		MyClass cb = callback;
		if (cb == null) return;
		cb.timeout();
	}
}
```
### 拥有对ClassLoader和无法刷新的缓存的强大引用

在像应用程序服务器或OSGI这样的动态系统中，应格外小心，不要阻止ClassLoader进行垃圾回收。在应用程序服务器中取消部署和重新部署各个应用程序时，将为它们创建新的类加载器。旧的未使用，应该收集。如果从容器代码到您的应用程序代码中只有一个悬挂引用，那么Java不会让这种情况发生。

由于在整个企业应用程序中使用了各种库，因此直接意味着，库应尽其最大努力，不要保留对对象（以及它们的类加载器）的非自愿强引用。

这不容易。诸如`java.beans.Introspector`来自JDK或 `org.apache.commons.beanutils.PropertyUtils`来自Apache BeanUtils或 `org.springframework.beans.CachedIntrospectionResults`来自Spring的类实现了缓存，以加速其内部工作。它们对您传递给它们进行分析的类保持强烈的引用。幸运的是，它们提供了刷新其缓存的方法。但是，找到所有可能具有内部缓存的类并在适当的时间刷新它们对于开发人员来说几乎是不可能的工作。

如果您碰巧是`org.apache.commons.el.BeanInfoManager`从Apache Commons EL 使用的，则可能存在泄漏。这个古老的类保留了强大的引用缓存，这些引用只会在内存不足之前不断增长。而且它没有冲洗方法。甚至Tomcat也必须实现一种涉及反射的 [变通办法](http://issues.apache.org/bugzilla/attachment.cgi?id=18538&action=diff)以对其进行清理。

如果这些库首先只使用软引用或弱引用，那就更好了。快速提醒：

软引用和弱引用在其为零的时间点上基本上有所不同。

*   WeakReference：在最后一个对对象的强引用消失时，或多或少同时将其为null。典型用于类加载器引用（如果没有类加载器，则类加载器有什么用）。但是，如果_在_ ClassLoader实现中使用它_，_则要小心。
*   SoftReference：只要内存允许，即使最后一个对对象的强引用消失，该引用也会保留。典型用于缓存。

仅当库仅从其自己的包中缓存对象（没有外部引用）时，最好不使用这些特殊引用，而仅使用普通引用。

使用软引用或弱引用也有助于应用程序的运行时行为：如果内存变紧，则要在内存上花费的最后一件事就是缓存。因此，垃圾收集器将在必要时回收缓存使用的内存。这里的一个不好的例子是JBoss的SQL语句缓存：它是完全静态的，并且即使在很紧的情况下也可以使用很多内存。另一个不好的例子是JBoss的身份验证缓存。

而且，每个静态缓存都必须始终提供一种刷新其内容的简单方法。（干净的）缓存（与例如写入缓存相反）的本质是其内容不重要，可以随时安全地丢弃。缓存的限制是另一个陷阱。高速缓存永远都不会变大，也永远不会高速缓存对象。这是一个非常糟糕的示例，它是JDK DNS缓存的默认设置（它完全忽略DNS记录的生存期，并将否定查询永远存储在无边界列表中）。您的API文档应说明是否以及何时进行缓存。这也有助于用户估计运行时性能。

### 嵌套同步语句
```
class Message {
  private long id;
  ...
  public synchronized int compareTo(Message that) {
    synchronized (that) {
      return Long.compare(id, that.id);
    }
  }
}
```
上面的代码想提供一个线程安全的compareTo（）方法。开发人员意识到对id字段的访问需要在所属实例上进行同步。因此，这里有两个嵌套的同步语句，一个用于保护this.id，一个用于保护that.id。不幸的是，该代码在被多个线程使用时会迅速死锁。我们想在这里支持多线程。当线程1 `a.compareTo(b)`和线程2都这样做时， `b.compareTo(a)`它们将尝试以相反的顺序获得对a和b的锁定，并且将死锁。记住锁定规则一：所有线程必须始终以相同的顺序进行锁定。我们可以重写该方法，以便完全不嵌套同步语句。
```
public int compareTo(Message that) {
  long a;
  long b;
  synchronized (this) {
    a = this.id;
  }
  synchronized (that) {
    b = that.id;
  }
  return Long.compare(a, b);
}
```
### 通过RandomAccessFile进行随机文件访问
```
RandomAccessFile raf = new RandomAccessFile(f, "r");
for (...) {
  raf.seek(pos);
  byte b = raf.readByte();
}
```
尽管它的名称如此，但`java.io.RandomAccessFile`该类不太适合以随机访问的方式访问文件。即：查找，读取，查找，读取等。这些命令中的每一个都直接在文件描述符上发出相应的系统调用/ ioctl。每个C程序员都知道这种文件访问速度很慢，应将其替换为内存映射文件访问。您可以通过MappedByteBuffer在Java中完成此操作。在我的笔记本电脑上，速度快了50倍。
```
FileInputStream in = new FileInputStream(f);
MappedByteBuffer map = in.getChannel().map(MapMode.READ\_ONLY, 0, f.lengt());
for (...) {
  byte b = map.get(pos);
}
```