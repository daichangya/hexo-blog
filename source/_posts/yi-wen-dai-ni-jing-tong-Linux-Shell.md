---
title: 一文带你精通 Linux Shell 编程
id: 218c8a93-6a25-449d-9d0e-8362aa59418b
date: 2024-12-08 16:33:46
author: daichangya
cover: https://images.jsdiff.com/Linux.jpg
excerpt: 一、Shell编程简介 1.1 什么是Shell 从程序员角度看，Shell是用C语言编写的程序；从用户角度，它是与Linux操作系统沟通的桥梁。用户可输入命令执行，也能用Shell脚本编程完成复杂操作。在Linux系统管理领域，Shell编程至关重要，是每个Linux用户的必修课。
  1.2 She
permalink: /archives/yi-wen-dai-ni-jing-tong-Linux-Shell/
categories:
- linux
---

## 一、Shell编程简介
### 1.1 什么是Shell
从程序员角度看，Shell是用C语言编写的程序；从用户角度，它是与Linux操作系统沟通的桥梁。用户可输入命令执行，也能用Shell脚本编程完成复杂操作。在Linux系统管理领域，Shell编程至关重要，是每个Linux用户的必修课。

### 1.2 Shell种类
Linux的Shell种类繁多，常见的有Bourne Shell（/usr/bin/sh或/bin/sh）、Bourne Again Shell（/bin/bash）、C Shell（/usr/bin/csh）、K Shell（/usr/bin/ksh）、Shell for Root（/sbin/sh）等。不同Shell语法不同，基本掌握一种即可，本文重点关注Bash（Bourne Again Shell），因其易用且免费，在日常工作中广泛使用，也是多数Linux系统默认的Shell。

### 1.3 Shell脚本格式
使用vi等文本编辑器编写Shell脚本格式固定。首行“#!/bin/sh”（或“#!/bin/bash”）指定解释脚本的Shell程序，缺此行执行脚本会出错。后续是主程序，以“#”开头为注释行。若一行未写完，行尾加“\”可与下一行合并。编辑完成后，将脚本存为“filename.sh”，文件名后缀表明是Bash脚本。执行前需用“chmod +x filename.sh”改为可执行权限，然后用“./filename.sh”执行。

### 1.4 变量赋值与取值
Shell Script是弱类型语言，使用变量无需声明类型。变量赋值格式为“variable_name = variable_value”，对已有值变量赋值会覆盖旧值。取值时在变量名前加“$”，如“$variable_name”，变量可在引号中使用。若有混淆，可用花括号区分，如“echo "Hi, ${a}s"”。单引号中的变量不进行替换操作。

### 1.5 相关Linux命令
- **env**：显示用户环境区中的变量及其取值。
- **set**：显示本地数据区和用户环境区中的变量及其取值。
- **unset**：删除指定变量当前取值，使其为NULL。
- **export**：将本地数据区中的变量转移到用户环境区。

## 二、Shell编程语法
### 2.1 if语句
if语句用于流程控制，语法如下：
<separator></separator>
```bash
if …; then
…
elif …; then
…
else
…
fi
```
条件部分以分号分隔，常用条件测试有：
- **文件判断**：“[ -f "$file" ]”判断$file是否为文件。
- **数值比较**：“[ $a -lt 3 ]”判断$a值是否小于3，“-gt”和“-le”分别表示大于和小于等于。
- **权限判断**：“[ -x "$file" ]”判断$file是否存在且有可执行权限，“-r”测试文件可读性。
- **变量判断**：“[ -n "$a" ]”判断变量$a是否有值，“-z”测试空串。
- **字符串判断**：“[ "$a" = "$b" ]”判断$a和$b取值是否相等。
- **逻辑判断**：“[ cond1 -a cond2 ]”判断cond1和cond2是否同时成立，“-o”表示cond1和cond2有一个成立。

条件测试部分空格很重要，方括号两侧、“-f”“-lt”“=”等符号两侧都要有空格，否则Shell解释脚本会出错。

