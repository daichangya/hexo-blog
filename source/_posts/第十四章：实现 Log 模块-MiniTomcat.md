---
title: 第十四章：实现 Log 模块-MiniTomcat
id: 2579552d-b699-447a-8445-96f7df74997a
date: 2024-11-23 16:23:17
author: daichangya
cover: https://images.jsdiff.com/MiniTomcat2.jpg
excerpt: "功能目标： 实现 Log 模块，支持日志记录和日志级别管理。 实现内容： Log 模块：实现一个日志组件，用于记录请求日志、错误日志和系统日志。 日志级别：支持不同的日志级别（INFO、DEBUG、ERROR 等），以便控制日志的详细程度。 实现方式：设计一个简单的 Logger 类，提供不同级别的"
permalink: /archives/di-14-zhang-shi-xian-log-mo-kuai-minitomcat/
categories:
 - minitomcat
---

### 功能目标：

+   实现 **Log 模块**，支持日志记录和日志级别管理。
    

### 实现内容：

+   **Log 模块**：实现一个日志组件，用于记录请求日志、错误日志和系统日志。
    
+   **日志级别**：支持不同的日志级别（INFO、DEBUG、ERROR 等），以便控制日志的详细程度。
    
+   **实现方式**：设计一个简单的 `Logger` 类，提供不同级别的日志输出，并配置输出格式和文件路径。
    

* * *

### 14.1 日志记录的重要性

在 Web 应用开发中，日志记录是非常重要的。日志帮助我们跟踪系统的运行状态，诊断问题，并提供可用的监控信息。常见的日志类型包括：

+   **请求日志**：记录每个 HTTP 请求的相关信息。
    
+   **错误日志**：记录程序异常和错误信息。
    
+   **系统日志**：记录系统级别的信息，如服务启动、停止等事件。
    

为了更高效地记录日志，我们需要将日志分为不同的级别，并根据日志级别来输出不同的日志内容。

* * *

### 14.2 日志级别的设计

常见的日志级别如下：

+   **DEBUG**：最详细的日志，用于调试阶段，记录系统的详细信息。
    
+   **INFO**：常规信息，记录系统的正常操作，如请求处理过程等。
    
+   **WARN**：警告信息，用于记录可能出现问题的地方，但不一定会导致错误。
    
+   **ERROR**：错误信息，用于记录异常或错误，系统无法继续运行的情况。
    

我们可以通过控制日志级别来决定输出多少日志信息，避免在生产环境中输出过多的调试信息。

* * *

### 14.3 实现 Logger 类

#### **实现步骤**

**1\. 定义日志级别枚举**

```java
public enum LogLevel {
    DEBUG, INFO, WARN, ERROR, FATAL
}
```

**2\. 创建日志记录器接口**

```java
package com.daicy.minitomcat.log;

public interface Logger {

    void log(LogLevel level, String message);

    void log(LogLevel level, String message, Throwable throwable);

    // debug级别日志
    void debug(String message);

    // info级别日志
    void info(String message) ;

    // warn级别日志
    void warn(String message);

    // error级别日志
    void error(String message);
}
```

创建抽象类

```java
package com.daicy.minitomcat.log;

import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public abstract class AbstractLogger implements Logger{

    final LogLevel minLogLevel;

    protected AbstractLogger(LogLevel minLogLevel) {
        this.minLogLevel = minLogLevel;
    }

    private String throwableToString(Throwable throwable) {
        StringBuilder sb = new StringBuilder();
        for (StackTraceElement element : throwable.getStackTrace()) {
            sb.append("\tat ").append(element).append("\n");
        }
        return sb.toString();
    }


    String getCurrentTime() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        return LocalDateTime.now().format(formatter);
    }


    @Override
    public void log(LogLevel level, String message, Throwable throwable) {
        if (level.ordinal() >= minLogLevel.ordinal()) {
            String logMessage = message +  "\n" + throwableToString(throwable);
            log(level, logMessage);
        }
    }

    // debug级别日志
    @Override
    public void debug(String message) {
        log(LogLevel.DEBUG, message);
    }

    // info级别日志
    @Override
    public void info(String message) {
        log(LogLevel.INFO, message);
    }

    // warn级别日志
    @Override
    public void warn(String message) {
        log(LogLevel.WARN, message);
    }

    // error级别日志
    @Override
    public void error(String message) {
        log(LogLevel.ERROR, message);
    }
}
```

