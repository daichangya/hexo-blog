---
title: ResultSet自动封装数据到实体对象
id: 1130
date: 2024-10-31 22:01:49
author: daichangya
excerpt: ResultSet自动封装数据到实体对象
permalink: /archives/ResultSet-zi-dong-feng-zhuang-shu-ju/
tags:
- jdbc
---


```
package com.daicy.util;
 
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
public class AntResult {
 
 private Object[] beanMatch(Class clazz, String beanProperty) {
  Object[] result = new Object[2];
  char beanPropertyChars[] = beanProperty.toCharArray();
  beanPropertyChars[0] = Character.toUpperCase(beanPropertyChars[0]);
  String s = new String(beanPropertyChars);
  String names[] = { ("set" + s).intern(), ("get" + s).intern(),
    ("is" + s).intern(), ("write" + s).intern(),
    ("read" + s).intern() };
  Method getter = null;
  Method setter = null;
  Method methods[] = clazz.getMethods();
  for (int i = 0; i &lt; methods.length; i++) {
   Method method = methods[i];
   // 只取公共字段
   if (!Modifier.isPublic(method.getModifiers()))
    continue;
   String methodName = method.getName().intern();
   for (int j = 0; j &lt; names.length; j++) {
    String name = names[j];
    if (!name.equals(methodName))
     continue;
    if (methodName.startsWith("set")
      || methodName.startsWith("read"))
     setter = method;
    else
     getter = method;
   }
  }
  result[0] = getter;
  result[1] = setter;
  return result;
 }
 
 private void beanRegister(Object object, String beanProperty, String value) {
  Object[] beanObject = beanMatch(object.getClass(), beanProperty);
  Object[] cache = new Object[1];
  Method getter = (Method) beanObject[0];
  Method setter = (Method) beanObject[1];
  try {
   // 通过get获得方法类型
   String methodType = getter.getReturnType().getName();
   if (methodType.equalsIgnoreCase("long")) {
    cache[0] = new Long(value);
    setter.invoke(object, cache);
   } else if (methodType.equalsIgnoreCase("int")
     || methodType.equalsIgnoreCase("integer")) {
    cache[0] = new Integer(value);
    setter.invoke(object, cache);
   } else if (methodType.equalsIgnoreCase("short")) {
    cache[0] = new Short(value);
    setter.invoke(object, cache);
   } else if (methodType.equalsIgnoreCase("float")) {
    cache[0] = new Float(value);
    setter.invoke(object, cache);
   } else if (methodType.equalsIgnoreCase("double")) {
    cache[0] = new Double(value);
    setter.invoke(object, cache);
   } else if (methodType.equalsIgnoreCase("boolean")) {
    cache[0] = new Boolean(value);
    setter.invoke(object, cache);
   } else if (methodType.equalsIgnoreCase("java.lang.String")) {
    cache[0] = value;
    setter.invoke(object, cache);
   } else if (methodType.equalsIgnoreCase("java.io.InputStream")) {
   } else if (methodType.equalsIgnoreCase("char")) {
    cache[0] = (Character.valueOf(value.charAt(0)));
    setter.invoke(object, cache);
   }
  } catch (Exception e) {
   e.printStackTrace();
  }
 }
 
 public Collection get(final Connection connection, final Class clazz,
   final String sql) {
  // 创建PreparedStatement
  PreparedStatement ptmt = null;
  // 创建resultset
  ResultSet rset = null;
  // 创建collection
  Collection collection = null;
  try {
   // 赋予实例
   ptmt = connection.prepareStatement(sql);
   rset = ptmt.executeQuery();
   collection = get(rset, clazz);
  } catch (SQLException e) {
   System.err.println(e.getMessage());
  } finally {
   try {
    // 关闭rs并释放资源
    if (rset != null) {
     rset.close();
     rset = null;
    }
    // 关闭ps并释放资源
    if (ptmt != null) {
     ptmt.close();
     ptmt = null;
    }
   } catch (SQLException e) {
    System.err.println(e.getMessage());
   }
  }
  return collection;
 }
 public Collection get(final ResultSet result, final Class clazz) {
  // 创建collection
  Collection collection = null;
  try {
   ResultSetMetaData rsmd = result.getMetaData();
   // 获得数据列数
   int cols = rsmd.getColumnCount();
   // 创建等同数据列数的arraylist类型collection实例
   collection = new ArrayList(cols);
   // 遍历结果集
   while (result.next()) {
    // 创建对象
    Object object = null;
    try {
     // 从class获得对象实体
     object = clazz.newInstance();
    } catch (Exception e) {
    }
    // 循环每条记录
    for (int i = 1; i &lt;= cols; i++) {
     beanRegister(object, rsmd.getColumnName(i), result
       .getString(i));
    }
    // 将数据插入collection
    collection.add(object);
   }
  } catch (SQLException e) {
   System.err.println(e.getMessage());
  } finally {
  }
  return collection;
 }
 
 //===========================================//
 
 public static void main(String[] args) {
  // 加载驱动
  try {
   Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
  } catch (ClassNotFoundException e) {
   e.printStackTrace();
  }
  // 连接字符串
  String url = "jdbc:sqlserver://localhost:1433;databaseName=test";
  Connection connection = null;
  PreparedStatement ps = null;
  ResultSet rs = null;
  try {
   // 创建连接
   connection = DriverManager.getConnection(url, "sa", "javalife");
   AntResult test = new AntResult();
   // Ltest是我测试用类，实际操作请注入相关对象，支持set，get，is，read，writer为前缀数据对，更多请继续添加。
   Collection collection = test.get(connection,
   com.ant.po.UserInfo.class, "select * from userinfo");
   for (Iterator it = collection.iterator(); it.hasNext();) {
   com.ant.po.UserInfoltest = (com.ant.po.UserInfo) it.next();
    System.out.println(ltest.getUserid() + ":" + ltest.getUserName());
   }
  }
  // SQL异常，用于抛出SQL语句处理中所引发的错误。
  catch (SQLException e) {
   System.err.println(e.getMessage());
  }
  // finally，此标识用以包含必须访问的内容。
  finally {
   try {
    // 关闭connection并释放资源
    if (connection != null) {
     connection.close();
     connection = null;
    }
   } catch (SQLException e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
   }
   // 如果关闭时产生异常将由此抛出
  }
 }
}
//需要注意的是 类中的属性要和 数据库的列名保持一致。再想一个问题，struts 的 FormBean 是
//不是用这个原理封装的数据啊。  今天很累了，改天把这个类在封装下，配合以前做的通用分页前台
//通用存储过程分页取得数据集后台，做个 jar 包 只需要传递一个类，在前台页面通过 el 表达
//式进行
//数据的展示和分页功能的实现。 这个程序真是越做越简单！
```

```
//UserInfo.java 实体类
package com.ant.entity;
public class UserInfo {
    private int userID;
    private String userName;
    private String userPass;
    public int getUserID() {
        return userID;
    }
    public void setUserID(int userID) {
        this.userID = userID;
    }
    public String getUserName() {
        return userName;
    }
    public void setUserName(String userName) {
        this.userName = userName;
    }
    public String getUserPass() {
        return userPass;
    }
    public void setUserPass(String userPass) {
        this.userPass = userPass;
    }
    
}
```
