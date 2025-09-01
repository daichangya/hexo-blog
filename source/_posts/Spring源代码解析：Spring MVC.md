---
title: Spring源代码解析：Spring MVC
id: 784
date: 2024-10-31 22:01:46
author: daichangya
excerpt: "下面我们对Spring MVC框架代码进行分析,对于webApplicationContext的相关分析可以参见以前的文档，我们这里着重分析Spring Web MVC框架的实现.我们从分析DispatcherServlet入手： //这里是对DispatcherServlet的初始化方法，根据名字我们很方面的看到对各个Spring MVC主要元素的初始"
permalink: /archives/20004765/
categories:
 - spring
---

下面我们对Spring MVC框架代码进行分析,对于webApplicationContext的相关分析可以参见以前的文档，我们这里着重分析Spring Web MVC框架的实现.我们从分析DispatcherServlet入手：  

    //这里是对DispatcherServlet的初始化方法，根据名字我们很方面的看到对各个Spring MVC主要元素的初始化
    protected void initFrameworkServlet() throws ServletException, BeansException {
        initMultipartResolver();
        initLocaleResolver();
        initThemeResolver();
        initHandlerMappings();
        initHandlerAdapters();
        initHandlerExceptionResolvers();
        initRequestToViewNameTranslator();
        initViewResolvers();
    }

  
看到注解我们知道，这是DispatcherSerlvet的初始化过程，它是在WebApplicationContext已经存在的情况下进行的，也就意味着在初始化它的时候，IOC容器应该已经工作了，这也是我们在web.xml中配置Spring的时候，需要把DispatcherServlet的 load-on-startup的属性配置为2的原因。  
对于具体的初始化过程，很容易理解，我们拿initHandlerMappings（）来看看：  


    private void initHandlerMappings() throws BeansException {
        if (this.detectAllHandlerMappings) {
             // 这里找到所有在上下文中定义的HandlerMapping,同时把他们排序
             // 因为在同一个上下文中可以有不止一个handlerMapping,所以我们把他们都载入到一个链里进行维护和管理
            Map matchingBeans = BeanFactoryUtils.beansOfTypeIncludingAncestors(
                    getWebApplicationContext(), HandlerMapping.class, true, false);
            if (!matchingBeans.isEmpty()) {
                this.handlerMappings = new ArrayList(matchingBeans.values());
                // 这里通过order属性来对handlerMapping来在list中排序
                Collections.sort(this.handlerMappings, new OrderComparator());
            }
        }
        else {
            try {
                Object hm = getWebApplicationContext().getBean(HANDLER\_MAPPING\_BEAN_NAME, HandlerMapping.class);
                this.handlerMappings = Collections.singletonList(hm);
            }
            catch (NoSuchBeanDefinitionException ex) {
                // Ignore, we'll add a default HandlerMapping later.
            }
        }

        //如果在上下文中没有定义的话，那么我们使用默认的BeanNameUrlHandlerMapping
        if (this.handlerMappings == null) {
            this.handlerMappings = getDefaultStrategies(HandlerMapping.class);
        ........
        }
    }

  
怎样获得上下文环境，可以参见我们前面的对IOC容器在web环境中加载的分析。 DispatcherServlet把定义了的所有HandlerMapping都加载了放在一个List里待以后进行使用,这个链的每一个元素都是一个handlerMapping的配置，而一般每一个handlerMapping可以持有一系列从URL请求到 Spring Controller的映射，比如SimpleUrl  
HandlerMaaping中就定义了一个map来持有这一系列的映射关系。  
DisptcherServlet通过HandlerMapping使得Web应用程序确定一个执行路径，就像我们在HanderMapping中看到的那样，HandlerMapping只是一个借口：  

