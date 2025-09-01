---
title: Mac 电脑上 Apache JMeter 的安装及使用指南
id: e850eb9b-3eef-4cd2-8d25-bcf72a8bd51d
date: 2024-12-03 13:27:23
author: daichangya
excerpt: 以下是 Mac 电脑上 Apache JMeter 的安装及使用指南，适合初学者快速上手。 1. 什么是 Apache JMeter Apache
  JMeter 是一款开源的性能测试工具，用于测试 Web 应用程序、API 和其他系统的负载性能。它可以通过图形界面或命令行运行，支持多种协议（如 HT
permalink: /archives/Mac-dian-nao-shang-Apache-JMeter-de-an/
categories:
- 压力测试
---

以下是 **Mac 电脑上 Apache JMeter 的安装及使用指南**，适合初学者快速上手。

---

### **1. 什么是 Apache JMeter**
Apache JMeter 是一款开源的性能测试工具，用于测试 Web 应用程序、API 和其他系统的负载性能。它可以通过图形界面或命令行运行，支持多种协议（如 HTTP、FTP、SOAP、JDBC 等）。

---

### **2. 安装 Apache JMeter**

#### **方法一：通过 Homebrew 安装**
1. **检查是否安装 Homebrew**：
   在终端输入以下命令，检查是否已安装 Homebrew：
   ```bash
   brew --version
   ```
   如果未安装，执行以下命令安装：
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **安装 JMeter**：
   ```bash
   brew install jmeter
   ```

3. **验证安装**：
   安装完成后，运行以下命令查看 JMeter 版本：
   ```bash
   jmeter --version
   ```
   显示 JMeter 版本号即表示安装成功。

#### **方法二：手动下载 JMeter**
1. **下载 JMeter**：
   - 访问 [JMeter 官方下载页面](https://jmeter.apache.org/download_jmeter.cgi)。
   - 下载最新版本的 `.tgz` 文件。
<separator></separator>
2. **解压 JMeter 文件**：
   打开终端，进入下载目录并解压：
   ```bash
   tar -xvzf apache-jmeter-<version>.tgz
   ```
   例如：
   ```bash
   tar -xvzf apache-jmeter-5.6.1.tgz
   ```

3. **运行 JMeter**：
   进入解压后的 `bin` 目录，运行以下命令启动 GUI：
   ```bash
   cd apache-jmeter-<version>/bin
   ./jmeter
   ```

---

### **3. 配置环境变量（可选）**
为方便使用，可以将 JMeter 的 `bin` 目录添加到 PATH 环境变量中：
1. 打开终端，编辑配置文件：
   ```bash
   nano ~/.zshrc
   ```
2. 添加以下内容：
   ```bash
   export JMETER_HOME=/path/to/apache-jmeter-<version>
   export PATH=$JMETER_HOME/bin:$PATH
   ```
   将 `/path/to/apache-jmeter-<version>` 替换为实际路径。
3. 保存并刷新配置：
   ```bash
   source ~/.zshrc
   ```

---

### **4. 使用 Apache JMeter**

#### **启动 JMeter**
1. 打开终端，输入以下命令启动 JMeter 图形界面：
   ```bash
   jmeter
   ```
   如果是手动下载的版本，需要进入 `bin` 目录后运行：
   ```bash
   ./jmeter
   ```

2. 启动成功后，将看到 JMeter 的 GUI 界面。

#### **创建一个测试计划**
1. **新建测试计划**：
   - 在菜单中点击 `File > New` 创建新的测试计划。

2. **添加线程组**：
   - 在左侧测试计划上右键，选择 `Add > Threads (Users) > Thread Group`。
   - 配置线程组的参数，如线程数、Ramp-Up 时间、循环次数。

3. **添加取样器**：
   - 在线程组上右键，选择 `Add > Sampler > HTTP Request`。
   - 配置 `HTTP Request`，如目标服务器地址和路径。

4. **添加监听器**：
   - 在线程组上右键，选择 `Add > Listener > View Results Tree`。
   - 监听器用于查看请求和响应的详细信息。

5. **运行测试**：
   - 点击界面顶部的绿色三角形按钮（▶），运行测试。
   - 查看监听器中的结果，检查请求和响应。

---

### **5. 使用命令行运行 JMeter**
如果不需要图形界面，可以通过命令行运行 JMeter：
1. **保存测试计划**：
   在 GUI 中保存测试计划为 `.jmx` 文件。

2. **运行测试**：
   ```bash
   jmeter -n -t <test-plan-file>.jmx -l <result-file>.jtl
   ```
   - `-n`：非 GUI 模式。
   - `-t`：指定测试计划文件。
   - `-l`：指定结果文件路径。

3. **生成 HTML 报告**：
   ```bash
   jmeter -n -t <test-plan-file>.jmx -l <result-file>.jtl -e -o <output-folder>
   ```
   - `-e`：生成 HTML 报告。
   - `-o`：指定报告的输出目录。

---

### **6. 实战案例：测试一个简单的 API**
以测试 `https://jsonplaceholder.typicode.com/posts` 为例：
1. **设置 HTTP 请求**：
   - 添加一个 HTTP 请求取样器。
   - 配置：
     - `Server Name or IP`：`jsonplaceholder.typicode.com`
     - `Path`：`/posts`
     - `Method`：`GET`

2. **运行测试**：
   点击运行按钮（▶），观察结果。

3. **查看监听器结果**：
   在 `View Results Tree` 中查看请求和响应内容。

---

### **7. 常见问题**
1. **JMeter 无法启动**：
   - 检查是否安装了 Java。
   - 验证环境变量 `JAVA_HOME` 是否正确。
   - 使用以下命令检查 Java 版本：
     ```bash
     java -version
     ```
   - 如果未安装 Java，可以通过 Homebrew 安装：
     ```bash
     brew install openjdk
     ```

2. **监听器结果为空**：
   - 确保线程组中配置了循环次数和请求数。
   - 检查网络连接是否正常。

3. **高并发测试卡顿**：
   - 尽量使用命令行模式运行测试。
   - 增加线程池大小，提高并发能力。

---

通过以上指南，您可以在 Mac 上顺利安装和使用 Apache JMeter，并开展性能测试！