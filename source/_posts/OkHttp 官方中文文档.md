---
title: OkHttp 官方中文文档
id: 1455
date: 2024-10-31 22:01:56
author: daichangya
permalink: /archives/okhttp%E5%AE%98%E6%96%B9%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/
tags: 
 - http
---


    [本文翻译来自 官方OkHttp Wiki](https://github.com/square/okhttp/wiki)

## 一、Calls

HTTP客户端的工作是接受你的**request**，并产生它的**response**。这个在理论上是简单的，但在实践中确是很棘手。

### 1.1 [请求](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Request.html)

每一个HTTP请求中都包含一个URL，一个方法（如*GET*或*POST*），和一个请求头列表（*headers*）。请求还可以含有一个请求体（body）：一个特定内容类型的数据流。

### 1.2 [响应](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Response.html)

每一个HTTP响应中都包含一个状态码（如*200*代表成功，*404*代表未找​​到），一个响应头列表（*headers*）和一个可选的响应体（*body*）。

### 1.3重写请求

当你的OkHttp发送一个HTTP请求，你在描述一个高层次的要求：“给我获取这个网址中的这些请求头。”对于正确性和效率，OkHttp发送前会重写你的请求。

OkHttp可以在原先的请求中添加请求头（*headers*），包括*Content-Length*, *Transfer-Encoding*, *User-Agent*, *Host*, *Connection*, 和 *Content-Type*。除非请求头已经存在压缩响应，否则它还将添加一个*Accept-Encoding*请求头。如果你有*cookies*，OkHttp还将添加一个*Cookie*请求头。

一些请求会有一个缓存的响应。当这个缓存的响应不是最新的时候，OkHttp会发送一个有条件的GET来下载更新的响应，如果它比缓存还新。它将会添加需要的请求头，如*IF-Modified-Since*和*If-None-Match*。

### 1.4重写响应

如果使用的是透明压缩，OkHttp会丢失相应的响应头*Content-Encoding*和*Content-Length*，这是因为它们不能用于解压响应体（*body*）。

如果一个条件*GET*是成功的，在指定的规范下，响应来自于网络和缓存的合并。

### 1.5后续请求

当你的请求的URL已经移动，Web服务器将返回一个响应码像*302*，以表明本文档的新的URL。OkHttp将按照重定向检索最终响应。

如果响应问题是一个的授权盘问，OkHttp将会要求身份验证（如果有一个已经配置好），以满足盘问。如果身份验证提供凭据，请求将会带着凭证进行重试。

### 1.6请求重试

有时连接失败：要么是连接池已经过时和断开，或是Web服务器本身无法达成。如果有一个是可用的，OkHttp将会使用不同的路由进行请求重试。

### 1.7 [呼叫](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Call.html)

随着重写，重定向，后续和重试，你简单的要求可能会产生很多请求和响应。OkHttp使用呼叫（*Call*）并通过许多必要的中间请求和响应来满足你请求的任务模型。通常情况，这是不是很多！如果您的网址被重定向，或者如果您故障转移到另一个IP地址，但它会欣慰的知道你的代码会继续工作。

通过以下两种方式进行呼叫：  
\- **同步**：直到响应,你的线程块是可读的。  
\- **异步**：你在任何线程进行排队请求，并且当响应是可读的时候，你会在另一个线程得到[回调](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Callback.html)。

呼叫（*Calls*）可以在任何线程中取消。如果它尚未完成，它将作为失败的呼叫（*Calls*）！当呼叫（Call）被取消的时候，如果代码试图进行写请求体（*request body*）或读取响应体（*response body*）会遭受*IOException*异常。

### 1.8调度

对于同步调用，你带上你自己的线程，并负责管理并发请求。并发连接过多浪费资源; 过少的危害等待时间。

对于异步调用，[调度](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Dispatcher.html)实现了最大同时请求策略。您可以设置每个Web服务器最大值（默认值为5），和整体值（默认为64）。

## 二、Connections

虽然只提供了URL，但是OkHttp计划使用三种类型连接到你的web服务器：URL, Address, 和 Route。

### 2.1[URLs](http://square.github.io/okhttp/3.x/okhttp/okhttp3/HttpUrl.html)

URLs（如[https://github.com/square/okhttp](https://github.com/square/okhttp)）是HTTP和因特网的基础。除了是网络上通用和分散的命名方案，他们还指定了如何访问网络资源。

##### URLs摘要：

*   它们指定该呼叫(*Call*)可以被明文（*HTTP*）或加密的（*HTTPS*），但不指定用哪种加密算法。他们也不指定如何验证对方的证书（*[HostnameVerifier](https://developer.android.com/reference/javax/net/ssl/HostnameVerifier.html)*）或证书可以信任（*[SSLSocketFactory](https://developer.android.com/reference/org/apache/http/conn/ssl/SSLSocketFactory.html)*）。
*   他们不指定是否应使用特定的代理服务器或如何与该代理服务器进行身份验证。

他们还具体：每个URL识别特定的路径（如 */square/okhttp*）和查询（如 *?q=sharks&lang=en*）。每个Web服务器主机的网址。

### 2.2 [Addresses](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Address.html)

Addresses指定网络服务器（如*github.com*）和所有的静态必要的配置，以及连接到该服务器：端口号，HTTPS设置和首选的网络协议（如*HTTP / 2*或*SPDY*）。

共享相同地址的URL也可以共享相同的基础TCP套接字连接。共享一个连接有实实在在的性能优点：更低的延迟，更高的吞吐量（由于TCP慢启动）和保养电池。OkHttp使用的[ConnectionPool](http://square.github.io/okhttp/3.x/okhttp/okhttp3/ConnectionPool.html)自动重用HTTP / 1.x的连接和多样的HTTP/ 2和SPDY连接。

在OkHttp地址的某些字段来自URL（*scheme*, *hostname*, *port*），其余来自[OkHttpClient](http://square.github.io/okhttp/3.x/okhttp/okhttp3/OkHttpClient.html)。

### 2.3 [Routes](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Route.html)

Routes提供连接到一个网络服务器所必需的动态信息。就是尝试特定的IP地址（如由DNS查询发现），使用确切的代理服务器（如果一个特定的IP地址的[ProxySelector](https://developer.android.com/reference/java/net/ProxySelector.html)在使用中）和协商的TLS版本（HTTPS连接）。

可能有单个地址对应多个路由。例如，在多个数据中心托管的Web服务器，它可能会在其DNS响应产生多个IP地址。

### 2.4[Connections](http://square.github.io/okhttp/3.x/okhttp/okhttp3/Connection.html)

当你使用OkHttp进行一个URL请求时，下面是它的操作流程：

1.  它使用URL和配置OkHttpClient创建一个**address**。此地址指定我们将如何连接到网络服务器。
2.  它通过地址从连接池中取回一个连接。
3.  如果它没有在池中找到连接，它会选择*route*尝试。这通常意味着使用一个DNS请求， 以获取服务器的IP地址。如果需要，它会选择一个的TLS版本和代理服务器。
4.  如果它是一个新的route，它连接通过建立无论是直接的socket连接，socket连接使用TLS安全通道（用于HTTPS通过一个HTTP代理），或直接TLS连接。它的TLS握手是必要的。
5.  它发送HTTP请求并读取响应。  
    如果有连接出现问题，OkHttp将选择另一条route，然后再试一次。这带来的好处是当一个服务器的地址的一个子集是不可达时，OkHttp能够自动恢复。当连接池是过时或者试图TLS版本不受支持时，这种方式是很有用的。

一旦响应已经被接收到，该连接将被返回到池中，以便它可以在将来的请求中被重用。连接在池中闲置一段时间后，它会被赶出。

## 三、Recipes

我们已经写了一些方法，演示了如何解决OkHttp常见问题。通过阅读他们了解一切是如何正常工作的。可以自由剪切和粘贴这些例子。

### 3.1同步获取

下载文件，打印其头部，并以字符串形式打印其响应体。

该*string()* 方法在响应体中是方便快捷的小型文件。但是，如果响应体较大（大于1 MIB以上），它会将整个较大文件加载到内存中，所以应该避免*string()* 。在这种情况下，更倾向于将响应体作为流进行处理。

```java
 private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://publicobject.com/helloworld.txt")
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    Headers responseHeaders = response.headers();
    for (int i = 0; i < responseHeaders.size(); i++) {
      System.out.println(responseHeaders.name(i) + ": " + responseHeaders.value(i));
    }

    System.out.println(response.body().string());
  }
```

### 3.2异步获取

下载一个工作线程的文件，当响应是可读的时候，获取回调（*Callback*）。当响应头已经准备好后，将产生回调（*Callback*）。读取响应体可能一直阻塞。目前OkHttp不提供异步API来接收响应体的部位。

```java
private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://publicobject.com/helloworld.txt")
        .build();

    client.newCall(request).enqueue(new Callback() {
      @Override public void onFailure(Call call, IOException e) {
        e.printStackTrace();
      }

      @Override public void onResponse(Call call, Response response) throws IOException {
        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

        Headers responseHeaders = response.headers();
        for (int i = 0, size = responseHeaders.size(); i < size; i++) {
          System.out.println(responseHeaders.name(i) + ": " + responseHeaders.value(i));
        }

        System.out.println(response.body().string());
      }
    });
  }
```

### 3.3访问头

典型的HTTP头工作就像一个*Map*<*String, String*\> ：每个字段都有一个值或无值。但是，一些头部(*headers*)允许多个值，比如Guava的Multimap。例如，它共同为一个HTTP响应提供多个*Vary*头。OkHttp的API，试图使这两种情况下都能舒适使用。

当写请求头，用*header(name, value)*来为唯一出现的*name*设置*value*。如果它本身存在值，在添加新的*value*之前，他们会被移除。使用*addHeader(name, value)*来添加头部不需要移除当前存在的*headers*。

当读取响应头，用*header(name)*返回最后设置name的value。如果没有*value*，*header(name)*将返回null。可以使用*headers(name)*来读取所有列表字段的值，。

要访问所有的头部，用*Headers*类，它支持索引访问。

```java
 private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://api.github.com/repos/square/okhttp/issues")
        .header("User-Agent", "OkHttp Headers.java")
        .addHeader("Accept", "application/json; q=0.5")
        .addHeader("Accept", "application/vnd.github.v3+json")
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println("Server: " + response.header("Server"));
    System.out.println("Date: " + response.header("Date"));
    System.out.println("Vary: " + response.headers("Vary"));
  }
```

### 3.4Posting a String

使用HTTP POST的请求体发送到服务。下面例子post了一个markdown文档到一个的Web服务（将markdown作为HTML）。由于整个请求体是同时在内存中，应避免使用此API发送较大（大于1 MIB）的文件。

```java
public static final MediaType MEDIA_TYPE_MARKDOWN
      = MediaType.parse("text/x-markdown; charset=utf-8");

  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    String postBody = ""
        + "Releases\n"
        + "--------\n"
        + "\n"
        + " * _1.0_ May 6, 2013\n"
        + " * _1.1_ June 15, 2013\n"
        + " * _1.2_ August 11, 2013\n";

    Request request = new Request.Builder()
        .url("https://api.github.com/markdown/raw")
        .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, postBody))
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
  }
```

### 3.5 Post Streaming

在这里，我们POST请求体作为*stream*。将正在生成请求体的内容写入到*stream*中。下面例子*streams*直接进入 [Okio](https://github.com/square/okio)缓冲水槽。你的程序可能更喜欢使用OutputStream，你可以通过BufferedSink.outputStream（）获得 OutputStream。

```java
 public static final MediaType MEDIA_TYPE_MARKDOWN
      = MediaType.parse("text/x-markdown; charset=utf-8");

  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    RequestBody requestBody = new RequestBody() {
      @Override public MediaType contentType() {
        return MEDIA_TYPE_MARKDOWN;
      }

      @Override public void writeTo(BufferedSink sink) throws IOException {
        sink.writeUtf8("Numbers\n");
        sink.writeUtf8("-------\n");
        for (int i = 2; i <= 997; i++) {
          sink.writeUtf8(String.format(" * %s = %s\n", i, factor(i)));
        }
      }

      private String factor(int n) {
        for (int i = 2; i < n; i++) {
          int x = n / i;
          if (x * i == n) return factor(x) + " × " + i;
        }
        return Integer.toString(n);
      }
    };

    Request request = new Request.Builder()
        .url("https://api.github.com/markdown/raw")
        .post(requestBody)
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
  }
```

### 3.6 Posting a File

将文件作为请求体是很容易的。

```java
public static final MediaType MEDIA_TYPE_MARKDOWN
      = MediaType.parse("text/x-markdown; charset=utf-8");

  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    File file = new File("README.md");

    Request request = new Request.Builder()
        .url("https://api.github.com/markdown/raw")
        .post(RequestBody.create(MEDIA_TYPE_MARKDOWN, file))
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
  }
```

### 3.7 发布表单参数

使用*FormBody.Builder*建立一个请求体，它就像一个HTML 的标记。*Names* 和*values*将使用HTML兼容的表单URL编码进行编码。

```java
 private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    RequestBody formBody = new FormBody.Builder()
        .add("search", "Jurassic Park")
        .build();
    Request request = new Request.Builder()
        .url("https://en.wikipedia.org/w/index.php")
        .post(formBody)
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
  }
```

### 3.8 发布multipart请求

*MultipartBody.Builder*可以构建与*HTML*文件上传表单兼容的复杂请求主体。*multipart*请求体的每一部分本身就是请求体，并且可以定义自己的头部。如果存在，这些头应该描述的部分请求体，如它的*Content-Disposition*。如果*Content-Length* 和 *Content-Type*头部可以使用，则他们会自动添加。

```java
 private static final String IMGUR_CLIENT_ID = "...";
  private static final MediaType MEDIA_TYPE_PNG = MediaType.parse("image/png");

  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    // Use the imgur image upload API as documented at https://api.imgur.com/endpoints/image
    RequestBody requestBody = new MultipartBody.Builder()
        .setType(MultipartBody.FORM)
        .addFormDataPart("title", "Square Logo")
        .addFormDataPart("image", "logo-square.png",
            RequestBody.create(MEDIA_TYPE_PNG, new File("website/static/logo-square.png")))
        .build();

    Request request = new Request.Builder()
        .header("Authorization", "Client-ID " + IMGUR_CLIENT_ID)
        .url("https://api.imgur.com/3/image")
        .post(requestBody)
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
  }
```

### 3.9 通过GSON解析响应的JSON

GSON是实现JSON和Java对象之间便利转换的API。这里，我们用它来解码从GitHub的API 响应的JSON。

需要注意的是*ResponseBody.charStream（）*使用的*Content-Type*响应头进行解码时，所使用的字符集默认为UTF-8 。

```java
private final OkHttpClient client = new OkHttpClient();
  private final Gson gson = new Gson();

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://api.github.com/gists/c2a7c39532239ff261be")
        .build();
    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    Gist gist = gson.fromJson(response.body().charStream(), Gist.class);
    for (Map.Entry<String, GistFile> entry : gist.files.entrySet()) {
      System.out.println(entry.getKey());
      System.out.println(entry.getValue().content);
    }
  }

  static class Gist {
    Map<String, GistFile> files;
  }

  static class GistFile {
    String content;
  }
```

### 3.10 响应缓存

要缓存响应，你需要有一个缓存目录来进行读取和写入，并限制缓存的大小。缓存目录应该是私有的，不被信任的应用程序不能够阅读其内容！

多个缓存同时访问相同的缓存目录，这是错误的。大多数应用程序应该调用一次*new OkHttpClient()*，在任何地方都使用相同的实例和自己的缓存配置。否则，这两个缓存实例将踩到对方，破坏响应缓存，这可能使你的程序崩溃。

响应缓存使用HTTP头进行配置。您可以添加请求头*Cache-Control: max-stale=3600*，这样OkHttp的缓存就会遵循他们。你的网络服务器可以通过自己的响应头配置缓存多长时间的响应，如*Cache-Control: max-age=9600*。有缓存头强制缓存的响应，强制网络响应，或强制使用条件GET验证的网络响应。

```java
 private final OkHttpClient client;

  public CacheResponse(File cacheDirectory) throws Exception {
    int cacheSize = 10 * 1024 * 1024; // 10 MiB
    Cache cache = new Cache(cacheDirectory, cacheSize);

    client = new OkHttpClient.Builder()
        .cache(cache)
        .build();
  }

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://publicobject.com/helloworld.txt")
        .build();

    Response response1 = client.newCall(request).execute();
    if (!response1.isSuccessful()) throw new IOException("Unexpected code " + response1);

    String response1Body = response1.body().string();
    System.out.println("Response 1 response:          " + response1);
    System.out.println("Response 1 cache response:    " + response1.cacheResponse());
    System.out.println("Response 1 network response:  " + response1.networkResponse());

    Response response2 = client.newCall(request).execute();
    if (!response2.isSuccessful()) throw new IOException("Unexpected code " + response2);

    String response2Body = response2.body().string();
    System.out.println("Response 2 response:          " + response2);
    System.out.println("Response 2 cache response:    " + response2.cacheResponse());
    System.out.println("Response 2 network response:  " + response2.networkResponse());

    System.out.println("Response 2 equals Response 1? " + response1Body.equals(response2Body));
  }
```

使用*CacheControl.FORCE_NETWORK*可以禁止使用缓存的响应。使用*CacheControl.FORCE_CACHE*可以禁止使用网络。警告：如果您使用FORCE_CACHE和响应来自网络，OkHttp将会返回一个504不可满足请求的响应。

### 3.11 取消Call

通过Call.cancel（）来立即停止正在进行的Call。如果一个线程目前正在写请求或读响应，它还将收到一个IOException异常。当一个Call不需要时，使用取消Call来保护网络; 例如，当用户从应用程序导航离开。同步和异步调用可以被取消。

```java
private final ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);
  private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://httpbin.org/delay/2") // This URL is served with a 2 second delay.
        .build();

    final long startNanos = System.nanoTime();
    final Call call = client.newCall(request);

    // Schedule a job to cancel the call in 1 second.
    executor.schedule(new Runnable() {
      @Override public void run() {
        System.out.printf("%.2f Canceling call.%n", (System.nanoTime() - startNanos) / 1e9f);
        call.cancel();
        System.out.printf("%.2f Canceled call.%n", (System.nanoTime() - startNanos) / 1e9f);
      }
    }, 1, TimeUnit.SECONDS);

    try {
      System.out.printf("%.2f Executing call.%n", (System.nanoTime() - startNanos) / 1e9f);
      Response response = call.execute();
      System.out.printf("%.2f Call was expected to fail, but completed: %s%n",
          (System.nanoTime() - startNanos) / 1e9f, response);
    } catch (IOException e) {
      System.out.printf("%.2f Call failed as expected: %s%n",
          (System.nanoTime() - startNanos) / 1e9f, e);
    }
  }
```

### 3.12 超时

当无法访问查询时，将调用超时失败。超时在网络划分中可以是由于客户端连接问题，服务器可用性的问题，或两者之间的任何东西。OkHttp支持连接，读取和写入超时。

```java
private final OkHttpClient client;

  public ConfigureTimeouts() throws Exception {
    client = new OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .writeTimeout(10, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build();
  }

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://httpbin.org/delay/2") // This URL is served with a 2 second delay.
        .build();

    Response response = client.newCall(request).execute();
    System.out.println("Response completed: " + response);
  }
```

### 3.13 每个呼叫配置

所有的HTTP客户端都在OkHttpClient中配置，这包括代理设置，超时和缓存。当你需要改变单一Call的配置时，调用*OkHttpClient.newBuilder（）* 。这将返回共享相同的连接池，调度和配置的原客户端的建造器。在下面的例子中，我们做了500毫秒超时，另外一个3000毫秒超时请求。

```java
private final OkHttpClient client = new OkHttpClient();

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://httpbin.org/delay/1") // This URL is served with a 1 second delay.
        .build();

    try {
      // Copy to customize OkHttp for this request.
      OkHttpClient copy = client.newBuilder()
          .readTimeout(500, TimeUnit.MILLISECONDS)
          .build();

      Response response = copy.newCall(request).execute();
      System.out.println("Response 1 succeeded: " + response);
    } catch (IOException e) {
      System.out.println("Response 1 failed: " + e);
    }

    try {
      // Copy to customize OkHttp for this request.
      OkHttpClient copy = client.newBuilder()
          .readTimeout(3000, TimeUnit.MILLISECONDS)
          .build();

      Response response = copy.newCall(request).execute();
      System.out.println("Response 2 succeeded: " + response);
    } catch (IOException e) {
      System.out.println("Response 2 failed: " + e);
    }
  }
```

### 3.14 认证处理

OkHttp能够自动重试未经授权的请求。当响应是*401 Not Authorized*，一个*Authenticator*被要求提供凭据。应该建立一个包含缺少凭据的新要求。如果没有凭证可用，则返回null跳过重试。

使用*Response.challenges（）*获得任何认证挑战方案和领域。当完成一个基本的挑战，用*Credentials.basic(username, password)*编码请求头。

```java
private final OkHttpClient client;

  public Authenticate() {
    client = new OkHttpClient.Builder()
        .authenticator(new Authenticator() {
          @Override public Request authenticate(Route route, Response response) throws IOException {
            System.out.println("Authenticating for response: " + response);
            System.out.println("Challenges: " + response.challenges());
            String credential = Credentials.basic("jesse", "password1");
            return response.request().newBuilder()
                .header("Authorization", credential)
                .build();
          }
        })
        .build();
  }

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("http://publicobject.com/secrets/hellosecret.txt")
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    System.out.println(response.body().string());
  }
```

为了避免验证时不工作的重试，你可以返回null放弃。例如，当这些确切的凭据已经尝试,您可以跳过重试：

```java
if (credential.equals(response.request().header("Authorization"))) {
    return null; //如果我们已经使用这些凭据失败，不重试
   }
```

当你的应用尝试的次数超过了限制的次数时，你可以跳过重试：

```java
if (responseCount(response) >= 3) {
    return null; //如果我们已经失败了3次，放弃。 .
  }
```

这上面的代码依赖于下面的*responseCount（）*方法：

```java
 private int responseCount(Response response) {
    int result = 1;
    while ((response = response.priorResponse()) != null) {
      result++;
    }
    return result;
  }
```

## 四、拦截器

拦截器是一个强大的机制，它可以监控，重写和重试Calls。下面是一个简单记录传出请求和响应传入的拦截器。

```java
class LoggingInterceptor implements Interceptor {
  @Override public Response intercept(Interceptor.Chain chain) throws IOException {
    Request request = chain.request();

    long t1 = System.nanoTime();
    logger.info(String.format("Sending request %s on %s%n%s",
        request.url(), chain.connection(), request.headers()));

    Response response = chain.proceed(request);

    long t2 = System.nanoTime();
    logger.info(String.format("Received response for %s in %.1fms%n%s",
        response.request().url(), (t2 - t1) / 1e6d, response.headers()));

    return response;
  }
}
```

呼叫*chain.proceed(request)*是实现每个拦截器的的重要组成部分。这个看起来简单的方法是，所有的HTTP工作情况，产生满足请求的响应。

拦截器可以链接。假设你有一个可以压缩和校验的拦截器：你需要确定数据是否可以压缩，然后再执行校验，或者是先校验然后再压缩。为了拦截器被调用，OkHttp使用列表来跟踪拦截器，。  
![这里写图片描述](https://img-blog.csdn.net/20160628191638424)

### 4.1 应用拦截器

拦截器可以注册为应用拦截器或网络拦截器。我们将使用*LoggingInterceptor*来区别。

通过在*OkHttpClient.Builder*上调用*addInterceptor（）*来注册应用程序拦截器：

```java
OkHttpClient client = new OkHttpClient.Builder()
    .addInterceptor(new LoggingInterceptor())
    .build();

Request request = new Request.Builder()
    .url("http://www.publicobject.com/helloworld.txt")
    .header("User-Agent", "OkHttp Example")
    .build();

Response response = client.newCall(request).execute();
response.body().close();
```

该URL [http://www.publicobject.com/helloworld.txt](http://www.publicobject.com/helloworld.txt)重定向到[https://publicobject.com/helloworld.txt](https://publicobject.com/helloworld.txt)，并OkHttp遵循这种自动重定向。我们的应用拦截器被调用一次，并且从返回的响应*chain.proceed（）*具有重定向：

```
INFO: Sending request http://www.publicobject.com/helloworld.txt on null
User-Agent: OkHttp Example

INFO: Received response for https://publicobject.com/helloworld.txt in 1179.7ms
Server: nginx/1.4.6 (Ubuntu)
Content-Type: text/plain
Content-Length: 1759
Connection: keep-alive
```

我们可以看到，我们被重定向是因为*response.request().url()*不同于*request.url（）* 。这两个日志语句记录两个不同的URL。

### 4.2 网络拦截器

注册网络拦截器很类似。调用*addNetworkInterceptor（）*代替*addInterceptor（）* ：

```java
OkHttpClient client = new OkHttpClient.Builder()
    .addNetworkInterceptor(new LoggingInterceptor())
    .build();

Request request = new Request.Builder()
    .url("http://www.publicobject.com/helloworld.txt")
    .header("User-Agent", "OkHttp Example")
    .build();

Response response = client.newCall(request).execute();
response.body().close();
```

当我们运行这段代码，拦截器运行两次。一个是初始请求[http://www.publicobject.com/helloworld.txt](http://www.publicobject.com/helloworld.txt)，另一个是用于重定向到[https://publicobject.com/helloworld.txt](https://publicobject.com/helloworld.txt)。

```
INFO: Sending request http://www.publicobject.com/helloworld.txt on Connection{www.publicobject.com:80, proxy=DIRECT hostAddress=54.187.32.157 cipherSuite=none protocol=http/1.1}
User-Agent: OkHttp Example
Host: www.publicobject.com
Connection: Keep-Alive
Accept-Encoding: gzip

INFO: Received response for http://www.publicobject.com/helloworld.txt in 115.6ms
Server: nginx/1.4.6 (Ubuntu)
Content-Type: text/html
Content-Length: 193
Connection: keep-alive
Location: https://publicobject.com/helloworld.txt

INFO: Sending request https://publicobject.com/helloworld.txt on Connection{publicobject.com:443, proxy=DIRECT hostAddress=54.187.32.157 cipherSuite=TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA protocol=http/1.1}
User-Agent: OkHttp Example
Host: publicobject.com
Connection: Keep-Alive
Accept-Encoding: gzip

INFO: Received response for https://publicobject.com/helloworld.txt in 80.9ms
Server: nginx/1.4.6 (Ubuntu)
Content-Type: text/plain
Content-Length: 1759
Connection: keep-alive
```

网络请求还包含很多数据，如OkHttp加入*Accept-Encoding: gzip*头部通知支持压缩响应。网络拦截器的链具有非空的连接，它可用于询问IP地址和连接到网络服务器的TLS配置。

### 4.3 应用程序和网络拦截之间进行选择

每个拦截器链(*interceptor chain*)都具有相对优势。

#### 应用拦截器

*   不必担心像重定向和重试的中间响应。
*   总是被调用一次，即使HTTP响应来自缓存服务。
*   观察应用程序的原意。不关心OkHttp注入的头文件，如 *If-None-Match*。
*   允许短路和不调用*Chain.proceed（）* 。
*   允许重试，并多次调用Chain.proceed（） 。

#### 网络拦截器

*   能够操作像重定向和重试的中间响应。
*   在短路网络上不调用缓存的响应。
*   观察在网络上传输的数据。
*   访问*Connection*承载请求。

### 4.4重写请求

拦截器可以添加，删除或替换请求头。他们还可以转换请求体。例如，如果你连接到已知支持它的网络服务器，你可以使用应用程序拦截器添加请求体的压缩。

```
/** This interceptor compresses the HTTP request body. Many webservers can't handle this! */
final class GzipRequestInterceptor implements Interceptor {
  @Override public Response intercept(Interceptor.Chain chain) throws IOException {
    Request originalRequest = chain.request();
    if (originalRequest.body() == null || originalRequest.header("Content-Encoding") != null) {
      return chain.proceed(originalRequest);
    }

    Request compressedRequest = originalRequest.newBuilder()
        .header("Content-Encoding", "gzip")
        .method(originalRequest.method(), gzip(originalRequest.body()))
        .build();
    return chain.proceed(compressedRequest);
  }

  private RequestBody gzip(final RequestBody body) {
    return new RequestBody() {
      @Override public MediaType contentType() {
        return body.contentType();
      }

      @Override public long contentLength() {
        return -1; // We don't know the compressed length in advance!
      }

      @Override public void writeTo(BufferedSink sink) throws IOException {
        BufferedSink gzipSink = Okio.buffer(new GzipSink(sink));
        body.writeTo(gzipSink);
        gzipSink.close();
      }
    };
  }
}
```

### 4.5 重写响应

相对应的，拦截器也可以重写响应头和转换响应体。通常不要重写请求头，因为它可能违反了Web服务器的期望导致更危险！

在一个棘手的情况下，如果已经做好应对的后果，重写响应头是解决问题的有效方式。例如，您可以修复服务器的配置错误的*Cache-Control*响应头以便更好地响应缓存：

```
/** Dangerous interceptor that rewrites the server's cache-control header. */
private static final Interceptor REWRITE_CACHE_CONTROL_INTERCEPTOR = new Interceptor() {
  @Override public Response intercept(Interceptor.Chain chain) throws IOException {
    Response originalResponse = chain.proceed(chain.request());
    return originalResponse.newBuilder()
        .header("Cache-Control", "max-age=60")
        .build();
  }
};
```

通常此方法效果最好，它补充了在Web服务器上相应的修复！

### 4.6 可用性

OkHttp的拦截器需要OkHttp 2.2或更高。不幸的是，拦截器不能与OkUrlFactory工作，或者建立在这之上的库，包括 Retrofit ≤1.8和 Picasso≤2.4。

## 五、 HTTPS

OkHttp试图平衡两个相互竞争的担忧：

*   连接到尽可能多的主机越好。这包括运行最新版本的先进主机*[boringssl](https://boringssl.googlesource.com/boringssl/)*和运行旧版的日期主机[*OpenSSL*](https://www.openssl.org/)。
*   安全的连接。这包括远程Web服务器证书的验证和强密码交换的数据隐私。

当涉及到HTTPS服务器的连接，OkHttp需要知道提供哪些[TLS版本](http://square.github.io/okhttp/3.x/okhttp/okhttp3/TlsVersion.html)和[密码套件](http://square.github.io/okhttp/3.x/okhttp/okhttp3/CipherSuite.html)。如果客户端想要最大限度地连接包括过时的TLS版本和弱由设计的密码套件。通过使用最新版本的TLS和实力最强的加密套件来最大限度地提高客户端的安全性。

具体的安全与连接是由[*ConnectionSpec*](http://square.github.io/okhttp/3.x/okhttp/okhttp3/ConnectionSpec.html)接口决定。OkHttp包括三个内置的连接规格：

*   *MODERN_TLS*是连接到现代的HTTPS服务器安全的配置。
*   *COMPATIBLE_TLS*是连接到一个安全，但不是现代的-HTTPS服务器的安全配置。
*   *CLEARTEXT*是用于不安全配置的http：//网址。  
    默认情况下，OkHttp先尝试*MODERN_TLS*连接，如果现代配置失败的话将退回到*COMPATIBLE_TLS*连接。

在每一个规范的TLS版本和密码套件都可随每个发行版而更改。例如，在OkHttp 2.2，我们下降支持响应[POODLE](http://googleonlinesecurity.blogspot.ca/2014/10/this-poodle-bites-exploiting-ssl-30.html)攻击的SSL 3.0。而在OkHttp 2.3我们下降的支持*[RC4](http://en.wikipedia.org/wiki/RC4#Security)*。对于桌面Web浏览器，保持最新的OkHttp是保持安全的最好办法。

你可以用一组自定义TLS版本和密码套件建立自己的连接规格。例如，限制配置三个备受推崇的密码套件。它的缺点是，它需要的Andr​​oid 5.0+和一个类似的电流网络服务器

```java
ConnectionSpec spec = new ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)  
    .tlsVersions(TlsVersion.TLS_1_2)
    .cipherSuites(
          CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
          CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
          CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM_SHA256)
    .build();

OkHttpClient client = new OkHttpClient.Builder() 
    .connectionSpecs(Collections.singletonList(spec))
    .build();
```

### 5.1证书钉扎

默认情况下，OkHttp信任主机平台的证书颁发机构。这种策略最多的连接，但它受证书颁发机构的袭击，如[*2011 DigiNotar*](http://www.computerworld.com/article/2510951/cybercrime-hacking/hackers-spied-on-300-000-iranians-using-fake-google-certificate.html)的攻击。它还假定您的HTTPS服务器的证书是由证书颁发机构签署。

使用[*CertificatePinner*](http://square.github.io/okhttp/3.x/okhttp/okhttp3/CertificatePinner.html)来限制哪些证书和证书颁发机构是可信任的。证书钉扎增强了安全性，但这会限制你的服务器团队更新自己的TLS证书。在没有你的服务器的TLS管理员的同意下，不要使用证书钉扎！

```java
public CertificatePinning() {
    client = new OkHttpClient.Builder()
        .certificatePinner(new CertificatePinner.Builder()
            .add("publicobject.com", "sha256/afwiKY3RxoMmLkuRW1l7QsPZTJPwDS2pdDROQjXw8ig=")
            .build())
        .build();
  }

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://publicobject.com/robots.txt")
        .build();

    Response response = client.newCall(request).execute();
    if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

    for (Certificate certificate : response.handshake().peerCertificates()) {
      System.out.println(CertificatePinner.pin(certificate));
    }
  }
```

### 5.2定制信任证书

下面完整的代码示例演示了如何用自定义证书替换主机平台的证书。如上所述，在没有你的服务器的TLS管理员的同意下，不要使用自定义证书！

```java
private final OkHttpClient client;

  public CustomTrust() {
    SSLContext sslContext = sslContextForTrustedCertificates(trustedCertificatesInputStream());
    client = new OkHttpClient.Builder()
        .sslSocketFactory(sslContext.getSocketFactory())
        .build();
  }

  public void run() throws Exception {
    Request request = new Request.Builder()
        .url("https://publicobject.com/helloworld.txt")
        .build();

    Response response = client.newCall(request).execute();
    System.out.println(response.body().string());
  }

  private InputStream trustedCertificatesInputStream() {
    ... // Full source omitted. See sample.
  }

  public SSLContext sslContextForTrustedCertificates(InputStream in) {
    ... // Full source omitted. See sample.
  }
```