public interface HandlerMapping {
  public static final String PATH\_WITHIN\_HANDLER\_MAPPING\_ATTRIBUTE =
                    Conventions.getQualifiedAttributeName(HandlerMapping.class, "pathWithinHandlerMapping");
      //实际上维护一个HandlerExecutionChain,这是典型的Command的模式的使用，这个执行链里面维护handler和拦截器
    HandlerExecutionChain getHandler(HttpServletRequest request) throws Exception;
}

  
他的具体实现只需要实现一个接口方法，而这个接口方法返回的是一个HandlerExecutionChain,实际上就是一个执行链，就像在Command模式描述的那样，这个类很简单，就是一个持有一个Interceptor链和一个Controller：  


public class HandlerExecutionChain {

    private Object handler;

    private HandlerInterceptor\[\] interceptors;
   
    ........
}

  
而这些Handler和Interceptor需要我们定义HandlerMapping的时候配置好，比如对具体的 SimpleURLHandlerMapping,他要做的就是根据URL映射的方式注册Handler和Interceptor，自己维护一个放映映射的handlerMap，当需要匹配Http请求的时候需要使用这个表里的信息来得到执行链。这个注册的过程在IOC容器初始化 SimpleUrlHandlerMapping的时候就被完成了，这样以后的解析才可以用到map里的映射信息，这里的信息和bean文件的信息是等价的，下面是具体的注册过程：  

    protected void registerHandlers(Map urlMap) throws BeansException {
        if (urlMap.isEmpty()) {
            logger.warn("Neither 'urlMap' nor 'mappings' set on SimpleUrlHandlerMapping");
        }
        else {
            //这里迭代在SimpleUrlHandlerMapping中定义的所有映射元素
            Iterator it = urlMap.keySet().iterator();
            while (it.hasNext()) {
                //这里取得配置的url
                String url = (String) it.next();
                //这里根据url在bean定义中取得对应的handler
                Object handler = urlMap.get(url);
                // Prepend with slash if not already present.
                if (!url.startsWith("/")) {
                    url = "/" + url;
                }
                //这里调用AbstractHandlerMapping中的注册过程
                registerHandler(url, handler);
            }
        }
    }

  
在AbstractMappingHandler中的注册代码：  


    protected void registerHandler(String urlPath, Object handler) throws BeansException, IllegalStateException {
        //试图从handlerMap中取handler,看看是否已经存在同样的Url映射关系
        Object mappedHandler = this.handlerMap.get(urlPath);
        if (mappedHandler != null) {
        ........
        }

        //如果是直接用bean名做映射那就直接从容器中取handler
        if (!this.lazyInitHandlers && handler instanceof String) {
            String handlerName = (String) handler;
            if (getApplicationContext().isSingleton(handlerName)) {
                handler = getApplicationContext().getBean(handlerName);
            }
        }
        //或者使用默认的handler.
        if (urlPath.equals("/*")) {
            setDefaultHandler(handler);
        }
        else {
       //把url和handler的对应关系放到handlerMap中去
            this.handlerMap.put(urlPath, handler);
            ........
        }
    }

  
handlerMap是持有的一个HashMap,里面就保存了具体的映射信息：  

    private final Map handlerMap = new HashMap();

  
而SimpleUrlHandlerMapping对接口HandlerMapping的实现是这样的，这个getHandler根据在初始化的时候就得到的映射表来生成DispatcherServlet需要的执行链  

    public final HandlerExecutionChain getHandler(HttpServletRequest request) throws Exception {
        //这里根据request中的参数得到其对应的handler,具体处理在AbstractUrlHandlerMapping中
        Object handler = getHandlerInternal(request);
        //如果找不到对应的，就使用缺省的handler
        if (handler == null) {
            handler = this.defaultHandler;
        }
        //如果缺省的也没有，那就没办法了
        if (handler == null) {
            return null;
        }
        // 如果handler不是一个具体的handler,那我们还要到上下文中取
        if (handler instanceof String) {
            String handlerName = (String) handler;
            handler = getApplicationContext().getBean(handlerName);
        }
        //生成一个HandlerExecutionChain,其中放了我们匹配上的handler和定义好的拦截器，就像我们在HandlerExecutionChain中看到的那样，它持有一个handler和一个拦截器组。
        return new HandlerExecutionChain(handler, this.adaptedInterceptors);
    }

  
