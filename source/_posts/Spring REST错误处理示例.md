---
title: Spring REST错误处理示例
id: 1425
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/springrest%E9%94%99%E8%AF%AF%E5%A4%84%E7%90%86%E7%A4%BA%E4%BE%8B/
---


在本文中，我们将向您展示Spring Boot REST应用程序中的错误处理。

使用的技术：

*   Spring Boot 2.1.2发布
*   Spring 5.1.4。发布
*   Maven 3
*   Java 8

1\. /error
-------

1.1默认情况下，Spring Boot提供了一个`BasicErrorController`用于`/error`处理所有错误的映射控制器，并`getErrorAttributes`生成一个带有错误详细信息，HTTP状态和异常消息的JSON响应。

    {
    	"timestamp":"2019-02-27T04:03:52.398+0000",
    	"status":500,
    	"error":"Internal Server Error",
    	"message":"...",
    	"path":"/path"
    }


BasicErrorController.java

    package org.springframework.boot.autoconfigure.web.servlet.error;
    
    //...
    
    @Controller
    @RequestMapping("${server.error.path:${error.path:/error}}")
    public class BasicErrorController extends AbstractErrorController {
    
    	//...
    
    	@RequestMapping
    	public ResponseEntity<Map<String, Object>> error(HttpServletRequest request) {
    		Map<String, Object> body = getErrorAttributes(request,
    				isIncludeStackTrace(request, MediaType.ALL));
    		HttpStatus status = getStatus(request);
    		return new ResponseEntity<>(body, status);
    	}


在IDE中，在此方法中放置一个断点，您将了解Spring Boot如何生成默认的JSON错误响应。

2.Custom Exception
-------

在Spring Boot中，我们可以`@ControllerAdvice`用来处理自定义异常。

2.1Custom Exception

BookNotFoundException.java

    package com.jsdiff.error;
    
    public class BookNotFoundException extends RuntimeException {
    
        public BookNotFoundException(Long id) {
            super("Book id not found : " + id);
        }
    
    }


如果未找到图书，则控制器抛出上述错误 `BookNotFoundException`

BookController.java

    package com.jsdiff;
    
    //...
    
    @RestController
    public class BookController {
    
        @Autowired
        private BookRepository repository;
    
        // Find
        @GetMapping("/books/{id}")
        Book findOne(@PathVariable Long id) {
            return repository.findById(id)
                    .orElseThrow(() -> new BookNotFoundException(id));
        }
    
    	//...
    }


默认情况下，Spring Boot会生成以下JSON错误响应，即http 500错误。



    curl localhost:8080/books/5
    
    {
    	"timestamp":"2019-02-27T04:03:52.398+0000",
    	"status":500,
    	"error":"Internal Server Error",
    	"message":"Book id not found : 5",
    	"path":"/books/5"
    }


2.2如果未找到图书，则应返回404错误而不是500错误，我们可以像这样重写状态代码：

CustomGlobalExceptionHandler.java

    package com.jsdiff.error;
    
    import org.springframework.http.HttpHeaders;
    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.web.bind.MethodArgumentNotValidException;
    import org.springframework.web.bind.annotation.ControllerAdvice;
    import org.springframework.web.bind.annotation.ExceptionHandler;
    import org.springframework.web.bind.annotation.RestControllerAdvice;
    import org.springframework.web.context.request.WebRequest;
    import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;
    
    import javax.servlet.http.HttpServletResponse;
    import javax.validation.ConstraintViolationException;
    import java.io.IOException;
    import java.util.Date;
    import java.util.LinkedHashMap;
    import java.util.List;
    import java.util.Map;
    import java.util.stream.Collectors;
    
    @ControllerAdvice
    public class CustomGlobalExceptionHandler extends ResponseEntityExceptionHandler {
    
        // Let Spring BasicErrorController handle the exception, we just override the status code
        @ExceptionHandler(BookNotFoundException.class)
        public void springHandleNotFound(HttpServletResponse response) throws IOException {
            response.sendError(HttpStatus.NOT_FOUND.value());
        }
    
    	//...
    }


2.3现在返回404。



    curl localhost:8080/books/5
    
    {
    	"timestamp":"2019-02-27T04:21:17.740+0000",
    	"status":404,
    	"error":"Not Found",
    	"message":"Book id not found : 5",
    	"path":"/books/5"
    }


2.4此外，我们可以自定义整个JSON错误响应：

CustomErrorResponse.java

    package com.jsdiff.error;
    
    import com.fasterxml.jackson.annotation.JsonFormat;
    
    import java.time.LocalDateTime;
    
    public class CustomErrorResponse {
    
        @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd hh:mm:ss")
        private LocalDateTime timestamp;
        private int status;
        private String error;
    
        //...getters setters
    }


CustomGlobalExceptionHandler.java

    package com.jsdiff.error;
    
    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.web.bind.annotation.ControllerAdvice;
    import org.springframework.web.bind.annotation.ExceptionHandler;
    import org.springframework.web.context.request.WebRequest;
    import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;
    
    import java.time.LocalDateTime;
    
    @ControllerAdvice
    public class CustomGlobalExceptionHandler extends ResponseEntityExceptionHandler {
    
        @ExceptionHandler(BookNotFoundException.class)
        public ResponseEntity<CustomErrorResponse> customHandleNotFound(Exception ex, WebRequest request) {
    
            CustomErrorResponse errors = new CustomErrorResponse();
            errors.setTimestamp(LocalDateTime.now());
            errors.setError(ex.getMessage());
            errors.setStatus(HttpStatus.NOT_FOUND.value());
    
            return new ResponseEntity<>(errors, HttpStatus.NOT_FOUND);
    
        }
    
    	//...
    }




    curl localhost:8080/books/5
    {
    	"timestamp":"2019-02-27 12:40:45",
    	"status":404,
    	"error":"Book id not found : 5"
    }


3\. JSR 303 Validation error
---------------

3.1对于Spring `@valid`验证错误，它将抛出`handleMethodArgumentNotValid`

CustomGlobalExceptionHandler.java

    package com.jsdiff.error;
    
    import org.springframework.http.HttpHeaders;
    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.web.bind.MethodArgumentNotValidException;
    import org.springframework.web.bind.annotation.ControllerAdvice;
    import org.springframework.web.bind.annotation.ExceptionHandler;
    import org.springframework.web.context.request.WebRequest;
    import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;
    
    import javax.servlet.http.HttpServletResponse;
    import javax.validation.ConstraintViolationException;
    import java.io.IOException;
    import java.util.Date;
    import java.util.LinkedHashMap;
    import java.util.List;
    import java.util.Map;
    import java.util.stream.Collectors;
    
    @ControllerAdvice
    public class CustomGlobalExceptionHandler extends ResponseEntityExceptionHandler {
    
        //...
    
        // @Validate For Validating Path Variables and Request Parameters
        @ExceptionHandler(ConstraintViolationException.class)
        public void constraintViolationException(HttpServletResponse response) throws IOException {
            response.sendError(HttpStatus.BAD_REQUEST.value());
        }
    
        // error handle for @Valid
        @Override
        protected ResponseEntity<Object>
        handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
                                     HttpHeaders headers,
                                     HttpStatus status, WebRequest request) {
    
            Map<String, Object> body = new LinkedHashMap<>();
            body.put("timestamp", new Date());
            body.put("status", status.value());
    
            //Get all fields errors
            List<String> errors = ex.getBindingResult()
                    .getFieldErrors()
                    .stream()
                    .map(x -> x.getDefaultMessage())
                    .collect(Collectors.toList());
    
            body.put("errors", errors);
    
            return new ResponseEntity<>(body, headers, status);
    
        }
    
    }


