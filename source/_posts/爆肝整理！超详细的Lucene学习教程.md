---
title: 爆肝整理！超详细的Lucene学习教程
id: e207b549-9755-4fe4-887f-2061a6633371
date: 2024-12-09 16:17:25
author: daichangya
cover: https://images.jsdiff.com/Lucene.jpg
excerpt: "一、Lucene简介 1.1 什么是Lucene Lucene是一个强大的全文搜索框架，并非拿来即用的应用产品，而是提供了实现如百度、谷歌桌面搜索等产品的工具。 1.2 Lucene能做什么 Lucene功能看似单一，实则潜力无限。它允许输入若干字符串，提供全文搜索服务，能精准定位关键词位置。利用L"
permalink: /archives/bao-gan-zheng-li-chao-xiang-xi-de-lucenexue-xi-jiao-cheng/
categories:
 - 文件索引
---

## 一、Lucene简介
### 1.1 什么是Lucene
Lucene是一个强大的全文搜索框架，并非拿来即用的应用产品，而是提供了实现如百度、谷歌桌面搜索等产品的工具。

### 1.2 Lucene能做什么
Lucene功能看似单一，实则潜力无限。它允许输入若干字符串，提供全文搜索服务，能精准定位关键词位置。利用Lucene，我们可以为站内新闻建立索引，打造专属资料库；索引数据库表字段，避免“%like%”导致的锁表问题；甚至开发个人搜索引擎。

### 1.3 你该不该选择Lucene
以下是一些测试数据供参考，若能接受，则可选择Lucene：
- 测试一：250万记录，约300M文本，生成约380M索引，800线程下平均处理时间300ms。
- 测试二：37000记录，索引数据库两个varchar字段，索引文件2.6M，800线程下平均处理时间1.5ms。

## 二、Lucene的工作方式
Lucene提供的服务包含写入和读出两部分。

### 2.1 写入流程
1. 源字符串经analyzer处理，包括分词（将字符串分成单词）和去除stopword（可选操作）。
2. 将源中必要信息加入Document的各个Field，按需索引和存储Field。
3. 把索引写入存储器（内存或磁盘）。

### 2.2 读出流程
1. 用户提供的搜索关键词经analyzer处理。
2. 用处理后的关键词搜索索引，找到对应的Document。
3. 用户根据需求从找到的Document中提取所需Field。

## 三、关键概念解读
### 3.1 Analyzer（分析器）
分析器将字符串按规则分词并去除无效词，如英文“of”、“the”，中文“的”、“地”等。其目的是按语义划分，英文因以单词为单位且空格分隔，分词较易；中文则需特定方法。例如，对于句子“我爱北京天安门”，分析器会将其分词，去除无效词后得到“我爱 北京 天安门”（假设的理想分词结果）。

### 3.2 Document（文档）
用户提供的源数据（如文本文件、字符串或数据库记录）经索引后以Document形式存储在索引文件中，搜索结果也以Document列表返回。比如一篇新闻文章，经Lucene处理后就是一个Document。

### 3.3 Field（字段）
一个Document可包含多个Field，如文章的“标题”“正文”“最后修改时间”等。Field有存储和索引两个属性，通过不同组合满足需求。以文章为例，若要对标题和正文全文搜索，需将它们的索引属性设为真；若希望直接从搜索结果提取标题，则标题域存储属性为真，正文域因太大可设为假，需要时再读取文件；仅提取最后修改时间则其存储属性为真，索引属性为假。

### 3.4 Term（词项）
Term是搜索最小单位，表示文档中的一个词语，由词语及其所在field组成。如在一篇关于旅游的文章中，“风景”这个词在正文中出现，那么“风景”和“正文”就构成一个Term。

### 3.5 Tocken（标记）
Tocken是Term的一次出现，包含term文本、起止偏移和类型字符串。同一句话中相同词语多次出现用同一Term表示，但不同位置用不同Tocken标记。例如“我爱北京天安门，天安门上太阳升”，“天安门”出现两次，是同一个Term，但两个位置分别有不同的Tocken。

### 3.6 Segment（段）
添加索引时，document先写入小文件（segment），再合并成大索引文件。比如有多个新闻文档，它们会先分别进入不同segment，然后合并。
<separator></separator>
## 四、Lucene的结构
Lucene包括core和sandbox两部分，core是稳定核心，sandbox包含附加功能如highlighter、各种分析器。Lucene core有七个包：
### 4.1 analysis
包含内建分析器，如WhitespaceAnalyzer（按空白字符分词）、StopAnalyzer（添加stopword过滤）、StandardAnalyzer（常用）。
### 4.2 document
定义文档数据结构，如Document类和Field类。
### 4.3 index
有索引读写类，IndexWriter负责写入segment并合并优化，IndexReader关注索引文件中文档组织形式及删除操作。
### 4.4 queryParser
解析查询语句，将查询按语法组成各种Query类查找结果。
### 4.5 search
包含从索引搜索结果的类，如TermQuery、BooleanQuery等。
### 4.6 store
包含索引存储类，如Directory定义存储结构，FSDirectory存于文件，RAMDirectory存于内存，MmapDirectory使用内存映射。
### 4.7 util
包含公共工具类，如时间和字符串转换工具。