我们看看具体的handler查找过程：  

    protected Object getHandlerInternal(HttpServletRequest request) throws Exception {
        //这里的HTTP Request传进来的参数进行分析，得到具体的路径信息。
        String lookupPath = this.urlPathHelper.getLookupPathForRequest(request);
        .......//下面是根据请求信息的查找
        return lookupHandler(lookupPath, request);
    }

    protected Object lookupHandler(String urlPath, HttpServletRequest request) {
        // 如果能够直接能在SimpleUrlHandlerMapping的映射表中找到，那最好。
        Object handler = this.handlerMap.get(urlPath);
        if (handler == null) {
            // 这里使用模式来对map中的所有handler进行匹配，调用了Jre中的Matcher类来完成匹配处理。
            String bestPathMatch = null;
            for (Iterator it = this.handlerMap.keySet().iterator(); it.hasNext();) {
                String registeredPath = (String) it.next();
                if (this.pathMatcher.match(registeredPath, urlPath) &&
                                (bestPathMatch == null || bestPathMatch.length() <= registeredPath.length())) {
                    //这里根据匹配路径找到最象的一个
                    handler = this.handlerMap.get(registeredPath);
                    bestPathMatch = registeredPath;
                }
            }

            if (handler != null) {
                exposePathWithinMapping(this.pathMatcher.extractPathWithinPattern(bestPathMatch, urlPath), request);
            }
        }
        else {
            exposePathWithinMapping(urlPath, request);
        }
        //
        return handler;
    }

  
我们可以看到，总是在handlerMap这个HashMap中找，当然如果直接找到最好，如果找不到，就看看是不是能通过Match Pattern的模式找，我们一定还记得在配置HnaderMapping的时候是可以通过ANT语法进行配置的，其中的处理就在这里。  
这样可以清楚地看到整个HandlerMapping的初始化过程 - 同时，我们也看到了一个具体的handler映射是怎样被存储和查找的 - 这里生成一个ExecutionChain来储存我们找到的handler和在定义bean的时候定义的Interceptors.  
让我们回到DispatcherServlet，初始化完成以后，实际的对web请求是在doService()方法中处理的，我们知道DispatcherServlet只是一个普通的Servlet:  

    protected void doService(HttpServletRequest request, HttpServletResponse response) throws Exception {
        .......
        //这里把属性信息进行保存
        Map attributesSnapshot = null;
        if (WebUtils.isIncludeRequest(request)) {
            logger.debug("Taking snapshot of request attributes before include");
            attributesSnapshot = new HashMap();
            Enumeration attrNames = request.getAttributeNames();
            while (attrNames.hasMoreElements()) {
                String attrName = (String) attrNames.nextElement();
                if (this.cleanupAfterInclude || attrName.startsWith(DispatcherServlet.class.getName())) {
                    attributesSnapshot.put(attrName, request.getAttribute(attrName));
                }
            }
        }

        // Make framework objects available to handlers and view objects.
        request.setAttribute(WEB\_APPLICATION\_CONTEXT_ATTRIBUTE, getWebApplicationContext());
        request.setAttribute(LOCALE\_RESOLVER\_ATTRIBUTE, this.localeResolver);
        request.setAttribute(THEME\_RESOLVER\_ATTRIBUTE, this.themeResolver);
        request.setAttribute(THEME\_SOURCE\_ATTRIBUTE, getThemeSource());

        try {
             //这里使实际的处理入口
            doDispatch(request, response);
        }
        finally {
            // Restore the original attribute snapshot, in case of an include.
            if (attributesSnapshot != null) {
                restoreAttributesAfterInclude(request, attributesSnapshot);
            }
        }
    }

  
