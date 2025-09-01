---
title: 用java实现JDBC数据库连接池
id: 524
date: 2024-10-31 22:01:44
author: daichangya
excerpt: 这次写数据库连接池主要想解决的还是servlet访问数据库获取数据的稳定性问题，于是便研究了一下，下面来讲一讲如何用java来写一个适合自己用的数据库连接池。这个东西大家并不陌生，通过使用数据连接池我们能够更好地控制程序和数据库之间建立的连接，减小数据库访问压力，也便于管理连接，提高了利用率和工作性能。　　设计数据库连接池，个人认为应该注意以下几点：　　1、能够控制连接池的大小
permalink: /archives/yong-java-shi-xian-JDBC-shu-ju-ku-lian/
tags:
- jdbc
---

 

这次写数据库连接池主要想解决的还是servlet访问数据库获取数据的稳定性问题，于是便研究了一下，下面来讲一讲如何用java来写一个适合自己用的数据库连接池。这个东西大家并不陌生，通过使用数据连接池我们能够更好地控制程序和数据库之间建立的连接，减小数据库访问压力，也便于管理连接，提高了利用率和工作性能。

　　设计数据库连接池，个人认为应该注意以下几点：

　　1、能够控制连接池的大小

　　2、有一个统一的接口用于获得连接

　　3、使用后的连接要有一个接口能够接受并处理掉

　　4、连接池要有自我维护能力，比如说暂时提高连接池大小以应对可能的连接小高潮，或者处理多余的连接

　　ok，我们先确定连接池的数据结构：

```
    public class SimpleConnetionPool {
        private static LinkedList m_notUsedConnection = new LinkedList();
        private static HashSet m_usedUsedConnection = new HashSet();
        private static String m_url = "";
        private static String m_user = "";
        private static String m_password = "";
        private static int m_maxConnect = 3;
        static final boolean DEBUG = false;
        static private long m_lastClearClosedConnection = System
                .currentTimeMillis();
        public static long CHECK_CLOSED_CONNECTION_TIME = 5000; // 5秒
    }
```

　　然后我们看看数据库连接池的核心部分，首先是清除连接池中多余的连接。我们每隔一段时间就对连接池中的所有连接进行检查，第一轮循环判断这些链接是否已经关闭，如果关闭了则直接移除它们，第二轮循环则是根据目前规定的最大数量裁撤空闲连接。

```
    private static void clearClosedConnection() {
            long time = System.currentTimeMillis();
    
            // 时间不合理，没有必要检查
            if (time < m_lastClearClosedConnection) {
                time = m_lastClearClosedConnection;
                return;
            }
    
            // 时间太短，没有必要检查
            if (time - m_lastClearClosedConnection < CHECK_CLOSED_CONNECTION_TIME) {
                return;
            }
    
            m_lastClearClosedConnection = time;
    
            // 开始检查没有使用的Connection
            Iterator iterator = m_notUsedConnection.iterator();
            while (iterator.hasNext()) {
                Connection con = (Connection) iterator.next();
    
                try {
                    if (con.isClosed()) {
                        iterator.remove();
                    }
                } catch (SQLException e) {
                    iterator.remove();
    
                    if (DEBUG) {
                        System.out.println("问题连接已断开");
                    }
                }
            }
    
            // 清除多余的Connection
            int decrease = getDecreasingConnectionCount();
    
            while (decrease > 0&& m_notUsedConnection.size() > 0) {
                Connection con = (Connection) m_notUsedConnection.removeFirst();
    
                try {
                    con.close();
                } catch (SQLException e) {
    
                }
    
                decrease--;
            }
        }
```

　　接下来我们看一下申请一个新的连接是如何进行的，首先我们先调用之前的清理器来清除多余的连接和无法使用的连接，之后在空闲连接中寻找是否有可是的连接，如果有符合的则直接分配出去，但是要是没找到的话该怎么办呢？

　　这时候我们就需要建立新的连接来提供了，建立新的连接后我们将其中一个分配出去，剩下的加入到空闲连接中去等待分配就可以了。

