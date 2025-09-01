---
title: 每个Web开发者都应掌握的URL编码知识
id: 3f2fd56a-3628-420f-8d81-3d80d927f6ef
date: 2024-12-12 16:47:23
author: daichangya
excerpt: "一、URL编码简介 在Web开发领域，URL编码是一项至关重要但又常常被误解的技术。URL作为互联网上资源的地址标识，其编码方式直接影响着数据的正确传输与解析。从我们日常上网冲浪开始，URL就无处不在，比如“"
permalink: /archives/mei-ge-webkai-fa-zhe-du-ying-zhang-wo-de-urlbian-ma-zhi-shi/
categories:
 - 其他
---

## 一、URL编码简介
在Web开发领域，URL编码是一项至关重要但又常常被误解的技术。URL作为互联网上资源的地址标识，其编码方式直接影响着数据的正确传输与解析。从我们日常上网冲浪开始，URL就无处不在，比如“http://www.google.com”，它看似简单，实则有着严格定义的结构。一个完整的URL包含了协议（scheme）、主机地址（host address）、端口（port）、路径（path）、路径参数（path parameters）、查询参数（query parameters）以及片段（fragment）等部分。然而，在处理URL时，开发者往往会遇到诸多陷阱，因此深入理解URL编码对于构建稳定、高效的Web应用程序至关重要。

### （一）通用URL语法
1. **基本结构剖析**
   - URL的基本结构由多个部分组成，以“https://bob:bobby@www.lunatech.com:8080/file;p=1?q=2#third”为例，其中“https”是协议，定义了后续部分的结构和通信方式；“bob”为用户，“bobby”是密码（这种包含用户和密码的形式在实际中并不常见于普通URL，但在特定场景下存在）；“www.lunatech.com”是主机地址；“8080”为端口号；“/file”是路径，表示资源在服务器上的位置；“p=1”是路径参数；“q=2”是查询参数；“third”是片段，用于指向HTML文件中的特定部分。
2. **协议的作用**
   - 协议决定了URL中其余部分的组织方式，不同协议如HTTP、HTTPS、FTP等，对主机名、端口、路径等的定义和使用方式有所不同。例如，HTTP协议主要用于Web资源的传输，而FTP协议用于文件传输。

### （二）HTTP URL语法
1. **路径结构与示例**
   - HTTP URL中的路径部分类似于文件系统的分层结构，以“/photos/egypt/cairo/first.jpg”为例，“photos”是根文件夹，“egypt”在“photos”下，“cairo”在“egypt”下，“first.jpg”是最终的文件。每个路径片段可以有可选的路径参数，如“/file;p=1”，其中“p”是参数名，“1”是参数值。
2. **查询参数的使用**
   - 查询部分紧跟在路径后，以“?”隔开，包含多个以“&”分隔的参数。例如“/file?q=2”，“q”是查询参数名，“2”是参数值。在提交HTML表单或进行搜索时经常使用查询参数，如在Google搜索中，用户输入的关键词等信息就是通过查询参数传递给服务器的。
3. **片段的功能**
   - 片段部分用于指定HTML文件中的具体位置，当点击包含片段的链接时，浏览器会自动滚动到页面相应位置，而不是从顶部开始显示。比如在一个长页面中，通过片段可以快速定位到某个章节或特定内容。
<separator></separator>
### （三）URL编码的原理
1. **编码规则**
   - URL编码将特殊字符转换为对URL解析无意义的无害形式。具体做法是将字符转换为特定字符编码（如UTF - 8）的字节序列，然后将字节转换为十六进制形式，并在前面加上“%”。例如，问号“?”的URL编码形式为“%3F”。
2. **浏览器中的编码和解码**
   - 多数浏览器在显示URL前会对其解码，将百分号编码字节转回原本字符，在获取网络资源时又会重新编码。这一过程对用户来说通常是透明的，但开发者必须清楚其背后的机制，以避免出现编码问题。

## 二、URL常见陷阱

### （一）字符编码的选择
1. **问题阐述**
   - URL编码规范未明确规定使用何种字符编码，这导致了混乱。虽然ASCII字母数字字符一般无需转义，但ASCII之外的保留字（如法语单词“nœud”中的“œ”）需要编码。而Unicode虽然包含所有字符，但它本身不是一种编码，其多种编码方式（如UTF - 8、UTF - 16等）又让开发者面临选择难题。对于HTTP URL，其编码方式可能取决于HTML页面编码格式或HTTP头，这使得编码的确定变得复杂，容易引发错误。
2. **示例说明**
   - 假设一个URL中包含中文字符，如果编码方式选择不当，可能导致服务器无法正确解析该URL，从而无法获取正确的资源。