**3\. 实现基础日志类** 创建一个 `ConsoleLogger`，将日志输出到控制台：

```java
package com.daicy.minitomcat.log;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class ConsoleLogger extends AbstractLogger {

    public ConsoleLogger(LogLevel minLogLevel) {
        super(minLogLevel);
    }

    @Override
    public void log(LogLevel level, String message) {
        if (level.ordinal() >= minLogLevel.ordinal()) {
            System.out.println(formatLog(level, message));
        }
    }

    @Override
    public void log(LogLevel level, String message, Throwable throwable) {
        if (level.ordinal() >= minLogLevel.ordinal()) {
            System.out.println(formatLog(level, message));
            throwable.printStackTrace(System.out);
        }
    }

    private String formatLog(LogLevel level, String message) {
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        return String.format("[%s] [%s] %s", timestamp, level, message);
    }
}
```

**4\. 增加文件日志支持** 扩展 `FileLogger`，将日志保存到文件：

```java
package com.daicy.minitomcat.log;

import java.io.FileWriter;
import java.io.IOException;


public class FileLogger extends AbstractLogger {
    private final String logFilePath;

    public FileLogger(LogLevel minLogLevel, String logFilePath) {
        super(minLogLevel);
        this.logFilePath = logFilePath;
    }


    @Override
    public void log(LogLevel level, String message) {
        if (level.ordinal() >= minLogLevel.ordinal()) {
            String logMessage = String.format("[%s] [%s] %s", getCurrentTime(), level, message);
            // 输出到文件
            try (FileWriter writer = new FileWriter(logFilePath, true)) {
                writer.write(logMessage + "\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
```

**5\. 创建日志管理器** 日志管理器用于统一管理日志记录器：

```java
package com.daicy.minitomcat.log;

import java.util.ArrayList;
import java.util.List;

public class LogManager  {
    private static final List<Logger> loggers = new ArrayList<>();

    public static void addLogger(Logger logger) {
        loggers.add(logger);
    }

    public static void log(LogLevel level, String message) {
        for (Logger logger : loggers) {
            logger.log(level, message);
        }
    }

    public static void log(LogLevel level, String message, Throwable throwable) {
        for (Logger logger : loggers) {
            logger.log(level, message, throwable);
        }
    }


    // debug级别日志
    public static void  debug(String message) {
        log(LogLevel.DEBUG, message);
    }

    // info级别日志
    public static void  info(String message) {
        log(LogLevel.INFO, message);
    }

    // warn级别日志
    public static void  warn(String message) {
        log(LogLevel.WARN, message);
    }

    // error级别日志
    public static void  error(String message) {
        log(LogLevel.ERROR, message);
    }
}
```

**6\. 集成日志模块** 在 MiniTomcat 中，添加统一的日志调用：

```java
LogManager.addLogger(new ConsoleLogger(LogLevel.INFO));
LogManager.addLogger(new FileLogger(LogLevel.DEBUG, "mini-tomcat.log"));
```

在需要记录日志的地方调用：

```java
LogManager.log(LogLevel.INFO, "MiniTomcat started");
LogManager.log(LogLevel.ERROR, "Error handling request", exception);
```

* * *

#### **测试日志模块**

1.  启动 MiniTomcat，观察控制台是否输出正确的日志。
    
2.  查看日志文件内容，确保日志条目正确写入。
    
3.  修改日志级别，验证不同级别的日志过滤效果。
    

* * *

#### **优化与扩展**

