---
title: 从InputStream到ByteArrayInputStream
id: 879
date: 2024-10-31 22:01:47
author: daichangya
excerpt: "本篇主要分析：1.如何将byte数组适配至ByteArrayInputStream，对应与IO部分的适配器模式；2.BufferedInputStream的工作原理，对应于IO的装饰器模式，会首先研究InputStream和FilterInputStream的源代码，同时会将要谈谈软件设计中的缓存相关的知识。后面专门一章分析PipedInputStream和PipedOutStream，简单谈谈管"
permalink: /archives/9319775/
categories:
 - java基础
 - java源码分析
---

本篇主要分析：1.如何将byte数组适配至ByteArrayInputStream，对应与IO部分的适配器模式；2.BufferedInputStream的工作原理，对应于IO的装饰器模式，会首先研究InputStream和FilterInputStream的源代码，同时会将要谈谈软件设计中的缓存相关的知识。后面专门一章分析PipedInputStream和PipedOutStream，简单谈谈管道相关的知识，以及软件架构的想法。
### 1 InputStream
InputStream 是输入字节流部分，装饰器模式的顶层类。主要规定了输入字节流的公共方法。
```
package java.io;
public abstract class InputStream implements Closeable {
    private static final int SKIP\_BUFFER\_SIZE = 2048;  //用于skip方法，和skipBuffer相关
    private static byte[] skipBuffer;    // skipBuffer is initialized in skip(long), if needed.
public abstract int read() throws IOException;  //从输入流中读取下一个字节，
                                                                                             //正常返回0-255，到达文件的末尾返回-1
                                                        //在流中还有数据，但是没有读到时该方法会阻塞（block）
                                                        //Java IO和New IO的区别就是阻塞流和非阻塞流
                                                        //抽象方法哦！不同的子类不同的实现哦！
         //将流中的数据读入放在byte数组的第off个位置先后的len个位置中
         //放回值为放入字节的个数。
   public int read(byte b[], int off, int len) throws IOException {           //
         if (b == null) {
             throw new NullPointerException();
         } else if (off < 0 || len < 0 || len > b.length - off) {
             throw new IndexOutOfBoundsException();
         } else if (len == 0) {
             return 0;
         }        //检查输入是否正常。一般情况下，检查输入是方法设计的第一步
         int c = read();                                                              //读取下一个字节
         if (c == -1) {    return -1;   }                           //到达文件的末端返回-1
         b[off] = (byte)c;                                                   //放回的字节downcast
         int i = 1;                                                                        //已经读取了一个字节
         try {
             for (; i < len ; i++) {                          //最多读取len个字节，所以要循环len次
                   c = read();                                       //每次循环从流中读取一个字节
                                                                                    //由于read方法阻塞，
//所以read(byte[],int,int)也会阻塞
                   if (c == -1) {            break;           }       //到达末尾，理所当然放回-1
                   b[off + i] = (byte)c;                                    //读到就放入byte数组中
             }
         } catch (IOException ee) {     }
         return i;
         //上面这个部分其实还有一点比较重要，int i = 1;在循环的外围，或许你经常见到，
         //或许你只会在循环是才声明，为什么呢？
         //声明在外面，增大了变量的生存周期（在循环外面），所以后面可以return返回
         //极其一般的想法。在类成员变量生命周期中使用同样的理念。
         //在软件设计中，类和类的关系中也是一样的。
    }        //这个方法在利用抽象方法read，某种意义上简单的Templete模式。
    public int read(byte b[]) throws IOException {
                   return read(b, 0, b.length);
    }                           //利用上面的方法read(byte[] b)
    public long skip(long n) throws IOException {
         long remaining = n;                                  //方法内部使用的、表示要跳过的字节数目，
//使用它完成一系列字节读取的循环
         int nr;
         if (skipBuffer == null)
             skipBuffer = new byte[SKIP\_BUFFER\_SIZE];                   //初始化一个跳转的缓存
         byte[] localSkipBuffer = skipBuffer;                                      //本地化的跳转缓存
         if (n <= 0) {    return 0;      }                           //检查输入参数，应该放在方法的开始
         while (remaining > 0) {                                      //一共要跳过n个，每次跳过部分，循环
             nr = read(localSkipBuffer, 0, (int) Math.min(SKIP\_BUFFER\_SIZE, remaining));
                                                        //利用上面的read(byte[],int,int)方法尽量读取n个字节
             if (nr < 0) {  break;    }                          //读到流的末端，则返回
             remaining -= nr;                                       //没有完全读到需要的，则继续循环
         }       
         return n - remaining;//返回时要么全部读完，要么因为到达文件末端，读取了部分
    }
    public int available() throws IOException {                  //查询流中还有多少可以读取的字节
                   return 0;
    }
         //该方法不会block。在java中抽象类方法的实现一般有以下几种方式：
//1.抛出异常（java.util）；2.“弱”实现。象上面这种。子类在必要的时候覆盖它。
//3.“空”实现。下面有例子。
    public void close() throws IOException {}
         //关闭当前流、同时释放与此流相关的资源
    public synchronized void mark(int readlimit) {}
         //在当前位置对流进行标记，必要的时候可以使用reset方法返回。
         //markSupport可以查询当前流是否支持mark
    public synchronized void reset() throws IOException {
                   throw new IOException("mark/reset not supported");
    }
         //对mark过的流进行复位。只有当流支持mark时才可以使用此方法。
//看看mark、available和reset方法。体会为什么？！
    public boolean markSupported() {           //查询是否支持mark
                   return false;
    }                 //绝大部分不支持，因此提供默认实现，返回false。子类有需要可以覆盖。
}
```
	