### （二）保留字符集的复杂性
1. **不同部分的保留字符差异**
   - 在URL的不同部分，保留字符集各不相同。例如在路径片段部分，空格被编码为“%20”，“+”字符可保持不编码；而在查询部分，空格可能被编码为“+”（为向后兼容）或“%20”，“+”作为通配符结果会被编译为“%2B”。这意味着相同的字符在不同部分编码方式不同，如“blue+light blue”在路径和查询部分会有不同编码形式。
2. **保留字符的实际情况**
   - 许多开发者对保留字符存在误解，比如“+”在路径部分被允许且表示正号而非空格，“?”在查询部分允许不被转义等。像“http://example.com/:@ -._~!$&'()* +, =;:@ -._~!$&'()* +, =:@ -._~!$&'()* +, ==?/?:@ -._~!$'()* +, ;=/?:@ -._~!$'()* +, ;==#/?:@ -._~!$&'()* +, ;=”这样看似混乱的地址，按照规则却是合法的，其路径部分可解析为特定的值。

### （三）解码后的URL问题
1. **无法解析的情况**
   - URL的语法在解码前有意义，解码后可能出现保留字导致解析错误。例如“http://example.com/blue%2Fred%3Fand+green”，解码前路径片段为“blue%2Fred%3Fand+green”，解码后变为“blue/red?and+green”，原本请求的是一个名为“blue%2Fred%3Fand+green”的文件，解码后却被错误解析为“blue”文件夹下名为“red?and+green”的文件，以及查询参数“and green”。
2. **无法重新编码为相同形式**
   - 若将“http://example.com/blue%2Fred%3Fand+green”解码为“http://example.com/blue/red?and+green”后再编码，得到的将是“http://example.com/blue/red?and+green”，与解码前的URL不同，这是因为解码后的URL已成为有效URL，再次编码不会还原为原始形式。

## 三、在Java中正确处理URL

### （一）避免使用错误的编码类
1. **问题所在**
   - `java.net.URLEncoder`和`java.net.URLDecoder`类并非用于编码或解码整个URL。其API文档明确指出，它们主要用于HTML表单编码，类似于查询部分的编码方式。使用它们来处理整个URL是错误的，尽管许多开发者误以为JDK中有标准类可正确处理URL编码（实际上是各部分分开处理），从而错用了`URLEncoder`。
2. **正确做法示例**
   - 假设要构建一个包含路径片段“a/b?c”的URL，错误的做法是：
```java
String pathSegment = "a/b?c";
String url = "http://example.com/" + pathSegment;
```
   - 正确的做法是使用专门的工具类（如自定义的`URLUtils`）对路径片段进行编码：
```java
String pathSegment = "a/b?c";
String url = "http://example.com/" + URLUtils.encodePathSegment(pathSegment);
```
   - 这样可以得到正确编码的URL“http://example.com/a%2Fb%3Fc”。同样，对于查询子串也需注意，如：
```java
String value = "a&b==c";
String url = "http://example.com/?query=" + value;
```
   - 这会得到错误的URL，应改为：
```java
String value = "a&b==c";
String url = "http://example.com/?query=" + URLUtils.encodeQueryParameter(value);
```

### （二）注意URI相关方法的使用
1. **`URI.getPath()`的问题**
   - `URI.getPath()`方法在处理URL时存在缺陷。一旦URL被解码，句法信息可能丢失。例如：
```java
URI uri = new URI("http://example.com/a%2Fb%3Fc");
for(String pathSegment : uri.getPath().split("/"))
  System.err.println(pathSegment);
```
   - 上述代码会先将路径“a%2Fb%3Fc”解码为“a/b?c”，然后在不应该分割的地方（如“?”处）将地址分割为地址片段，导致错误结果。
2. **正确使用示例**
   - 正确的做法是使用`URI.getRawPath()`方法获取未解码的路径，并在需要时手动处理路径参数：
```java
URI uri = new URI("http://example.com/a%2Fb%3Fc");
for(String pathSegment : uri.getRawPath().split("/"))
  System.err.println(URLUtils.decodePathSegment(pathSegment));
```

### （三）Apache Commons HTTPClient的问题
1. **问题描述**
   - Apache Commons HTTPClient 3的`URI`类使用`Apache Commons Codec`的`URLCodec`进行URL编码，这存在问题。它犯了与使用`java.net.URLEncoder`同样的错误，不但使用了错误的编码器，还错误地按照每一部分都具有同样的预定设置进行解码。