```
    public static synchronized Connection getConnection() {
            // 关闭清除多余的连接
            clearClosedConnection();
    
            // 输出当前总连接数
            if(DEBUG)
                System.out.println("当前总连接数：" + getConnectionCount());
    
            // 寻找空闲的连接
            while (m_notUsedConnection.size() > 0) {
                try {
                    Connection con = (Connection) m_notUsedConnection.removeFirst();
    
                    if (con.isClosed()) {
                        continue;
                    }
    
                    m_usedUsedConnection.add(con);
                    if (DEBUG) {
                        // System.out.println("连接初始化成功");
                    }
                    return con;
                } catch (SQLException e) {
                }
            }
    
            // 没有找到，建立一些新的连接以供使用
            int newCount = getIncreasingConnectionCount();
            LinkedList list = new LinkedList();
            Connection con = null;
    
            for (int i = 0; i < newCount; i++) {
                con = getNewConnection();
                if (con != null) {
                    list.add(con);
                }
            }
    
            // 没有成功建立连接，访问失败
            if (list.size() == 0)
                return null;
    
            // 成功建立连接，使用的加入used队列，剩下的加入notUsed队列
            con = (Connection) list.removeFirst();
            m_usedUsedConnection.add(con);
            m_notUsedConnection.addAll(list);
            list.clear();
    
            return con;
        }
```

　　根据之前总结的我们还需要一个，就是交还连接了，这个很简单，把占用中的链接移出来放到空闲连接里就可以了~很简单吧~

```
    static synchronized void pushConnectionBackToPool(Connection con) {
            boolean exist = m_usedUsedConnection.remove(con);
            if (exist) {
                m_notUsedConnection.addLast(con);
            }
        }
```

　　这就是这个数据连接池的核心部分了，现在我们来看整套代码就容易多了，其实需要注意的就是刚才说的那些：

