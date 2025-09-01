---
title: Redis源码分析（sds）
id: 1494
date: 2024-10-31 22:01:58
author: daichangya
permalink: /archives/redis%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90sds/
categories:
 - redis
---

源码版本：`redis-4.0.1`  
源码位置：[https://github.com/antirez/sds](https://github.com/antirez/sds)

# 一、SDS简介

sds (Simple Dynamic String)，`Simple`的意思是简单，`Dynamic`即动态，意味着其具有动态增加空间的能力，扩容不需要使用者关心。`String`是字符串的意思。说白了就是用C语言自己封装了一个字符串类型，这个项目由Redis作者`antirez`创建，作为Redis中基本的数据结构之一，现在也被独立出来成为了一个单独的项目，项目地址位于[这里](https://github.com/antirez/sds)。

sds 有两个版本，在`Redis 3.2`之前使用的是第一个版本，其数据结构如下所示：

```code
typedef char *sds;      //注意，sds其实不是一个结构体类型，而是被typedef的char*，好处见下文

struct sdshdr {
    unsigned int len;   //buf中已经使用的长度
    unsigned int free;  //buf中未使用的长度
    char buf[];         //柔性数组buf
};
```

但是在`Redis 3.2 版本`中，对数据结构做出了修改，针对不同的长度范围定义了不同的结构，如下，这是目前的结构：

```code
typedef char *sds;      

struct __attribute__ ((__packed__)) sdshdr5 {     // 对应的字符串长度小于 1<<5
    unsigned char flags; /* 3 lsb of type, and 5 msb of string length */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr8 {     // 对应的字符串长度小于 1<<8
    uint8_t len; /* used */                       //目前字符创的长度
    uint8_t alloc;                                //已经分配的总长度
    unsigned char flags;                          //flag用3bit来标明类型，类型后续解释，其余5bit目前没有使用
    char buf[];                                   //柔性数组，以'\0'结尾
};
struct __attribute__ ((__packed__)) sdshdr16 {    // 对应的字符串长度小于 1<<16
    uint16_t len; /* used */
    uint16_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr32 {    // 对应的字符串长度小于 1<<32
    uint32_t len; /* used */
    uint32_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr64 {    // 对应的字符串长度小于 1<<64
    uint64_t len; /* used */
    uint64_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};

```

新版带来的好处就是针对长度不同的字符串做了优化，选取不同的数据类型`uint8_t`或者`uint16_t`或者`uint32_t`等来表示长度、一共申请字节的大小等。上面结构体中的`__attribute__ ((__packed__))` 设置是告诉编译器取消字节对齐，则结构体的大小就是按照结构体成员实际大小相加得到的。

# 二、SDS的优势和不足

sds和一般的自定义String相比，有自己的优势和不足，假设我们用C语言自己定义一个String结构体，一般会这么定义：

```code
struct mysds {
    char *buf;                          //存储实际字符
    size_t len;                         //字符串的长度
    ... possibly more fields here ...   //其他的成员
};
```

如果我们要打印buf的内容，如下这样使用：

```code
struct mysds *sds = mysdsnew("Hello World");    //假设mysdsnew函数中分配空间并初始化buf为"Hello World"
printf("%s", sds->buf);

Out> Hello World
```

即我们打印的`buf`是属于`struct mysds`的一个成员，我们需要通过指针操作它。但是`Redis sds`与之不同，它的定义是`typedef char *sds;`，如果使用它实现上面的功能，我们的代码是：

```code
sds sds = sdsnew("Hello World");
printf("%s", sds);

Out> Hello World
```

在这里我们直接输出的是`sds`,之所以可以这样，是因为它的结构如下所示:

```code
+--------+-------------------------------+-----------+
| Header | Binary safe C alike string... | Null term |
+--------+-------------------------------+-----------+
         |
         `-> Pointer returned to the user.
```

我们通过`sdsnew`返回的实际上是一个`char *`类型的指针，这个指针指向的是字符串的开始位置，它的头部信息是在字符串前面分配的，这样带来的好处有：

*   我们可以把sds传递给任何使用`char *`为参数的函数，包括一些库函数（strcmp,strcat等），而不用通过结构体获取地址再传递。
*   可以直接访问单个字符`printf("%c %c\n", sds[0], sds[1]);`如果使用`mysds`则需要每次获取下buf的地址`mysds->buf[1]`再访问。
*   分配的空间地址连续，对高速缓存命中率更加友好。即一次连续分配`Header+String+Null`，因此对于一个`sds`，它的各个部分总是内存连续的，但是上面的`mysds`通常需要两次`malloc`,如下所示：

```code
struct mysds *sds = (struct mysds *) malloc(sizeof(struct mysds));
sds->buf = (char *) malloc(SIZE);
//这两次malloc不能保证sds和buf内存地址是连续的
```

除了上面的优点，sds还有一些缺点：

*   API返回后不能确定内部是否重新分配了空间

```code
s = sdscat(s, "Some more data"); 
```

`s`既是参数，又作为了返回值，原因是我们在调用sdscat函数之前不确定s的剩余空间是否足够分配出  
data长度的字节，如果不够的话，内部会重新malloc空间，然后把目前的sds包括头部全部挪过去，这样的话如果我们没有把返回的地址重新赋值给s,那么s实际上是失效的。

*   如果sds会在程序的不同位置共享，则在修改字符串时候必须修改所有的应用。因为它本身是一个`char *`的地址，一旦在一个地方重新分配了，则其他地方的会失效。

# 三、创建、扩容和销毁

接下来我们以一个例子来跟踪源码展示`sds`的`创建`、`扩容`和`销毁`等过程，这是我们的源代码：

```code
int main(int argc, char *argv[]) {
    sds s = sdsnew("Hello World,");
    printf("Length:%d, Type:%d\n", sdslen(s), sdsReqType(sdslen(s)));

    s = sdscat(s, "The length of this sentence is greater than 32 bytes");
    printf("Length:%d, Type:%d\n", sdslen(s), sdsReqType(sdslen(s)));

    sdsfree(s);
    return 0;
}

Out>
Length:12, Type:0
Length:64, Type:1

```

首先我们创建了一个`sds`名为`s`，初始化为”Hello World”，然后打印它的`length`和`type`分别为`12`和`0`,接着我们继续给`s`追加了一个字符串，使得它的长度变成了`64`,获取`type`，发现变成了`1`，最后`free`掉`s`，有关`type`的定义，位于`sds.h`头文件，随着长度不同，`type`也会发生变化。

```code
#define SDS_TYPE_5  0     //长度小于 1<<5 即32，类型为SDS_TYPE_5
#define SDS_TYPE_8  1     // ...
#define SDS_TYPE_16 2
#define SDS_TYPE_32 3
#define SDS_TYPE_64 4
```

下面我们从sdsnew出发，去看下它的实现：

```code
/* Create a new sds string starting from a null terminated C string. */
sds sdsnew(const char *init) {
    size_t initlen = (init == NULL) ? 0 : strlen(init);
    return sdsnewlen(init, initlen);
}
```

可以看到`sdsnew`实际上调用了`sdsnewlen`，帮我们计算了传进去的字符串长度，然后传给`sdsnewlen`，继续看`sdsnewlen`

```
sds sdsnewlen(const void *init, size_t initlen) {
    void *sh;
    sds s;
    char type = sdsReqType(initlen);
    /* Empty strings are usually created in order to append. Use type 8
     * since type 5 is not good at this. */
    if (type == SDS_TYPE_5 && initlen == 0) type = SDS_TYPE_8;
    int hdrlen = sdsHdrSize(type);
    unsigned char *fp; /* flags pointer. */

    sh = s_malloc(hdrlen+initlen+1);
    if (!init)
        memset(sh, 0, hdrlen+initlen+1);
    if (sh == NULL) return NULL;
    s = (char*)sh+hdrlen;
    fp = ((unsigned char*)s)-1;
    switch(type) {
        case SDS_TYPE_5: {
            *fp = type | (initlen << SDS_TYPE_BITS);
            break;
        }
        case SDS_TYPE_8: {
            SDS_HDR_VAR(8,s);
            sh->len = initlen;
            sh->alloc = initlen;
            *fp = type;
            break;
        }
        case SDS_TYPE_16: {
            SDS_HDR_VAR(16,s);
            sh->len = initlen;
            sh->alloc = initlen;
            *fp = type;
            break;
        }
        case SDS_TYPE_32: {
            SDS_HDR_VAR(32,s);
            sh->len = initlen;
            sh->alloc = initlen;
            *fp = type;
            break;
        }
        case SDS_TYPE_64: {
            SDS_HDR_VAR(64,s);
            sh->len = initlen;
            sh->alloc = initlen;
            *fp = type;
            break;
        }
    }
    if (initlen && init)
        memcpy(s, init, initlen);
    s[initlen] = '\0';
    return s;
}
```

函数基本流程如下所示：

*   `char type = sdsReqType(initlen);`根据我们传入的初始化字符串长度获取类型，获取代码如下:

```
static inline char sdsReqType(size_t string_size) {
    if (string_size < 1<<5)
        return SDS_TYPE_5;
    if (string_size < 1<<8)
        return SDS_TYPE_8;
    if (string_size < 1<<16)
        return SDS_TYPE_16;
#if (LONG_MAX == LLONG_MAX)
    if (string_size < 1ll<<32)
        return SDS_TYPE_32;
#endif
    return SDS_TYPE_64;
}
```

函数根据字符串大小的不同返回不同的类型。

*   `int hdrlen = sdsHdrSize(type);`根据上一步获取的`type`通过`sdsHdrSize`函数获得`Header`的长度，`sdsHdrSize`代码如下：

```
static inline int sdsHdrSize(char type) {
    switch(type&SDS_TYPE_MASK) {
        case SDS_TYPE_5:
            return sizeof(struct sdshdr5);
        case SDS_TYPE_8:
            return sizeof(struct sdshdr8);
        case SDS_TYPE_16:
            return sizeof(struct sdshdr16);
        case SDS_TYPE_32:
            return sizeof(struct sdshdr32);
        case SDS_TYPE_64:
            return sizeof(struct sdshdr64);
    }
    return 0;
}
```

这个函数直接`return`了相应的结构体大小。

*   接下来`malloc`申请了`hdrlen+initlen+1`大小的空间，表示`头部+字符串+Null`,然后让`s`指向了字符串的首地址，`fp`指向了头部的最后一个字节，也就是`flag`。
    
*   然后我们的程序进入了`switch`，因为类型为`SDS_TYPE_5`,所以执行了`*fp = type | (initlen << SDS_TYPE_BITS);` 对于`SDS_TYPE_5`类型来说，长度信息实际上也是存在`flag`里面的，因为最大长度是`31`，占`5bit`，还有`3bit`表示type。
    
*   接着`break`出来后，完成了字符串的拷贝工作，然后给s结尾置’\\0’，`s[initlen] = '\0';`，至此，sdsnew调用完毕，此时我们的`sds`结构如下图所示：
    

![这里写图片描述](https://img-blog.csdn.net/20171101230737067)

`flag`大小为`1`字节，中间的`String`长度为`11`字节,后面还有一个`\0`结尾。接着我们的代码执行输出长度和类型，然后调用了`sdscat`函数，如下：

```
s = sdscat(s, "The length of this sentence is greater than 32 bytes");

```

我们给原始的`s`继续追加了超过`32`个字符，其实目的是为了是它转变成`SDS_TYPE_8`类型，sdscat的代码如下所示：

```code
sds sdscat(sds s, const char *t) {
    return sdscatlen(s, t, strlen(t));
}
```

它调用了`sdscatlen`函数：

```code
sds sdscatlen(sds s, const void *t, size_t len) {
    size_t curlen = sdslen(s);

    s = sdsMakeRoomFor(s,len);
    if (s == NULL) return NULL;
    memcpy(s+curlen, t, len);
    sdssetlen(s, curlen+len);
    s[curlen+len] = '\0';
    return s;
}
```

*   `size_t curlen = sdslen(s);`首先获取了当前的长度`curlen`,接着调用了`sdsMakeRoomFor`函数，这个函数比较关键，它能保证`s`的空间足够，如果空间不足会动态分配，代码如下：

```code

sds sdsMakeRoomFor(sds s, size_t addlen) {
    void *sh, *newsh;
    size_t avail = sdsavail(s);
    size_t len, newlen;
    char type, oldtype = s[-1] & SDS_TYPE_MASK;
    int hdrlen;

    /* Return ASAP if there is enough space left. */
    if (avail >= addlen) return s;

    len = sdslen(s);
    sh = (char*)s-sdsHdrSize(oldtype);
    newlen = (len+addlen);
    if (newlen < SDS_MAX_PREALLOC)
        newlen *= 2;
    else
        newlen += SDS_MAX_PREALLOC;

    type = sdsReqType(newlen);

    /* Don't use type 5: the user is appending to the string and type 5 is
     * not able to remember empty space, so sdsMakeRoomFor() must be called
     * at every appending operation. */
    if (type == SDS_TYPE_5) type = SDS_TYPE_8;

    hdrlen = sdsHdrSize(type);
    if (oldtype==type) {
        newsh = s_realloc(sh, hdrlen+newlen+1);
        if (newsh == NULL) return NULL;
        s = (char*)newsh+hdrlen;
    } else {
        /* Since the header size changes, need to move the string forward,
         * and can't use realloc */
        newsh = s_malloc(hdrlen+newlen+1);
        if (newsh == NULL) return NULL;
        memcpy((char*)newsh+hdrlen, s, len+1);
        s_free(sh);
        s = (char*)newsh+hdrlen;
        s[-1] = type;
        sdssetlen(s, len);
    }
    sdssetalloc(s, newlen);
    return s;
}

```

*   `size_t avail = sdsavail(s);`首先调用`sdsavail`函数获取了当前`s`可用空间的大小，`sdsavail`函数如下：

```code
static inline size_t sdsavail(const sds s) {
    unsigned char flags = s[-1];
    switch(flags&SDS_TYPE_MASK) {
        case SDS_TYPE_5: {
            return 0;
        }
        case SDS_TYPE_8: {
            SDS_HDR_VAR(8,s);
            return sh->alloc - sh->len;
        }
        case SDS_TYPE_16: {
            SDS_HDR_VAR(16,s);
            return sh->alloc - sh->len;
        }
        case SDS_TYPE_32: {
            SDS_HDR_VAR(32,s);
            return sh->alloc - sh->len;
        }
        case SDS_TYPE_64: {
            SDS_HDR_VAR(64,s);
            return sh->alloc - sh->len;
        }
    }
    return 0;
}
```

对于`SDS_TYPE_5`类型，直接`return 0`,对于其他类型，需要在`Header`获取`alloc`和`len`然后相减，获取`Header`的宏如下：

```code
SDS_HDR_VAR(8,s);

#define SDS_HDR_VAR(T,s) struct sdshdr##T *sh = (void*)((s)-(sizeof(struct sdshdr##T)));

//本质上就是用s的地址减去（偏移）相应头部结构体大小的地址，就到了Header的第一个字节

return sh->alloc - sh->len;

//然后返回可用字节大小

```

*   `if (avail >= addlen) return s;` 接着判断大小，如果空间是足够的，则将s返回，函数结束。
*   否则我们获取到目前的长度，然后给它加上`sdscat`所追加的字符串长度，如果此时的新长度没有超过`SDS_MAX_PREALLOC=1024*1024`，我们再给新长度`x2`，这样做是为了避免频繁调用`malloc`。
*   `type = sdsReqType(newlen);` 然后我们需要根据新长度重新获取type类型。
*   `if (oldtype==type)`然后判断type是否发生了变化，来决定扩充空间还是重新申请空间。对于我们的例子，接下来需要重新分配空间，如下，走`else`分支：

```code
else {
        /* Since the header size changes, need to move the string forward,
         * and can't use realloc */
        newsh = s_malloc(hdrlen+newlen+1);      //重新分配Header+newlen+1的空间
        if (newsh == NULL) return NULL;
        memcpy((char*)newsh+hdrlen, s, len+1);  //将String部分拷贝至新String部分
        s_free(sh);                             //把旧的sds全部释放
        s = (char*)newsh+hdrlen;                
        s[-1] = type;                           //将type更新
        sdssetlen(s, len);                      //设置大小
    }
    sdssetalloc(s, newlen);                     //设置alloc大小
    return s;                                   //将新的s返回
}
```

当`sdsMakeRoomFor`函数返回后，`sdscatlen`函数继续执行，将需要添加的字符串拷贝至新的空间，然后设置长度和最后的`\0`就返回了。此时`s`变成了下面这样：

![这里写图片描述](https://img-blog.csdn.net/20171101230810257)

需要注意的是执行代码打印出来长度为`64`指的是已经分配的长度，也就是`len`的大小，图片上的`128`是`alloc`的大小，则此时可用长度还有`64`字节，下次如果再追加小于`64`字节的内容就不会重新分配了。最后我们看下`free`的过程，代码如下：

```code
void sdsfree(sds s) {
    if (s == NULL) return;
    s_free((char*)s-sdsHdrSize(s[-1]));
}
```

很简单，如果为`NULL`就返回，否则得到`Header`的首地址然后释放，`sdsHdrSize(s[-1])`是根据`flag`类型获取`Header`的长度，用`s`减去（偏移）`Header`长度个字节就到头部了。上面的过程基本上分析清楚了`sds`有关于创建和扩容以及释放的过程，这样其实已经把握了`sds`的大体脉络，接下来我们看一下它还实现了哪些方便的接口供我们使用。

# 四、其他的接口和特性

1、`sdssplitargs`函数可以将字符串分割，它会默认按`\n、空格、\t、\r、、0`以及`双引号和单引号`进行分割，如下所示:

```code

eg1:
int args;
sds *arr = sdssplitargs("H\ne\tl\rlo Wor\ald",&args);

printf("args is :%d\n",args);
for (int i = 0; i < args; ++i) {
    printf("%s ", arr[i]);
}
sdsfreesplitres(arr,args);       //注意free方式

Out>
args is :5
H e l lo Wor ld


eg2；
sds *arr = sdssplitargs("\"Hello\" World",&args);

Out>
args is :2
Hello World

eg3：
sds *arr = sdssplitargs("\x41 \x42 \x43",&args);

Out>
args is :3
A B C    //把16进制转成了10进制
```

2、`sdssplitlen`也是分割字符串的函数，不过它只可以指定一个分割符号进行分割，但是这个符号可以是一个字符串。

```code
sds s = sdsnew("Hello_-_World");
int args;
sds *arr = sdssplitlen(s, sdslen(s), "_-_", 3, &args);
printf("args is :%d\n", args);
for (int i = 0; i < args; ++i) {
    printf("%s ", arr[i]);
}

Out>
args is :2
Hello World 
```

3、`sdscatprintf()`格式化字符串，类似于`sprintf()`：

```code
int a = 1,b = 1;
sds s = sdsnew("Sum is: ");
s = sdscatprintf(s, "%d+%d = %d", a, b, a+b);
printf("%s\n", s);


Out>
Sum is: 1+1 = 2
```

4、`sdscatfmt`类似于`sdscatprintf`，但是比`sdscatprintf`要快，因为它不依赖于`libc`提供的`sprintf()`函数，但是它指实现了一部分格式化语义，如下：

```code
* However this function only handles an incompatible subset of printf-alike
* format specifiers:
*
* %s - C String
* %S - SDS string
* %i - signed int
* %I - 64 bit signed integer (long long, int64_t)
* %u - unsigned int
* %U - 64 bit unsigned integer (unsigned long long, uint64_t)
* %% - Verbatim "%" character.


sds s = sdsnewlen("Hello ",6);
s = sdscatfmt(s,"%s"," World");
printf("%s\n",s);

Out>
Hello  World
```

5、`sdstrim`可以剔除sds中指定的字符:

```code
sds s = sdsnew("AA...AA.a.aa.aHelloWorldiii :::");
s = sdstrim(s, "A. a:i");
printf("%s\n",s);

>Out
HelloWorld
```

6、`sdsrange`类似于`substring`的功能，可以返回子串

```code
sds s = sdsnew("Hello World");
sdsrange(s, 1, -1);     // 1 表示第一个字符，-1 表示倒数第一个字符
printf("%s\n", s);

Out>
ello World 
```

7、`sdsmapchars`可以将字符串中指定字符替换。

```code
sds s = sdsnew("Hello World");
s = sdsmapchars(s, "o", "u", 1);     //将o替换成u
printf("%s\n",s);

Out>
Hellu Wurld
```

\[完\]