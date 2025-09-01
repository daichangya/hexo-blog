---
title: Redis 中如何使用 lua脚本
id: 1421
date: 2024-10-31 22:01:55
author: daichangya
excerpt: "Lua：Redis用户指南你应该听说过Redis具有嵌入式脚本语言，但是还没有尝试过吗？下面您在Redis服务器上使用Lua的功能时需要了解的内容。你好，Lu！我们的第一个Redis Lua脚本仅返回一个值，而没有实际与Redis进行任何有意义的交互"
permalink: /archives/redis-lua/
categories:
 - redis
---

1. [如何在ubuntu18.04上安装和保护redis](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8ubuntu1804%E4%B8%8A%E5%AE%89%E8%A3%85%E5%92%8C%E4%BF%9D%E6%8A%A4redis)
2. [如何连接到Redis数据库](https://blog.jsdiff.com/archives/howtoconnecttoaredisdatabase)
3. [如何管理Redis数据库和Keys](https://blog.jsdiff.com/archives/howtomanageredisdatabasesandkeys)
4. [如何在Redis中管理副本和客户端](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86%E5%89%AF%E6%9C%AC%E5%92%8C%E5%AE%A2%E6%88%B7%E7%AB%AF)
5. [如何在Redis中管理字符串](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86%E5%AD%97%E7%AC%A6%E4%B8%B2)
6. [如何在Redis中管理list](https://blog.jsdiff.com/archives/listsinredis)
7. [如何在Redis中管理Hashes](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86hashes)
8. [如何在Redis中管理Sets](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E7%AE%A1%E7%90%86sets)
9. [如何在Redis中管理Sorted Sets](https://blog.jsdiff.com/archives/howtomanagesortedsetsinredis)
10. [如何在Redis中运行事务](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E5%9C%A8redis%E4%B8%AD%E8%BF%90%E8%A1%8C%E4%BA%8B%E5%8A%A1)
11. [如何使Redis中的Key失效](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BD%BFredis%E4%B8%AD%E7%9A%84keys%E5%A4%B1%E6%95%88)
12. [如何解决Redis中的故障](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E8%A7%A3%E5%86%B3redis%E4%B8%AD%E7%9A%84%E9%97%AE%E9%A2%98)
13. [如何从命令行更改Redis的配置](https://blog.jsdiff.com/archives/%E5%A6%82%E4%BD%95%E4%BB%8E%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%9B%B4%E6%94%B9redis%E7%9A%84%E9%85%8D%E7%BD%AE)
14. [Redis数据类型简介](https://blog.jsdiff.com/archives/redis%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B%E7%AE%80%E4%BB%8B)
15. [Redis 中如何使用 lua脚本](https://blog.jsdiff.com/archives/redis-lua)
16. [Redis 常用命令指南](https://blog.jsdiff.com/archives/redis-command)


Lua：Redis用户指南
=============

你应该听说过Redis具有嵌入式脚本语言，但是还没有尝试过吗？下面您在Redis服务器上使用Lua的功能时需要了解的内容。

你好，Lu！
------

我们的第一个Redis Lua脚本仅返回一个值，而没有实际与Redis进行任何有意义的交互：

    local msg = "Hello, world!"
    return msg

这很简单。第一行使用我们的消息设置了一个局部变量，第二行从Redis服务器将该值返回给客户端。将此文件另存为`hello.lua`并按以下方式运行：

    redis-cli --eval hello.lua

### 连接问题？

本`redis-cli`示例假定您在本地运行Redis服务器。

运行此命令将打印“ Hello，world！”。的第一个参数 `EVAL`是完整的lua脚本-在这里，我们使用`cat` 命令从文件中读取脚本。第二个参数是脚本将访问的RedisKey的数量。我们简单的“ Hello World”脚本不访问任何键，因此我们使用`0`。

访问键和参数
------

假设我们正在构建一个URL缩短器。每次出现URL时，我们都希望存储它并返回一个唯一的数字，该数字可用于以后访问URL。

我们将使用Lua脚本从Redis使用获取脚本的唯一ID，`INCR`然后立即将URL存储在以唯一ID为键的哈希中：

    local link_id = redis.call("INCR", KEYS[1])
    redis.call("HSET", KEYS[2], link_id, ARGV[1])
    return link_id

我们是使用`call()`函数首次在此访问Redis 。 `call()`的参数是发送给Redis的命令：首先是我们`INCR <key>`，然后是we `HSET <key> <field> <value>`。这两个命令将按顺序运行-该脚本执行时Redis不会执行任何其他操作，并且运行速度非常快。

我们正在访问两个Lua表，`KEYS`和`ARGV`。表是关联数组，是Lua构造数据的唯一机制。出于我们的目的，您可以将它们视为您最熟悉的任何语言中的数组的等效项，但请注意，这两种Lua主义使刚接触该语言的人们绊倒了：

*   表是基于一个表的，也就是说，索引从1开始。因此，第一个元素`mytable`是`mytable[1]`，第二个元素是，依此类推 `mytable[2]`。
    
*   表不能包含nil值。如果某个操作产生的表为`[ 1, nil, 3, 4 ]`，则结果将为`[ 1 ]`—该表在第一个nil值处被 _截断_。
    

调用此脚本时，还需要传递`KEYS` 和`ARGV`表的值。在原始Redis协议中，命令如下所示：

    EVAL $incrset.lua 2 links:counter links:url https://blog.jsdiff.com/
    

调用时`EVAL`，在脚本之后，我们提供将要访问的脚本`2`的数目 `KEYS`，然后列出我们的`KEYS`，最后为提供值`ARGV`。

通常，当我们使用Redis Lua脚本构建应用程序时，Redis客户端库将负责指定键数。上面的代码块是出于完整性考虑而显示的，但这是在命令行上执行此操作的更简单方法：

    redis-cli --eval incrset.lua links:counter links:urls , https://blog.jsdiff.com/

当使用`--eval`如上述，逗号中隔离`KEYS[]`从`ARGV[]`项目。

为了清楚起见，这是我们的原始脚本，这次是 `KEYS`并`ARGV`扩展了：

    local link_id = redis.call("INCR", "links:counter")
    redis.call("HSET", "links:urls", link_id, "https://blog.jsdiff.com.com")
    return link_id

为Redis编写Lua脚本时，应仅通过`KEYS`表访问所访问的每个键。该`ARGV`表用于传递参数-这是我们要存储的URL的值。

条件逻辑：递增和递归
----------

上面的示例为我们的URL缩短器保存了链接，但是我们还需要跟踪URL的访问次数。为此，我们将在Redis中的哈希中保留一个计数器。当用户附带一个链接标识符时，我们将检查它是否存在，如果存在则增加我们的计数器：

    if redis.call("HEXISTS", KEYS[1], ARGV[1]) == 1 then
      return redis.call("HINCRBY", KEYS[1], ARGV[1], 1)
    else
      return nil
    end

每次有人单击短链接时，我们都会运行此脚本来跟踪该链接是否再次共享。我们使用调用脚本`EVAL`并传入`links:visits`我们的单个Key，并将从上一个脚本返回的链接标识符作为单个参数传递 。

没有散​​列的脚本看起来几乎一样。这是一个仅在标准RedisKey存在的情况下递增其脚本的脚本：

    if redis.call("EXISTS",KEYS[1]) == 1 then
      return redis.call("INCR",KEYS[1])
    else
      return nil
    end

SCRIPT LOAD and EVALSHA
-------

请记住，当Redis运行Lua脚本时，它将不会运行其他任何东西。最好的脚本只是使用最小的逻辑位简单地扩展了小原子数据操作的现有Redis词汇表。Lua脚本中的错误可以完全锁定Redis服务器-最好使内容简短并易于调试。

即使它们通常很短，我们也不必每次都想运行完整的Lua脚本。在实际的应用程序中，您将在应用程序启动时（或在部署时）向Redis注册每个Lua脚本，然后稍后通过其唯一的SHA-1标识符调用这些脚本。

    redis-cli SCRIPT LOAD "return 'hello world'"
    # "5332031c6b470dc5a0dd9b4bf2030dea6d65de91"
    
    redis-cli EVALSHA 5332031c6b470dc5a0dd9b4bf2030dea6d65de91 0
    # "hello world"

`SCRIPT LOAD`在实时应用程序中，通常不需要显式调用，因为`EVAL`隐式加载了传递给它的脚本。只有未找到脚本时，应用程序才能尝试`EVALSHA`乐观地返回到`EVAL`。


什么时候使用Lua？
----------

为lua Redis的支持用几分重叠`WATCH`/ `MULTI`/ `EXEC` 块，其组操作，以便它们被一起执行。那么，您如何选择一个使用另一个？`MULTI`块中的每个操作都必须是独立的，但是对于Lua而言，后续操作可以取决于早期操作的结果。使用Lua脚本还可以避免`WATCH`使用时可能使饥饿的客户端饿死的竞争状况。

Lua有很多库
-----

Redis Lua解释器加载七个库：base， [table](http://www.lua.org/pil/19.1.html)， [string](http://www.lua.org/pil/20.html)， [math](http://www.lua.org/pil/18.html)， [debug](http://www.lua.org/pil/23.html)， [cjson](http://www.kyne.com.au/~mark/software/lua-cjson-manual.html)和[cmsgpack](https://github.com/antirez/lua-cmsgpack)。前几个是标准库，可让您执行任何语言所期望的基本操作。最后两个让Redis理解JSON和MessagePack －这是一个非常有用的功能，我一直想知道为什么我不经常使用它。

具有公共API的Web应用程序倾向于到处都是JSON。因此，也许您在正常的RedisKey中存储了一堆JSON Blob，并且您想访问其中的一些特定值，就像您将它们存储为散列一样。借助Redis JSON支持，这很容易：

    if redis.call("EXISTS", KEYS[1]) == 1 then
      local payload = redis.call("GET", KEYS[1])
      return cjson.decode(payload)[ARGV[1]]
    else
      return nil
    end

在这里，我们检查Key是否存在，如果不存在则快速返回nil。然后，我们从Redis中获取JSON值，并使用进行解析`cjson.decode()`，然后返回请求的值。

    redis-cli set apple '{ "color": "red", "type": "fruit" }'
    # OK
    
    redis-cli --eval json-get.lua apple , type
    # "fruit"

将此脚本加载到Redis服务器中，可以将Redis中存储的JSON值视为哈希值。如果您的对象很小，那么即使我们必须解析每次访问的值，这实际上也相当快。

如果您正在为需要性能的系统开发内部API，那么您可能会选择[MessagePack而](http://msgpack.org/)不是JSON，因为它更小，更快。幸运的是，与Redis（在大多数地方一样），MessagePack几乎可以替代JSON：

    if redis.call("EXISTS", KEYS[1]) == 1 then
      local payload = redis.call("GET", KEYS[1])
      return cmsgpack.unpack(payload)[ARGV[1]]
    else
      return nil
    end

运算数字
----

Lua和Redis具有不同的类型系统，因此了解跨Redis-Lua边界时值如何变化很重要。当一个数字从Lua返回到Redis客户端时，它变成一个整数-小数点后的任何数字都将被删除：

    local indiana_pi = 3.2
    return indiana_pi

运行此脚本时，Redis将返回3的整数-您会丢失有趣的pi。看起来很简单，但是当您在脚本中间开始与Redis交互时，事情会变得有些棘手。一个例子：

    local indiana_pi = 3.2
    redis.call("SET", "pi", indiana_pi)
    return redis.call("GET", "pi")

这里的结果值是一个字符串：`"3.2"`为什么？Redis没有专用的数字类型。当我们首次使用`SET`该值时，Redis将其保存为字符串，从而丢失了Lua最初认为该值是浮点数这一事实的所有记录。当我们稍后提取值时，它仍然是一个字符串。

使用`GET`/ 进行访问的Redis中的值`SET`应视为字符串，除非像`INCR`和`DECR`对它们进行数字操作时除外。这些特殊的数字运算实际上将返回整数答复（并根据数学规则处理存储的值），但是Redis中存储的值的“类型”仍然是字符串值。

Redis 使用Lua常见错误
-----

这些是我们在Redis中使用Lua时最常见的错误：

*   与大多数流行语言不同，表在Lua中是基于一个的。KEYS表中的第一个元素是`KEYS[1]`，第二个元素是，依此类推`KEYS[2]`。
    
*   nil值终止Lua中的表。这样`[ 1, 2, nil, 3 ]`会自动成为`[1, 2]`。不要在表中使用nil值。
    
*   `redis.call`会引发异常样式的Lua错误，同时 `redis.pcall`会自动捕获所有错误并将其作为可检查的表返回。
    
*   Lua数字在发送给Redis时会转换为整数-小数点后的所有内容都会丢失。返回之前，将所有浮点数转换为字符串。
    
*   请确保在表中指定您在Lua脚本中使用的所有键`KEYS` ，否则您的脚本可能会在Redis的未来版本中损坏。
    
*   Lua脚本与Redis中的任何其他操作一样：执行它们时，其他任何程序都不会运行。将脚本视为扩展Redis服务器词汇的一种方法-使它们简短明了。
    

进一步阅读
-----

在线上有很多关于Lua和Redis的有用资源-以下是我使用的一些资源：

*   [评估文件](http://redis.io/commands/eval)
*   [Lua参考手册](http://www.lua.org/manual/5.1/manual.html)
*   [Lua教程目录](http://lua-users.org/wiki/TutorialDirectory)