## 五、如何建索引
### 5.1 最简单的索引代码示例
```java
IndexWriter writer = new IndexWriter("/data/index/", new StandardAnalyzer(), true);
Document doc = new Document();
doc.add(new Field("title", "lucene introduction", Field.Store.YES, Field.Index.TOKENIZED));
doc.add(new Field("content", "lucene works well", Field.Store.YES, Field.Index.TOKENIZED));
writer.addDocument(doc);
writer.optimize();
writer.close();
```
这段代码先创建IndexWriter，指定索引目录、分析器并设为覆盖已有索引。然后创建Document，添加“title”和“content”两个Field并存储和索引。添加文档后优化索引，最后关闭writer。

### 5.2 将索引直接写在内存
```java
Directory dir = new RAMDirectory();
IndexWriter writer = new IndexWriter(dir, new StandardAnalyzer(), true);
Document doc = new Document();
doc.add(new Field("title", "lucene introduction", Field.Store.YES, Field.Index.TOKENIZED));
doc.add(new Field("content", "lucene works well", Field.Store.YES, Field.Index.TOKENIZED));
writer.addDocument(doc);
writer.optimize();
writer.close();
```
此代码创建RAMDirectory并传给writer，实现将索引写入内存。

### 5.3 索引文本文件
```java
Field field = new Field("content", new FileReader(file));
```
这里的file是要索引的文本文件，该构造函数读取文件内容并索引，但不存储。

## 六、如何维护索引
### 6.1 删除索引
Lucene提供两种删除document的方法：
1. `void deleteDocument(int docNum)`：根据文档在索引中的编号删除，但编号通常难以知晓，实用性有限。
2. `void deleteDocuments(Term term)`：根据参数term搜索并批量删除结果。例如：
```java
Directory dir = FSDirectory.getDirectory(PATH, false);
IndexReader reader = IndexReader.open(dir);
Term term = new Term(field, key);
reader.deleteDocuments(term);
reader.close();
```

### 6.2 更新索引
Lucene无专门更新方法，需先删除旧document再加入新的。如：
```java
Directory dir = FSDirectory.getDirectory(PATH, false);
IndexReader reader = IndexReader.open(dir);
Term term = new Term("title", "lucene introduction");
reader.deleteDocuments(term);
reader.close();
IndexWriter writer = new IndexWriter(dir, new StandardAnalyzer(), true);
Document doc = new Document();
doc.add(new Field("title", "lucene introduction", Field.Store.YES, Field.Index.TOKENIZED));
doc.add(new Field("content", "lucene is funny", Field.Store.YES, Field.Index.TOKENIZED));
writer.addDocument(doc);
writer.optimize();
writer.close();
```

## 七、如何搜索
Lucene搜索强大，提供多种辅助查询类（继承自Query类），可组合完成复杂操作，还提供Sort类排序和Filter类限制查询条件。

### 7.1 各种Query类型
1. **TermQuery**：查询特定域中包含特定词的document。如查询“content”域中含“lucene”的document：
```java
Term t = new Term("content", "lucene");
Query query = new TermQuery(t);
```
2. **BooleanQuery**：组合多个查询条件，实现“与”“或”逻辑。如查询“content”域中含“java”或“perl”的document：
```java
TermQuery termQuery1 = new TermQuery(new Term("content", "java"));
TermQuery termQuery2 = new TermQuery(new Term("content", "perl"));
BooleanQuery booleanQuery = new BooleanQuery();
booleanQuery.add(termQuery1, BooleanClause.Occur.SHOULD);
booleanQuery.add(termQuery2, BooleanClause.Occur.SHOULD);
```
3. **WildcardQuery**：通配符查询，“?”匹配一个任意字符，“*”匹配零个或多个任意字符。如搜索以“use”开头的词：
```java
Query query = new WildcardQuery(new Term("content", "use*"));
```
4. **PhraseQuery**：查找特定词语距离在一定范围内的文章。如查找“中”和“日”挨得较近（5个字距离内）的文章：
```java
PhraseQuery query = new PhraseQuery();
query.setSlop(5);
query.add(new Term("content", "中"));
query.add(new Term("content", "日"));
```
5. **PrefixQuery**：搜索以特定词开头的词语。如搜以“中”开头的词：
```java
PrefixQuery query = new PrefixQuery(new Term("content", "中"));
```
6. **FuzzyQuery**：用Levenshtein算法搜索相似term。如搜索与“wuzza”相似的词：
```java
Query query = new FuzzyQuery(new Term("content", "wuzza"));
```
7. **RangeQuery**：搜索指定范围内的document。如搜索时间域在20060101到20060130之间的document：
```java
RangeQuery query = new RangeQuery(new Term("time", "20060101"), new Term("time", "20060130"), true);
```