我们看到，对于请求的处理实际上是让doDispatch()来完成的 - 这个方法很长，但是过程很简单明了：  




    protected void doDispatch(final HttpServletRequest request, HttpServletResponse response) throws Exception {
        HttpServletRequest processedRequest = request;
        //这是从handlerMapping中得到的执行链
        HandlerExecutionChain mappedHandler = null;
        int interceptorIndex = -1;
       
        ........
        try {
            //我们熟悉的ModelAndView开始出现了。
            ModelAndView mv = null;
            try {
                processedRequest = checkMultipart(request);

                // 这是我们得到handler的过程
                mappedHandler = getHandler(processedRequest, false);
                if (mappedHandler == null || mappedHandler.getHandler() == null) {
                    noHandlerFound(processedRequest, response);
                    return;
                }

                // 这里取出执行链中的Interceptor进行前处理
                if (mappedHandler.getInterceptors() != null) {
                    for (int i = 0; i < mappedHandler.getInterceptors().length; i++) {
                        HandlerInterceptor interceptor = mappedHandler.getInterceptors()\[i\];
                        if (!interceptor.preHandle(processedRequest, response, mappedHandler.getHandler())) {
                            triggerAfterCompletion(mappedHandler, interceptorIndex, processedRequest, response, null);
                            return;
                        }
                        interceptorIndex = i;
                    }
                }

                //在执行handler之前，用HandlerAdapter先检查一下handler的合法性：是不是按Spring的要求编写的。
                HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());
                mv = ha.handle(processedRequest, response, mappedHandler.getHandler());

                // 这里取出执行链中的Interceptor进行后处理
                if (mappedHandler.getInterceptors() != null) {
                    for (int i = mappedHandler.getInterceptors().length - 1; i >= 0; i--) {
                        HandlerInterceptor interceptor = mappedHandler.getInterceptors()\[i\];
                        interceptor.postHandle(processedRequest, response, mappedHandler.getHandler(), mv);
                    }
                }
            }
           
            ........

            // Did the handler return a view to render?
            //这里对视图生成进行处理
            if (mv != null && !mv.wasCleared()) {
                render(mv, processedRequest, response);
            }
            .......
    }

  
我们很清楚的看到和MVC框架紧密相关的代码,比如如何得到和http请求相对应的执行链，怎样执行执行链和怎样把模型数据展现到视图中去。  
先看怎样取得Command对象，对我们来说就是Handler - 下面是getHandler的代码：  


    protected HandlerExecutionChain getHandler(HttpServletRequest request, boolean cache) throws Exception {
      //在ServletContext取得执行链 - 实际上第一次得到它的时候，我们把它放在ServletContext进行了缓存。
      HandlerExecutionChain handler =
                (HandlerExecutionChain) request.getAttribute(HANDLER\_EXECUTION\_CHAIN_ATTRIBUTE);
        if (handler != null) {
            if (!cache) {
                request.removeAttribute(HANDLER\_EXECUTION\_CHAIN_ATTRIBUTE);
            }
            return handler;
        }
        //这里的迭代器迭代的时在initHandlerMapping中载入的上下文所有的HandlerMapping
        Iterator it = this.handlerMappings.iterator();
        while (it.hasNext()) {
            HandlerMapping hm = (HandlerMapping) it.next();
            .......
            //这里是实际取得handler的过程,在每个HandlerMapping中建立的映射表进行检索得到请求对应的handler
            handler = hm.getHandler(request);

            //然后把handler存到ServletContext中去进行缓存
            if (handler != null) {
                if (cache) {
                    request.setAttribute(HANDLER\_EXECUTION\_CHAIN_ATTRIBUTE, handler);
                }
                return handler;
            }
        }
        return null;
    }

  
