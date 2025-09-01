---
title: Python中使用httplib2 – HTTP GET和POST示例
id: 1369
date: 2024-10-31 22:01:52
author: daichangya
excerpt: "学习使用Pythonhttplib2模块。的超文本传输协议（HTTP）是用于分布式，协作，超媒体信息系统的应用协议。HTTP是万维网数据通信的基础。Pythonhttplib2模块提供了用于通过HTTP访问Web资源的方法。它支持许多功能，例如HTTP和HTTPS，身份验证，缓存，重定向和压缩。$s"
permalink: /archives/python%E4%B8%AD%E4%BD%BF%E7%94%A8httplib2httpget%E5%92%8Cpost%E7%A4%BA%E4%BE%8B/
categories:
 - python基础教程
---

1. [Python基础教程](https://blog.jsdiff.com/archives/python基础教程)
2. [在SublimeEditor中配置Python环境](https://blog.jsdiff.com/archives/在sublimeeditor中配置python环境)
3. [Python代码中添加注释](https://blog.jsdiff.com/archives/python代码中添加注释)
4. [Python中的变量的使用](https://blog.jsdiff.com/archives/python中的变量的使用)
5. [Python中的数据类型](https://blog.jsdiff.com/archives/python中的数据类型)
6. [Python中的关键字](https://blog.jsdiff.com/archives/python中的关键字)
7. [Python字符串操作](https://blog.jsdiff.com/archives/python字符串操作)
8. [Python中的list操作](https://blog.jsdiff.com/archives/python中的list操作)
9. [Python中的Tuple操作](https://blog.jsdiff.com/archives/python中的tuple操作)
10. [Pythonmax（）和min（）–在列表或数组中查找最大值和最小值](https://blog.jsdiff.com/archives/pythonmax和min在列表或数组中查找最大值和最小值)
11. [Python找到最大的N个（前N个）或最小的N个项目](https://blog.jsdiff.com/archives/python找到最大的n个前n个或最小的n个项目)
12. [Python读写CSV文件](https://blog.jsdiff.com/archives/python读写csv文件)
13. [Python中使用httplib2–HTTPGET和POST示例](https://blog.jsdiff.com/archives/python中使用httplib2httpget和post示例)
14. [Python将tuple开箱为变量或参数](https://blog.jsdiff.com/archives/python将tuple开箱为变量或参数)
15. [Python开箱Tuple–太多值无法解压](https://blog.jsdiff.com/archives/python开箱tuple太多值无法解压)
16. [Pythonmultidict示例–将单个键映射到字典中的多个值](https://blog.jsdiff.com/archives/pythonmultidict示例将单个键映射到字典中的多个值)
17. [PythonOrderedDict–有序字典](https://blog.jsdiff.com/archives/pythonordereddict有序字典)
18. [Python字典交集–比较两个字典](https://blog.jsdiff.com/archives/python字典交集比较两个字典)
19. [Python优先级队列示例](https://blog.jsdiff.com/archives/python优先级队列示例)


学习使用Python [httplib2](https://github.com/httplib2/httplib2)模块。的超文本传输协议（HTTP）是用于分布式，协作，超媒体信息系统的应用协议。HTTP是万维网数据通信的基础。

Python httplib2模块提供了用于通过HTTP访问Web资源的方法。它支持许多功能，例如HTTP和HTTPS，身份验证，缓存，重定向和压缩。

```
$ service nginx status

* nginx is running
```
我们在本地主机上运行nginx Web服务器。我们的一些示例将连接到本地运行的nginx服务器上的PHP脚本。

目录
[检查httplib2库版本](#version)
[使用httplib2读取网页](#read-webpage)
[发送HTTP HEAD请求](#http-head)
[发送HTTP GET请求](#http-get)
[发送HTTP POST请求](#http-post)
[发送用户代理信息](#user-agent)
[将用户名/密码添加到请求](#authentication)

检查httplib2库版本
-------------

第一个程序打印库的版本，其版权和文档字符串。
```
#!/usr/bin/python3

import httplib2

print(httplib2.__version__)

print(httplib2.__copyright__)

print(httplib2.__doc__)
```
在httplib2.__version__给出的版本httplib2库中，httplib2.__copyright__给出了其版权，以及httplib2.__doc__它的文档字符串。

```
$ ./version.py

0.8

Copyright 2006, Joe Gregorio

httplib2

A caching http interface that supports ETags and gzip

to conserve bandwidth.

Requires Python 3.0 or later

Changelog:

2009-05-28, Pilgrim: ported to Python 3

2007-08-18, Rick: Modified so it's able to use a socks proxy if needed.
```
这是示例的示例输出。

使用httplib2读取网页
--------------

在下面的示例中，我们展示了如何从名为[www.something.com](http://www.something.com)的网站获取HTML内容。
```
#!/usr/bin/python3

import httplib2

http = httplib2.Http()

content = http.request("[http://www.something.com](http://www.something.com)")[1]

print(content.decode())
```
使用创建一个HTTP客户端httplib2.HTTP()。使用该request()方法创建一个新的HTTP请求。默认情况下，它是一个GET请求。返回值是响应和内容的元组。
```
$ ./get_content.py

<html><head><title>Something.</title></head>

<body>Something.</body>

</html>
```
这是示例的输出。

#### 剥离HTML标签

以下程序获取一个小型网页，并剥离其HTML标签。
```
#!/usr/bin/python3

import httplib2

import re

http = httplib2.Http()

content = http.request("[http://www.something.com](http://www.something.com)")[1]

stripped = re.sub('<[^<]+?>', '', content.decode())

print(stripped)
```
一个简单的正则表达式用于剥离HTML标记。请注意，我们正在剥离数据，我们没有对其进行清理。（这是两件事。）
```
$ ./strip_tags.py

Something.

Something.
```
该脚本将打印网页的标题和内容。

#### 检查响应状态

响应对象包含status提供响应状态代码的属性。
```
#!/usr/bin/python3

import httplib2

http = httplib2.Http()

resp = http.request("[http://www.something.com](http://www.something.com)")[0]

print(resp.status)

resp = http.request("[http://www.something.com/news/](http://www.something.com/news/)")[0]

print(resp.status)
```
我们使用request()方法执行两个HTTP请求，并检查返回的状态。
```
$ ./get_status.py

200

404
```
200是成功HTTP请求的标准响应，而404则表明找不到所请求的资源。

发送HTTP HEAD请求
-------------

HTTP HEAD方法检索文档标题。标头由字段组成，包括日期，服务器，内容类型或上次修改时间。
```
#!/usr/bin/python3

import httplib2

http = httplib2.Http()

resp = http.request("[http://www.something.com](http://www.something.com)", "HEAD")[0]

print("Server: " + resp['server'])

print("Last modified: " + resp['last-modified'])

print("Content type: " + resp['content-type'])

print("Content length: " + resp['content-length'])
```
该示例打印服务器，上次修改时间，内容类型和www.something.com网页的内容长度。
```
$ ./do_head.py

Server: Apache/2.4.12 (FreeBSD) OpenSSL/1.0.1l-freebsd mod_fastcgi/mod_fastcgi-SNAP-0910052141

Last modified: Mon, 25 Oct 1999 15:36:02 GMT

Content type: text/html

Content length: 72
```
这是程序的输出。从输出中，我们可以看到该网页是由FreeBSD托管的Apache Web服务器交付的。该文档的最后修改时间为1999年。网页是HTML文档，其长度为72个字节。

发送HTTP GET请求
------------

HTTP GET方法请求指定资源的表示形式。对于此示例，我们还将使用greet.php脚本：
```
<?php

echo "Hello " . htmlspecialchars($_GET['name']);

?>
```
在/usr/share/nginx/html/目录内，我们有此greet.php文件。该脚本返回name变量的值，该值是从客户端检索的。

该htmlspecialchars()函数将特殊字符转换为HTML实体；例如＆到＆amp.。
```
#!/usr/bin/python3

import httplib2

http = httplib2.Http()

content = http.request("[http://localhost/greet.php?name=Peter](http://localhost/greet.php?name=Peter)",

method="GET")[1]

print(content.decode())
```
该脚本将带有值的变量发送到服务器上的PHP脚本。该变量直接在URL中指定。
```
$ ./mget.py

Hello Peter

这是示例的输出。

$ tail -1 /var/log/nginx/access.log

127.0.0.1 - - [21/Aug/2016:17:32:31 +0200] "GET /greet.php?name=Peter HTTP/1.1" 200 42 "-"

"Python-httplib2/0.8 (gzip)"
```
我们检查了nginx访问日志。

发送HTTP POST请求
-------------

POST请求方法请求Web服务器接受并存储请求消息正文中包含的数据。上载文件或提交完整的Web表单时经常使用它。
```
<?php

echo "Hello " . htmlspecialchars($_POST['name']);

?>
```
在本地Web服务器上，我们有此target.php文件。它只是将过帐的值打印回客户。
```
#!/usr/bin/python3

import httplib2

import urllib

http = httplib2.Http()

body = {'name': 'Peter'}

content = http.request("[http://localhost/target.php](http://localhost/target.php)",

method="POST",

headers={'Content-type': 'application/x-www-form-urlencoded'},

body=urllib.parse.urlencode(body) )[1]

print(content.decode())
```
脚本发送name带有Peter值的键的请求。数据使用urllib.parse.urlencode()方法进行编码，并在请求的正文中发送。
```
$ ./mpost.py

Hello Peter
```
这是mpost.py脚本的输出。
```
$ tail -1 /var/log/nginx/access.log

127.0.0.1 - - [23/Aug/2016:12:21:07 +0200] "POST /target.php HTTP/1.1"

200 37 "-" "Python-httplib2/0.8 (gzip)"
```
使用POST方法时，不会在请求URL中发送该值。

发送用户代理信息
--------

在本节中，我们指定用户代理的名称。
```
<?php

echo $_SERVER['HTTP_USER_AGENT'];

?>
```
在nginx文档根目录下，我们有agent.php文件。它返回用户代理的名称。
```
#!/usr/bin/python3

import httplib2

http = httplib2.Http()

content = http.request("[http://localhost/agent.php](http://localhost/agent.php)", method="GET",

headers={'user-agent': 'Python script'})[1]

print(content.decode())
```
该脚本向脚本创建一个简单的GET请求agent.php。在headers字典中，我们指定用户代理。PHP脚本将读取此内容，并将其返回给客户端。
```
$ ./user_agent.py

Python script
```
服务器使用我们随请求发送的代理名称进行了响应。

向请求添加用户名/密码
-----------

客户端的add_credentials()方法设置用于领域的名称和密码。安全领域是一种用于保护Web应用程序资源的机制。
```
$ sudo apt-get install apache2-utils

$ sudo htpasswd -c /etc/nginx/.htpasswd user7

New password:

Re-type new password:

Adding password for user user7
```
我们使用该htpasswd工具创建用于基本HTTP身份验证的用户名和密码。
```
location /secure {

auth_basic "Restricted Area";

auth_basic_user_file /etc/nginx/.htpasswd;

}
```
在nginx /etc/nginx/sites-available/default配置文件中，我们创建一个安全页面。领域的名称为“禁区”。
```
<!DOCTYPE html>

<html lang="en">

<head>

<title>Secure page</title>

</head>

<body>

<p>

This is a secure page.

</p>

</body>

</html>
```
在/usr/share/nginx/html/secure目录中，我们有上面的HTML文件。
```
#!/usr/bin/python3

import httplib2

user = 'user7'

passwd = '7user'

http = httplib2.Http()

http.add_credentials(user, passwd)

content = http.request("[http://localhost/secure/](http://localhost/secure/)")[1]

print(content.decode())
```
该脚本连接到安全网页；它提供访问该页面所需的用户名和密码。
```
$ ./credentials.py

<!DOCTYPE html>

<html lang="en">

<head>

<title>Secure page</title>

</head>

<body>

<p>

This is a secure page.

</p>

</body>

</html>
```
使用正确的凭据，脚本将返回受保护的页面。

在本教程中，我们探索了Python httplib2模块。