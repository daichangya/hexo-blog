---
title: 谈谈数据库中MyISAM与InnoDB区别
id: 219
date: 2024-10-31 22:01:41
author: daichangya
excerpt: MyISAM：这个是默认类型，它是基于传统的ISAM类型，ISAM是Indexed Sequential Access Method (有索引的顺序访问方法)
  的缩写，它是存储记录和文件的标准方法。与其他存储引擎比较，MyISAM具有检查和修复表格的大多数工具。 MyISAM表格可以被压缩，而且它们支持全文搜索。它们不是事务安全的，而且也不支持外键。如果事物回滚将造成不完全回滚，不具有原子性。如果
permalink: /archives/tan-tan-shu-ju-ku-zhong-MyISAM-yu/
tags:
- mysql
---

 

MyISAM：这个是默认类型，它是基于传统的ISAM类型，ISAM是Indexed Sequential Access Method (有索引的顺序访问方法) 的缩写，它是存储记录和文件的标准方法。与其他存储引擎比较，MyISAM具有检查和修复表格的大多数工具。 [MyISAM](http://www.nowamagic.net/librarys/veda/tag/MyISAM)表格可以被压缩，而且它们支持全文搜索。它们不是事务安全的，而且也不支持外键。如果事物回滚将造成不完全回滚，不具有原子性。如果执行大量的SELECT，MyISAM是更好的选择。

MyIASM是IASM表的新版本，有如下扩展：

*   二进制层次的可移植性。
*   NULL列索引。
*   对变长行比ISAM表有更少的碎片。
*   支持大文件。
*   更好的索引压缩。
*   更好的键吗统计分布。
*   更好和更快的auto_increment处理。

InnoDB：这种类型是事务安全的。它与BDB类型具有相同的特性，它们还支持外键。InnoDB表格速度很快，具有比BDB还丰富的特性， 因此如果需要一个事务安全的存储引擎，建议使用它。如果你的数据执行大量的INSERT或UPDATE，出于性能方面的考虑，应该使用InnoDB表。对于支持事物的InnoDB类型的表，影响速度的主要原因是AUTOCOMMIT默认设置是打开的，而且程序没有显式调用BEGIN 开始事务，导致每插入一条都自动Commit，严重影响了速度。可以在执行sql前调用begin，多条sql形成一个事物(即使autocommit打开也可以)，将大大提高性能。

具体可以看看下表：

<table style="border-collapse:collapse;border:1px solid rgb(136,136,136);width:544px;color:rgb(51,51,51);font-family:Georgia, 'Times New Roman', 'Bitstream Charter', Times, serif;font-size:12px;line-height:18px;"><tbody><tr><td style="border:1px solid rgb(170,170,170);">&nbsp;</td><td style="border:1px solid rgb(170,170,170);"><span style="color:rgb(68,68,68);">MyISAM</span></td><td style="border:1px solid rgb(170,170,170);"><span style="color:rgb(68,68,68);">InnoDB</span></td></tr><tr><td style="border:1px solid rgb(170,170,170);"><span style="color:rgb(68,68,68);">构成上区别</span></td><td style="border:1px solid rgb(170,170,170);"><p style="text-indent:2em;line-height:20.399999618530273px;letter-spacing:1px;">每个MyISAM在磁盘上存储成三个文件。文件名为表名，扩展名为文件类型。</p>.frm 文件存储表定义；<br>.MYD(MYData) 数据文件的扩展名；<br>.MYI(MYIndex) 索引文件的扩展名。</td><td style="border:1px solid rgb(170,170,170);">基于磁盘的资源是InnoDB表空间数据文件和它的日志文件，InnoDB 表的大小只受限于操作系统文件的大小，一般为 2GB</td></tr><tr><td style="border:1px solid rgb(170,170,170);"><span style="color:rgb(68,68,68);">事务处理方面</span></td><td style="border:1px solid rgb(170,170,170);">MyISAM类型的表强调的是性能，其执行速度比InnoDB类型更快，但是不提供事务支持。</td><td style="border:1px solid rgb(170,170,170);"><p style="text-indent:2em;line-height:20.399999618530273px;letter-spacing:1px;">InnoDB提供事务<span style="color:rgb(68,68,68);">支持事务</span>，外部键等高级数据库功能。</p></td></tr><tr><td style="border:1px solid rgb(170,170,170);"><span style="color:rgb(68,68,68);">锁</span></td><td style="border:1px solid rgb(170,170,170);">表级锁</td><td style="border:1px solid rgb(170,170,170);"><p style="text-indent:2em;line-height:20.399999618530273px;letter-spacing:1px;"><span style="color:rgb(68,68,68);">行级锁</span></p><p style="text-indent:2em;line-height:20.399999618530273px;letter-spacing:1px;">InnoDB表的行锁也不是绝对的，如果在执行一个SQL语句时MySQL不能确定要扫描的范围，InnoDB表同样会锁全表，例如update table set num=1 where name like “%aaa%”</p></td></tr><tr><td style="border:1px solid rgb(170,170,170);"><span style="color:rgb(68,68,68);">select、insert、update、delete操作</span></td><td style="border:1px solid rgb(170,170,170);">如果执行大量的 SELECT，MyISAM 是更好的选择。</td><td style="border:1px solid rgb(170,170,170);"><p style="text-indent:2em;line-height:20.399999618530273px;letter-spacing:1px;">1.如果你的数据执行大量的INSERT或UPDATE，出于性能方面的考虑，应该使用InnoDB表。</p><p style="text-indent:2em;line-height:20.399999618530273px;letter-spacing:1px;">2.DELETE FROM table时，InnoDB不会重新建立表，而是一行一行的删除。</p><p style="text-indent:2em;line-height:20.399999618530273px;letter-spacing:1px;">3.LOAD TABLE FROM MASTER操作对InnoDB是不起作用的，解决方法是首先把InnoDB表改成MyISAM表，导入数据后再改成InnoDB表，但是对于使用的额外的InnoDB特性（例如外键）的表不适用。</p></td></tr><tr><td style="border:1px solid rgb(170,170,170);"><span style="color:rgb(68,68,68);">对于AUTO_INCREMENT类型的字段</span></td><td style="border:1px solid rgb(170,170,170);">必须包含只有该字段的索引</td><td style="border:1px solid rgb(170,170,170);">可以和其他字段一起建立联合索引</td></tr><tr><td style="border:1px solid rgb(170,170,170);">&nbsp;</td><td style="border:1px solid rgb(170,170,170);">&nbsp;</td><td style="border:1px solid rgb(170,170,170);">InnoDB不支持FULLTEXT类型的索引。</td></tr><tr><td style="border:1px solid rgb(170,170,170);">&nbsp;</td><td style="border:1px solid rgb(170,170,170);">MyISAM类型的二进制数据文件可以在不同操作系统中迁移</td><td style="border:1px solid rgb(170,170,170);">&nbsp;</td></tr></tbody></table>

以下是一些细节和具体实现的差别：

1.  InnoDB不支持FULLTEXT类型的索引。
2.  InnoDB 中不保存表的具体行数，也就是说，执行select count(*) from table时，[InnoDB](http://www.nowamagic.net/librarys/veda/tag/InnoDB)要扫描一遍整个表来计算有多少行，但是MyISAM只要简单的读出保存好的行数即可。注意的是，当count(*)语句包含 where条件时，两种表的操作是一样的。
3.  对于AUTO_INCREMENT类型的字段，InnoDB中必须包含只有该字段的索引，但是在MyISAM表中，可以和其他字段一起建立联合索引。
4.  DELETE FROM table时，InnoDB不会重新建立表，而是一行一行的删除。
5.  LOAD TABLE FROM MASTER操作对InnoDB是不起作用的，解决方法是首先把InnoDB表改成MyISAM表，导入数据后再改成InnoDB表，但是对于使用的额外的InnoDB特性（例如外键）的表不适用。

综上所述，任何一种表都不是万能的，只有恰当的针对业务类型来选择合适的表类型，才能最大的发挥MySQL的性能优势。