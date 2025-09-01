---
title: 解锁common-dbutils：简化JDBC操作的神器
id: 231638c1-b85a-4301-b412-bd6476730f46
date: 2024-12-10 10:27:46
author: daichangya
cover: https://images.jsdiff.com/Java01.jpg
excerpt: "在Java开发中，与数据库交互是常见且关键的任务，而JDBC作为Java连接数据库的标准方式，其原生操作有时显得繁琐复杂。今天，我们将深入探索Apache组织提供的开源JDBC工具类库——common-dbutils，它将为我们的数据库操作带来极大的便利，让你轻松上手，快速提升开发效率。 一、com"
permalink: /archives/jie-suo-common-dbutils/
categories:
 - java
---

在Java开发中，与数据库交互是常见且关键的任务，而JDBC作为Java连接数据库的标准方式，其原生操作有时显得繁琐复杂。今天，我们将深入探索Apache组织提供的开源JDBC工具类库——common-dbutils，它将为我们的数据库操作带来极大的便利，让你轻松上手，快速提升开发效率。

## 一、common-dbutils简介
common-dbutils犹如一位贴心助手，为我们简化了JDBC的使用流程。它是一个小巧却功能强大的类包，只需花费短短几分钟，你就能掌握其基本用法，开启高效数据库操作的大门。

### （一）功能特性
- 提供简洁的API，减少大量重复代码编写。
- 自动处理资源的创建与释放，如连接、语句和结果集，避免资源泄露。
- 支持多种数据处理方式，方便将结果集转换为Java对象或集合，轻松融入业务逻辑。

### （二）适用场景
无论是小型项目快速迭代，还是大型企业级应用的数据库交互，common-dbutils都能大显身手，特别是在对开发速度和代码简洁性有较高要求的场景中表现出色。

