---
title: 关于ClassLoader中getResource与getResourceAsStream的疑问
id: 359
date: 2024-10-31 22:01:42
author: daichangya
excerpt: "某日临近下班，一个同事欲任何类中获取项目绝对路径，不通过Request方式获取，可是始终获取不到预想的路径。于是晚上回家google了一下，误以为是System.getProperty(\"java.class.path\")-未实际进行测试，早上来和同事沟通，提出了使用这个内置方法，结果人家早已验证过，该方法是打印出CLASSPATH环境变量的值。"
permalink: /archives/guan-yu-classloaderzhong-getresourceyu-getresourceasstreamde-yi-wen/
categories:
  - Java
tags:
  - 文件操作
  - ClassLoader
---

背景：

某日临近下班，一个同事欲任何类中获取项目绝对路径，不通过Request方式获取，可是始终获取不到预想的路径。于是晚上回家google了一下，误以为是System.getProperty("java.class.path")-未实际进行测试，早上来和同事沟通，提出了使用这个内置方法，结果人家早已验证过，该方法是打印出CLASSPATH环境变量的值。

于是乎，继续google，找到了Class的getResource与getResourceAsStream两个方法。这两个方法会委托给ClassLoader对应的同名方法。以为这样就可以搞定(实际上确实可以搞定)，但验证过程中却发生了奇怪的事情。

软件环境：Windows XP、Resin、Tomcat6.0、Myeclipse、JDK1.5

发展：
我的验证思路是这样的：

1、定义一个Servlet，然后在该Servlet中调用Path类的getPath方法，getPath方法返回工程classpath的绝对路径，显示在jsp中。

2、另外在Path类中，通过Class的getResourceAsStream读取当前工程classpath路径中的a.txt文件，写入到getResource路径下的b.txt。

由于时间匆忙，代码没有好好去组织。大致能看出上述两个功能，很简单不做解释。

Path.java
```
public class Path {
	
	public String getPath() throws IOException{
		
		InputStream is = this.getClass().getResourceAsStream("/a.txt");
		
		File file = new File(Path.class.getResource("/").getPath()+"/b.txt");
		
		OutputStream os = new FileOutputStream(file);
		int bytesRead = 0;
		byte\[\] buffer = new byte\[8192\];
		while ((bytesRead = is.read(buffer, 0, 8192)) != -1) {
		os.write(buffer, 0, bytesRead);
		}
		os.close();
		is.close();
		
		return this.getClass().getResource("/").getPath();
	}
}
```
PathServlet.java
```
public class PathServlet extends HttpServlet {
	private static final long serialVersionUID = 4443655831011903288L;
	
	public void doGet(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
		Path path = new Path();
		
		request.setAttribute("path", path.getPath());
		PrintWriter out = response.getWriter();
		
		out.println("Class.getResource('/').getPath():" + path.getPath());
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
		doGet(request, response);
	}
}
```
在此之前使用main函数测试Path.class.getResource("/").getPath()打印出预想的路径为：/D:/work/project/EhCacheTestAnnotation/WebRoot/WEB-INF/classes/

于是将WEB应用部署到Resin下，运行定义好的Servlet，出乎意料的结果是：/D:/work/resin-3.0.23/webapps/WEB-INF/classes/ 。特别奇怪，怎么会丢掉项目名称：EhCacheTestAnnotation呢？

还有一点值得注意，getPath方法中使用getResourceAsStream("/a.txt")却正常的读到了位于下图的a.txt。

![](http://static.oschina.net/uploads/space/2011/1214/105317_Mgn7_129471.png)  
  
然后写到了如下图的b.txt中。代码中是这样实现的：File file = new File(Path.class.getResource("/").getPath()+"/b.txt");本意是想在a.txt文件目录下再写入b.txt。结果却和料想的不一样。

![](http://static.oschina.net/uploads/space/2011/1214/105409_baBe_129471.png)

请注意，区别还是丢掉了项目名称。

写的比较乱，稍微总结下：

程序中使用ClassLoader的两个方法：getResourceAsStream和getResource。但是事实证明在WEB应用的场景下却得到了不同的结果。大家别误会啊，看名字他们两个方法肯定不一样，这个我知道，但是getResourceAsStream总会获取指定路径下的文件吧，示例中的参数为"/a.txt"，正确读取“/D:/work/resin-3.0.23/webapps/EhCacheTestAnnotation/WEB-INF/classes/ ”下的a.txt，可是将文件写到getResource方法的getPath返回路径的b.txt文件。两个位置的差别在项目名称(EhCacheTestAnnotation)。

这样我暂且得出一个结论：通过getResourceAsStream和getResource两个方法获取的路径是不同的。但是为什么呢？

于是查看了ClassLoader的源码，贴出getResource和getResourceAsStream的源码。

```
    public URL getResource(String name) {
        URL url;
        if (parent != null) {
            url = parent.getResource(name);
        } else {
            url = getBootstrapResource(name);
        }
        if (url == null) {
            url = findResource(name);
        }
        return url;
    }


    public InputStream getResourceAsStream(String name) {
        URL url = getResource(name);
        try {
            return url != null ? url.openStream() : null;
        } catch (IOException e) {
            return null;
        }
    }
```
从代码中看，getResourceAsStream将获取URL委托给了getResource方法。天啊，这是怎么回事儿？由此我彻底迷茫了，百思不得其解。

但是没有因此就放弃，继续回想了一遍整个过程：
1、在main函数中，测试getResource与getResourceAsStream是完全相同的，正确的。
2、将其部署到Resin下，导致了getResource与getResourceAsStream获取的路径不一致。

一个闪光点，是不是与web容器有关啊，于是换成Tomcat6.0。OMG，“奇迹”出现了，真的是这样子啊，换成Tomcat就一样了啊！和预想的一致。

在Tomcat下运行结果如下图：

![](http://static.oschina.net/uploads/space/2011/1214/105637_KOkv_129471.png)  

对，这就是我想要的。

因此我对Resin产生了厌恶感，之前也因为在Resin下程序报错，在Tomcat下正常运行而纠结了好久。记得看《松本行弘的程序世界》中对C++中的多继承是这样评价的(大概意思)：多重继承带来的负面影响多数是由于使用不当造成的。是不是因为对Resin使用不得当才使得和Tomcat下得到不同的结果。

最终，在查阅Resin配置文件resin.conf时候在<host-default>标签下发现了这样一段：

```
<class-loader>
        <compiling-loader path="webapps/WEB-INF/classes"/>
        <library-loader path="webapps/WEB-INF/lib"/>
 </class-loader>
```

其中的compiling-loader很可能与之有关，遂将其注释掉，一切正常。担心是错觉，于是将compiling-loader的path属性改成：webapps/WEB-INF/classes1，然后运行pathServlet，b.txt位置如下图：

![](http://static.oschina.net/uploads/space/2011/1214/105818_kHCh_129471.png)  

确实与compiling-loader有关。

结局：

终于通过将<class-loader>标签注释掉，同样可以在Resin中获取“预想”的路径。验证了的确是使用Resin的人出了问题。

疑问：

但是没有这样就结束，我继续对getResource的源码进行了跟进，由于能力有限，没有弄清楚getResource的原理。
最终留下了两个疑问：
1、如果追踪到getResource方法的最底层(也许是JVM层面)，它实现的原理是什么？
2、为何Resin中<class-loader>的配置会对getResource产生影响，但是对getResourceAsStream毫无影响(getResourceAsStream可是将获取路径委托给getResource的啊)。还是这里我理解或者使用错误了？

在这里也请明白人指明。