2. **影响及解决方案**
   - 这种错误的编码和解码方式可能导致URL在传输和处理过程中出现问题，如无法正确解析或与其他系统交互。开发者在使用时应谨慎，若可能，尽量避免使用该类的默认编码方式，或者寻找替代方案来确保URL编码的正确性。

## 四、在Web应用程序的每个层次处理URL编码问题

### （一）创建URL时进行编码
1. **HTML文件中的编码示例**
   - 在HTML文件中，对于动态生成URL的地方，要确保正确编码。例如，将：
```html
var url = "#{vl:encodeURL(contextPath + '/view/' + resource.name)}";
```
   - 替换为：
```html
var url = "#{contextPath}/view/#{vl:encodeURLPathSegment(resource.name)}";
```
   - 这样可以对路径片段进行正确编码。对于查询参数也应采用类似的方式，确保每个部分都按照正确的规则进行编码，避免因编码错误导致链接失效或资源获取错误。

### （二）确保URL重写过滤器正确处理
1. **Url重写过滤器的作用与问题**
   - Url重写过滤器用于将漂亮的地址转换为应用依赖的网址，但在处理过程中涉及URL解码和重新编码，容易出现问题。例如，将“http://beta.visiblelogistics.com/view/resource/FOO/bar”转换为“http://beta.visiblelogistics.com/resources/details.seam?owner=FOO&name=bar”的过程中，需要从路径部分解码并重新编码为查询值部分。
2. **正确配置示例**
   - 最初的规则可能如下：
```xml
<urlrewrite decode-using="utf-8">
<rule>
<from> ^/view/resource/(.*)/(.*)$</from>
<to encode="false">/resources/details.seam?owner=$1&name=$2</to>
</rule>
</urlrewrite>
```
   - 这种方式在重写过滤器中只有两种处理网址重写的方法：先解码网址做规则匹配或不进行解码直接处理。更好的选择是后者，特别是在移动网址部分或包含URL解码路径分隔符的匹配路径部分时。同时，可以使用内建函数`escape(String)`和`unescape(String)`处理网站转码和解码，但在撰写文章时，Url Rewrite Filter Beta 3.2存在一些限制，如网址解码使用`java.net.URLDecoder`（错误的方式），`escape(String)`和`unescape(String)`内建函数使用`java.net.URLDecoder`和`java.net.URLEncoder`（不够强大，无法处理所有情况）。
   - 经过修正后的规则可以这样写：
```xml
<urlrewrite decode-using="null">
<rule>
<from> ^/view/resource/(.*)/(.*)$</from>
<to encode="false">/resources/details.seam
?owner=${escape:${unescapePath:$1}}
&name=${escape:${unescapePath:$2}}</to>
</rule>
</urlrewrite>
```
   - 不过，仍存在一些问题需要进一步解决，如内建函数的编码功能应更完善，需要从http请求确定编码方式，保留的旧函数仍有问题，需要增加更多局部特定的编码和解码函数以及鉴别per - rule解码行为的方法等。

### （三）正确使用Apache mod - rewrite
1. **Apache mod - rewrite的功能与问题**
   - Apache mod - rewrite是Apache Web服务器的网址重写模块，可用于流量代理等操作，如将“http://beta.visiblelogistics.com/foo”的流量代理到“http://our - internal - server:8080/vl/foo”。但它默认会解码网址并重新编码重写后的网址，这是错误的，因为解码后的网址不能被重新编码为原始形式。
2. **解决方法示例**
   - 一种避免错误的方法是通过`THE_REQUEST`来进行网址匹配。例如：
```apacheconf
# 允许路径片段中的URL编码斜杠
AllowEncodedSlashes On
# 启用mod - rewrite
RewriteEngine on
# 使用THE_REQUEST不解码URL，因为不需要将URI部分移动到其他部分，所以无需解码/重新编码
RewriteCond %{THE_REQUEST} "^[a-zA-Z]+ /(.*) HTTP/\d\.\d$"
RewriteRule ^(.*)$ http://our - internal - server:8080/vl/%1 [P,L,NE]
```
   - 这样可以在不进行不必要的解码和重新编码的情况下完成网址重写操作，确保URL的正确性和稳定性。

## 五、总结与展望
URL编码在Web开发中虽然看似基础，但其中的细节和陷阱众多。开发者需要深入理解URL的语法结构、编码规则以及在不同场景下的正确处理方式，从Java代码中的URL构建到Web应用程序各个层次（如HTML文件、URL重写过滤器、Apache服务器模块等）的处理，都要确保编码的准确性。只有这样，才能构建出稳定、可靠的Web应用程序，避免因URL编码问题导致的各种错误和故障。同时，也希望相关技术标准能够不断完善，为开发者提供更便捷、准确的URL编码处理支持。