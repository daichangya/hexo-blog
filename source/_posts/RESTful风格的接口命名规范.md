---
title: RESTful风格的接口命名规范
id: 1585
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/restful%E9%A3%8E%E6%A0%BC%E7%9A%84%E6%8E%A5%E5%8F%A3%E5%91%BD%E5%90%8D%E8%A7%84%E8%8C%83/
categories:
 - 软件设计
---

最近实习单位的leader要求我调研一下RESTful风格的接口命名规范，然后把项目里的URL名整体规范化修改一下，以下是我调研之后的对于RESTful的了解。

REST是一个术语的缩写，REpresentational State Transfer，中文直译是“表征状态转移”。  
REST是一套风格约定，RESTful是它的形容词形式。比如一套实现了REST风格的接口，可以称之为RESTful接口。

目前，我们的项目里，基本只有GET和POST两种http方法，如下图，无疑浪费了 HTTP 协议的潜力，而 REST 则充分利用了 HTTP 规范中的方法，达到接口描述的语义化。  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190612141032514.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDc1OTA5,size_16,color_FFFFFF,t_70)  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190612141108663.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1MDc1OTA5,size_16,color_FFFFFF,t_70)

REST 描述了 HTTP 层里客户端和服务器端的数据交互规则；客户端通过向服务器端发送 HTTP（s）请求，接收服务器的响应，完成一次 HTTP 交互。这个交互过程中，REST 架构约定两个重要方面就是HTTP请求的所采用方法，以及请求的链接。

> 因此，REST 规范可以简单粗暴抽象成以下两个规则：
> 
> *   请求 API 的 URL 表示用来定位资源；
> *   请求的 METHOD 表示对这个资源进行的操作；

以下将以这两个规则为基础，描述如何构造一个符合 REST 规范的请求。

## 一、API的url

URL 用来定位资源，跟要进行的操作区分开，这就意味着URL不该有任何动词。

#### 1.1 下面示例中的 get、create、search 等动词，都不应该出现在 REST 架构的后端接口路径中。比如：

`/api/getUser`  
`/api/createApp`  
`/api/searchResult`  
`/api/deleteAllUsers`

#### 1.2 当我们需要对单个用户进行操作时，根据操作的方式不同可能需要下面的这些接口：

`/api/getUser （用来获取某个用户的信息，还需要以参数方式传入用户 id 信息）`  
`/api/updateUser （用来更新用户信息）`  
`/api/deleteUser （用来删除单个用户）`  
`/api/resetUser （重置用户的信息）`

#### 1.3 可能在更新用户不同信息时，提供不同的接口，比如：

`/api/updateUserName`  
`/api/updateUserEmail`  
`/api/updateUser`

#### 1.4 总结：

以上三种情况的弊端在于：首先加上了动词，肯定是使 URL 更长了；其次对一个资源实体进行不同的操作就是一个不同的 URL，造成 URL 过多难以管理。

其实当你回过头看“URL”这个术语的定义时，更能理解这一点。URL 的意思是统一资源定位符，这个术语已经清晰的表明，一个 URL 应该用来定位资源，而不应该掺入对操作行为的描述。

**在 REST 架构的链接应该是这个样子**：

1.  URL 中不应该出现任何表示操作的动词，链接只用于对应资源；
    
2.  URL 中应该单复数区分，推荐的实践是永远只用复数；比如`GET /api/users`表示获取用户的列表；如果获取单个资源，传入 ID，比如`/api/users/123`表示获取单个用户的信息；
    
3.  按照资源的逻辑层级，对 URL 进行嵌套，比如一个用户属于某个团队，而这个团队也是众多团队之一；那么获取这个用户的接口可能是这样：`GET /api/teams/123/members/234` 表示获取 id 为 123 的小组下，id 为234 的成员信息。  
    按照类似的规则，可以写出如下的接口  
    `/api/teams （对应团队列表）`  
    `/api/teams/123 （对应 ID 为 123 的团队）`  
    `/api/teams/123/members （对应 ID 为 123 的团队下的成员列表）`  
    `/api/teams/123/members/456 （对应 ID 为 123 的团队下 ID 未 456 的成员）`
    

## 二、API 请求的方法

实际上，我们不只有GET 和 POST 可用，在 REST 架构中，有以下几个重要的请求方法：GET，POST，PUT，PATCH，DELETE。

接下来主要介绍PUT，PATCH和DELETE。

#### 2.1 UPDATE（PUT和PATCH）

【Update】资源的更新，用于更新的 HTTP 方法有两个，PUT 和 PATCH。他们都应当被实现为幂等方法，即多次同样的更新请求应当对服务器产生同样的副作用。