4\. ResponseEntityExceptionHandler
----------------------------------

4.1如果不确定，Spring Boot会抛出什么异常，则在此方法中放置一个断点以进行调试。

ResponseEntityExceptionHandler.java

    package org.springframework.web.servlet.mvc.method.annotation;
    
    //...
    public abstract class ResponseEntityExceptionHandler {
    
    	@ExceptionHandler({
    			HttpRequestMethodNotSupportedException.class,
    			HttpMediaTypeNotSupportedException.class,
    			HttpMediaTypeNotAcceptableException.class,
    			MissingPathVariableException.class,
    			MissingServletRequestParameterException.class,
    			ServletRequestBindingException.class,
    			ConversionNotSupportedException.class,
    			TypeMismatchException.class,
    			HttpMessageNotReadableException.class,
    			HttpMessageNotWritableException.class,
    			MethodArgumentNotValidException.class,
    			MissingServletRequestPartException.class,
    			BindException.class,
    			NoHandlerFoundException.class,
    			AsyncRequestTimeoutException.class
    		})
    	@Nullable
    	public final ResponseEntity<Object> handleException(Exception ex, WebRequest request) throws Exception {
    		HttpHeaders headers = new HttpHeaders();
    
    		if (ex instanceof HttpRequestMethodNotSupportedException) {
    			HttpStatus status = HttpStatus.METHOD_NOT_ALLOWED;
    			return handleHttpRequestMethodNotSupported((HttpRequestMethodNotSupportedException) ex, headers, status, request);
    		}
    		else if (ex instanceof HttpMediaTypeNotSupportedException) {
    			HttpStatus status = HttpStatus.UNSUPPORTED_MEDIA_TYPE;
    			return handleHttpMediaTypeNotSupported((HttpMediaTypeNotSupportedException) ex, headers, status, request);
    		}
    		//...
    	}
    
    	//...
    
    }


