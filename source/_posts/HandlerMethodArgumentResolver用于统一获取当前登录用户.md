---
title: HandlerMethodArgumentResolver用于统一获取当前登录用户
id: 1578
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/handlermethodargumentresolver%E7%94%A8%E4%BA%8E%E7%BB%9F%E4%B8%80%E8%8E%B7%E5%8F%96%E5%BD%93%E5%89%8D%E7%99%BB%E5%BD%95%E7%94%A8%E6%88%B7/
categories:
 - spring-cloud
---

**目录**

[一、最原始直接](#t0)

[二、AOP](#t1)

[三、拦截器+方法参数解析器](#t2)

[ 3.1 自定义权限拦截器](#t3)

[ 3.2 自定义参数注解](#t4)

[ 3.3 自定义方法参数解析器](#t5)

[ 3.4 配置MVC](#t6)

* * *

*   环境：SpringBoot 2.0.4.RELEASE
*   需求：很多Controller方法，刚进来要先获取当前登录用户的信息，以便做后续的用户相关操作。
*   准备工作：前端每次请求都传token，后端封装一方法tokenUtils.getUserByToken(token)，根据token解析得到currentUserInfo。

这是一个常见的业务需求，为实现这个需求，有以下几种解决方案：

## 一、最原始直接

即，每个Controller开始，先调用tokenUtils.getUserByToken(token)，不够优雅。

## 二、AOP

AOP可以解决很多切面类问题，将currentUser放到request里；比起拦截器稍重。

## 三、拦截器+方法参数解析器

使用**mvc拦截器HandlerInterceptor**+**方法参数解析器HandlerMethodArgumentResolver**最合适。

SpringMVC提供了mvc拦截器**HandlerInterceptor**，包含以下3个方法：

*   preHandle
*   postHandle
*   afterCompletion

**HandlerInterceptor**经常被用来解决拦截事件，如用户鉴权等。另外，Spring也向我们提供了多种解析器Resolver，如用来统一处理异常的**HandlerExceptionResolver**，以及今天的主角**HandlerMethodArgumentResolver**。**HandlerMethodArgumentResolver**是用来处理方法参数的解析器，包含以下2个方法：

*   supportsParameter（满足某种要求，返回true，方可进入resolveArgument做参数处理）
*   resolveArgument

 知识储备已到位，接下来着手实现，主要分为三步走：

1.  自定义权限拦截器AuthenticationInterceptor拦截所有request请求，并将token解析为currentUser，最终放到request中；
2.  自定义参数注解@CurrentUser，添加至controller的方法参数user之上；
3.  自定义方法参数解析器CurrentUserMethodArgumentResolver，取出request中的user，并赋值给添加了@CurrentUser注解的参数user。

###  3.1 自定义权限拦截器

自定义权限拦截器**AuthenticationInterceptor**，需实现**HandlerInterceptor。**在preHandle中调用tokenUtils.getUserByToken(token)，获取到当前用户，最后塞进request中，如下：

```java
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
 
import edp.core.utils.TokenUtils;
import edp.core.consts.Consts;
import edp.davinci.model.User;
 
public class AuthenticationInterceptor implements HandlerInterceptor {
 
    @Autowired
    private TokenUtils tokenUtils;
 
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String token = request.getHeader("Authorization");
        User user = tokenUtils.getUserByToken(token);
        request.setAttribute(Consts.CURRENT_USER, user);
        return true;
    }
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
    }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
    }
}
```

###  3.2 自定义参数注解

自定义方法参数上使用的注解@CurrentUser，代表被它注解过的参数的值都需要由方法参数解析器**CurrentUserMethodArgumentResolver**来“注入”，如下：

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
 
/**
 * 自定义 当前用户 注解
 * 注解 参数
 * 此注解在验证token通过后，获取当前token包含用户
 */
@Target({ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
public @interface CurrentUser {
}
```

给各Controller类中RequestMapping方法的参数添加此注解，如下：

```java
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import edp.davinci.core.common.Constants;
import edp.core.annotation.CurrentUser;
import javax.servlet.http.HttpServletRequest;
 
@RestController
@RequestMapping(value = Constants.BASE_API_PATH + "/download")
public class DownloadController {
 
    @GetMapping(value = "/page", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public ResponseEntity getDownloadRecordPage(@CurrentUser User user, HttpServletRequest request) {
        ...
    }
}
```

###  3.3 自定义方法参数解析器

自定义方法参数解析器**CurrentUserMethodArgumentResolver**，需实现**HandlerMethodArgumentResolver**。

```java
import org.springframework.core.MethodParameter;
import org.springframework.web.bind.support.WebDataBinderFactory;
import org.springframework.web.context.request.NativeWebRequest;
import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.method.support.ModelAndViewContainer;
 
import edp.core.annotation.CurrentUser;
import edp.core.consts.Consts;
import edp.davinci.model.User;
 
/**
 * @CurrentUser 注解 解析器
 */
public class CurrentUserMethodArgumentResolver implements HandlerMethodArgumentResolver {
    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        return parameter.getParameterType().isAssignableFrom(User.class)
                && parameter.hasParameterAnnotation(CurrentUser.class);
    }
 
    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer, NativeWebRequest webRequest, WebDataBinderFactory binderFactory) {
        return  (User) webRequest.getAttribute(Consts.CURRENT_USER, RequestAttributes.SCOPE_REQUEST);
    }
}
```

As we all know，拦截器定义好以后，在SpringMVC项目中，需要去SpringMVC的配置文件springmvc.xml添加该拦截器；但是在SpringBoot中，省去了很多配置文件，取而代之的是被注解**@Configuration**标识的配置类，SpringMVC配置文件对应的配置类需继承**WebMvcConfigurationSupport**。同理，解析器定义好以后，也需被添加到SpringMVC的配置文件或配置类中。最后，额外的一步，配置mvc。

###  3.4 配置MVC

定义MVC配置类，需继承**WebMvcConfigurationSupport**。分别在addInterceptors和addArgumentResolvers方法中，添加自定义的拦截器和参数解析器，如下：

```java
import static edp.core.consts.Consts.EMPTY;
 
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
 
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport;
 
import com.alibaba.fastjson.serializer.SerializerFeature;
import com.alibaba.fastjson.serializer.ValueFilter;
import com.alibaba.fastjson.support.config.FastJsonConfig;
import com.alibaba.fastjson.support.spring.FastJsonHttpMessageConverter;
 
import edp.davinci.core.common.Constants;
import edp.davinci.core.inteceptor.AuthenticationInterceptor;
import edp.davinci.core.inteceptor.CurrentUserMethodArgumentResolver;
 
 
@Configuration
public class WebMvcConfig extends WebMvcConfigurationSupport {
 
    @Value("${file.userfiles-path}")
    private String filePath;
 
    /**
     * 登录校验拦截器
     *
     * @return
     */
    @Bean
    public AuthenticationInterceptor loginRequiredInterceptor() {
        return new AuthenticationInterceptor();
    }
 
    /**
     * CurrentUser 注解参数解析器
     *
     * @return
     */
    @Bean
    public CurrentUserMethodArgumentResolver currentUserMethodArgumentResolver() {
        return new CurrentUserMethodArgumentResolver();
    }
 
    /**
     * 参数解析器
     *
     * @param argumentResolvers
     */
    @Override
    protected void addArgumentResolvers(List<HandlerMethodArgumentResolver> argumentResolvers) {
        argumentResolvers.add(currentUserMethodArgumentResolver());
        super.addArgumentResolvers(argumentResolvers);
    }
 
    @Override
    protected void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loginRequiredInterceptor())
                .addPathPatterns(Constants.BASE_API_PATH + "/**")
                .excludePathPatterns(Constants.BASE_API_PATH + "/login");
        super.addInterceptors(registry);
    }
 
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/**")
                .addResourceLocations("classpath:/META-INF/resources/")
                .addResourceLocations("classpath:/static/page/")
                .addResourceLocations("classpath:/static/templates/")
                .addResourceLocations("file:" + filePath);
    }
 
    @Override
    protected void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        FastJsonHttpMessageConverter fastConverter = new FastJsonHttpMessageConverter();
        FastJsonConfig fastJsonConfig = new FastJsonConfig();
        fastJsonConfig.setSerializerFeatures(SerializerFeature.QuoteFieldNames,
                SerializerFeature.WriteEnumUsingToString,
                SerializerFeature.WriteMapNullValue,
                SerializerFeature.WriteDateUseDateFormat,
                SerializerFeature.DisableCircularReferenceDetect);
        fastJsonConfig.setSerializeFilters((ValueFilter) (o, s, source) -> {
            if (null != source && (source instanceof Long || source instanceof BigInteger) && source.toString().length() > 15) {
                return source.toString();
            } else {
                return null == source ? EMPTY : source;
            }
        });
 
        //处理中文乱码问题
        List<MediaType> fastMediaTypes = new ArrayList<>();
        fastMediaTypes.add(MediaType.APPLICATION_JSON_UTF8);
        fastConverter.setSupportedMediaTypes(fastMediaTypes);
        fastConverter.setFastJsonConfig(fastJsonConfig);
        converters.add(fastConverter);
    }
}
```

以上。