---
title: 加密 DB2 Universal Database 中的数据值
id: 88
date: 2024-10-31 22:01:40
author: daichangya
excerpt: "本文描述如何使用 IBM DB2 Universal Database Version (Unix & Windows) 中提供的新函数轻松地将数据加密集成到数据库应用程序中。多年来，数据库已经能够阻止未经授权的人看到其中的数据，这通常是通过数据库管理器中的特权和权限来实现的。在当前的环境下，对存储数据的保密的需求日益增长。这意味着即使 DBA 对表中的数据有完全的访问权限，但是表中可能还有数据拥有者不希望任何其他人看到的某些信息。特别是对于基于 Web 的应用程序，这一问题就更加明显了，在这种应用程序中，用户输入的数据（比如信用卡号）需要保存起来，以备同一用户以后使用该应用程序。同时，用户拥有者希望能够确保任何其他人不能访问这种数据。"
permalink: /archives/12714991/
tags: 
 - db2
---

## 简介

本文描述如何使用 IBM DB2 Universal Database Version (Unix & Windows) 中提供的新函数轻松地将数据加密集成到数据库应用程序中。多年来，数据库已经能够阻止未经授权的人看到其中的数据，这通常是通过数据库管理器中的特权和权限来实现的。在当前的环境下，对存储数据的保密的需求日益增长。这意味着即使 DBA 对表中的数据有完全的访问权限，但是表中可能还有数据拥有者不希望任何其他人看到的某些信息。特别是对于基于 Web 的应用程序，这一问题就更加明显了，在这种应用程序中，用户输入的数据（比如信用卡号）需要保存起来，以备同一用户以后使用该应用程序。同时，用户拥有者希望能够确保任何其他人不能访问这种数据。

为了实现这种功能，DB2 内置了一些 SQL 函数，这些函数允许应用程序加密和解密数据。当将数据插入到数据库中时，可以使用用户提供的加密密码对其加密。当检索该数据的时候，必须提供相同的密码才能解密数据。对于要多次使用同一个密码的情况，可以使用一个赋值语句设置 ENCRYPTION PASSWORD 值，并令其在某次连接期间内有效。

本文将描述这些 SQL 函数，并给出一些关于如何使用这些加密函数的例子。我们还将讨论在关系数据库中使用加密数据的设计和性能相关事项。

## 实现

下面显示了这些新的 SQL 函数的签名。在 DB2 文档的 SQL Reference 部分中有更详细的文档。（为了确保对加密的数据使用正确的数据类型和长度，请务必阅读 SQL Reference 中 ENCRYPT 函数下的“Table Column Definition”部分。）

> Encrypt (StringDataToEncrypt, PasswordOrPhrase, PasswordHint)  
> Decrypt_Char(EncryptedData, PasswordOrPhrase)  
> GetHint(EncryptedData)  
> Set Encryption Password  

##### 您是否收到 SQL0440N 消息？