如果在ServletContext中可以取得handler则直接返回，实际上这个handler是缓冲了上次处理的结果 - 总要有第一次把这个handler放到ServletContext中去：  
如果在ServletContext中找不到handler,那就通过持有的handlerMapping生成一个，我们看到它会迭代当前持有的所有的 handlerMapping,因为可以定义不止一个，他们在定义的时候也可以指定顺序，直到找到第一个，然后返回。先找到一个 handlerMapping,然后通过这个handlerMapping返回一个执行链，里面包含了最终的Handler和我们定义的一连串的 Interceptor。具体的我们可以参考上面的SimpleUrlHandlerMapping的代码分析知道getHandler是怎样得到一个 HandlerExecutionChain的。  
得到HandlerExecutionChain以后，我们通过HandlerAdapter对这个Handler的合法性进行判断：  

    protected HandlerAdapter getHandlerAdapter(Object handler) throws ServletException {
        Iterator it = this.handlerAdapters.iterator();
        while (it.hasNext()) {
            //同样对持有的所有adapter进行匹配
            HandlerAdapter ha = (HandlerAdapter) it.next();
            if (ha.supports(handler)) {
                return ha;
            }
        }
        ........
    }

  
通过判断，我们知道这个handler是不是一个Controller接口的实现，比如对于具体的HandlerAdapter - SimpleControllerHandlerAdapter:  


public class SimpleControllerHandlerAdapter implements HandlerAdapter {
   
    public boolean supports(Object handler) {
        return (handler instanceof Controller);
    }
    .......
}

  
简单的判断一下handler是不是实现了Controller接口。这也体现了一种对配置文件进行验证的机制。  
让我们再回到DispatcherServlet看到代码：  

                mv = ha.handle(processedRequest, response, mappedHandler.getHandler());

  
这个就是对handle的具体调用！相当于Command模式里的Command.execute();理所当然的返回一个ModelAndView，下面就是一个对View进行处理的过程：  

            if (mv != null && !mv.wasCleared()) {
                render(mv, processedRequest, response);
            }

  
调用的是render方法：  


   protected void render(ModelAndView mv, HttpServletRequest request, HttpServletResponse response)
            throws Exception {response.setLocale(locale);

        View view = null;
        //这里把默认的视图放到ModelAndView中去。
        if (!mv.hasView()) {
            mv.setViewName(getDefaultViewName(request));
        }

        if (mv.isReference()) {
            // 这里对视图名字进行解析
            view = resolveViewName(mv.getViewName(), mv.getModelInternal(), locale, request);
        .......
        }
        else {
            // 有可能在ModelAndView里已经直接包含了View对象，那我们就直接使用。
            view = mv.getView();
        ........
        }

        //得到具体的View对象以后，我们用它来生成视图。
        view.render(mv.getModelInternal(), request, response);
    }

  
从整个过程我们看到先在ModelAndView中寻找视图的逻辑名，如果找不到那就使用缺省的视图，如果能够找到视图的名字，那就对他进行解析得到实际的需要使用的视图对象。还有一种可能就是在ModelAndView中已经包含了实际的视图对象，这个视图对象是可以直接使用的。  
不管怎样，得到一个视图对象以后，通过调用视图对象的render来完成数据的显示过程，我们可以看看具体的JstlView是怎样实现的，我们在JstlView的抽象父类 AbstractView中找到render方法：  


    public void render(Map model, HttpServletRequest request, HttpServletResponse response) throws Exception {
        ......
        // 这里把所有的相关信息都收集到一个Map里
        Map mergedModel = new HashMap(this.staticAttributes.size() + (model != null ? model.size() : 0));
        mergedModel.putAll(this.staticAttributes);
        if (model != null) {
            mergedModel.putAll(model);
        }

        // Expose RequestContext?
        if (this.requestContextAttribute != null) {
            mergedModel.put(this.requestContextAttribute, createRequestContext(request, mergedModel));
        }
        //这是实际的展现模型数据到视图的调用。
        renderMergedOutputModel(mergedModel, request, response);
    }

  