### 2 FilterInputStream
这是字节输入流部分装饰器模式的核心。是我们在装饰器模式中的Decorator对象，主要完成对其它流装饰的基本功能。下面是它的源代码:
```
package java.io;
//该类对被装饰的流进行基本的包裹。不增加额外的功能。
//客户在需要的时候可以覆盖相应的方法。具体覆盖可以在ByteInputStream中看到！
public class FilterInputStream extends InputStream {
    protected volatile InputStream in;                       //将要被装饰的字节输入流
    protected FilterInputStream(InputStream in) {   //通过构造方法传入此被装饰的流
                   this.in = in;
    }
         //装饰器的代码特征：被装饰的对象一般是装饰器的成员变量
         //上面几行可以看出。
         //下面这些方法，完成最小的装饰――0装饰，只是调用被装饰流的方法而已
    public int read() throws IOException {
                   return in.read();
    }
    public int read(byte b[]) throws IOException {
                   return read(b, 0, b.length);
    }
    public int read(byte b[], int off, int len) throws IOException {
                   return in.read(b, off, len);
    }
    public long skip(long n) throws IOException {
                   return in.skip(n);
    }
    public int available() throws IOException {
                   return in.available();
    }
    public void close() throws IOException {
                   in.close();
    }
    public synchronized void mark(int readlimit) {
                   in.mark(readlimit);
    }
    public synchronized void reset() throws IOException {
                   in.reset();
    }
    public boolean markSupported() {
                   return in.markSupported();
}
//以上的方法，都是通过调用被装饰对象in完成的。没有添加任何额外功能
//装饰器模式中的Decorator对象，不增加被装饰对象的功能。
//它是装饰器模式中的核心。更多关于装饰器模式的理论请阅读博客中的文章。
}
```
以上分析了所有字节输入流的公共父类InputStream和装饰器类FilterInputStream类。他们是装饰器模式中两个重要的类。更多细节请阅读博客中装饰器模式的文章。下面将讲解一个具体的流ByteArrayInputStream，不过它是采用适配器设计模式。
### 3 ByteArray到ByteArrayInputStream的适配
```
// ByteArrayInputStream内部有一个byte类型的buffer。
//很典型的适配器模式的应用――将byte数组适配流的接口。
//下面是源代码分析：
package java.io;
public class ByteArrayInputStream extends InputStream {
    protected byte buf[];                //内部的buffer，一般通过构造器输入
protected int pos;                   //当前位置的cursor。从0至byte数组的长度。
//byte[pos]就是read方法读取的字节
    protected int mark = 0;           //mark的位置。
    protected int count;                          //流中字节的数目。不一定与byte[]的长度一致？？？
    public ByteArrayInputStream(byte buf[]) {//从一个byte[]创建一个ByteArrayInputStream
         this.buf = buf;                                                      //初始化流中的各个成员变量
        this.pos = 0;
         this.count = buf.length;                              //count就等于buf.length
    }
    public ByteArrayInputStream(byte buf[], int offset, int length) {                //构造器
         this.buf = buf;
        this.pos = offset;                                                                                      //与上面不同
         this.count = Math.min(offset + length, buf.length);
        this.mark = offset;                                                                                             //与上面不同
    }
    public synchronized int read() {                                           //从流中读取下一个字节
                   return (pos < count) ? (buf[pos++] & 0xff) : -1; //返回下一个位置的字节
                                                                                                                //流中没有数据则返回-1
    }
         //下面这个方法很有意思！从InputStream中可以看出其提供了该方法的实现。
         //为什么ByteArrayInputStream要覆盖此方法呢？
         //同样的我们在Java Collections Framework中可以看到：
//AbstractCollection利用iterator实现了Collecion接口的很多方法。但是，
//在ArrayList中却有很多被子类覆盖了。为什么如此呢？？
    public synchronized int read(byte b[], int off, int len) {
         if (b == null) {                                                               //首先检查输入参数的状态是否正确
             throw new NullPointerException();
         } else if (off < 0 || len < 0 || len > b.length - off) {
             throw new IndexOutOfBoundsException();
         }
         if (pos >= count) {             return -1;             }
         if (pos + len > count) {      len = count - pos;         }
         if (len <= 0) {           return 0;     }
         System.arraycopy(buf, pos, b, off, len);                     //java中提供数据复制的方法
         pos += len;
         return len;
    }
         //出于速度的原因！他们都用到System.arraycopy方法。想想为什么？
         //某些时候，父类不能完全实现子类的功能，父类的实现一般比较通用。
//当子类有更有效的方法时，我们会覆盖这些方法。这样可是不太OO的哦！
         //下面这个方法，在InputStream中也已经实现了。
//但是当时是通过将字节读入一个buffer中实现的，好像效率低了一点。
//看看下面这段代码，是否极其简单呢？！
    public synchronized long skip(long n) {
         if (pos + n > count) {    n = count - pos;       }        //当前位置，可以跳跃的字节数目
         if (n < 0) {       return 0;     }                                    //小于0，则不可以跳跃
         pos += n;                                                                              //跳跃后，当前位置变化
         return n;
    }                                    //比InputStream中的方法简单、高效吧！
    public synchronized int available() {
                   return count - pos;
    }
         //查询流中还有多少字节没有读取。
//在我们的ByteArrayInputStream中就是当前位置以后字节的数目。
    public boolean markSupported() {                   
                   return true;
    }        //ByteArrayInputStream支持mark所以返回true
    public void mark(int readAheadLimit) {            
                   mark = pos;
    }
//在流中当前位置mark。
//在我们的ByteArrayInputStream中就是将当前位置赋给mark变量。
//读取流中的字节就是读取字节数组中当前位置向后的的字节。
    public synchronized void reset() {
                   pos = mark;
    }
         //重置流。即回到mark的位置。
    public void close() throws IOException {   }
         //关闭ByteArrayInputStream不会产生任何动作。为什么？仔细考虑吧！！
}
```
上面我们分3小节讲了装饰器模式中的公共父类（对应于输入字节流的InputStream）、Decorator（对应于输入字节流的FilterInputStream）和基本被装饰对象（对应于输入字节流的媒体字节流）。下面我们就要讲述装饰器模式中的具体的包装器（对应于输入字节流的包装器流）。
### 4 BufferedInputStream
#### 4.1原理及其在软件硬件中的应用

       1.read――read(byte[] ,int , int)
       2.BufferedInputStream
       3.《由一个简单的程序谈起》
       4\. Cache
       5.Pool
       6.Spling Printer