### 2.2 Here文档
Here文档用于将多行文本传递给命令，格式以“<<”开始，后跟字符串，文档结束时该字符串也要出现。例如：
```bash
cat<<HELP
ren -- renames a number of files using sed regular expressions
USAGE:
ren 'regexp' 'replacement' files
EXAMPLE:
rename all *.HTM files in *.html:
ren 'HTM$' 'html' *.HTM
HELP
```
### 2.3 循环语句
Shell Script中的循环有以下几种格式：
- **while循环**：
```bash
while [ cond1 ] && { || } [ cond2 ] …; do
…
done
```
- **for循环**：
```bash
for var in …; do
…
done
```
- **for循环（C语言风格）**：
```bash
for (( cond1; cond2; cond3 )) do
…
done
```
- **until循环**：
```bash
until [ cond1 ] && { || } [ cond2 ] …; do
…
done
```
循环中可使用“break”和“continue”中断操作。例如：
```bash
Sum=0
i=0
while [ $i!= "100" ]
do
i=`expr $i + 1`
Sum=`expr $Sum + $i`
done
echo $i $Sum
```
### 2.4 case语句
case语句类似C语言多分支结构，语法如下：
```bash
case var in
pattern 1 )
… ;;
pattern 2 )
… ;;
*)
… ;;
esac
```
例如：
```bash
while getopts vc: OPTION
do
case $OPTION in
c) COPIES=$OPTARG
ehco "$COPIES";;
v) echo "suyang";;
\?) exit 1;;
esac
done
```
### 2.5 select扩展
用于交互式应用，语法如下：
```bash
select var in …; do
break;
done
```
例如：
```bash
#!/bin/bash
echo "Your choice?"
select var in "a" "b" "c"; do
break
done
echo $var
```
### 2.6 函数定义
语法形式如下：
```bash
functionname()
{
…
}
```
函数中处理参数方法与脚本参数相同，用“$1”“$2”表示第一、第二个参数，“$*”表示参数列表。

### 2.7 脚本调试
- **使用echo输出变量取值**：简单查看变量值。
- **使用-x参数**：执行脚本并显示所有变量取值，如“sh -x filename.sh”。
- **使用-n参数**：不执行脚本，返回语法错误。

## 三、特殊变量与字符
### 3.1 系统环境变量
- **$HOME**：使用者自己的目录。
- **$PATH**：执行命令时搜寻的目录。
- **$TZ**：时区。
- **$MAILCHECK**：检查新信件的间隔秒数。
- **$PS1**：命令列提示号。
- **$PS2**：命令未打完时，Shell要求再输入的提示号。
- **$MANPATH**：man指令的搜寻路径。

### 3.2 特殊变量
- **$0**：程序执行名字。
- **$n**：程序的第n个参数值（n = 1..9）。
- **$*和$@**：程序的所有参数（略有区别，$*将所有参数视为一个整体，$@将每个参数视为独立个体）。
- **$#**：程序的参数个数。
- **$$**：程序的PID。
- **$!**：执行上一个指令的PID。
- **$?**：执行上一个指令的返回值。

### 3.3 shell中的变元
- **\***：任意字符串。
- **?**：一个任意字符。
- **[abc]**：a、b、c三者中之一。
- **[a - n]**：从a到n的任一字符。

### 3.4 特殊字符表示
- **\b**：退回。
- **\c**：打印一行时无换行符。
- **\f**：换页。
- **\r**：回车。
- **\t**：制表。
- **\v**：垂直制表。
- **\\**：反斜线本身。

### 3.5 判断文件属性
格式为“-操作符 filename”，常见操作符有：
- **-e**：文件存在返回0，否则返回1。
- **-r**：文件可读返回0，否则返回1。
- **-w**：文件可写返回0，否则返回1。
- **-x**：文件可执行返回0，否则返回1。
- **-o**：文件属于用户本人返回0，否则返回1。
- **-z**：文件长度为0返回0，否则返回1。
- **-f**：文件为普通文件返回0，否则返回1。
- **-d**：文件为目录文件时返回0，否则返回1。

### 3.6 测试字符串
- **字符串1 = 字符串2**：两字串相等为真。
- **字符串1!= 字符串2**：两字串不等为真。
- **-n字符串**：字符串长度大于0为真。
- **-z字符串**：字符串长度为0为真。
- **字符串（直接判断）**：字符串非空为真。

