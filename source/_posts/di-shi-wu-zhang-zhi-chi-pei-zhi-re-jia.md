---
title: 第十五章：支持配置热加载和自动部署-MiniTomcat
id: feed602b-4dce-4083-87e0-57f87e83c31a
date: 2024-11-23 16:24:12
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat.jpg
excerpt: 功能目标： 支持热部署（Hot Deployment）功能，能够在不重启服务器的情况下加载新的 Web 应用。 监控应用目录的变化，当检测到新的
  Web 应用时，自动加载该应用的 Servlet 和资源。 支持 web.xml 的重新加载和应用更新。 实现内容： 实现一个 目录监控机制，当检测到应用
permalink: /archives/di-shi-wu-zhang-zhi-chi-pei-zhi-re-jia/
categories:
- minitomcat
---

### 功能目标：

+   **支持热部署（Hot Deployment）功能**，能够在不重启服务器的情况下加载新的 Web 应用。
    
+   监控应用目录的变化，当检测到新的 Web 应用时，自动加载该应用的 Servlet 和资源。
    
+   支持 `web.xml` 的重新加载和应用更新。
    

### 实现内容：

+   实现一个 **目录监控机制**，当检测到应用目录中的变化（如新增应用、修改或删除文件）时，自动加载或卸载应用。
    
+   支持 **web.xml 文件的重新加载**，使得配置更新后能自动生效。
    
+   提供一个简单的 **文件监控线程**，持续检测应用目录中的变化，并在变化发生时触发相关的加载或卸载操作。
    

* * *

### 15.1 热部署的设计

热部署的关键是动态地检测文件系统的变化，并自动加载或卸载 Web 应用。为此，我们可以借助 **Java NIO** 提供的 **WatchService**，实现对应用目录中文件的监控。

#### 15.1.1 设计思路

1.  **文件监控**：使用 `WatchService` 监控应用目录中的文件变化。包括新增、修改或删除操作。
    
2.  **自动加载应用**：当监控到新的应用目录或文件发生变化时，自动加载或更新应用的 Servlet 和配置。
    
3.  **重新加载配置**：当 `web.xml` 文件发生变化时，重新加载该配置文件，并应用新的路由和初始化参数。
    

#### 15.1.2 使用 `WatchService` 实现文件监控

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.core.StandardContext;

import java.net.URL;
import java.nio.file.*;

import static com.daicy.minitomcat.HttpServer.CONF_PATH;

public class HotDeployment {

//    private static final String APP_BASE_PATH = "/path/to/apps";  // Web 应用目录

