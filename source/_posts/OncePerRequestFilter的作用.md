---
title: OncePerRequestFilter的作用
id: 1576
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/onceperrequestfilter%E7%9A%84%E4%BD%9C%E7%94%A8/
tags: 
 - filter
---



在spring中，filter都默认继承OncePerRequestFilter，但为什么要这样呢？

OncePerRequestFilter顾名思义，他能够确保在一次请求只通过一次filter，而不需要重复执行。

```
public final void doFilter(ServletRequest request, ServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        if(request instanceof HttpServletRequest && response instanceof HttpServletResponse) {
            HttpServletRequest httpRequest = (HttpServletRequest)request;
            HttpServletResponse httpResponse = (HttpServletResponse)response;
            String alreadyFilteredAttributeName = this.getAlreadyFilteredAttributeName();
            boolean hasAlreadyFilteredAttribute = request.getAttribute(alreadyFilteredAttributeName) != null;
            if(!hasAlreadyFilteredAttribute && !this.skipDispatch(httpRequest) && !this.shouldNotFilter(httpRequest)) {
                request.setAttribute(alreadyFilteredAttributeName, Boolean.TRUE);

                try {
                    this.doFilterInternal(httpRequest, httpResponse, filterChain);
                } finally {
                    request.removeAttribute(alreadyFilteredAttributeName);
                }
            } else {
                filterChain.doFilter(request, response);
            }

        } else {
            throw new ServletException("OncePerRequestFilter just supports HTTP requests");
        }
    }
```

常识上都认为，一次请求本来就只过一次，为什么还要由此特别限定呢，实际上此方式是为了兼容不同的web container，特意而为之（jsr168），

也就是说并不是所有的container都像我们期望的只过滤一次，servlet版本不同，表现也不同

```
/**
* Filter base class that guarantees to be just executed once per request,
* on any servlet container. It provides a {@link #doFilterInternal}
* method with HttpServletRequest and HttpServletResponse arguments.
*
* <p>The {@link #getAlreadyFilteredAttributeName} method determines how
* to identify that a request is already filtered. The default implementation
* is based on the configured name of the concrete filter instance.
*
* @author Juergen Hoeller
* @since 06.12.2003
*/
```

如，servlet2.3与servlet2.4也有一定差异 

```
在servlet-2.3中，Filter会过滤一切请求，包括服务器内部使用forward转发请求和<%@ include file="/index.jsp"%>的情况。

到了servlet-2.4中Filter默认下只拦截外部提交的请求，forward和include这些内部转发都不会被过滤，但是有时候我们需要 forward的时候也用到Filter。
```

因此，为了兼容各种不同的运行环境和版本，默认filter继承OncePerRequestFilter是一个比较稳妥的选择