---
title: Java：列出目录中的文件
id: 1432
date: 2024-10-31 22:01:55
author: daichangya
permalink: /archives/Java-lie-chu-mu-lu-zhong-de-wen-jian/
---

## Java：列出目录中的文件

### 介绍

许多应用程序都以某种方式处理文件，而文件操作是任何编程语言中的核心知识之一。

为了操作文件，我们需要知道它们的位置。如果要完成此任务，那么对目录中的文件进行概述是至关重要的，特别是如果我们可以通过迭代对其执行操作的话。在Java中有几种方法可以做到这一点，我们将在本文中进行介绍。

为了简单起见，所有示例将针对以下文件树编写：

```
Programming
|-- minimax.c
|-- super_hack.py
|-- TODO.txt
`-- CodingMusic
    |-- Girl Talk - All Day.mp3
    |-- Celldweller - Frozen.mp3
    |-- Lim Taylor - Isn't It Wonderful.mp3
    `-- Radiohead - Everything in Its Right Place.mp3

```

### File.list（）

在不遍历子目录的情况下列出给定目录中文件和文件夹名称的最简单方法是helper方法`.list()`，该方法返回`String`数组。

我们通过`.list()`在`File`实例上使用方法来执行此操作：

```java
public class Pathnames {

    public static void main(String[] args) {
        // Creates an array in which we will store the names of files and directories
        String[] pathnames;

        // Creates a new File instance by converting the given pathname string
        // into an abstract pathname
        File f = new File("D:/Programming");

        // Populates the array with names of files and directories
        pathnames = f.list();

        // For each pathname in the pathnames array
        for (String pathname : pathnames) {
            // Print the names of files and directories
            System.out.println(pathname);
        }
    }
}

```

使用简单的for-each循环，我们遍历数组并打印出`String`数组。

```
CodingMusic
minimax.c
super_hack.py
TODO.txt

```

使用这种方法时，`CodingMusic`目录中的所有项目都不会显示出来，这种方法的缺点是我们不能对文件本身做任何事情。我们只是得到他们的名字。当我们只想以面值查看文件时很有用。

#### FilenameFilter

我们可以使用该`.list()`方法做的另一件事是创建一个`FilenameFilter`仅返回我们想要的文件的方法：

```java
File f = new File("D:/Programming");

// This filter will only include files ending with .py
FilenameFilter filter = new FilenameFilter() {
        @Override
        public boolean accept(File f, String name) {
            return name.endsWith(".py");
        }
    };

// This is how to apply the filter
pathnames = f.list(filter);

```

运行这段代码将产生：

```
super_hack.py

```

### File.listFiles（）

与前一种方法类似，该方法可用于返回文件和目录的名称，但是这次我们将它们作为`File`对象数组获得，这使我们能够直接操作它们：

```java
public class Pathnames {
    public static void main(String args[]) {

        // try-catch block to handle exceptions
        try {
            File f = new File("D:/Programming");

            FilenameFilter filter = new FilenameFilter() {
                @Override
                public boolean accept(File f, String name) {
                    // We want to find only .c files
                    return name.endsWith(".c");
                }
            };

            // Note that this time we are using a File class as an array,
            // instead of String
            File[] files = f.listFiles(filter);

            // Get the names of the files by using the .getName() method
            for (int i = 0; i < files.length; i++) {
                System.out.println(files[i].getName());
            }
        } catch (Exception e) {
            System.err.println(e.getMessage());
        }
    }
}

```

输出：

```
minimax.c

```

现在，让我们使用递归遍历文件系统并在`File`对象上使用更多方法：

```java
public class ListFilesRecursively {
    public void listFiles(String startDir) {
        File dir = new File(startDir);
        File[] files = dir.listFiles();

        if (files != null && files.length > 0) {
            for (File file : files) {
                // Check if the file is a directory
                if (file.isDirectory()) {
                    // We will not print the directory name, just use it as a new
                    // starting point to list files from
                    listDirectory(file.getAbsolutePath());
                } else {
                    // We can use .length() to get the file size
                    System.out.println(file.getName() + " (size in bytes: " + file.length()+")");
                }
            }
        }
    }
    public static void main(String[] args) {
        ListFilesRecursively test = new ListFilesRecursively();
        String startDir = ("D:/Programming");
        test.listFiles(startDir);
    }
}

```

输出：

```
Girl Talk - All Day.mp3 (size in bytes: 8017524)
Celldweller - Frozen.mp3 (size in bytes: 12651325)
Lim Taylor - Isn't It Wonderful.mp3 (size in bytes: 6352489)
Radiohead - Everything in Its Right Place.mp3 (size in bytes: 170876098)
minimax.c (size in bytes: 20662)
super_hack.py (size in bytes: 114401)
TODO.txt (size in bytes: 998)

```

### Files.walk（）

在Java 8和更高版本中，我们可以使用`java.nio.file.Files`类填充a `Stream`并使用它遍历文件和目录，同时递归遍历所有子目录。

请注意，在此示例中，我们将使用[Lambda表达式](https://blog.jsdiff.com/archives/lambda-expressions-in-java)：

```java
public class FilesWalk {
    public static void main(String[] args) {
        try (Stream<Path> walk = Files.walk(Paths.get("D:/Programming"))) {
            // We want to find only regular files
            List<String> result = walk.filter(Files::isRegularFile)
                    .map(x -> x.toString()).collect(Collectors.toList());

            result.forEach(System.out::println);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

```

在这里，我们`Stream`使用`.walk()`方法填充了一个，并传递了一个`Paths`参数。该`Paths`班由返回一个静态方法`Path`上的绳子基于URI -和使用`Path`，我们可以很容易地找到该文件。

在`Path`，`Paths`，`Files`，和许多其他类属于`java.nio`包，这是Java 7中引入了更现代的方式来表示非阻塞方式的文件。

然后，使用*Collections Framework*生成一个列表。

运行这段代码将产生：

```
D:\Programming\Coding Music\Radiohead - Everything in Its Right Place.mp3
D:\Programming\Coding Music\Lim Taylor - Isn't It Wonderful.mp3
D:\Programming\Coding Music\Celldweller - Frozen.mp3
D:\Programming\Coding Music\Girl Talk - All Day.mp3
D:\Programming\minimax.c
D:\Programming\super_hack.py
D:\Programming\TODO.txt

```

### 结论

以某种方式处理文件是大多数编程语言的核心任务，这包括在文件系统中列出和查找文件的能力。为了操作文件，我们需要知道它们的位置。如果要完成此任务，那么对目录中的文件进行概述是至关重要的，特别是如果我们可以通过迭代对其执行操作的话。

在本文中，我们展示了使用线性和递归方法在Java中列出文件系统上文件的多种不同方法。
