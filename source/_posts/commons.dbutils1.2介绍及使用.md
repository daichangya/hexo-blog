---
title: commons.dbutils1.2介绍及使用
id: 744
date: 2024-10-31 22:01:45
author: daichangya
excerpt: "一、结构介绍二、功能介绍commons.dbutils是一个对JDBC操作进行封装的类集，其有如下几个优点：（1）没有可能的资源泄漏，避免了繁锁的JDBC代码（2）代码更整洁（3）从ResultSet自动生成JavaBeans属性"
permalink: /archives/17741223/
tags: 
 - jdbc
---

 

### 一、结构介绍  

**高层结构图：**

![](https://p-blog.csdn.net/images/p_blog_csdn_net/gtuu0123/EntryImages/20090903/dbutils.png)

**wrappers包：**

![](https://p-blog.csdn.net/images/p_blog_csdn_net/gtuu0123/EntryImages/20090903/wrappers.png)

**handlers包（部分）:**

![](https://p-blog.csdn.net/images/p_blog_csdn_net/gtuu0123/EntryImages/20090903/handlers.png)

### 二、功能介绍

commons.dbutils是一个对JDBC操作进行封装的类集，其有如下几个优点：

（1）没有可能的资源泄漏，避免了繁锁的JDBC代码

（2）代码更整洁

（3）从ResultSet自动生成JavaBeans属性

（4）无其他依赖包

### 三、基本使用

基本用到的类有：QueryRunner、ResultSetHandler及其子类等

QueryRunner -- 执行查询的类，可以执行SELECT、INSERT、UPDATE、DELETE等语句，QueryRunner用ResultSetHandler的子类来处理ResultSet并返回结果；而包提供的ResultSetHandler子类使用RowProcessor的子类来处理ResultSet中的每一行；RowProcessor的默认实现为BasicRowProcessor；BeanProcessor不是RowProcessor，可以看作一个工具类

ResultHandler及其子类 -- 实现了Object handle(ResultSet rs) throws SQLException方法

AbstractListHandler -- 返回多行List的抽象类

ArrayHandler --  返回一行的Object\[\]

ArrayListHandler -- 返回List，每行是Object\[\]

BeanHandler -- 返回第一个Bean对象

BeanListHandler -- 返回List，每行是Bean

ColumnListHandler -- 返回一列的List

KeyedHandler -- 返回Map，具体见代码

MapHandler -- 返回单个Map

MapListHandler -- 返回List，每行是Map

ScalarHandler -- 返回列的头一个值

代码：

**\[java\]** [view plain](http://blog.csdn.net/gtuu0123/article/details/4516213# "view plain")[copy](http://blog.csdn.net/gtuu0123/article/details/4516213# "copy")

```
//建表语句
DROP TABLE IF EXISTS `test`.`user`;
CREATE TABLE  `test`.`user` (
  `name` varchar(10) DEFAULT NULL,
  `password` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
表中数据
'user1', 'pwd1'
'user2', 'pwd2'
//User类
public class User {
	private String name;
	private String pwd;
	public User(){
	}
	public void setName(String val) {
		this.name = val;
	}
	public void setPassword(String val) {
		this.pwd = val;
	}
	public String getName() {
		return name;
	}
	public String getPassword() {
		return pwd;
	}
}
```
```
package dbutiltest;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;
import org.apache.commons.dbutils.DbUtils;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.ResultSetHandler;
import org.apache.commons.dbutils.handlers.ArrayHandler;
import org.apache.commons.dbutils.handlers.ArrayListHandler;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;
import org.apache.commons.dbutils.handlers.ColumnListHandler;
import org.apache.commons.dbutils.handlers.KeyedHandler;
import org.apache.commons.dbutils.handlers.MapListHandler;
public class TestDbUtils {
	
	static {
		try {
			Class.forName("org.gjt.mm.mysql.Driver");
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
			System.exit(1);
		}
	}
	
	public Connection getConnection() {
		Connection conn = null;
		try {
			conn = DriverManager.getConnection(
					"jdbc:mysql://localhost:3306/test", "root", "pwd");
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return conn;
	}
	
	public static void main(String[] args) {
		TestDbUtils u = new TestDbUtils();
		u.testArrayHandler();
		u.testArrayListHandler();
		u.testBeanListHandler();
		u.testMapListHandler();
		u.testColumnListHandler();
		u.testNonQuery();
	}
	
	public void testArrayHandler() {
		System.out.println("----testArrayHandler----");
		String sql = "select * from user";
		ResultSetHandler handler = new ArrayHandler();
		QueryRunner query = new QueryRunner();
		Connection conn = null;
		try {
			conn = getConnection();
			Object[] arr = (Object[])query.query(conn, sql, handler);
			for (int i = 0; i < arr.length; i++) {
				System.out.println(arr[i].toString());
			}
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				DbUtils.close(conn);
			} catch (SQLException e) {
				// ignore
			}
		}
		
	}
	
	public void testArrayListHandler() {
		System.out.println("----testArrayListHandler----");
		String sql = "select * from user";
		ResultSetHandler handler = new ArrayListHandler();
		QueryRunner query = new QueryRunner();
		Connection conn = null;
		try {
			conn = getConnection();
			List list = (List)query.query(conn, sql, handler);
			for (int i = 0; i < list.size(); i++) {
				Object[] arr = (Object[])list.get(i);
				for (int j = 0; j < arr.length; j++) {
					System.out.print(arr[j] + "  ");
				}
				System.out.println();
			}
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				DbUtils.close(conn);
			} catch (SQLException e) {
				// ignore
			}
		}
		
	}
	
	public void testBeanListHandler() {
		System.out.println("----testBeanListHandler----");
		String sql = "select * from user where name=?";
		Object[] params = new Object[]{"user1"};
		ResultSetHandler handler = new BeanListHandler(User.class);
		QueryRunner query = new QueryRunner();
		Connection conn = null;
		try {
			conn = getConnection();
			List list = (List)query.query(conn, sql, params, handler);
			for (int i = 0; i < list.size(); i++) {
				User user = (User)list.get(i);
				System.out.println(user.getName() + "  " + user.getPassword());
			}
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				DbUtils.close(conn);
			} catch (SQLException e) {
				// ignore
			}
		}
	}
	
	public void testMapListHandler() {
		System.out.println("----testMapListHandler----");
		String sql = "select * from user where name=?";
		Object[] params = new Object[]{"user1"};
		ResultSetHandler handler = new MapListHandler();
		QueryRunner query = new QueryRunner();
		Connection conn = null;
		try {
			conn = getConnection();
			List list = (List)query.query(conn, sql, params, handler);
			for (int i = 0; i < list.size(); i++) {
				Map user = (Map)list.get(i);
				System.out.println(user.get("name") + "  " + user.get("password"));
			}
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				DbUtils.close(conn);
			} catch (SQLException e) {
				// ignore
			}
		}
	}
	
	public void testColumnListHandler() {
		System.out.println("----testColumnListHandler----");
		String sql = "select * from user";
		ResultSetHandler handler = new ColumnListHandler("name");
		QueryRunner query = new QueryRunner();
		Connection conn = null;
		try {
			conn = getConnection();
			List list = (List)query.query(conn, sql, handler);
			for (int i = 0; i < list.size(); i++) {
				System.out.println(list.get(i));
			}
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				DbUtils.close(conn);
			} catch (SQLException e) {
				// ignore
			}
		}
	}
	
	public void testKeyedHandler() {
		System.out.println("----testKeyedHandler----");
		String sql = "select * from user";
		ResultSetHandler handler = new KeyedHandler("name");
		QueryRunner query = new QueryRunner();
		Connection conn = null;
		try {
			conn = getConnection();
			Map map = (Map)query.query(conn, sql, handler);
			Map user = (Map)map.get("user2");
			System.out.println(user.get("password"));
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				DbUtils.close(conn);
			} catch (SQLException e) {
				// ignore
			}
		}
	}
	
	public void testNonQuery() {
		System.out.println("----testNonQuery----");
		String sql = "insert into `user` values('user_test','pwd_test')";
		QueryRunner query = new QueryRunner();
		Connection conn = null;
		try {
			conn = getConnection();
			query.update(conn, sql);
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				DbUtils.close(conn);
			} catch (SQLException e) {
				// ignore
			}
		}
	}
}
```

**关于wrappers包:**

**在新建 QueryRunner时，覆盖父类的方法wrap**

```
QueryRunner query = new QueryRunner() {
			protected ResultSet wrap(ResultSet rs) {
				return StringTrimmedResultSet.wrap(rs);
			}
		};
```

### 四、扩展

1.RowProcessor接口

2.ResultSetHandler接口