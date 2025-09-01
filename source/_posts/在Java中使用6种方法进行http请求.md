---
title: 在Java中使用6种方法进行http请求
id: 1594
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/%E5%9C%A8java%E4%B8%AD%E4%BD%BF%E7%94%A86%E7%A7%8D%E6%96%B9%E6%B3%95%E8%BF%9B%E8%A1%8Chttp%E8%AF%B7%E6%B1%82/
categories:
 - java
tags: 
 - http
---

Java 中发出 HTTP 请求的常见方法有：

1.  Java SE 的 HttpURLConnection 类
2.  Apache 的 HttpClient 第三方库
3.  Spring 的 RestTemplate 类
4.  JavaFX 的 WebEngine 类
5.  OkHttp 第三方库
6.  Retrofit 第三方库

以上列举的方法都是可以用来发出 HTTP 请求的，具体的使用方法参考如下
也可以参考官方文档和代码示例。


1.  Java SE 的 HttpURLConnection 类：

```

import java.io.*;
import java.net.*;

public class HttpRequestExample {
  public static void main(String[] args) throws IOException {
    URL url = new URL("https://www.example.com");
    HttpURLConnection con = (HttpURLConnection) url.openConnection();
    con.setRequestMethod("GET");
    int status = con.getResponseCode();
    BufferedReader in = new BufferedReader(
      new InputStreamReader(con.getInputStream()));
    String inputLine;
    StringBuffer content = new StringBuffer();
    while ((inputLine = in.readLine()) != null) {
      content.append(inputLine);
    }
    in.close();
    con.disconnect();
    System.out.println(content);
  }
}
```

2.  Apache 的 HttpClient 第三方库：

```
CloseableHttpClient client = HttpClients.createDefault();
HttpGet request = new HttpGet("http://www.example.com");
CloseableHttpResponse response = client.execute(request);
``` 

3.  Spring 的 RestTemplate 类：

```
RestTemplate restTemplate = new RestTemplate();
String response = restTemplate.getForObject("http://www.example.com", String.class);
```

4.  JavaFX 的 WebEngine 类：

```
WebEngine engine = new WebEngine();
engine.load("http://www.example.com");
```

5.  OkHttp 第三方库：

```
OkHttpClient client = new OkHttpClient();
Request request = new Request.Builder()
  .url("http://www.example.com")
  .build();
Response response = client.newCall(request).execute();
```

6.  Retrofit 第三方库：

```
Retrofit retrofit = new Retrofit.Builder()
  .baseUrl("http://www.example.com")
  .build();
MyApi api = retrofit.create(MyApi.class);
Call<ResponseBody> call = api.getData();
Response<ResponseBody> response = call.execute();
```

以上是常见的 Java 中发出 HTTP 请求的方法以及具体的示例，实际应用中可以根据需要选择适合的方法。