```
    package cn.com.css.cas.jdbc;
    
    import java.sql.Connection;
    import java.sql.Driver;
    import java.sql.DriverManager;
    import java.sql.SQLException;
    import java.util.HashSet;
    import java.util.Iterator;
    import java.util.LinkedList;
    
    /**
     * JDBC数据库连接池
     * 
     * @author Woud
     * 
     */
    public class SimpleConnetionPool {
        private static LinkedList m_notUsedConnection = new LinkedList();
        private static HashSet m_usedUsedConnection = new HashSet();
        private static String m_url = "";
        private static String m_user = "";
        private static String m_password = "";
        private static int m_maxConnect = 3;
        static final boolean DEBUG = false;
        static private long m_lastClearClosedConnection = System
                .currentTimeMillis();
        public static long CHECK_CLOSED_CONNECTION_TIME = 5000; // 5秒
    
        static {
            try {
                initDriver();
            } catch (InstantiationException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (IllegalAccessException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (ClassNotFoundException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    
        public SimpleConnetionPool(String url, String user, String password) {
            m_url = url;
            m_user = user;
            m_password = password;
        }
    
        private static void initDriver() throws InstantiationException,
                IllegalAccessException, ClassNotFoundException {
            Driver driver = null;
    
            // 读取MySql的Driver
            driver = (Driver) Class.forName("com.mysql.jdbc.Driver").newInstance();
            installDriver(driver);
    
            /*
             * // 读取postgresql的driver driver = (Driver)
             * Class.forName("org.postgresql.Driver").newInstance();
             * installDriver(driver);
             */
    
        }
    
        public static void installDriver(Driver driver) {
            try {
                DriverManager.registerDriver(driver);
            } catch (SQLException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    
        public static synchronized Connection getConnection() {
            // 关闭清除多余的连接
            clearClosedConnection();
    
            // 输出当前总连接数
            if(DEBUG)
                System.out.println("当前总连接数：" + getConnectionCount());
    
            // 寻找空闲的连接
            while (m_notUsedConnection.size() > 0) {
                try {
                    Connection con = (Connection) m_notUsedConnection.removeFirst();
    
                    if (con.isClosed()) {
                        continue;
                    }
    
                    m_usedUsedConnection.add(con);
                    if (DEBUG) {
                        // System.out.println("连接初始化成功");
                    }
                    return con;
                } catch (SQLException e) {
                }
            }
    
            // 没有找到，建立一些新的连接以供使用
            int newCount = getIncreasingConnectionCount();
            LinkedList list = new LinkedList();
            Connection con = null;
    
            for (int i = 0; i < newCount; i++) {
                con = getNewConnection();
                if (con != null) {
                    list.add(con);
                }
            }
    
            // 没有成功建立连接，访问失败
            if (list.size() == 0)
                return null;
    
            // 成功建立连接，使用的加入used队列，剩下的加入notUsed队列
            con = (Connection) list.removeFirst();
            m_usedUsedConnection.add(con);
            m_notUsedConnection.addAll(list);
            list.clear();
    
            return con;
        }
    
        public static Connection getNewConnection() {
            try {
                Connection con = DriverManager.getConnection(m_url, m_user,
                        m_password);
                return con;
            } catch (SQLException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
    
            return null;
        }
    
        static synchronized void pushConnectionBackToPool(Connection con) {
            boolean exist = m_usedUsedConnection.remove(con);
            if (exist) {
                m_notUsedConnection.addLast(con);
            }
        }
    
        public static int close() {
            int count = 0;
    
            Iterator iterator = m_notUsedConnection.iterator();
            while (iterator.hasNext()) {
                try {
                    ((Connection) iterator.next()).close();
                    count++;
                } catch (SQLException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            m_notUsedConnection.clear();
    
            iterator = m_usedUsedConnection.iterator();
            while (iterator.hasNext()) {
                try {
                    ((Connection) iterator.next()).close();
                } catch (SQLException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
            m_usedUsedConnection.clear();
    
            return count;
        }
    
        private static void clearClosedConnection() {
            long time = System.currentTimeMillis();
    
            // 时间不合理，没有必要检查
            if (time < m_lastClearClosedConnection) {
                time = m_lastClearClosedConnection;
                return;
            }
    
            // 时间太短，没有必要检查
            if (time - m_lastClearClosedConnection < CHECK_CLOSED_CONNECTION_TIME) {
                return;
            }
    
            m_lastClearClosedConnection = time;
    
            // 开始检查没有使用的Connection
            Iterator iterator = m_notUsedConnection.iterator();
            while (iterator.hasNext()) {
                Connection con = (Connection) iterator.next();
    
                try {
                    if (con.isClosed()) {
                        iterator.remove();
                    }
                } catch (SQLException e) {
                    iterator.remove();
    
                    if (DEBUG) {
                        System.out.println("问题连接已断开");
                    }
                }
            }
    
            // 清除多余的Connection
            int decrease = getDecreasingConnectionCount();
    
            while (decrease > 0&& m_notUsedConnection.size() > 0) {
                Connection con = (Connection) m_notUsedConnection.removeFirst();
    
                try {
                    con.close();
                } catch (SQLException e) {
    
                }
    
                decrease--;
            }
        }
    
        public static int getIncreasingConnectionCount() {
            int count = 1;
            count = getConnectionCount() / 4;
    
            if (count < 1)
                count = 1;
    
            return count;
        }
    
        public static int getDecreasingConnectionCount() {
            int count = 0;
    
            if (getConnectionCount() > m_maxConnect) {
                count = getConnectionCount() - m_maxConnect;
            }
    
            return count;
        }
    
        public static synchronized int getNotUsedConnectionCount() {
            return m_notUsedConnection.size();
        }
    
        public static synchronized int getUsedConnectionCount() {
            return m_usedUsedConnection.size();
        }
    
        public static synchronized int getConnectionCount() {
            return m_notUsedConnection.size() + m_usedUsedConnection.size();
        }
    
    }
```

　我们做好了这个连接池之后怎么用呢，这很简单，我们用Singleton模式做一个连接池管理器，然后对接口进行简单的封装后就可以进行使用了，管理器调用连接池的getconnection接口获得connect后和数据库建立连接，运行sql后交还connect并把结果反馈回来就可以了。