+   **异步日志**：使用线程池异步写入日志，提升性能。
    
+   **日志分割**：按日期或文件大小分割日志文件。
    
+   **可配置性**：从外部配置文件读取日志设置，例如日志级别、输出路径等。
    

通过以上步骤，我们成功为 MiniTomcat 构建了一个灵活、高效的日志模块。

* * *

### 14.4 配置和使用 Logger

在实际使用中，我们可以通过 `Logger` 类记录 Web 容器中的各种日志信息。

#### 14.4.1 配置和使用示例

```java
package com.daicy.minitomcat;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.Date;


public class LoggingFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        // 初始化操作，如果有需要可以在这里读取配置参数等
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        long startTime = System.currentTimeMillis();
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        LogManager.info("Request started at: " + startTime + " for path: " + request.getRequestURI());

        filterChain.doFilter(servletRequest, servletResponse);

        long endTime = System.currentTimeMillis();
        LogManager.info("Request completed at: " + endTime + " for path: " + request.getRequestURI() + " Took: " + (endTime - startTime) + "ms");
    }

    @Override
    public void destroy() {
        // 清理资源操作
    }
}
```

在这个示例中，我们创建了一个 `Logger` 实例，日志级别为 `INFO`。这意味着 `DEBUG` 级别的日志将不会输出，而 `INFO`、`WARN` 和 `ERROR` 级别的日志会被输出。

输出结果（控制台和 `mini-tomcat.log` 文件中）如下：

```
[2024-11-23 15:39:00] [INFO] Servlet context initialized.
[2024-11-23 15:39:00] [INFO] HelloServlet initialized.
[2024-11-23 15:39:00] [INFO] HTTP Connector is running on port 8080
[2024-11-23 15:39:07] [INFO] Accepted connection from /0:0:0:0:0:0:0:1
[2024-11-23 15:39:07] [INFO] Accepted connection from /0:0:0:0:0:0:0:1
[2024-11-23 15:39:07] [INFO] Session created with ID: afeb595f-354d-4b6a-a136-f11ba15f4bb2
[2024-11-23 15:39:07] [INFO] LogValve: Logging request /hello
[2024-11-23 15:39:07] [INFO] Request started at: 1732347547912 for path: /hello
[2024-11-23 15:39:07] [INFO] Request completed at: 1732347547912 for path: /hello Took: 0ms
[2024-11-23 15:39:40] [INFO] Server stopping...
[2024-11-23 15:39:40] [INFO] HelloServlet destroyed.
[2024-11-23 15:39:40] [INFO] Servlet context destroyed.
```

* * *

### 14.5 日志管理和扩展

#### 14.5.1 日志级别管理

在生产环境中，我们通常会将日志级别设置为 `INFO` 或更高的级别，这样可以避免过多的调试信息输出。而在开发和调试过程中，`DEBUG` 级别的日志有助于我们进行问题排查。

#### 14.5.2 日志文件管理

为了防止日志文件过大，我们可以定期轮换日志文件。例如，使用时间戳或文件大小来分割日志文件。日志文件的管理可以通过日志框架（如 Log4j 或 SLF4J）来实现。

#### 14.5.3 日志的多线程安全

如果系统是多线程的，日志输出可能会受到线程竞争的影响。可以通过同步方法或使用线程安全的日志框架来确保日志输出的正确性。

* * *

### 14.6 学习收获

通过实现日志模块，我们学习了以下内容：

1.  **日志级别控制**：我们掌握了日志级别控制的原理，理解了如何根据不同的日志级别输出不同的日志信息。
    
2.  **日志输出到文件和控制台**：我们实现了日志的双重输出，既能在控制台显示，也能记录到日志文件中，方便后期分析。
    
3.  **日志模块的可扩展性**：通过 `Logger` 类的设计，我们可以灵活地扩展日志模块，支持更多功能，如日志轮转、异步日志等。
    

通过日志模块的实现，我们为 Web 容器的调试、监控和运维提供了基础支持。