注解写的很清楚了，先把所有的数据模型进行整合放到一个Map - mergedModel里，然后调用renderMergedOutputModel();这个renderMergedOutputModel是一个模板方法，他的实现在InternalResourceView也就是JstlView的父类：  

     protected void renderMergedOutputModel(
            Map model, HttpServletRequest request, HttpServletResponse response) throws Exception {

        // Expose the model object as request attributes.
        exposeModelAsRequestAttributes(model, request);

        // Expose helpers as request attributes, if any.
        exposeHelpers(request);

        // 这里得到InternalResource定义的内部资源路径。
        String dispatcherPath = prepareForRendering(request, response);

        //这里把请求转发到前面得到的内部资源路径中去。
        RequestDispatcher rd = request.getRequestDispatcher(dispatcherPath);
        if (rd == null) {
            throw new ServletException(
                    "Could not get RequestDispatcher for \[" + getUrl() + "\]: check that this file exists within your WAR");
        }
        .......
    }

  
首先对模型数据进行处理，exposeModelAsRequestAttributes是在AbstractView中实现的，这个方法把 ModelAndView中的模型数据和其他request数据统统放到ServletContext当中去，这样整个模型数据就通过 ServletContext暴露并得到共享使用了：  

  protected void exposeModelAsRequestAttributes(Map model, HttpServletRequest request) throws Exception {
        Iterator it = model.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry entry = (Map.Entry) it.next();
            ..........
            String modelName = (String) entry.getKey();
            Object modelValue = entry.getValue();
            if (modelValue != null) {
                request.setAttribute(modelName, modelValue);
            ...........
            }
            else {
                request.removeAttribute(modelName);
                .......
            }
        }
    }

  
让我们回到数据处理部分的exposeHelper();这是一个模板方法，其实现在JstlView中实现：  

public class JstlView extends InternalResourceView {

    private MessageSource jstlAwareMessageSource;


    protected void initApplicationContext() {
        super.initApplicationContext();
        this.jstlAwareMessageSource =
                JstlUtils.getJstlAwareMessageSource(getServletContext(), getApplicationContext());
    }

    protected void exposeHelpers(HttpServletRequest request) throws Exception {
        JstlUtils.exposeLocalizationContext(request, this.jstlAwareMessageSource);
    }

}

  
在JstlUtils中包含了对于其他而言jstl特殊的数据处理和设置。  
过程是不是很长？我们现在在哪里了？呵呵，我们刚刚完成的事MVC中View的render，对于InternalResourceView的render 过程比较简单只是完成一个资源的重定向处理。需要做的就是得到实际view的internalResource路径，然后转发到那个资源中去。怎样得到资源的路径呢通过调用：  


     protected String prepareForRendering(HttpServletRequest request, HttpServletResponse response)
            throws Exception {

        return getUrl();
    }

  
那这个url在哪里生成呢？我们在View相关的代码中没有找到，实际上，他在ViewRosolve的时候就生成了，在UrlBasedViewResolver中：  

    protected AbstractUrlBasedView buildView(String viewName) throws Exception {
        AbstractUrlBasedView view = (AbstractUrlBasedView) BeanUtils.instantiateClass(getViewClass());
        view.setUrl(getPrefix() + viewName + getSuffix());
        String contentType = getContentType();
        if (contentType != null) {
            view.setContentType(contentType);
        }
        view.setRequestContextAttribute(getRequestContextAttribute());
        view.setAttributesMap(getAttributesMap());
        return view;
    }

  