*   PUT 用于更新资源的全部信息，在请求的 body 中需要传入修改后的全部资源主体；
*   PATCH 用于局部更新，在 body 中只需要传入需要改动的资源字段。

PATCH 的作用在于如果一个资源有很多字段，在进行局部更新时，只需要传入需要修改的字段即可。否则在用 PUT 的情况下，你不得不将整个资源模型全都发送回服务器，造成网络资源的极大浪费。

#### 2.2 DELETE

【Delete】资源的删除，相应的请求 HTTP 方法就是 DELETE。这个也应当被实现为一个幂等的方法。如：`DELETE /api/users/123`

用于删除服务器上 ID 为 123 的资源，多次请求产生副作用都是，是服务器上 ID 为 123 的资源不存在。

## 三、过滤

REST 风格的接口地址，表示的可能是单个资源，也可能是资源的集合；当我们需要访问资源集合时，设计良好的接口应当接受参数，允许只返回满足某些特定条件的资源列表。

支持提供关键词进行搜索，以及排序

`GET /api/users?keyword=libinm&sort=classId`

支持根据字段进行过滤

`GET /api/users?gender=1`

当我们都熟悉且遵循这样的规范后，基本可以看到一个 REST 风格的接口就知道如何使用这个接口进行 CRUD 操作了。比如下面这面这个接口就表示搜索 ID 为 123 的图书馆的书，并且书的信息里包含关键字「game」，返回前十条满足条件的结果。

`GET /api/libraries/123/books?keyword=game&sort=price&limit=10&offset=0`

## 四、正确示例

标准的格式是

> http(s): [//server.com](https://server.com/) /app-name /{version} /{domain} /{rest-convention}

{version}代表api的版本信息。  
{domain}是一个你可以用来定义任何技术的区域(例如：安全-允许指定的用户可以访问这个区域)或者业务上的原因(例如：同样的功能在同一个前缀之下。)  
{rest-convention} 代表这个域(domain)下，约定的rest接口集合。

*   单资源( singular-resourceX )  
    url样例：order/ (order即指那个单独的资源X)  
    GET – 返回一个新的order  
    POST- 创建一个新的order，从post请求携带的内容获取值。
    
*   单资源带id(singular-resourceX/{id} )  
    URL样例：order/1 ( order即指那个单独的资源X )  
    GET – 返回id是1的order  
    DELETE – 删除id是1的order  
    PUT – 更新id是1的order，order的值从请求的内容体中获取。
    
*   复数资源(plural-resourceX/)  
    URL样例:orders/  
    GET – 返回所有orders
    
*   复数资源查找(plural-resourceX/search)  
    URL样例：orders/search?name=123  
    GET – 返回所有满足查询条件的order资源。(实例查询，无关联) – order名字等于123的。
    
*   复数资源查找(plural-resourceX/searchByXXX)  
    URL样例：orders/searchByItems?name=ipad  
    GET – 将返回所有满足自定义查询的orders – 获取所有与items名字是ipad相关联的orders。
    
*   单数资源(singular-resourceX/{id}/pluralY)  
    URL样例：order/1/items/ (这里order即为资源X，items是复数资源Y)  
    GET – 将返回所有与order id 是1关联的items。
    
*   singular-resourceX/{id}/singular-resourceY/  
    URL样例：order/1/item/  
    GET – 返回一个瞬时的新的与order id是1关联的item实例。  
    POST – 创建一个与order id 是1关联的item实例。Item的值从post请求体中获取。
    
*   singular-resourceX/{id}/singular-resourceY/{id}/singular-resourceZ/  
    URL样例：order/1/item/2/package/  
    GET – 返回一个瞬时的新的与item2和order1关联的package实例。  
    POST – 创建一个新的与item 2和order1关联的package实例，package的值从post请求体中获得。
    

上面的规则可以在继续递归下去，并且复数资源后面永远不会再跟随负数资源。  
总结几个关键点，来更清晰的表述规则。

> 在使用复数资源的时候，返回的是最后一个复数资源使用的实例。  
> 在使用单个资源的时候，返回的是最后一个但是资源使用的实例。  
> 查询的时候，返回的是最后一个复数实体使用的实例(们)。

# 四、其他规范

一些其他规范：  
规则1：URI结尾不应包含（/）  
规则2：正斜杠分隔符（/）必须用来指示层级关系  
规则3：应使用连字符（ - ）来提高URI的可读性  
规则4：不得在URI中使用下划线（_）  
规则5：URI路径中全都使用小写字母