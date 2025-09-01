---
title: 深度剖析MyBatis：核心类的奥秘与强大功能
id: 0c28c09a-e720-466e-b29a-c60318e2af68
date: 2024-12-10 11:09:30
author: daichangya
cover: https://images.jsdiff.com/MyBatis.jpg
excerpt: 在Java持久层框架的世界里，MyBatis以其灵活、高效的特性备受开发者青睐。今天，让我们一同深入探究MyBatis中几个至关重要的类，揭开它们的神秘面纱，领略MyBatis的强大魅力。
  一、MappedStatement：SQL语句的映射使者 （一）功能概述 MappedStatement在My
permalink: /archives/shen-du-pou-xi-MyBatis-he-xin-lei-de-ao/
categories:
- mybatis
---

在Java持久层框架的世界里，MyBatis以其灵活、高效的特性备受开发者青睐。今天，让我们一同深入探究MyBatis中几个至关重要的类，揭开它们的神秘面纱，领略MyBatis的强大魅力。

## 一、MappedStatement：SQL语句的映射使者
### （一）功能概述
MappedStatement在MyBatis框架中扮演着关键角色，它犹如一座桥梁，将XML文件中的SQL语句节点（如`<select>`、`<update>`、`<insert>`标签）与Java代码紧密相连。在MyBatis框架初始化阶段，会对XML配置文件进行深度扫描和解析，将其中的SQL语句节点逐一转化为一个个MappedStatement对象，从而构建起SQL语句与代码逻辑之间的映射关系。
![MyBatis.jpg](https://images.jsdiff.com/MyBatis.jpg)

### （二）实例解析
以一个简单的XML Mapper文件为例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="mybatis.UserDao">
    <cache type="org.mybatis.caches.ehcache.LoggingEhcache"/>
    <resultMap id="userResultMap" type="UserBean">
        <id property="userId" column="user_id"/>
        <result property="userName" column="user_name"/>
        <result property="userPassword" column="user_password"/>
        <result property="createDate" column="create_date"/>
    </resultMap>
    <select id="find" parameterType="UserBean" resultMap="userResultMap">
        select * from user
        <where>
            <if test="userName!=null and userName!=''">
                and user_name = #{userName}
            </if>
            <if test="userPassword!=null and userPassword!=''">
                and user_password = #{userPassword}
            </if>
            <if test="createDate!=null">
                and create_date = #{createDate}
            </if>
        </where>
    </select>
    <select id="find2" parameterType="UserBean" resultMap="userResultMap">
        select * from user
        <where>
            <if test="userName!=null and userName!=''">
                and user_name = #{userName}
            </if>
            <if test="userPassword!=null and userPassword!=''">
                and user_password = #{userPassword}
            </if>
            <if test="createDate!=null">
                and create_date = #{createDate}
            </if>
        </where>
    </select>
</mapper>
```
MyBatis对这个文件进行解析后，会注册两个MappedStatement对象，分别对应`id`为`find`和`find2`的`<select>`节点。在MyBatis框架中，为了确保每个MappedStatement对象的唯一性，其标识采用Mapper文件的`namespace`加上节点本身的`id`值。例如，上述两个MappedStatement对象在MyBatis框架中的唯一标识分别是`mybatis.UserDao.find`和`mybatis.UserDao.find2`。
<separator></separator>
### （三）源码探秘
打开MappedStatement对象的源码，我们可以看到其中包含了众多属性，这些属性与XML元素的属性存在着紧密的对应关系。其中，比较关键的属性包括：
- **ParameterMap对象**：用于表示查询参数，它明确了输入参数的类型和映射关系，确保SQL语句在执行时能够正确获取参数值。
- **ResultMap列表（resultMaps）**：负责定义SQL查询结果与Java对象之间的映射规则，使得MyBatis能够将从数据库中获取的数据准确无误地封装成JavaBean对象，方便在Java代码中进行处理。
- **SqlSource对象**：这是最为重要的属性之一，它承担着执行动态SQL计算和获取的重任。通过这个对象，MappedStatement能够根据用户提供的查询参数对象，动态生成要执行的SQL语句，充分展现了MyBatis的灵活性。

### （四）工作流程
MappedStatement对象的工作流程清晰而高效。当用户发起查询请求时，它首先接收用户传递的查询参数对象，然后借助SqlSource对象，根据参数对象的具体值动态计算出实际要执行的SQL语句。接着，将计算好的SQL语句发送到数据库执行，获取查询结果。最后，利用ResultMap列表将查询结果封装为JavaBean对象，并返回给用户。这个过程完美体现了MyBatis的核心价值：“根据用户提供的查询参数对象，动态执行SQL语句，并将结果封装为Java对象”。

### （五）类图展示
```plantuml
class MappedStatement {
    - resource: String
    - configuration: Configuration
    - id: String
    - fetchSize: Integer
    - timeout: Integer
    - statementType: StatementType
    - resultSetType: ResultSetType
    - sqlSource: SqlSource
    - cache: Cache
    - parameterMap: ParameterMap
    - resultMaps: List<ResultMap>
    - flushCacheRequired: boolean
    - useCache: boolean
    - resultOrdered: boolean
    - sqlCommandType: SqlCommandType
    - keyGenerator: KeyGenerator
    - keyProperties: String[]
    - keyColumns: String[]
    - hasNestedResultMaps: boolean
    - databaseId: String
    - statementLog: Log
    - lang: LanguageDriver
    + MappedStatement()
}
```

## 二、SqlSource：动态SQL的幕后大师
### （一）接口定义
SqlSource是一个接口类，在MappedStatement对象中作为一个关键属性存在。其代码如下：
```java
package org.apache.ibatis.mapping;

public interface SqlSource {
    BoundSql getBoundSql(Object parameterObject);
}
```
这个接口仅有一个方法`getBoundSql(Object parameterObject)`，该方法返回一个BoundSql对象。BoundSql对象代表了一次SQL语句的实际执行内容，而SqlSource对象的核心职责就是根据传入的参数对象，动态计算并生成这个BoundSql对象。

### （二）常用实现类
SqlSource最常用的实现类是DynamicSqlSource，其代码如下：
```java
package org.apache.ibatis.scripting.xmltags;

import java.util.Map;

import org.apache.ibatis.builder.SqlSourceBuilder;
import org.apache.ibatis.mapping.BoundSql;
import org.apache.ibatis.mapping.SqlSource;
import org.apache.ibatis.session.Configuration;

public class DynamicSqlSource implements SqlSource {
    private Configuration configuration;
    private SqlNode rootSqlNode;

    public DynamicSqlSource(Configuration configuration, SqlNode rootSqlNode) {
        this.configuration = configuration;
        this.rootSqlNode = rootSqlNode;
    }

    public BoundSql getBoundSql(Object parameterObject) {
        DynamicContext context = new DynamicContext(configuration, parameterObject);
        rootSqlNode.apply(context);
        SqlSourceBuilder sqlSourceParser = new SqlSourceBuilder(configuration);
        Class<?> parameterType = parameterObject == null? Object.class : parameterObject.getClass();
        SqlSource sqlSource = sqlSourceParser.parse(context.getSql(), parameterType, context.getBindings());
        BoundSql boundSql = sqlSource.getBoundSql(parameterObject);
        for (Map.Entry<String, Object> entry : context.getBindings().entrySet()) {
            boundSql.setAdditionalParameter(entry.getKey(), entry.getValue());
        }
        return boundSql;
    }
}
```
在`getBoundSql`方法中，通过创建`DynamicContext`对象，并调用`rootSqlNode.apply(context)`启动了一个基于递归实现的动态计算SQL语句的过程。这个过程借助Ognl根据传入的参数对象计算表达式，从而生成该次调用过程中实际要执行的SQL语句。

### （三）动态SQL计算过程
1. 首先，创建`DynamicContext`对象，传入`Configuration`和参数对象。`DynamicContext`会对参数对象进行“map”化处理，即将传入的POJO对象转换为一个类似Map的数据结构，以便后续统一使用Map接口方法来访问数据。
2. 接着，调用`rootSqlNode.apply(context)`，这是动态计算SQL语句的核心步骤。`rootSqlNode`会根据传入的参数对象，通过Ognl计算表达式，逐步构建出实际要执行的SQL语句，并将其添加到`DynamicContext`的`sqlBuilder`中。
3. 然后，创建`SqlSourceBuilder`对象，使用它来解析`DynamicContext`中的SQL语句和参数类型，生成一个新的`SqlSource`对象。
4. 最后，从新生成的`SqlSource`对象中获取`BoundSql`对象，并将`DynamicContext`中的绑定参数设置到`BoundSql`对象中，最终返回`BoundSql`对象，代表了这次动态计算得到的实际SQL语句和相关参数。

### （四）类图展示
```plantuml
interface SqlSource {
    + getBoundSql(Object parameterObject): BoundSql
}

class DynamicSqlSource {
    - configuration: Configuration
    - rootSqlNode: SqlNode
    + DynamicSqlSource(Configuration configuration, SqlNode rootSqlNode)
    + getBoundSql(Object parameterObject): BoundSql
}
```

## 三、DynamicContext：参数处理的核心枢纽
### （一）功能介绍
DynamicContext类在MyBatis的参数处理和动态SQL计算过程中起着至关重要的作用。它主要负责对传入的参数对象进行处理，将其转换为适合动态SQL计算的格式，并提供了一系列方法用于操作和获取SQL相关的信息。

### （二）源码分析
1. 在`DynamicContext`的构造函数中，根据传入的参数对象是否为`Map`类型，有两种不同的处理方式来构造`ContextMap`对象。`ContextMap`是一个继承自`HashMap`的内部类，其作用是统一参数的访问方式，使得无论是普通的POJO对象还是`Map`对象，都可以通过`Map`接口方法来访问数据。
2. 当传入的参数对象不是`Map`类型时，MyBatis会使用`MetaObject`对象对其进行封装。在动态计算SQL过程中，当需要获取数据时，通过`Map`接口的`get`方法包装`MetaObject`对象的取值过程，从而实现对POJO对象属性的访问。
3. `DynamicContext`类中的静态初始块`static { OgnlRuntime.setPropertyAccessor(ContextMap.class, new ContextAccessor()); }`表明MyBatis使用Ognl来计算动态SQL语句。`ContextAccessor`是`DynamicContext`的内部类，实现了Ognl中的`PropertyAccessor`接口，为Ognl提供了如何使用`ContextMap`参数对象的具体说明，从而完成了整个参数对象的“map”化处理。

### （三）参数传递和使用过程
1. 传入的参数对象首先被统一封装为`ContextMap`对象。
2. Ognl运行时环境在动态计算SQL语句时，按照`ContextAccessor`中描述的`Map`接口方式来访问和读取`ContextMap`对象，获取计算过程中所需的参数。
3. `ContextMap`对象内部可能封装了一个普通的POJO对象，也可能是直接传递的`Map`对象，但从外部来看，都是通过`Map`接口来读取数据，实现了对不同类型参数的无差别化处理。

### （四）类图展示
```plantuml
class DynamicContext {
    - bindings: ContextMap
    - sqlBuilder: StringBuilder
    - uniqueNumber: int
    + PARAMETER_OBJECT_KEY: String
    + DATABASE_ID_KEY: String
    + DynamicContext(Configuration configuration, Object parameterObject)
    + getBindings(): Map<String, Object>
    + bind(String name, Object value)
    + appendSql(String sql)
    + getSql(): String
    + getUniqueNumber(): int
    static class ContextMap {
        - parameterMetaObject: MetaObject
        + ContextMap(MetaObject parameterMetaObject)
        + get(Object key): Object
    }
    static class ContextAccessor {
        + getProperty(Map context, Object target, Object name): Object
        + setProperty(Map context, Object target, Object name, Object value)
    }
}
```

### （五）示例验证
以下是一个Junit测试方法，用于验证MyBatis参数获取过程中对Map对象和普通POJO对象的无差别化处理：
```java
@Test
public void testSqlSource() throws Exception {
    String resource = "mybatis/mybatis-config.xml";
    InputStream inputStream = Resources.getResourceAsStream(resource);
    SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder()
          .build(inputStream);
    SqlSession session = sqlSessionFactory.openSession();

    try {
        Configuration configuration = session.getConfiguration();
        MappedStatement mappedStatement = configuration
              .getMappedStatement("mybatis.UserDao.find2");
        assertNotNull(mappedStatement);

        UserBean param = new UserBean();
        param.setUserName("admin");
        param.setUserPassword("admin");
        BoundSql boundSql = mappedStatement.getBoundSql(param);
        String sql = boundSql.getSql();

        Map<String, Object> map = new HashMap<>();
        map.put("userName", "admin");
        map.put("userPassword", "admin");
        BoundSql boundSql2 = mappedStatement.getBoundSql(map);
        String sql2 = boundSql2.getSql();

        assertEquals(sql, sql2);

        UserBean bean = session.selectOne("mybatis.UserDao.find2", map);
        assertNotNull(bean);
    } finally {
        session.close();
    }
}
```
在这个测试中，第一次使用`UserBean`对象获取和计算SQL语句，第二次使用`HashMap`对象进行同样的操作，甚至直接使用`HashMap`对象启动了一次`session`对象的查询。测试结果通过，充分说明了MyBatis在参数获取过程中，对`Map`对象和普通POJO对象的无差别化处理，因为在内部，两者都会被封装，然后通过`Map`接口来访问。

通过对MyBatis中这几个重要类的深入剖析，我们清晰地了解了MyBatis的核心工作机制。MappedStatement作为SQL语句的映射使者，协调了SQL与Java代码之间的关系；SqlSource则是动态SQL的幕后大师，根据参数动态生成可执行的SQL语句；DynamicContext作为参数处理的核心枢纽，确保了参数的统一访问和动态SQL计算的顺利进行。这些类相互协作，共同构建了MyBatis强大而灵活的持久层框架，为开发者提供了高效、便捷的数据库操作体验。