### 7.2 QueryParser
Lucene提供类似SQL语句的查询语句，可自动拆分交给相应Query执行。如：
- TermQuery可用“field:key”方式，如“content:lucene”。
- BooleanQuery中“与”用“+”，“或”用“ ”，如“content:java content:perl”。
- WildcardQuery仍用“?”和“*”，如“content:use*”。
- PhraseQuery用“~”，如“content:"中日"~5”。
- PrefixQuery用“*”，如“中*”。
- FuzzyQuery用“~”，如“content: wuzza ~”。
- RangeQuery用“[]”或“{}”，前者闭区间，后者开区间，如“time:[20060101 TO 20060130]”。

### 7.3 Filter
Filter限制查询索引子集，类似SQL的“where”但有区别，它预处理数据源后交给查询语句，代价较大。常用的有RangeFilter（设定搜索范围）和QueryFilter（在上次查询结果中搜索）。例如：
```java
Directory dir = FSDirectory.getDirectory(PATH, false);
IndexSearcher is = new IndexSearcher(dir);
QueryParser parser = new QueryParser("content", new StandardAnalyzer());
Query query = parser.parse("title:lucene content:lucene");
RangeFilter filter = new RangeFilter("time", "20060101", "20060230", true, true);
Hits hits = is.search(query, filter);
for (int i = 0; i < hits.length(); i++) {
    Document doc = hits.doc(i);
    System.out.println(doc.get("title"));
}
is.close();
```

### 7.4 Sort
通过Sort实现结果排序，如按时间排序：
```java
Sort sort = new Sort("time"); // 升序
Sort sort = new Sort("time", true); // 降序
```

## 八、分析器
分析器作用是按语义切分句子为词语。英文有成熟的StandardAnalyzer，中文分词则较复杂。Lucene的StandardAnalyzer虽能对中文分词，但效果不佳，如搜索“如果”可能匹配“牛奶不如果汁好喝”，且索引文件大。sandbox中的ChineseAnalyzer和CJKAnalyzer也存在分词不准问题。基于词库的分词法是较好选择，通过词库匹配实现更准确分词，常见分词方法有正向最大匹配和逆向最大匹配。实际应用中，中科院的ICTCLAS和JE - Analysis较常用，ICTCLAS是动态链接库，java调用不便且有安全隐患，JE - Analysis效果较好且使用方便。

## 九、性能优化
### 9.1 优化创建索引性能
1. **设置IndexWriter参数**
   - `setMaxBufferedDocs(int maxBufferedDocs)`：控制写入新segment前内存中document数目，增大可加快建索引速度，默认10。
   - `setMaxMergeDocs(int maxMergeDocs)`：控制segment中最大document数目，较小值利于追加索引速度，默认Integer.MAX_VALUE，一般无需修改。
   - `setMergeFactor(int mergeFactor)`：控制多个segment合并频率，较大值建索引快，默认10，建索引时可设为100。
2. **RAMDirectory缓写**
   - 先将索引写入RAMDirectory，达到一定数量再批量写入FSDirectory，减少磁盘IO次数。
3. **选择较好分析器**
   - 可减小索引文件大小，但可能增加时间成本，如StandardAnalyzer耗时133分钟，MMAnalyzer耗时150分钟（测试数据）。

### 9.2 优化搜索性能
1. **将索引放入内存（RAMDirectory）**
   - 虽直观但实践中RAMDirectory和FSDirectory速度相近，且lucene搜索耗内存，数据量大时可能out of memory，作用不大。
2. **优化时间范围限制**
   - **RangeQuery**：实现是展开时间范围为BooleanClause加入BooleanQuery，范围过大可能抛异常，可设置BooleanQuery.setMaxClauseCount(int maxClauseCount)扩大，但有限制且占用内存大。
   - **RangeFilter**：遍历所有索引生成BitSet标记document，耗时，90%以上查询时间耗费在此。
   - **优化思路**
     - **缓存Filter结果**：以RangeFilter对象为键缓存filter结果BitSet，可利用CachingWrapperFilter类，但要注意其缓存机制与需求不同，仅作为封装类。
     - **降低时间精度**：时间粒度越大，对比越快，搜索时间越短，在不影响功能前提下，尽量降低时间精度，最好不使用filter。
3. **使用更好的分析器**
   - 索引文件小了搜索会加快，但提升有限，较好分析器相对于最差分析器对性能提升在20%以下。

## 十、经验总结
1. **关键词区分大小写**：如“or”“AND”“TO”等关键词只认大写，小写视为普通单词。
2. **读写互斥性**：同一时刻只能有一个写操作，但写时可搜索。
3. **文件锁**：写索引过程强行退出会在tmp目录留lock文件，影响后续写操作，需手工删除。
4. **时间格式**：Lucene只支持“yyMMddHHmmss”格式时间，其他格式不认。
5. **设置boost**：搜索时可设置字段权重，如认为标题中关键词更重要，可增大标题的boost值（默认1.0），使搜索结果优先显示标题含关键词文章（未使用排序时）。

希望通过这篇教程，能帮助大家全面掌握Lucene，开启高效全文搜索之旅！如果在学习过程中有任何疑问，欢迎随时交流。