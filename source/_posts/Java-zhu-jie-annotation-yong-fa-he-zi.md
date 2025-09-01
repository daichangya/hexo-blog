---
title: Java注解annotation用法和自定义注解处理器
id: 502
date: 2024-10-31 22:01:43
author: daichangya
excerpt: 前言：在J2EE中，注解使得开发更加便利，省去了生成XML文件的过程，在Hibernate实体声明中，可以简简单单的用几个注解就可以免去生成一个XML的文件操作。这里就主要论述一下annotation的用法和自定义注解处理器。当在创建描述符性质的类或接口时，有大量重复性的工作时候，就可以利用注解来实现。
permalink: /archives/Java-zhu-jie-annotation-yong-fa-he-zi/
categories:
- java基础
---

 

前言：

在J2EE中，注解使得开发更加便利，省去了生成XML文件的过程，在Hibernate实体声明中，可以简简单单的用几个注解就可以免去生成一个XML的文件操作。这里就主要论述一下annotation的用法和自定义注解处理器。当在创建描述符性质的类或接口时，有大量重复性的工作时候，就可以利用注解来实现。

基本语法：

 Java目前包括三种标准注解和四种元注解。元注解主要负责注解其他注解的。

 三种标准注解：

@Override，表示当前的方法定义覆盖了父类中的方法。必须要有相同的方法签名即(方法名，参数类型，参数顺序，参数个数)都一样。否则在编译过程中发出错误提示。

@Deprecated,对不应该再使用的方法添加注解，当使用这个方法的时候，会在编译时候显示提示信息。

@SuppressWarnings,关闭不当的编译器报警信息

四种元注解：

 @Target,表示该注解可以用什么地方。

如CONSTRUCTOR,构造器声明；FIELD,域声明;METHOD,方法声明;TYPE，类，接口或enum声明

 @Retention,表示需要在什么级别保存该注解信息。

  如SOURCE,注解将被编译器丢弃；CLASS,注解在class文件可用，但会被VM丢弃

RUNTIME,VM将在运行期间也保留注解，可以使用反射机制读取注解信息

 @Documented,将此注解包含到Javadoc中。

 @Inherited,允许子类继承父类的注解。

定义注解：

自定义注解是以@interface为标志的。如同一个接口的定义，这里面定义的每个方法名，就是使用注解时候的元素名，方法的返回值就是元素的类型，可以利用default来声明默认值，不过对于非基本类型，不能设置为null为默认值，一般对于字符串使用空字符串作为其默认值。

如下所示：

```
package whut.annotation;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
//定义一个注解
@Target(ElementType.METHOD)//定义该注解将应用于什么地方，方法或者域
@Retention(RetentionPolicy.RUNTIME)//定义该注解在哪一个级别可用
public @interface UseCase {
    //注解元素，可以指定默认值，在使用注解的时候，可以直接给元素赋值如id=5
    public int id();
    public String description() default "no description";
     //利用枚举来设置参数类型
     public enum ParameterType { STRING, SHORT, INT, BOOL, LONG, OBJECT };
     // 默认值,在使用注解的时候，只需要为元素赋值
     public ParameterType type() default ParameterType.STRING;
}
```

使用注解：

在类中任意的域值前，或者方法前等直接@注解名，如@UseCase（id=5），使用注解的过程中，必须对于没有设置默认值的元素进行赋值操作，对于每个元素进行按照名-值对的方式赋值。如果在注解定义中有名为value的元素，并且它是唯一需要赋值的，可以直接在括号里给出value所需要的值。

   注解是不能继承的。

下面是一个基本的利用非apt实现的注解处理器模型。

这个模型可以注解实体，进行数据库的映射建表操作。是最最基本的操作。

注解定义:将四个注解名是在不同的文件中。

```
package whut.annotationDB;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
//定义字段的约束
public @interface Constraints {
    boolean primaryKey() default false;
    boolean allowNull() default true;
    boolean unique() default false;
}
////////////////////////////
package whut.annotationDB;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
@Target(ElementType.TYPE)//类，接口或enum
@Retention(RetentionPolicy.RUNTIME)
//定义表名的注解
public @interface DBTable {
    public String name() default "";
}
///////////////////////////
package whut.annotationDB;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
@Target(ElementType.FIELD)//类，接口或enum
@Retention(RetentionPolicy.RUNTIME)
public @interface SQLInteger {
      String name() default "";
      //嵌套注解的功能,将column类型的数据库约束信息嵌入其中
      Constraints constraints() default @Constraints;
}
///////////////////////////////
package whut.annotationDB;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
@Target(ElementType.FIELD)//类，接口或enum
@Retention(RetentionPolicy.RUNTIME)
public @interface SQLString {
    int value() default 0;
    String name() default "";
    //注解元素中引用别的注解，
    Constraints constraints() default @Constraints;
}
```