### 3.7 测试两个整数关系
- **数字1 -eq数字2**：两数相等为真。
- **数字1 -ne数字2**：两数不等为真。
- **数字1 -gt数字2**：数字1大于数字2为真。
- **数字1 -ge数字2**：数字1大于等于数字2为真。
- **数字1 -lt数字2**：数字1小于数字2为真。
- **数字1 -le数字2**：数字1小于等于数字2为真。

### 3.8 逻辑测试
- **-a**：与。
- **-o**：或。
- **!**：非。

### 3.9 特殊字符引用
1. **$符号**
   - **echo $?**：显示上一条指令退出状态，判断上条命令执行是否成功。
   - **echo "$?"**：效果同上。
   - **echo '$?'**：显示“$?”字符串。
   - **echo \$?**：显示“$?”字符串。
   - **echo "\$?"**：显示“$?”字符串。
   双引号中$符号有特殊意义，单引号可屏蔽特殊字符意义，反斜杠也可屏蔽特殊字符特殊含义。
2. **\反斜杠**
   反斜杠可屏蔽特殊符号特殊含义，如“echo \$A”显示“$A”，“echo \`”显示“`”，“echo \"”显示双引号，“echo \\”显示“\”。
3. **`反引号`**
   反引号用于命令替换，将其中字符串作为命令执行，结果赋给变量，如“A=`date`”，“echo $A”显示当时时间串。