## 二、下载与环境准备
### （一）获取common-dbutils
1. 打开Apache官方网站的commons-dbutils网页：[http://commons.apache.org/dbutils/](http://commons.apache.org/dbutils/)。
2. 在左边导航栏选择“Download”进入下载页面。
3. 这里提供了两种下载选项：
   -Binary：编译好的jar包，我们直接下载此文件到本地。
   -source：源代码包，供有需要的开发者查看和修改源码。

### （二）项目集成
1. 解压下载的文件，你会看到`commons-dbutils-1.8.1.jar`，这就是我们要使用的核心jar包。
2. 将其添加到你的Java项目中。以常见的Java项目为例，在Eclipse中，右键点击项目名称，选择“Build Path” -> “Configure Build Path”，在弹出的对话框中选择“Libraries”选项卡，点击“Add External JARs”，找到解压后的`commons-dbutils-1.8.1.jar`并添加。

### （三）依赖项引入
common-dbutils依赖于JDBC驱动，如果你使用的是MySQL数据库，还需要下载并引入MySQL的JDBC驱动（如`mysql-connector-java-5.1.6-bin.jar`）到项目中，步骤与添加common-dbutils的jar包类似。

## 三、核心API剖析
### （一）DbUtils类：资源管理大师
DbUtils是我们在数据库操作中的得力管家，它专注于处理连接、驱动加载等常规任务，所有方法均为静态，方便随时调用。

1. **连接关闭方法**
   -`public static void close(…) throws java.sql.SQLException`：提供了三个重载的关闭方法，用于关闭Connection、Statement和ResultSet。它会先检查参数是否为NULL，若不为NULL则执行关闭操作。
   -`public static void closeQuietly(…)`：这组方法不仅能在参数为NULL时避免关闭异常，还能隐藏程序中抛出的SQLException。其中`closeQuietly(Connection conn,Statement stmt,ResultSet rs)`尤为实用，在大多数数据库操作场景中，我们需要同时处理连接、声明和结果集，使用此方法可在最后统一关闭资源，简化代码结构。
   -`public static void CommitAndCloseQuietly(Connection conn)`：用于提交连接并关闭，且在关闭时不向上抛出可能发生的SQL异常，确保操作的平稳性。
2. **驱动加载方法**
   -`public static boolean loadDriver(java.lang.String driverClassName)`：负责装载并注册JDBC驱动程序，成功时返回true。使用此方法，无需手动捕捉`ClassNotFoundException`异常，使代码更加简洁。

### （二）QueryRunner类：查询执行引擎
QueryRunner类是我们执行SQL查询和更新操作的强大引擎，与ResultSetHandler配合使用，能以极少的代码完成复杂的数据库操作。

1. **构造方法**
   -默认构造方法：创建一个QueryRunner实例，后续操作需手动提供数据库连接。
   -带数据源参数的构造方法：接受一个`javax.sql.DataSource`作为参数，无需为每个方法提供数据库连接，数据源会自动获取新连接进行操作，适用于连接池场景。
2. **查询方法**
   -`public Object query(Connection conn, String sql, Object[] params, ResultSetHandler rsh) throws SQLException`：执行带参数的查询操作，参数数组中的元素将替换查询语句中的占位符。它内部自动处理`PreparedStatement`和`ResultSet`的创建与关闭，并通过`ResultSetHandler`将结果集转换为易于使用的格式。
   -`public Object query(String sql, Object[] params, ResultSetHandler rsh) throws SQLException`：与前一个方法类似，但不从方法参数获取数据库连接，而是从构造方法提供的数据源或通过`setDataSource`方法设置的数据源中获取。
   -`public Object query(Connection conn, String sql, ResultSetHandler rsh) throws SQLException`：执行不带参数的查询操作。
3. **更新方法**
   -`public int update(Connection conn, String sql, Object[] params) throws SQLException`：执行插入、更新或删除等更新操作，参数数组用于替换SQL语句中的占位符。
   -`public int update(Connection conn, String sql) throws SQLException`：执行不带参数的更新操作。

### （三）ResultSetHandler接口：结果集转换专家
ResultSetHandler接口专注于将`java.sql.ResultSet`转换为我们需要的格式，其核心方法`Object handle(java.sql.ResultSet.rs)`接受结果集作为参数，并返回转换后的对象。由于返回类型为`java.lang.Object`，除原始Java类型外，可根据需求灵活返回各种类型。

common-dbutils为该接口提供了九个实用的实现类，满足常见的数据处理需求：
1. **ArrayHandler**：将结果集中的第一行数据转换为对象数组。
2. **ArrayListHandler**：把结果集中的每一行数据转换为对象数组，并存储在List中。
3. **BeanHandler**：将结果集中的第一行数据封装到对应的JavaBean实例中。
4. **BeanListHandler**：把结果集中的每一行数据封装到JavaBean实例中，再存入List。
5. **ColumnListHandler**：将结果集中某一列的数据存储到List中。
6. **KeyedHandler**：把结果集中的每一行数据封装到Map里，再根据指定的key将这些Map存入另一个Map中。
7. **MapHandler**：将结果集中的第一行数据封装到Map中，键为列名，值为对应数据。
8. **MapListHandler**：把结果集中的每一行数据封装到Map里，然后存入List。
9. **ScalarHandler**：将结果集中某一条记录的某一列数据存储为Object。

如果这些实现类无法满足特定需求，开发者可轻松创建自己的实现类，定制个性化的数据处理逻辑。

### （四）其他辅助类和接口
1. **QueryLoader类**：作为属性文件加载器，可将属性文件中的SQL语句加载到内存中，方便管理和复用SQL。
2. **SqlNullCheckedResultSet类**：用于在SQL语句执行后，对结果集中的NULL值进行替换，确保数据的完整性和一致性。
3. **StringTrimmedResultSet类**：能够去除ResultSet中字段的左右空格，提高数据的准确性和可读性。
4. **RowProcessor接口及其实现类BasicRowProcessor**：提供了将结果集行数据转换为其他格式的功能，进一步拓展了数据处理的灵活性。

## 四、实战演练：员工信息管理系统
### （一）数据库准备
我们使用MySQL 5数据库服务器，创建名为“test”的数据库，并执行以下建表语句：
```sql
CREATE TABLE `employee` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(50) default NULL,
  `age` int(11) default NULL,
  `position` varchar(50) default NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
插入一些示例数据，以便后续操作：
```sql
INSERT INTO `employee` (`name`, `age`, `position`) VALUES ('张三', 25, '程序员');
INSERT INTO `employee` (`name`, `age`, `position`) VALUES ('李四', 30, '项目经理');
INSERT INTO `employee` (`name`, `age`, `position`) VALUES ('王五', 28, '测试工程师');
```

### （二）Java项目搭建
1. 创建Java工程，结构如下：
   -`src`：存放Java源文件。
       -`org.blog.jsdiff.common`：包含工具类。
           -`MyDbUtils.java`：用于获取数据库连接等操作。
       -`com.jsdiff.dao`：数据访问对象（DAO）层。
           -`DAOException.java`：自定义异常类。
           -`EmployeeDao.java`：员工数据访问接口实现类。
       -`com.jsdiff.domain`：实体类。
           -`Employee.java`：员工实体类。
   -`lib`：存放项目依赖的jar包，如`commons-dbutils-1.8.1.jar`和`mysql-connector-java-5.1.6-bin.jar`。
   -`JRE System Library [jdk1.6.0]`：Java运行时环境库。

### （三）代码实现
1. **Employee类（员工实体类）**
```java
package com.jsdiff.domain;

public class Employee {
    private int id;
    private String name;
    private int age;
    private String position;

    public Employee() {
    }

    public Employee(int age, String name, String position) {
        super();
        this.age = age;
        this.name = name;
        this.position = position;
    }

    // 生成所有属性的getter和setter方法
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getPosition() {
        return position;
    }

    public void setPosition(String position) {
        this.position = position;
    }

    @Override
    public String toString() {
        return "[id=" + this.id + ",name=" + this.name + ",age=" + age
                + ",position=" + this.position + "]";
    }
}
```
2. **EmployeeDao类（员工数据访问对象类）**
```java
package com.jsdiff.dao;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

import org.apache.commons.dbutils.DbUtils;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;
import org.blog.jsdiff.common.MyDbUtils;
import com.jsdiff.domain.Employee;

public class EmployeeDao {
    /**
     * 新增一个员工实例
     * 
     * @param empl  员工对象
     * @param conn  数据库连接
     * @throws DAOException
     */
    public void insertEmployee(Connection conn, Employee empl) throws DAOException {
        String sql = "INSERT INTO employee(name,age,position) VALUES(?,?,?)";
        try {
            QueryRunner qr = new QueryRunner();
            Object[] params = { empl.getName(), empl.getAge(), empl.getPosition() };
            qr.update(conn, sql, params);
        } catch (SQLException e) {
            throw new DAOException(e);
        }
    }

    /**
     * 根据ID删除一个员工实例
     * 
     * @param conn  数据库连接
     * @param id    员工ID
     * @throws DAOException
     */
    public void deleteEmloyeeById(Connection conn, int id) throws DAOException {
        String sql = "DELETE FROM employee WHERE id=?";
        try {
            QueryRunner qr = new QueryRunner();
            qr.update(conn, sql, id);
        } catch (SQLException e) {
            throw new DAOException(e);
        }
    }

    /**
     * 更新员工的信息
     * 
     * @param conn  数据库连接
     * @param empl  员工对象
     * @throws DAOException
     */
    public void updateEmployee(Connection conn, Employee empl) throws DAOException {
        String sql = "UPDATE employee SET name=?,age=?,position=? WHERE id=?";
        try {
            QueryRunner qr = new QueryRunner();
            Object[] params = { empl.getName(), empl.getAge(),
                    empl.getPosition(), empl.getId() };
            qr.update(conn, sql, params);
        } catch (SQLException e) {
            throw new DAOException(e);
        }
    }

    /**
     * 根据ID获取该员工实例
     * 
     * @param conn  数据库连接
     * @param id    员工ID
     * @return 员工对象
     * @throws DAOException
     */
    public Employee getEmployeeById(Connection conn, int id) throws DAOException {
        Employee empl = null;
        String sql = "SELECT id,name,age,position FROM employee WHERE id=?";
        try {
            QueryRunner qr = new QueryRunner();
            empl = (Employee) qr.query(conn, sql, id,
                    new BeanHandler(Employee.class));
        } catch (SQLException e) {
            throw new DAOException(e);
        }
        return empl;
    }

    /**
     * 获取所有的员工列表
     * 
     * @param conn  数据库连接
     * @return 员工实例列表
     * @throws DAOException
     */
    @SuppressWarnings("unchecked")
    public List<Employee> getEmployeeList(Connection conn) throws DAOException {
        List<Employee> list = null;
        String sql = "SELECT id,name,age,position FROM employee";
        try {
            QueryRunner qr = new QueryRunner();
            list = (List<Employee>) qr.query(conn, sql,
                    new BeanListHandler(Employee.class));
        } catch (SQLException e) {
            throw new DAOException(e);
        }
        return list;
    }

    public static void main(String[] args) throws SQLException {
        Connection conn = MyDbUtils.getConnection();
        List<Employee> list = new EmployeeDao().getEmployeeList(conn);
        for (Employee empl : list) {
            System.out.println(empl);
        }
        DbUtils.close(conn);
    }
}
```
3. **MyDbUtils类（数据库连接工具类）**
```java
package org.blog.jsdiff.common;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import org.apache.commons.dbutils.DbUtils;

public class MyDbUtils {
    private static final String URL = "jdbc:mysql://localhost:3306/test";
    private static final String USERNAME = "root";
    private static final String PASSWORD = "password";

    static {
        try {
            // 加载MySQL驱动
            DbUtils.loadDriver("com.mysql.jdbc.Driver");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USERNAME, PASSWORD);
    }
}
```

### （四）功能测试
1. 在`EmployeeDao`类的`main`方法中，我们首先获取数据库连接，然后调用`getEmployeeList`方法查询所有员工信息并打印输出。运行`main`方法，控制台将显示员工列表：
```
[id=1,name=张三,age=25,position=程序员]
[id=2,name=李四,age=30,position=项目经理]
[id=3,name=王五,age=28,position=测试工程师]
```
2. 尝试新增员工：
```java
Employee newEmployee = new Employee(26, "赵六", "设计师");
Connection conn = MyDbUtils.getConnection();
EmployeeDao employeeDao = new EmployeeDao();
employeeDao.insertEmployee(conn, newEmployee);
List<Employee> updatedList = employeeDao.getEmployeeList(conn);
for (Employee empl : updatedList) {
    System.out.println(empl);
}
DbUtils.close(conn);
```
再次运行`main`方法，你会发现新员工“赵六”已成功插入数据库并显示在列表中。
3. 根据ID更新员工信息：
```java
Employee updatedEmployee = new Employee(27, "赵六", "高级设计师");
updatedEmployee.setId(4); // 假设新插入的员工ID为4
Connection conn = MyDbUtils.getConnection();
EmployeeDao employeeDao = new EmployeeDao();
employeeDao.updateEmployee(conn, updatedEmployee);
Employee retrievedEmployee = employeeDao.getEmployeeById(conn, 4);
System.out.println(retrievedEmployee);
DbUtils.close(conn);
```
运行后，员工“赵六”的年龄和职位信息将更新为“27”和“高级设计师”。
4. 根据ID删除员工：
```java
Connection conn = MyDbUtils.getConnection();
EmployeeDao employeeDao = new EmployeeDao();
employeeDao.deleteEmloyeeById(conn, 4);
List<Employee> finalList = employeeDao.getEmployeeList(conn);
for (Employee empl : finalList) {
    System.out.println(empl);
}
DbUtils.close(conn);
```
运行代码后，ID为4的员工（即“赵六”）将从数据库中删除，再次查询员工列表时，将不再显示该员工信息。

通过以上实战演练，我们可以看到common-dbutils在实际项目中的强大功能和便捷性，它极大地简化了数据库操作代码，提高了开发效率，让我们能够更专注于业务逻辑的实现。

## 五、总结与展望
common-dbutils为Java开发者在数据库操作领域提供了一种简洁、高效的解决方案。通过其核心类和接口，我们能够轻松应对各种常见的数据库任务，从简单的查询到复杂的数据更新和处理，都变得得心应手。

### （一）优势总结
1. 代码简洁性：大幅减少了与JDBC原生操作相关的样板代码，使代码结构更加清晰易读。
2. 资源管理自动化：自动处理连接、语句和结果集的创建与释放，有效避免了资源泄露的风险。
3. 数据处理灵活性：丰富的ResultSetHandler实现类满足了多样化的数据转换需求，同时支持自定义实现，适应各种特殊场景。

### （二）未来展望
随着技术的不断发展，数据库技术也在持续演进。common-dbutils作为一款优秀的工具库，也在不断适应新的需求和挑战。未来，我们期待它能够更好地支持新兴数据库技术，进一步优化性能，提供更多便捷的功能，为Java开发者在数据库操作领域带来更多的惊喜和便利。同时，我们也鼓励开发者积极探索和应用common-dbutils，结合自身项目需求，充分发挥其优势，为项目开发注入强大动力。

掌握common-dbutils，就等于掌握了一把开启高效数据库操作之门的钥匙。希望本文能够帮助你快速上手这个强大的工具，在Java开发之路上更加游刃有余。快来一起体验common-dbutils带来的便捷与高效吧！如果你在使用过程中有任何疑问或建议，欢迎在评论区留言分享。