实体使用注解：这里是运用了运行时候处理注解，所以RetentionPolicy.RUNTIME

```
package whut.annotationDB;
@DBTable(name="MEMBER")
public class Member {
    //在使用注解过程中，如果有元素是value，并且只有value需要赋值，
    //则只需要在()中将值写入
    @SQLString(30)
    private String firstName;
    @SQLString(50)
    private String lastName;
    @SQLInteger
    private Integer age;
    @SQLString(value=30,constraints=@Constraints(primaryKey=true))
    private String handle;
    public String getFirstName() {
        return firstName;
    }
    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }
    public String getLastName() {
        return lastName;
    }
    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
    public Integer getAge() {
        return age;
    }
    public void setAge(Integer age) {
        this.age = age;
    }
    public String getHandle() {
        return handle;
    }
    public void setHandle(String handle) {
        this.handle = handle;
    }
}
```

具体的非apt实现的注解处理器：

```
package whut.annotationDB;
import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
public class TableCreator {
    public Connection getConnection() {
        String user = "root";
        String password = "";
        String serverUrl = "jdbc:mysql://localhost:3306/carrent?user=root&password=";
        try {
            Class.forName("com.mysql.jdbc.Driver");
            Connection con = DriverManager.getConnection(serverUrl, user,
                    password);
            return con;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
    //实现创建表
    public static void main(String[] args) {
        TableCreator tc = new TableCreator();
        tc.executeCreateDB(Member.class);
    }
    public void executeCreateDB(Class<?> entity) {
        String sqlStr = explainAnnotation(entity);
        Connection con = getConnection();
        PreparedStatement psql = null;
        if (con != null && !sqlStr.equals("error")) {
            try {
                psql = con.prepareStatement(sqlStr);
                psql.execute();
            } catch (SQLException e) {
                e.printStackTrace();
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                try {
                    if (psql != null)
                        psql.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
                try {
                    if (con != null)
                        psql.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        } else
            System.out.println("failure to...");
    }
    // 真正的处理器,Class<?>必须用这个表明
    public String explainAnnotation(Class<?> entity) {
        // 获取指定类型的注解
        DBTable dbtable = entity.getAnnotation(DBTable.class);
        if (dbtable == null) {
            System.out.println("No DBTable annotation in class"
                    + entity.getName());
            return "error";
        } else {
            String tableName = dbtable.name();// 获取注解name值，即表名称
            // 当没有设置name值，直接利用类的名作为表名
            if (tableName.length() < 1)
                tableName = entity.getName().toUpperCase();// 转换大写
            // 准备处理字段注解
            List<String> columnsDefs = new ArrayList<String>();
            // 获取该类的所有字段
            for (Field field : entity.getDeclaredFields()) {
                String columnName = null;
                // 获取该字段所有的注解
                Annotation[] anns = field.getDeclaredAnnotations();
                // Annotation[] anns=field.getAnnotations();
                // 当有注解的时候
                if (anns.length >= 1) {
                    // 判断注解的类型
                    if (anns[0] instanceof SQLInteger) {
                        SQLInteger sInt = (SQLInteger) anns[0];
                        // 当没有name时候，将字段大写为列名
                        if (sInt.name().length() < 1)
                            columnName = field.getName().toUpperCase();
                        else
                            columnName = sInt.name();
                        columnsDefs.add(columnName + " INT"
                                + getConstraints(sInt.constraints()));
                    }
                    if (anns[0] instanceof SQLString) {
                        SQLString sString = (SQLString) anns[0];
                        // 当没有name时候，将字段大写为列名
                        if (sString.name().length() < 1)
                            columnName = field.getName().toUpperCase();
                        else
                            columnName = sString.name();
                        columnsDefs.add(columnName + " VARCHAR("
                                + sString.value() + ")"
                                + getConstraints(sString.constraints()));
                    }
                }
            }
            StringBuilder createDB = new StringBuilder("CREATE TABLE "
                    + tableName + "(");
            for (String cols : columnsDefs)
                createDB.append(" " + cols + ",");
            // 移除最后一个，号
            String tableSQL = createDB.substring(0, createDB.length() - 1)
                    + ");";
            // 输出创建表的过程
            System.out.println("Table Creation SQL is:\n" + tableSQL);
            return tableSQL;
        }
    }
    // 返回指定的约束
    public String getConstraints(Constraints con) {
        String constras = "";
        if (!con.allowNull())
            constras += " NOT NULL";
        if (con.primaryKey())
            constras += " PRIMARY KEY";
        if (con.unique())
            constras += " UNIQUE";
        return constras;
    }
}
```