4. **"双引号"**
   双引号可避免引用特殊字符，但部分特殊字符仍有特殊含义，如“$”“\”“`”“"”。单引号引起内容原样输出，双引号引起内容可能有特殊处理。要输出特殊字符原形，可用单引号或反斜杠，如“echo '"'”输出“"”，“echo "\""”也输出“"”。
5. **其它特殊字符**
   “<”“>”“*”“?”“[”“]”等特殊字符在双引号中可能有特殊含义，输出原形可用单引号或双引号引起来。

### 3.10 条件测试语句
1. **if条件语句**
   格式：
   ```bash
   if 条件表达式
   then #当条件为真时执行以下语句
   命令列表
   else #为假时执行以下语句
   命令列表
   fi
   ```
   if语句可嵌套，如：
   ```bash
   if test -f "$1"
   then
   lpr $1
   else
   if test -d "$1"
   then
   cd $1
   lpr $1
   else
   echo "$1不是文件或目录"
   fi
   fi
   ```
   也可改为：
   ```bash
   if test -f "$1"
   then
   lpr $1
   elif test -d "$1" #elif同else if
   then
   (cd $1;lpr $1)
   else
   echo "$1不是文件或目录"
   fi
   ```
2. **多重条件测试语句case**
   格式：
   ```bash
   case 字串 in
   模式) 命令列表;;
   模式) 命令列表;;
  ....
   esac
   ```
   例如：
   ```bash
   case $1 in
   *.c)
   cc $1
   ;;
   *.txt)
   lpr $1
   ;;
   *)
   echo "未知的类型"
   esac
   ```

### 3.11 循环语句
1. **while循环**
   命令格式：
   ```bash
   while 条件表
   do
   命令表
   done
   ```
   执行过程：先执行条件表，若最后一条语句退出状态为零（条件为真），执行循环体内命令表，然后再次检查条件表，如此循环，直到条件表最后一条语句退出状态非零。例如：
   ```bash
   Sum=0
   i=0
   while true #true是系统关键词，表示真
   do
   i=`expr $i + 1`
   Sum=`expr $Sum + $i`
   if [ $i = "100" ]
   then
   break;
   fi
   done
   echo $i $Sum
   ```
   也可改为：
   ```bash
   Sum=0
   i=0
   while [ $i!= "100" ]
   do
   i=`expr $i + 1`
   Sum=`expr $Sum + $i`
   done
   echo $i $Sum
   ```
   还可用until作为测试条件，与while相反，当条件为假时循环，如：
   ```bash
   Sum=0
   i=0
   until [ $i = "100" ]
   do
   i=`expr $i + 1`
   Sum=`expr $Sum + $i`
   done
   echo $i $Sum
   ```
2. **for循环**
   命令格式：
   ```bash
   for 变量 in 名字列表
   do
   命令列表
   done
   ```
   名字列表是空格分隔字符串列表，shell每次从列表取一个字符串赋给循环变量。例如：
   ```bash
   for File in a1 a2 a3 a4 a5
   do
   diff aa/$File bb/$File
   done
   ```
   也可省略in名字列表部分，用当前位置参数代替，如：
   ```bash
   for File
   do
   echo $File
   done
   ```
3. **循环控制语句**
   - **break**：不执行当前循环体内break下面语句，直接退出当前循环。
   - **continue**：忽略本循体内continue下面语句，从循环头开始执行。

### 3.12 命令组合
1. **圆括号**
   圆括号使shell创建子shell读取并执行括起来的命令，创建子进程运行组合程序，子进程操作不影响当前shell变量值，且当前shell用export输出的变量在子shell中有效。例如：
   ```bash
   (cd newdir;ls)
   ```
   注意圆括号在命令行中的特殊组合意义，若要输出其原义，需用双引号括起来，如“echo "a(b)"”。
2. **花括号**
   花括号由当前shell读取并执行括起来的命令，不创建子shell。左右花括号作为一条命令第一个字出现时才有特殊含义。例如：
   ```bash
   { cd olddir;ls; }
   ```
   退出状态等于最后一条括起来命令的退出状态。

### 3.13 可在当前shell中执行的命令
包括break、case、cd、continue、echo、eval、exec、exit、export、for、if、read、readonly、return、set、shift、test、times、trap、umask、until、wait、while、:、{}等。
### 四、实战案例

### 4.1 批量文件重命名脚本
以下脚本实现批量文件重命名功能，将指定扩展名的文件改为新的扩展名。
```bash
#!/bin/bash
# 检查参数个数
if [ $# -lt 2 ]; then
cat<<HELP
Usage: rename.sh old_extension new_extension [files]
HELP
exit 1
fi

OLD_EXT="$1"
NEW_EXT="$2"
shift
shift

# 循环处理文件
for file in $*; do
if [ -f "$file" ]; then
newfile=`echo "$file" | sed "s/${OLD_EXT}/${NEW_EXT}/g"`
if [ -f "$newfile" ]; then
echo "ERROR: $newfile exists already"
else
echo "Renaming $file to $newfile"
mv "$file" "$newfile"
fi
fi
done
```
使用方法：
```bash
./rename.sh txt log file1.txt file2.txt file3.txt
```
### 4.2 简单的备份脚本
该脚本用于备份指定目录到指定备份目录，备份文件以日期命名。
```bash
#!/bin/bash
SOURCE_DIR="/home/user/data"
BACKUP_DIR="/home/user/backup"
DATE=$(date +%Y%m%d)

# 创建备份目录（若不存在）
if [! -d "$BACKUP_DIR" ]; then
mkdir -p "$BACKUP_DIR"
fi

# 备份文件
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" "$SOURCE_DIR"
echo "Backup completed successfully to $BACKUP_DIR/data_$DATE.tar.gz"
```
### 4.3 系统信息收集脚本
此脚本收集系统的一些基本信息，如内存使用情况、磁盘使用情况等。
```bash
#!/bin/bash
# 内存使用情况
MEM_INFO=$(free -m)
echo "Memory Information:"
echo "$MEM_INFO"

# 磁盘使用情况
DISK_INFO=$(df -h)
echo "Disk Information:"
echo "$DISK_INFO"

# 当前登录用户
USER_INFO=$(who)
echo "Logged in Users:"
echo "$USER_INFO"
```
### 五、总结
Shell编程在Linux系统管理和自动化任务处理中具有不可替代的作用。通过掌握Shell脚本的基本语法、特殊变量、条件判断、循环结构以及各种命令的组合使用，能够高效地完成各种复杂任务，提高工作效率。无论是系统管理员还是普通Linux用户，深入学习Shell编程都将为更好地使用和管理Linux系统提供有力支持。不断实践和探索，能够发现Shell编程更多的强大功能，让Linux系统为我们提供更优质的服务。