---
title: Java 与 JSON 转换工具大对决：谁才是最强王者？
id: f5e2e805-cefc-40d4-90f3-e17d5fd54cbf
date: 2024-11-29 12:54:38
author: daichangya
cover: https://images.jsdiff.com/Java01.jpg
excerpt: 在当今的 Java 开发世界中，JSON 数据格式无处不在，无论是前后端交互、数据存储还是配置文件处理，都少不了它的身影。而将 Java 对象与
  JSON 之间进行高效转换，就成为了每个 Java 开发者必须掌握的技能。今天，我们就像一群勇敢的探险家，深入 Java 与 JSON 转换的神秘领域，对
permalink: /archives/Java-yu-JSON-zhuan-huan-gong-ju-da-dui/
categories:
- java
---

在当今的 Java 开发世界中，JSON 数据格式无处不在，无论是前后端交互、数据存储还是配置文件处理，都少不了它的身影。而将 Java 对象与 JSON 之间进行高效转换，就成为了每个 Java 开发者必须掌握的技能。今天，我们就像一群勇敢的探险家，深入 Java 与 JSON 转换的神秘领域，对 json-lib（ezmorph）、gson、flexJson、fastjson 和 jackson 这几款主流工具展开一场激烈的对比评测，看看它们在这场“性能与功能的盛宴”中究竟谁能脱颖而出！💥

## 一、工具简介：各显神通的转换利器🎯

### （一）json-lib（ezmorph）
json-lib 是一款功能丰富的 Java 与 JSON 转换工具，但它的使用相对复杂，依赖较多。它不仅可以实现 Java 与 JSON 的相互转换，还支持 XML 与 JSON 的转换，并且提供了自定义格式和属性过滤等高级功能。然而，这些强大功能的背后，是需要引入多个依赖库（ezmorph、commons-beanutils、commons-collections、groovy-all、oro、xom）的代价，这也使得它在一些简单场景下显得有些“臃肿”。

### （二）gson
gson 是 Google 推出的一款轻量级 JSON 处理库，以简单易用著称。它仅需一个依赖库，就能轻松实现 Java 与 JSON 的转换。其简洁的 API 设计让开发者能够快速上手，只需简单几行代码，就能完成复杂的对象转换，是追求简洁高效开发的首选。

### （三）flexJson
flexJson 是一个使用方便且无依赖的工具包，特别擅长处理复杂的 POJO 结构转换。它能够轻松应对树形多层结构，并且允许不同层对象中包含相同字段名的情况，这在处理一些复杂的数据模型时非常有用。其简洁的 API 让开发者无需过多配置，就能快速实现 Java 与 JSON 的转换。

### （四）fastjson
fastjson 是阿里巴巴开源的一款高性能 JSON 处理库，在性能方面表现卓越。它同样只需一个依赖库，就能实现高效的 Java 与 JSON 转换。其快速的序列化和反序列化速度，使其在对性能要求较高的场景中备受青睐。

### （五）jackson
jackson 是一款功能全面、性能稳定的 JSON 处理库。它也只需一个依赖库，就能轻松完成 Java 与 JSON 的转换工作。Jackson 提供了丰富的配置选项，可满足各种复杂的转换需求，并且在社区中拥有广泛的支持。

## 二、代码示例：实战中的转换操作✨

### （一）json-lib
1. **Java 转 JSON**
```java
// 准备测试数据
Classes sourceBean = TestCommon.getTestBean();

// 创建 JsonConfig 对象，用于配置转换规则
JsonConfig jc = new JsonConfig();
// 注册日期格式转换处理器，解决默认日期格式问题
jc.registerJsonValueProcessor(Date.class, new JsonDateValueProcessor());
// 设置属性过滤器，过滤掉为空的属性
jc.setJsonPropertyFilter(new PropertyFilter() {
    public boolean apply(Object source, String name, Object value) {
        if (value == null) {
            return true;
        }
        return false;
    }
});

// 将 Java 对象转换为 JSON 对象
JSONObject jsonObject = JSONObject.fromObject(sourceBean, jc);
String jsonStr = jsonObject.toString();
System.out.println("java->json: " + jsonStr);
```
2. **JSON 转 Java**
```java
// 注册日期格式解析器
JSONUtils.getMorpherRegistry().registerMorpher(
        new DateMorpher(new String[] { "yyyy-MM-dd HH:mm:ss", "yyyy-MM-dd" }));

jc = new JsonConfig();
jc.setRootClass(Classes.class);

// 创建一个 Map，用于指定内部集合中对象的类型
Map<String, Class> classMap = new HashMap<>();
classMap.put("students", Student.class);
jc.setClassMap(classMap);

// 将 JSON 字符串转换为 JSON 对象
JSONObject targetJo = JSONObject.fromObject(jsonStr, jc);
// 将 JSON 对象转换为 Java 对象
Classes targetBean = (Classes) JSONObject.toBean(targetJo, jc);

System.out.println("json->java: " + BeanUtils.describe(targetBean));
assertEquals(targetBean.getStudents().get(0).getName(), "张扇风");
```

### （二）gson
```java
package com.zt.test;

import junit.framework.TestCase;
import com.google.gson.Gson;

public class GsonTest extends TestCase {
    public void testGson() throws Exception {
        // 获取测试数据
        Classes sourceBean = TestCommon.getTestBean();
        Gson gson = new Gson();
        // Java 转 JSON
        String json = gson.toJson(sourceBean);
//        System.out.println(json);

        // JSON 转 Java
        Classes targetBean = gson.fromJson(json, Classes.class);
//        System.out.println(BeanUtils.describe(targetBean));
        assertEquals(targetBean.getStudents().get(0).getName(), "张扇风");
        assertEquals(targetBean.getStudents().get(0).getBirthday(), TestCommon.DATEFORMAT.parse("1800-01-01 01:00:00"));
    }

    public void testLoad() throws Exception {
        for (int i = 0; i < 100000; i++) {
            testGson();
        }
    }
}
```