如果您第一次试图使用 Encrypt 函数时遭到失败并收到错误消息 SQL0440N，并且您当前使用的数据库是在 Version 7.2 以前（version 7.1 Fixpak 3）创建的，那么请确保以具有 SYSADM 授权的用户身份对数据库执行了系统命令 `db2updv7` 。要了解关于使用 `db2updv7` 命令的更详细的信息，请参阅 Version 7 Fixpak 3 或更高版本的 [产品说明](http://www.ibm.com/cgi-bin/db2www/data/db2/udb/winos2unix/support/document.d2w/report?fn=db2ire71db2ir115.htm#Header_250)。

用于对数据加密的算法是一个 RC2 分组密码（block cipher），它带有一个 128 位的密钥。这个 128 位的密钥是通过消息摘要从密码得来的。加密密码与 DB2 认证无关，仅用于数据的加密和解密。

这里可以提供一个可选的参数 PasswordHint，这是一个字符串，可以帮助用户记忆用于对数据加密的 PasswordOrPhrase。（例如，可以使用 'George' 作为记忆 'Washington'的提示。）

## 列级加密

列级加密（column level encryption）意味着对于一个给定列中的所有值都使用相同的密码进行加密。这种类型的加密可以在视图中使用，也可以在使用了一个公共密码的情况下使用。当对一个或多个表中所有的行使用相同的密钥时，ENCRYPTION PASSWORD 专用寄存器将十分有用。

*例 1*：这个例子使用 ENCRYPTION PASSWORD 值来保存加密密码。它对雇员的社会保险号进行加密，并以经过加密的形式将其存储在 EMP 表中。

> create table emp (ssn varchar(124) for bit data);  
> set encryption password = 'Ben123';  
> insert into emp (ssn) values(encrypt('289-46-8832'));  
> insert into emp (ssn) values(encrypt('222-46-1904'));  
> insert into emp (ssn) values(encrypt('765-23-3221'));  
> select decrypt_char(ssn) from emp;  

*例 2*：这个例子在结合使用视图的情况下使用 ENCRYPTION PASSWORD 值来保存加密密码。下面的语句声明了 emp 表的一个视图：

> create view clear\_ssn (ssn) as select decrypt\_char(ssn) from emp;

在应用程序代码中，我们将 ENCRYPTION PASSWORD 设置为 'Ben123'，现在可以使用 clear_ssn 视图了。

> set encryption password = 'Ben123';  
> select ssn from clear_ssn;  

## 行-列（单元格）或 集合-列级加密

行-列（单元格）或 集合-列（Set-Column）级加密意味着在一个加密数据列内使用多个不同的密码。例如，Web 站点可能需要保存客户信用卡号（ccn）。在这个数据库中，每个客户可以使用他自己的密码或短语来加密 ccn。

*例 3*：Web 应用程序收集关于客户的用户信息。这种信息包括客户名称（存储在宿主变量 *custname*中）、信用卡号（存储在宿主变量 *cardnum*中）和密码（存储在宿主变量 *userpswd*中）。应用程序像下面这样执行客户信息的插入操作。

> insert into customer (ccn, name) values(encrypt(:cardnum, :userpswd), :custname)

当应用程序需要重新显示某客户的信用卡信息时，客户要输入密码，同样该密码也要存储在宿主变量 userpswd 中。之后，可以像下面这样检索该 ccn ：

> select decrypt_char(ccn, :userpswd) from customer where name = :custname;

*例 4*：这个例子使用提示来帮助客户记忆他们的密码。这里使用与例 3 相同的应用程序，该应用程序将提示保存到宿主变量 *pswdhint*中。假设 userpswd 的值是 'Chamonix'， *pswdhint*的值是 'Ski Holiday'。

> insert into customer (ccn, name)  
> values(encrypt(:cardnum, :userpswd, :pswdhint), :custname)

如果客户请求关于所使用的密码的提示，可以使用下面的查询。

> select gethint(ccn) into :pswdhint from customer where name = :custname;

*pswdhint*的值被设置为"Ski Holiday"。

## 加密非字符值

数值和日期/时间数据类型的加密通过强制类型转换得到间接的支持。非字符的 SQL 类型通过强制转换为 "varchar" 或 "char"，就可以被加密了。有关强制类型转换的更多信息，请参阅 SQL 参考文档中的 “Casting Between Data Types” 部分。

*例 5*：加密和解密 TIMESTAMP 数据时用到的强制类型转换函数。

> \-\- Create a table to store our encrypted value  
> create table etemp (c1 varchar(124) for bit data);  
> set encryption password 'next password';  
> \-\- Store encrypted timestamp  
> insert into etemp values encrypt(char(CURRENT TIMESTAMP));  
> \-\- Select & decrypt timestamp  
> select timestamp(decrypt_char(c1)) from etemp;

*例 6*：加密/解密 double 数据。

> set encryption password 'next password';  
> insert into etemp values encrypt(char(1.11111002E5));  
> select double(decrypt_char(c1)) from etemp;

## 性能

加密，就其本质而言，会使大部分 SQL 语句慢下来。但是如果多加注意，多加判断，还是可以将大量的额外开销降至最低。而且，加密数据对于数据库的设计有着很大的影响。通常，您需要对一个模式中的一些敏感数据元素进行加密，例如社会保险号、信用卡号、病人姓名，等等。而有些数据值就不是那么适于加密了 -- 例如布尔值（true 和 false），或者其他的像整数 1 到 10 这样的小型集合。这些值与列名一起很容易被猜出，因此需要判断加密是否真的有用。

在某些情况下，对加密的数据创建索引是很好的主意。加密数据的正确匹配及连接将使用您创建的索引。由于加密数据实质上是二进制数据，因此对加密数据进行范围检查时需要扫描表。范围检查需要解密某一列在所有行的值，因此应该避免进行范围检查，至少也应该进行适当的调优。

下面的场景阐明了我们的讨论。考虑一种常见的主从（master-detail）模式，程序员可以在很多项目中使用这种模式。我们将对雇员的社会保险号（ssn）实现列级加密。在主表 emp 和从表 empProject 中，ssn 将以加密的形式存储。

> \-\- Define Tables and Indexes for encrypted data  
> create table emp (ssn varchar(48) for bit data,  
>           name varchar(48) );  
> create unique index idxEmp on emp ( ssn ) includes (name) ;  
> create table empProject( ssn varchar(48) for bit data,  
>           projectName varchar(48) );  
> create index idxEmpPrj on empProject ( ssn );  
> \-\- Add some data  
> set encryption password = 'ssnPassWord';  
> insert into emp values (encrypt('480-93-7558'),'Super Programmer');  
> insert into emp values (encrypt('567-23-2678'),'Novice Programmer');  
> insert into empProject values (encrypt('480-93-7558'),'UDDI Project');  
> insert into empProject values (encrypt('567-23-2678'),'UDDI Project');  
> insert into empProject values (encrypt('480-93-7558'),'DB2 UDB Version 10');  
> \-\- Find the programmers working on UDDI select a.name, decrypt_char(a.ssn)  
>        from emp a, empProject b  
> where  
>        a.ssn = b.ssn  
>        and b.project ='UDDI Project';  
> \-\- Build a list of the projects that the programmer with ssn  
> \-\- '480-93-7558' is working on  
> select projectName  
>        from empProject  
> where ssn = encrypt('480-93-7558');  

相对于上面的例子，下面的两个例子是 **不**应该采用的反面典型。虽然这些查询同样能够返回正确的答案，但是它们会需要为所有行解密 ssn。当表很大的时候，这个问题就会变得突出起来。

> select a.name, decrypt_char(a.ssn)  
>        from emp a, empProject b  
> where  
>        decrypt\_char(a.ssn) = decrypt\_char(b.ssn)  
>        and b.project ='UDDI Project';  

该查询会要求解密 emp 表的每一行以及 empProject 表的每个 'UDDI Project' 行，以执行连接。

> select projectName  
>        from empProject  
> where decrypt_char(ssn)= '480-93-7558';  

该查询会要求解密 empProject 表中的每一行。

## 结束语

在本文中，我们演示了 IBM DB2 Universal Database 中的加密函数如何提供简单方式来加密敏感数据。这些函数可用来实现列级和行-列级的加密。在设计和实现期间，开发人员应该审视一些重要的性能相关事项。数据加密为隐藏私有数据增添了一种新的可用工具，即使对于管理人员，也能起到保密的作用。