    public void startDeploymentMonitor() {
        try {


            URL url = getClass().getResource(CONF_PATH);
            Path path = Paths.get(url.getPath());
            WatchService watchService = FileSystems.getDefault().newWatchService();

            // 注册监控事件：创建、修改和删除
            path.register(watchService, StandardWatchEventKinds.ENTRY_CREATE,
                    StandardWatchEventKinds.ENTRY_MODIFY,
                    StandardWatchEventKinds.ENTRY_DELETE);

            System.out.println("Monitoring directory for changes: " + path.toString());

            // 监控目录变化
            while (true) {
                WatchKey key;
                try {
                    key = watchService.take();  // 等待文件变化事件
                } catch (InterruptedException e) {
                    System.out.println("Monitoring interrupted");
                    return;
                }

                // 处理监控到的事件
                for (WatchEvent<?> event : key.pollEvents()) {
                    WatchEvent.Kind<?> kind = event.kind();
                    Path filePath = (Path) event.context();
                    System.out.println("Event detected: " + kind + " on file: " + filePath);

                    // 根据事件类型进行相应处理
                    if (kind == StandardWatchEventKinds.ENTRY_CREATE) {
                        // 新应用被添加，加载该应用
                        deployApplication(filePath);
                    } else if (kind == StandardWatchEventKinds.ENTRY_MODIFY) {
                        // 修改了应用，重新加载或更新
                        reloadApplication(filePath);
                    } else if (kind == StandardWatchEventKinds.ENTRY_DELETE) {
                        // 应用被删除，卸载应用
                        undeployApplication(filePath);
                    }
                }

                // 重置 key 以继续监控
                boolean valid = key.reset();
                if (!valid) {
                    break;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 部署新应用
    private void deployApplication(Path filePath) {
        System.out.println("Deploying new application: " + filePath);
        // 实际应用加载逻辑
        // 例如加载 Servlet、web.xml 配置等
    }

    // 重新加载应用
    private void reloadApplication(Path filePath) {
        System.out.println("Reloading application: " + filePath);
        // 重新加载应用的 Servlet 和配置
        try {
            HttpServer.context = new StandardContext("/conf/web.xml");
            HttpServer.context.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 卸载应用
    private void undeployApplication(Path filePath) {
        System.out.println("Undeploying application: " + filePath);
        // 卸载应用，释放资源
    }
}
```

#### 15.1.3 主要方法解析

+   **startDeploymentMonitor**：启动文件监控线程，持续监控应用目录中的变化。
    
+   **deployApplication**：当检测到新应用被创建时，执行部署操作，加载应用。
    
+   **reloadApplication**：当检测到应用被修改时，执行重新加载操作，更新配置或类文件。
    
+   **undeployApplication**：当检测到应用被删除时，执行卸载操作，移除应用及其资源。
    

* * *

### 15.2 web.xml 文件的重新加载

在热部署过程中，`web.xml` 文件的更新是非常重要的一部分。我们需要在 `web.xml` 文件被修改后重新加载它，以使新的配置生效。

#### 15.2.1 实现 web.xml 重新加载

```java
    // 重新加载应用
    private void reloadApplication(Path filePath) {
        System.out.println("Reloading application: " + filePath);
        // 重新加载应用的 Servlet 和配置
        try {
            HttpServer.context = new StandardContext(WEB_XML);
            HttpServer.context.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
```

#### 15.2.2 主要方法解析

+   **reloadApplication**：重新加载 `web.xml` 文件，并解析其中的配置，更新 Servlet 的路由和初始化参数。
    

* * *

### 15.3 集成文件监控与配置热加载

我们将 **HotDeployment** 组件和 **StandardContext** 结合，完成整个热部署过程。

#### 15.3.1 集成示例

```java
package com.daicy.minitomcat;

import com.daicy.minitomcat.core.StandardContext;
import com.daicy.minitomcat.servlet.ServletContextImpl;

import javax.servlet.*;

/**
 * @author 代长亚
 * 一个简单的 HTTP 服务器，用于处理 GET 请求并返回静态文件。
 */
public class HttpServer {
    // 静态文件根目录
    static final String WEB_ROOT = "webroot";

    public static final String CONF_PATH = "/conf";

    public static final String WEB_XML = CONF_PATH+ "/web.xml";

    public static ServletContextImpl servletContext = new ServletContextImpl();

    public static StandardContext context;

    public static HotDeployment hotDeployment = new HotDeployment();

    public static FilterManager filterManager = new FilterManager();

    private static ServletContextListenerManager servletContextListenerManager = new ServletContextListenerManager();

    public static HttpSessionListenerManager sessionListenerManager = new HttpSessionListenerManager();

    public static void main(String[] args) throws Exception {
        Thread daemonThread = new Thread(() -> {
            hotDeployment.startDeploymentMonitor();
        });
        // 将线程设置为守护线程，必须在启动线程之前调用
        daemonThread.setDaemon(true);
        daemonThread.start();

        servletContextListenerManager.addListener(new ServletContextListenerImpl());
        sessionListenerManager.addListener(new HttpSessionListenerImpl());
        // 启动监听器
        servletContextListenerManager.notifyContextInitialized(new ServletContextEvent(servletContext));
        context = new StandardContext(WEB_XML);
        context.start();
        filterManager.addFilter(new LoggingFilter());
        HttpConnector connector = new HttpConnector();
        connector.start();

        // 模拟服务器关闭
        Runtime.getRuntime().addShutdownHook(new Thread(HttpServer::stop));
    }

    public static void stop() {
        try {
            LogManager.getLogger().info("Server stopping...");
            context.stop();
            servletContextListenerManager.notifyContextDestroyed(new ServletContextEvent(servletContext));
            SessionManager.removeSession();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
```

* * *

### 15.4 学习收获

通过实现热加载和自动部署机制，我们学习了以下内容：

1.  **目录监控和事件处理**：我们使用 Java NIO 的 `WatchService` 实现了对文件系统的实时监控，能够及时响应目录中的变化。
    
2.  **热部署与应用更新**：通过监控目录变化，我们实现了在不重启服务器的情况下自动加载、更新或卸载应用。这为现代 Web 容器提供了动态部署的能力。
    
3.  **web.xml 文件的重新加载**：我们实现了 `web.xml` 配置文件的重新加载机制，能够在配置发生变化时自动更新容器的行为。
    

这些实现使得我们的 Web 容器在开发和生产环境中都具有高度的灵活性和动态扩展能力，可以支持快速迭代和应用的持续部署。

项目源代码地址：

https://github.com/daichangya/MiniTomcat/tree/chapter15/mini-tomcat