### （三）flexJson
1. **Java 转 JSON**
```java
// 获取测试数据
Classes sourceBean = TestCommon.getTestBean();
// 创建 JSONSerializer 对象
JSONSerializer serializer = new JSONSerializer();
// 进行深度序列化
String jsonStr = serializer.deepSerialize(sourceBean);
// 输出序列化后的 JSON 字符串
System.out.println("java -> json: " + jsonStr);
```
2. **JSON 转 Java**
```java
// 创建 JSONDeserializer 对象
JSONDeserializer deserializer = new JSONDeserializer();
// 反序列化 JSON 字符串为 Java 对象
Classes targetBean = (Classes) deserializer.deserialize(jsonStr);
System.out.println("json -> java: " + BeanUtils.describe(targetBean));
assertEquals(targetBean.getStudents().get(0).getName(), "张扇风");
```

### （四）fastjson
```java
package com.zt.test;

import junit.framework.TestCase;
import com.alibaba.fastjson.JSON;

public class FastJsonTest extends TestCase {
    public void testFastJson() throws Exception {
        // 获取测试数据
        Classes sourceBean = TestCommon.getTestBean();
        // Java 转 JSON
        String json = JSON.toJSONString(sourceBean);

//        System.out.println(json);

        // JSON 转 Java
        Classes targetBean = JSON.parseObject(json, Classes.class);

//        System.out.println(BeanUtils.describe(targetBean));
        assertEquals(targetBean.getStudents().get(0).getName(), "张扇风");
        assertEquals(targetBean.getStudents().get(0).getBirthday(), TestCommon.DATEFORMAT.parse("1800-01-01 01:00:00"));
    }

    public void testLoad() throws Exception {
        for (int i = 0; i < 100000; i++) {
            testFastJson();
        }
    }
}
```

### （五）jackson
```java
package com.zt.test;

import junit.framework.TestCase;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JacksonTest extends TestCase {
    public void testJackson() throws Exception {
        // 获取测试数据
        Classes sourceBean = TestCommon.getTestBean();
        // 创建 ObjectMapper 对象
        ObjectMapper mapper = new ObjectMapper();
        // Java 转 JSON
        String json = mapper.writeValueAsString(sourceBean);

//        System.out.println(json);

        // JSON 转 Java
        Classes targetBean = mapper.readValue(json, Classes.class);

//        System.out.println(BeanUtils.describe(targetBean));
        assertEquals(targetBean.getStudents().get(0).getName(), "张扇风");
        assertEquals(targetBean.getStudents().get(0).getBirthday(), TestCommon.DATEFORMAT.parse("1800-01-01 01:00:00"));
    }

    public void testLoad() throws Exception {
        for (int i = 0; i < 100000; i++) {
            testJackson();
        }
    }
}
```

|工具|代码简洁性|配置复杂性|
|---|---|---|
|json-lib|较复杂，需要配置 JsonConfig 等|高，涉及日期格式、属性过滤、内部集合类型等配置|
|gson|简洁，一行代码即可转换|低，基本无需额外配置|
|flexJson|简洁，调用方法简单|低，部分高级功能可能需要额外配置|
|fastjson|简洁，转换方法直观|低，提供一些可选配置，但基本转换很简单|
|jackson|适中，需要创建 ObjectMapper 对象|中，有一些常用配置选项，但相对容易掌握|]

## 三、性能对比：速度的较量💪

为了评估这些工具的性能，我们进行了一个简单的测试：单个用例测试 10 万次 Java 与 JSON 的相互转换，多次测试取平均速度。需要注意的是，这个测试并非绝对严格，但足以让我们看出它们在性能方面的相对优劣。

### （一）测试结果
- json-lib：平均耗时约 25 秒。
- gson：平均耗时约 15 秒。
- flexJson：平均耗时约 12 秒。
- fastjson：平均耗时约 3 秒。
- jackson：平均耗时约 87 秒。

### （二）结果分析
从测试结果可以看出，fastjson 在性能方面表现极为出色，远远领先于其他工具，其快速的序列化和反序列化速度使其非常适合对性能要求极高的场景，如大型系统中的数据处理和传输。gson 和 flexJson 的性能也较为不错，能够满足大多数常规应用场景的需求。jackson 的性能相对较弱，在大规模数据处理时可能会成为性能瓶颈。而 json-lib 由于其依赖较多，性能相对较差，在性能敏感的场景中不太推荐使用。

## 四、总结与选择：适合的才是最好的💡

经过对这几款 Java 与 JSON 转换工具的全面对比，我们可以看出它们各有优劣。

如果追求极致的性能，fastjson 无疑是最佳选择，它能够在大规模数据转换场景中为我们提供高效的支持。如果希望使用简单、无需过多配置，gson 和 flexJson 是不错的候选者，它们简洁的 API 能够让我们快速上手，轻松实现转换功能。jackson 则适合那些需要丰富配置选项和稳定性能的项目，其全面的功能和社区支持能够满足各种复杂需求。而 json-lib 虽然功能强大，但由于依赖较多和性能问题，在现代项目中使用相对较少，除非有特殊需求（如需要 XML 与 JSON 转换等），否则不太推荐使用。

在实际开发中，我们应根据项目的具体需求、性能要求和开发团队的技术栈等因素，综合考虑选择最适合的工具。希望通过这次对比评测，能够帮助广大 Java 开发者在面对 Java 与 JSON 转换任务时，做出明智的决策，打造出更加高效、稳定的应用程序！🚀