5\. DefaultErrorAttributes
--------------------------

5.1要覆盖所有异常的默认JSON错误响应，请创建一个bean并扩展 `DefaultErrorAttributes`

CustomErrorAttributes.java

    package com.jsdiff.error;
    
    import org.springframework.boot.web.servlet.error.DefaultErrorAttributes;
    import org.springframework.stereotype.Component;
    import org.springframework.web.context.request.WebRequest;
    
    import java.text.DateFormat;
    import java.text.SimpleDateFormat;
    import java.util.Date;
    import java.util.Map;
    
    @Component
    public class CustomErrorAttributes extends DefaultErrorAttributes {
    
        private static final DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    
        @Override
        public Map<String, Object> getErrorAttributes(WebRequest webRequest, boolean includeStackTrace) {
    
            // Let Spring handle the error first, we will modify later :)
            Map<String, Object> errorAttributes = super.getErrorAttributes(webRequest, includeStackTrace);
    
            // format & update timestamp
            Object timestamp = errorAttributes.get("timestamp");
            if (timestamp == null) {
                errorAttributes.put("timestamp", dateFormat.format(new Date()));
            } else {
                errorAttributes.put("timestamp", dateFormat.format((Date) timestamp));
            }
    
            // insert a new key
            errorAttributes.put("version", "1.2");
    
            return errorAttributes;
    
        }
    
    }


现在，日期时间已格式化，并且将新字段– `version`添加到JSON错误响应中。

    curl localhost:8080/books/5
    
    {
    	"timestamp":"2019/02/27 13:34:24",
    	"status":404,
    	"error":"Not Found",
    	"message":"Book id not found : 5",
    	"path":"/books/5",
    	"version":"1.2"
    }
    
    curl localhost:8080/abc
    
    {
    	"timestamp":"2019/02/27 13:35:10",
    	"status":404,
    	"error":"Not Found",
    	"message":"No message available",
    	"path":"/abc",
    	"version":"1.2"
    }


参考文献
----

*   [Spring Boot错误处理参考](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#boot-features-error-handling)
*   [DefaultErrorAttributes文档](https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/web/servlet/error/DefaultErrorAttributes.html)
*   [ResponseEntityExceptionHandler](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/servlet/mvc/method/annotation/ResponseEntityExceptionHandler.html)
*   [Spring REST验证示例](https://www.blog.jsdiff.com/spring-boot/spring-rest-validation-example/)
*   [Spring Boot安全功能](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#boot-features-security)
*   [带有引导的Hello Spring Security](https://docs.spring.io/spring-security/site/docs/current/guides/html5/helloworld-boot.html)
*   [维基百科– REST](https://en.wikipedia.org/wiki/Representational_state_transfer)