（最近比较忙，不讲了！）
#### 4.2 BufferedInputStream源代码分析
```
	package java.io;
import java.util.concurrent.atomic.AtomicReferenceFieldUpdater;
//该类主要完成对被包装流，加上一个缓存的功能
public class BufferedInputStream extends FilterInputStream {
    private static int defaultBufferSize = 8192;                                      //默认缓存的大小
    protected volatile byte buf[];                                                            //内部的缓存
    protected int count;                                                                                            //buffer的大小
    protected int pos;                                                                               //buffer中cursor的位置
    protected int markpos = -1;                                                                     //mark的位置
    protected int marklimit;                                                                            //mark的范围
//原子性更新。和一致性编程相关
    private static final
        AtomicReferenceFieldUpdater<BufferedInputStream, byte[]> bufUpdater =
        AtomicReferenceFieldUpdater.newUpdater (BufferedInputStream.class,  byte[].class, "buf");
    private InputStream getInIfOpen() throws IOException {  //检查输入流是否关闭，同时返回被包装流
        InputStream input = in;
         if (input == null)    throw new IOException("Stream closed");
        return input;
    }
    private byte[] getBufIfOpen() throws IOException {                       //检查buffer的状态，同时返回缓存
        byte[] buffer = buf;
         if (buffer == null)   throw new IOException("Stream closed");            //不太可能发生的状态
        return buffer;
    }
    public BufferedInputStream(InputStream in) {                               //构造器
                   this(in, defaultBufferSize);                                                              //指定默认长度的buffer
    }
    public BufferedInputStream(InputStream in, int size) {                           //构造器
                   super(in);
        if (size <= 0) {                                                                                         //检查输入参数
            throw new IllegalArgumentException("Buffer size <= 0");
        }
                   buf = new byte[size];                                                                     //创建指定长度的buffer
    }
         //从流中读取数据，填充如缓存中。
    private void fill() throws IOException {
        byte[] buffer = getBufIfOpen();                            //得到buffer
         if (markpos < 0)
             pos = 0;                                                             //mark位置小于0，此时pos为0
         else if (pos >= buffer.length)                               //pos大于buffer的长度
             if (markpos > 0) {        
                   int sz = pos - markpos;                            //
                   System.arraycopy(buffer, markpos, buffer, 0, sz);
                   pos = sz;
                   markpos = 0;
             } else if (buffer.length >= marklimit) {                 //buffer的长度大于marklimit时，mark失效
                   markpos = -1;                                                   //
                   pos = 0;                                                             //丢弃buffer中的内容
             } else {                                                                         //buffer的长度小于marklimit时对buffer扩容
                   int nsz = pos * 2;
                   if (nsz > marklimit)           nsz = marklimit;//扩容为原来的2倍，太大则为marklimit大小
                   byte nbuf[] = new byte[nsz];                    
                   System.arraycopy(buffer, 0, nbuf, 0, pos);        //将buffer中的字节拷贝如扩容后的buf中
                if (!bufUpdater.compareAndSet(this, buffer, nbuf)) {
//在buffer在被操作时，不能取代此buffer
                    throw new IOException("Stream closed");
                }
                buffer = nbuf;                                                               //将新buf赋值给buffer
             }
        count = pos;
         int n = getInIfOpen().read(buffer, pos, buffer.length - pos);
        if (n > 0)     count = n + pos;
    }
    public synchronized int read() throws IOException { //读取下一个字节
         if (pos >= count) {                                                                 //到达buffer的末端
             fill();                                                                    //就从流中读取数据，填充buffer
             if (pos >= count)  return -1;                                //读过一次，没有数据则返回-1
         }
         return getBufIfOpen()[pos++] & 0xff;                           //返回buffer中下一个位置的字节
    }
    private int read1(byte[] b, int off, int len) throws IOException {                 //将数据从流中读入buffer中
         int avail = count - pos;                                                                             //buffer中还剩的可读字符
         if (avail <= 0) {                                                                                        //buffer中没有可以读取的数据时
             if (len >= getBufIfOpen().length && markpos < 0) {             //将输入流中的字节读入b中
                   return getInIfOpen().read(b, off, len);
             }
             fill();                                                                                                //填充
             avail = count - pos;
             if (avail <= 0) return -1;
         }
         int cnt = (avail < len) ? avail : len;                                                  //从流中读取后，检查可以读取的数目
         System.arraycopy(getBufIfOpen(), pos, b, off, cnt);            //将当前buffer中的字节放入b的末端
         pos += cnt;
         return cnt;
    }
    public synchronized int read(byte b[], int off, int len)throws IOException {
        getBufIfOpen();                                                                             // 检查buffer是否open
        if ((off | len | (off + len) | (b.length - (off + len))) < 0) {            //检查输入参数是否正确
             throw new IndexOutOfBoundsException();
         } else if (len == 0) {
            return 0;
        }
         int n = 0;
        for (;;) {
            int nread = read1(b, off + n, len - n);
            if (nread <= 0)     return (n == 0) ? nread : n;
            n += nread;
            if (n >= len)     return n;
            // if not closed but no bytes available, return
            InputStream input = in;
            if (input != null && input.available() <= 0)     return n;
        }
    }
    public synchronized long skip(long n) throws IOException {
        getBufIfOpen();                                        // 检查buffer是否关闭
         if (n <= 0) {    return 0;      }                 //检查输入参数是否正确
         long avail = count - pos;                    //buffered中可以读取字节的数目
        if (avail <= 0) {                                          //可以读取的小于0，则从流中读取
            if (markpos <0)  return getInIfOpen().skip(n); //mark小于0，则mark在流中
            fill();                                  // 从流中读取数据，填充缓冲区。
            avail = count - pos;                                   //可以读的取字节为buffer的容量减当前位置
            if (avail <= 0)     return 0;
        }       
        long skipped = (avail < n) ? avail : n;      
        pos += skipped;                                       //当前位置改变
        return skipped;
    }
    public synchronized int available() throws IOException {
                   return getInIfOpen().available() + (count - pos);                 
    }
         //该方法不会block！返回流中可以读取的字节的数目。
         //该方法的返回值为缓存中的可读字节数目加流中可读字节数目的和
    public synchronized void mark(int readlimit) {  //当前位置处为mark位置
         marklimit = readlimit;
         markpos = pos;
    }
    public synchronized void reset() throws IOException {
        getBufIfOpen(); // 缓冲去关闭了，肯定就抛出异常！程序设计中经常的手段
                   if (markpos < 0)     throw new IOException("Resetting to invalid mark");
                   pos = markpos;
    }
    public boolean markSupported() {           //该流和ByteArrayInputStream一样都支持mark
                   return true;
    }
         //关闭当前流同时释放相应的系统资源。
    public void close() throws IOException {
        byte[] buffer;
        while ( (buffer = buf) != null) {
            if (bufUpdater.compareAndSet(this, buffer, null)) {
                InputStream input = in;
                in = null;
                if (input != null)    input.close();
                return;
            }
            // Else retry in case a new buf was CASed in fill()
        }
    }
}
```