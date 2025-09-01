---
title: Java 连接池的工作原理
id: 688
date: 2024-10-31 22:01:45
author: daichangya
excerpt: "什么是连接？连接，是我们的编程语言与数据库交互的一种方式。我们经常会听到这么一句话“数据库连接很昂贵“。有人接受这种说法，却不知道它的真正含义。因此，下面我将解释它究竟是什么。[如果你已经知道了，你可以跳到它的工作原理部分]"
permalink: /archives/17965373/
tags: 
 - jdbc
---

 

什么是连接？

连接，是我们的编程语言与数据库交互的一种方式。我们经常会听到这么一句话“数据库连接很昂贵“。

有人接受这种说法，却不知道它的真正含义。因此，下面我将解释它究竟是什么。\[如果你已经知道了，你可以跳到它的工作原理部分\]

创建连接的代码片段：
```
String connUrl = "jdbc:mysql://your.database.domain/yourDBname"; 
Class.forName("com.mysql.jdbc.Driver"); 
Connection con = DriverManager.getConnection (connUrl); 
```
当我们创建了一个Connection对象，它在内部都执行了什么：

1.“DriverManager”检查并注册驱动程序，  
2.“com.mysql.jdbc.Driver”就是我们注册了的驱动程序，它会在驱动程序类中调用“connect(url…)”方法。  
3.com.mysql.jdbc.Driver的connect方法根据我们请求的“connUrl”，创建一个“Socket连接”，连接到IP为“your.database.domain”，默认端口3306的数据库。  
4.创建的Socket连接将被用来查询我们指定的数据库，并最终让程序返回得到一个结果。

为什么昂贵？

现在让我们谈谈为什么说它“昂贵“。

如果创建Socket连接花费的时间比实际的执行查询的操作所花费的时间还要更长。

这就是我们所说的“数据库连接很昂贵”，因为连接资源数是1，它需要每次创建一个Socket连接来访问DB。

因此，我们将使用连接池。

连接池初始化时创建一定数量的连接，然后从连接池中重用连接，而不是每次创建一个新的。

怎样工作？

接下来我们来看看它是如何工作，以及如何管理或重用现有的连接。

我们使用的连接池供应者，它的内部有一个连接池管理器，当它被初始化：

1.它创建连接池的默认大小，比如指定创建5个连接对象，并把它存放在“可用”状态的任何集合或数组中。

例如，代码片段：

```

    String connUrl = "jdbc:mysql://your.database.domain/yourDBname";
    String driver = "com.mysql.jdbc.Driver";
    private Map<java.sql.Connection, String> connectionPool = null;

    private void initPool() {
        try {
            connectionPool = new HashMap<java.sql.Connection, String>();
            Class.forName(driver);
            java.sql.Connection con = DriverManager.getConnection(dbUrl);
            for (int poolInd = poolSize; poolInd < 0; poolInd++) {
                connectionPool.put(con, "AVAILABLE");
            }
        }
    }
```
2.当我们调用connectionProvider.getConnection()，然后它会从集合中获取一个连接，当然状态也会更改为“不可用”。

例如，代码片段：
```
 public java.sql.Connection getConnection() throws ClassNotFoundException, SQLException {
        boolean isConnectionAvailable = true;
        for (Entry<java.sql.Connection, String> entry : connectionPool.entrySet()) {
            synchronized (entry) {
                if (entry.getValue() == "AVAILABLE") {
                    entry.setValue("NOTAVAILABLE");
                    return (java.sql.Connection) entry.getKey();
                }
                isConnectionAvailable = false;
            }
        }
        if (!isConnectionAvailable) {
            Class.forName(driver);
            java.sql.Connection con = DriverManager.getConnection(connUrl);
            connectionPool.put(con, "NOTAVAILABLE");
            return con;
        }
        return null;
    }

```
3.当我们关闭得到的连接，ConnectionProvider是不会真正关闭连接。相反，只是将状态更改为“AVAILABLE”。

例如，代码片段：  
```
    public void closeConnection(java.sql.Connection connection) throws ClassNotFoundException, SQLException {
        for (Entry<java.sql.Connection, String> entry : connectionPool.entrySet()) {
            synchronized (entry) {
                if (entry.getKey().equals(connection)) {
                    //Getting Back the conncetion to Pool 
                    entry.setValue("AVAILABLE");
                }
            }
        }
    } 
```
基本上连接池的实际工作原理就是这样，但也有可能使用不同的方式。

现在，你可能有一个问题，我们是否可以创造我们自己的连接池机制？  
   
我的建议是使用已经存在的连接池机制，像[C3P0](http://www.oschina.net/p/c3p0)，[DBCP](http://www.oschina.net/p/dbcp)等。

  
[英文原文](http://kkarthikeyanblog.wordpress.com/2012/09/24/connection-pooling-what-why-how/) 