这里是生成View的地方，自然也把生成的url和其他一些和view相关的属性也配置好了。  
那这个ViewResolve是什么时候被调用的呢？哈哈，我们这样又要回到DispatcherServlet中去看看究竟，在DispatcherServlet中：  


    protected void render(ModelAndView mv, HttpServletRequest request, HttpServletResponse response)
            throws Exception {

        ........
        View view = null;

        // 这里设置视图名为默认的名字
        if (!mv.hasView()) {
            mv.setViewName(getDefaultViewName(request));
        }

        if (mv.isReference()) {
            //这里对视图名进行解析，在解析的过程中根据需要生成实际需要的视图对象。
            view = resolveViewName(mv.getViewName(), mv.getModelInternal(), locale, request);
           ..........
        }
       ......
   }

  
下面是对视图名进行解析的具体过程：  

protected View resolveViewName(String viewName, Map model, Locale locale, HttpServletRequest request)
            throws Exception {
         //我们有可能不止一个视图解析器
        for (Iterator it = this.viewResolvers.iterator(); it.hasNext();) {
            ViewResolver viewResolver = (ViewResolver) it.next();
            //这里是视图解析器进行解析并生成视图的过程。
            View view = viewResolver.resolveViewName(viewName, locale);
            if (view != null) {
                return view;
            }
        }
        return null;
    }

  
这里调用具体的ViewResolver对视图的名字进行解析 - 除了单纯的解析之外，它还根据我们的要求生成了我们实际需要的视图对象。具体的viewResolver在bean定义文件中进行定义同时在 initViewResolver()方法中被初始化到viewResolver变量中，我们看看具体的 InternalResourceViewResolver是怎样对视图名进行处理的并生成V视图对象的：对resolveViewName的调用模板在 AbstractCachingViewResolver中,  

    public View resolveViewName(String viewName, Locale locale) throws Exception {
        //如果没有打开缓存设置，那创建需要的视图
        if (!isCache()) {
            logger.warn("View caching is SWITCHED OFF -- DEVELOPMENT SETTING ONLY: This can severely impair performance");
            return createView(viewName, locale);
        }
        else {
            Object cacheKey = getCacheKey(viewName, locale);
            // No synchronization, as we can live with occasional double caching.
            synchronized (this.viewCache) {
                //这里查找缓存里的视图对象
                View view = (View) this.viewCache.get(cacheKey);
                if (view == null) {
                    //如果在缓存中没有找到，创建一个并把创建的放到缓存中去
                    view = createView(viewName, locale);
                    this.viewCache.put(cacheKey, view);
                ........
                }
                return view;
            }
        }
    }

  
关于这些createView(),loadView(),buildView()的关系，我们看看Eclipse里的call hiearchy  
然后我们回到view.render中完成数据的最终对httpResponse的写入，比如在AbstractExcelView中的实现:  

    protected final void renderMergedOutputModel(
            Map model, HttpServletRequest request, HttpServletResponse response) throws Exception {
        .........
        // response.setContentLength(workbook.getBytes().length);
        response.setContentType(getContentType());
        ServletOutputStream out = response.getOutputStream();
        workbook.write(out);
        out.flush();
    }

  
这样就和我们前面的分析一致起来了:DispatcherServlet在解析视图名的时候就根据要求生成了视图对象,包括在InternalResourceView中需要使用的url和其他各种和HTTP response相关的属性都会写保持在生成的视图对象中，然后就直接调用视图对象的render来完成数据的展示。  
这就是整个Spring Web MVC框架的大致流程，整个MVC流程由DispatcherServlet来控制。MVC的关键过程包括：  
配置到handler的映射关系和怎样根据请求参数得到对应的handler,在Spring中，这是由handlerMapping通过执行链来完成的，而具体的映射关系我们在bean定义文件中定义并在HandlerMapping载入上下文的时候就被配置好了。然后 DispatcherServlet调用HandlerMapping来得到对应的执行链，最后通过视图来展现模型数据，但我们要注意的是视图对象是在解析视图名的时候生成配置好的。这些作为核心类的HanderMapping,ViewResolver,View,Handler的紧密协作实现了MVC的功能。  
  