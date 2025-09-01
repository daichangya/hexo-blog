---
title: Java的Lock小结
id: 664
date: 2024-10-31 22:01:45
author: daichangya
excerpt: '多核时代

  摩尔定律告诉我们：当价格不变时，集成电路上可容纳的晶体管数目，约每隔18个月便会增加一倍，性能也将提升一倍。换言之，每一美元所能买到的电脑性能，将每隔18个月翻两倍以上。然而最近摩尔定律似乎遇到了麻烦，目前微处理器的集成度似乎到了极限，在目前的制造工艺和体系架构下很难再提高单个处理器的速度了，否则它就被烧坏了。所以现在的芯片制造商改变了策略，转而在一个电路板上集成更多的'
permalink: /archives/Java-de-Lock-xiao-jie/
categories:
- 多线程-并发
---

### 多核时代

      摩尔定律告诉我们：当价格不变时，集成电路上可容纳的晶体管数目，约每隔18个月便会增加一倍，性能也将提升一倍。换言之，每一美元所能买到的电脑性能，将每隔18个月翻两倍以上。然而最近摩尔定律似乎遇到了麻烦，目前微处理器的集成度似乎到了极限，在目前的制造工艺和体系架构下很难再提高单个处理器的速度了，否则它就被烧坏了。所以现在的芯片制造商改变了策略，转而在一个电路板上集成更多的处理器，也就是我们现在常见的多核处理器。

      这就给软件行业带来麻烦（也可以说带来机会，比如说就业机会，呵呵）。原来的情况是：我买一台频率比原来快一倍的处理器，那么我的程序就比原来快一倍，软件工程师什么也不用干。现在不一样了，我买一台双核的处理器，我的程序和原来一样慢，当然这条机器同时处理的任务可以变多了，但是对于单个任务来说并没有帮助。

      在几年前，并发(Concurrent)和并行(Paralleling)程序设计还是在少量的地方使用，现在在个人的PC机上已经是很常见了。（**Concurrency** and **parallelism**的区别参考 [这个帖子](http://stackoverflow.com/questions/1050222/concurrency-vs-parallelism-what-is-the-difference)）

      造个诸葛亮的价钱远远高于造三个臭皮匠！多核是在一台机器上的并发，但是单机也是会到极限，所以分布式的计算也是类似的思路，用大量普通的机器协作完成一项任务。

      但是要想编写一个正确并且高效的能利用多核的多线程程序不是件容易的是，更别说分布式的情况（网络问题，机器故障，负载均衡，。。。）。现在的编译器没有办法把单线程的程序自动编译成一个多线程的版本（如果到了那一天，估计所有的程序员就失业了）。所以只能提供一些语言上的支持（比如scala/erlang)或者mapreduce这样的框架。

      Java虽然没有提供scala那样的基于消息的模型，但是也提供了丰富的concurrent特性，并且屏蔽了平台的相关性（这不是件容易的事，比如多个处理器有自己的缓存，他们写的东西不会离开被其它处理器看到），下面我们看看java的内存模型(JMM)

### JMM([Java Memory Model](http://java.sun.com/docs/books/jls/third_edition/html/memory.html))

     并行程序有很多模型，比如共享内存模型，消息传递模型等等。这些模型或多或少的利用了平台相关的特性（在并行程序设计里很难回避平台的特性以便高效的通信），Java抽象出了自己的内存模型，使得开放人员看不到平台的差异（这不是件容易的事），不过即使这样，和传统程序不同，我们还是不能完全不了解一些体系架构的细节问题，至少我们得了解一些。

     在共享内存的多处理器体系架构里（我们现在用的服务器甚至笔记本都是），每个处理器都有自己的局部缓存并定期的使之与内存同步。不同的处理器架构保证了不同程度的缓存一致性(cache coherence)，所以操作系统，编译器和运行时环境必须一起努力来弥补平台的差异性。

      让每个处理器都知道其它处理器的状态的代价是非常昂贵的，所以大多数架构都不会保证一致性，这通常不会有什么问题：进程/线程直接并不共享信息，编译器可以调整代码执行顺序以便提高效率，我们都很开心。当然也有需要在线程之间进行同步的时候，比如某个线程要读取到另一个线程写入的信息，这个时候缓存里的数据就得同步到内存里才行。所以这些体系架构都提供了一些指令来完成数据的同步（当然这些指令是非常费时的，能不做就尽量不做）。这些指令一般叫做memory barriers or fences。当然只是很底层的一些东西，所幸Java提供了一些高层的抽象，让我们的生活变得容易一些。

**     sequential consistency： 我们假设一个线程执行（可能在多个处理器上切换），每个变量读取到的值都是最新的修改（也就是Cache里的立马生效），这样得到的结果是我们预期的。**

     但是让我们意外的事情是：如果我们不做任何事情，那么很可能会出现错误，比如下面的这个例子：     

```
public class NoVisibility {
    private static boolean ready;
    private static int number;
 
    private static class ReaderThread extends Thread {
        public void run() {
            while (!ready)
                Thread.yield();
            System.out.println(number);
        }
    }
 
    public static void main(String[] args) {
        new ReaderThread().start();
        number = 42;
        ready = true;
    }
}
```

     我们在主线程里先让number=42(初始值是0)，然后让ready=true，而另一个线程不断坚持是否ready，如果ready，那么读出number。很自然的我们期望子线程打印出42，但是很可能结果会另我们失望。编译器可能会调换number=42  和  ready=true的顺序（思考一下为什么它要这么干？为什么在单线程的情况下没有问题？），另外子线程可能永远在while里死循环。为什么？子线程会永远看不到ready的变化？这也许让很多人吃惊，事实确实如此，JSR并不保证这一点（虽然大多数时候子线程能够退出），参考[这个帖子](http://stackoverflow.com/questions/4934913/are-static-variables-shared-between-threads)和[JMM的文章](http://www.cs.umd.edu/~pugh/java/memoryModel/jsr-133-faq.html)

#### vilatile和snychronized（intrinsic Lock）

     vilatile关键字告诉编译器，一个线程对某个变量的修改立即对所有其它线程看见，加上这个能保证上面的程序不会死循环。但是不能保证读到42，也就是保证number=42和ready=true的执行顺序，要保证这点就要用到synchronized。

     synchronized能够保证执行的顺序，除此之外，它也能保证可见性。

```
public class NoVisibility {
    private static boolean ready;
    private static int number;
 
    private static class ReaderThread extends Thread {
        public void run() {
            boolean r=false;
            while (true){
                synchronized(NoVisibility.class){
                    r=ready;
                }
                if(r) break;
                else  Thread.yield();
            }    
            System.out.println(number);
        }
    }
 
    public static void main(String[] args) {
        new ReaderThread().start();
        synchronized(NoVisibility.class){
            number = 42;
            ready = true;
        }
    }
}
```

```
synchronized(NoVisibility.class){
       number = 42;
       ready = true;
 }
```

这段代码保证了两个语句的执行顺序

```
synchronized(NoVisibility.class){
       r=ready;        
}
```

这保证子线程能看到ready的变化 注意他们必须synchronized同一个对象，如果是下面的代码，则不能有任何保障。为什么？试想任何synchronized里的变量必须立即对所有的可见，那么代价太大， 比如我有这样的需求：我只要求两个语句顺序执行，它是否对别人可见我并不关心。

```
synchronized(AnotherObject){
       r=ready;        
}
```

每个对象都有个Monitor，所以synchronized也经常叫Monitor Lock，另外这个锁是语言内置的，所以也叫Intrinsic Lock。 这两个关键字是java1.5之前就有了，在java1.5之后新引进了java.util.concurrent包，这里有我们需要关注的很多东西，这里我们只关心Lock相关的接口和类。 不过synchronized来解决互斥不是很完美吗？我为什么要花力气搞这些新鲜东西呢？下面我们来看看synchronized解决不了（或者很难解决）的问题

#### 银行转账的例子

```
// Warning: deadlock-prone!
public void transferMoney(Account fromAccount,
                          Account toAccount,
                          DollarAmount amount)
        throws InsufficientFundsException {
    synchronized (fromAccount) {
        synchronized (toAccount) {
            if (fromAccount.getBalance().compareTo(amount) < 0)
                throw new InsufficientFundsException();
            else {
                fromAccount.debit(amount);
                toAccount.credit(amount);
            }
        }
    }
}
```

比如我要在两个用户之间转账，为了防止意外，我必须同时锁定两个账户。但是这可能造成死锁。比如：

```
A: transferMoney(myAccount, yourAccount, 10);
B: transferMoney(yourAccount, myAccount, 20);
```

当线程A锁住myAccount时，B锁住了toAccount，这个时候A尝试锁住toAccount，但是已经被B锁住，所以A不能继续运行，同理B也不能运行，造成死锁。

怎么解决呢？你也许回想，我先锁住一个账户，然后"尝试"锁定另一个账户，如果“失败”，那么我释放所有的锁，“休息”一下再继续尝试，当然两个线程节拍一致的话，可能造成“活锁”

可惜synchronized不能提供这样的语义，它一旦尝试加锁，只能拿到锁，你不能控制它，比如你可能有这样的需求：尝试拿锁30s，如果拿不到就算了，synchronized是没办法满足这样的需求的。另外你使用“鸵鸟”策略来解决死锁：什么也不干，如果死锁了，kill他们，重启他们。这种策略看起来很疯狂，不过如果死锁的概率很多，而避免死锁的算法很复杂，那这也是可以一试的策略（那一堆死锁发生的充分必要条件太麻烦了！！！）。下面我们仔细的来看看java1.5后提供的Lock接口及其相关类。

#### [Lock接口](http://download.oracle.com/javase/6/docs/api/java/util/concurrent/locks/Lock.html)

    Lock的基本用法如下，为了防止异常退出时没有释放锁，一般都在拿到锁后立马try，try住所有临界区的代码，然后finally释放锁。

    主要和synchronized的区别，synchronized里我们不用操心这些，如果synchronized保护的代码抛出异常，那么jvm会释放掉Monitor Lock。

```
     Lock l = ...
     l.lock();
     try {
         // access the resource protected by this lock
     } finally {
         l.unlock();
     }
```

  Lock.lock()在锁定成功后释放锁之前，它所保护的代码段必须与使用synchronized保护的代码段有相同的语义（可见性，顺序性）。

  所以从这个角度来说，Lock完全可以代替synchronized，那么是否应该抛弃掉synchronized呢？答案是否定的。

#####   是否应该抛弃synchronized？

   在java5引进Lock后，实现了Lock接口的类就是ReentrantLock（呆会再解释Reentrant），因为java5之前synchronized的实现很烂，同样是为了实现互斥，ReentrantLock会比synchronized速度上快很多，不过到了jdk6之后就不是这样了，下面是一个测试结果： ![](http://wiki.corp.qunar.com/download/attachments/9343688/pic1.JPG?version=1&modificationDate=1316166342211)  
   from book "Java Concurrency in Practice"  
  横轴是线程数，纵轴是ReentrantLock的吞吐量/IntrinsicLock的吞吐量。

  可以看出，jdk5中，ReentrantLock快很多，但是到了jdk6，他们就没什么大的差别了。

**  synchronized的优点**：锁的释放是语言内置的，不会出现忘记释放锁的情况，另外由于是语言内置的支持，调试是能很快知道锁被哪个线程持有，它加锁的次数。而Lock只是util.concurrent一个普通的类，所以调试器并不知道这个锁的任何信息，它只是一个普通的对象（当然你可以仔细观察每个线程的stack frame来看它在等待锁）。

  所以建议：**如果只是为了实现互斥，那么使用synchronized**（扔掉jdk5吧，现在都java7了），**如果想用Lock附加的功能，那么才使用Lock**。

  下面回来继续看Lock接口。  

#### Interface Lock

```
public interface Lock {
    void lock();
    void lockInterruptibly() throws InterruptedException;
    boolean tryLock();
    boolean tryLock(long timeout, TimeUnit unit)
        throws InterruptedException;
    void unlock();
    Condition newCondition();
}
```

#####   void lock();   

      尝试获取锁。如果锁被别人拿着，那么当前线程不在执行，也不能被调度，直到拿到锁为止。

#####   void lockInterruptibly() throws InterruptedException

      尝试获取锁，除非被interrupted。如果锁可以获取，那么立刻返回。

      如果无非获取锁，那么线程停止执行，并且不能被再调度，直到：

*     当前线程获得锁
*     **如果锁的实现支持interruption**，并且有其它线程interrupt当前线程。

      仔细阅读javadoc的第二个情况：Lock接口并不要求Lock的实现支持interruption，不过sun jdk的实现都是支持的。  
      这个函数在下面两个情况下抛出InterruptedException：

*     **如果锁的实现支持interruption**，并且有其它线程interrupt当前线程。
*     线程调用这个函数之前就被设置了interrupted状态位

      可以发现这个方法并不区分这个interrupted状态位是之前就有的还是lock过程中产生的。不管如果，抛出异常后会清除interrupted标记。

      使用这个方法，我们可以中断某个等锁的线程，比如我们检测到了死锁，那么我们可以中断这个线程。      

#####    boolean tryLock()

       尝试获取锁，如果可以，那么锁住对象然后返回true，否则返回false，不管怎么样，这个方法会立即返回。下面的例子展示了用这个方法来解决前面转账的死锁：

```
public boolean transferMoney(Account fromAcct,
                             Account toAcct,
                             DollarAmount amount,
                             long timeout,
                             TimeUnit unit)
        throws InsufficientFundsException, InterruptedException {
    long fixedDelay = getFixedDelayComponentNanos(timeout, unit);
    long randMod = getRandomDelayModulusNanos(timeout, unit);
    long stopTime = System.nanoTime() + unit.toNanos(timeout);
 
    while (true) {
        if (fromAcct.lock.tryLock()) {
            try {
                if (toAcct.lock.tryLock()) {
                    try {
                        if (fromAcct.getBalance().compareTo(amount)
                                < 0)
                            throw new InsufficientFundsException();
                        else {
                            fromAcct.debit(amount);
                            toAcct.credit(amount);
                            return true;
                        }
                    } finally {
                        toAcct.lock.unlock();
                    }
                 }
             } finally {
                 fromAcct.lock.unlock();
             }
         }
         if (System.nanoTime() < stopTime)
             return false;
         NANOSECONDS.sleep(fixedDelay + rnd.nextLong() % randMod);
     }
}
```

##### tryLock  boolean tryLock(long time, TimeUnit unit) throws InterruptedException

    和tryLock类似，不过不是立即返回，而是尝试一定时间后还拿不到锁就返回。

##### unlock

    释放锁

##### newCondition

     暂且不管

#### Class ReentrantLock

     这是sun jdk（open jdk）里唯一直接实现了Lock接口的类，所以如果你想用Lock的那些特性，比如tryLock，那么就应该首先考虑它。

     首先我们解释一下Reentrant。

      Reentrant翻译成中文应该是“可重入”，对于锁来说，可重入是指如果一个线程已经拿到过一把锁，那么它可以再次拿到锁。

      听起来似乎没有什么意思，让我们来看看“不可重入”锁可能的一些问题和需要使用”可重入“锁的场景吧。

```
public class Widget {
    public synchronized void doSomething() {
        ...
    }
}
 
public class LoggingWidget extends Widget {
    public synchronized void doSomething() {
        System.out.println(toString() + ": calling doSomething");
        super.doSomething();
    }
}
 
 
 
Widget widget=new LoggingWidget();
 
widget.doSomething();
```

       设想这样一个应用场景：我们有一个图的数据结构，我们需要遍历所有节点，找到满足某些条件的节点，锁定所有这些节点，然后对他们进行一些操作。由于图的遍历可能重复访问某个节点，如果简单的锁定每个满足条件的节点，那么可能死锁。当然我们可以自己用程序记下哪些节点已经访问过了，不过也可以把这就事情交给ReentrantLock，第二次锁定某个对象也会成功并立即返回。那么你可能会问，我释放锁的时候怎么记得它锁定过了多少次呢？如果释放少了，那么会死锁；释放多了，可能也会有问题（有些锁实现会抛出异常，但是JMM好像没有定义）。

       【上面的场景参考[http://stackoverflow.com/questions/1312259/what-is-the-re-entrant-lock-and-concept-in-general](http://stackoverflow.com/questions/1312259/what-is-the-re-entrant-lock-and-concept-in-general)】

       不用担心，ReentrantLock提供了getHoldCount方法，最后释放这么多次就好了。

       ReentrantLock会记下当前拿锁的线程，已经拿锁的次数，每次unlock都会减一，如果为零了，那么释放锁，另一个线程拿到锁并且计数器值为一。

       ReentrantLock的构造函数可以接受一个fairness的参数。如果为true，那么它会倾向于把锁给等待时间最长的线程。但是这样的代价也是巨大的：

             ![](http://wiki.corp.qunar.com/download/attachments/9343688/pic2.JPG?version=1&modificationDate=1316170951730)  
             横轴是并发线程数，参考方法是ConcurrentHashMap，另外分别用Nonfair Lock和 fair Lock封装普通的HashMap，可以看到，是否fair的差别是非常巨大的。  
           正如前面所说的，ReentrantLock是支持Interrupted的。

#### Interface ReadWriteLock

         有的应用场景下，有两类角色：Reader和Writer。Reader读取数据，Writer更新数据。多个Reader同时读取是没有问题的，但是Reader们和Writer是互斥的，并且Writer和Writer也是互斥的。而且很多应用中，Reader会很多，而Writer会比较少。这个接口就是为了解决这类特殊场景的。

```
public interface ReadWriteLock {
    Lock readLock();
    Lock writeLock();
}
 
用法：
ReadWriteLock rwl = ...;
//Reader threads
read(){
   rwl.readLock().lock();
   try{
      //entering critical setion
   }finally{
       rwl.readLock().unlock();
   }
}
write(){   rwl.writeLock().lock();   try{      //entering critical setion   }finally{       rwl.writeLock().unlock();   }}

 
```

####  Class ReentrantReadWriteLock

         这是Sun jdk里唯一实现ReadWriteLock接口的类。

         这个类的特性：

######            获取锁的顺序

                  这个类并不倾向Reader或者Writer，不过有个fairness的策略

######            非公平模式（默认）

                 如果很多Reader和Writer的话，很可能Reder一直能获取锁，而Writer可能会饥饿

######             公平模式

                 这种模式下，会尽量以请求锁的顺序来保证公平性。当前锁释放以后，等待时间最长的Writer或者一组Reader（Reader是一伙的！）获取锁。

                 如果锁被拿着，这时Writer来了，他会开始排队；如果Reader来了，如果它之前没有Writer并且当前拿锁的是Reader，那么它直接就拿到锁，当然如果是Writer拿着，那么它也只能排

                 队等锁。 不过如果Reader拿着锁，Writer排队，然后Reader排在Writer后，但是Writer放弃了排队（比如它用的是tryLock 30s），那么Reader直接拿到锁而不用排队。

                 还有就是ReentrantReadWriteLock.ReadLock.tryLock() 和 ReentrantReadWriteLock.WriteLock.tryLock()方法不管这些，一旦调用的时候能拿到锁，那么它们就会插队！！

######             Reentrancy

                 从名字就知道它支持可重入。

                 以前拿过锁的Reader和Writer可以继续拿锁。另外拿到WriteLock的线程可以拿到ReadLock，但是反之不然。

######             Lock downgrading

                  拿到WriteLock的可以直接变成ReadLock，不用释放WriteLock再从新请求ReadLock（这样需要重新排队），实现的方法是先拿到WriteLock，接着拿ReadLock（上面的特性保证了不会死锁），然后释放WriteLock，这样就得到一个ReadLock并立马持有。

######            **Interruption of lock acquisition**

**                  支持**

     ** 一个使用读写锁的例子            **            

```
class CachedData {
   Object data;
   volatile boolean cacheValid;
   ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
 
   void processCachedData() {
     rwl.readLock().lock();
     if (!cacheValid) {
        // Must release read lock before acquiring write lock
        rwl.readLock().unlock();
        rwl.writeLock().lock();
        // Recheck state because another thread might have acquired
        //   write lock and changed state before we did.
        if (!cacheValid) {
          data = ...
          cacheValid = true;
        }
        // Downgrade by acquiring read lock before releasing write lock
        rwl.readLock().lock();
        rwl.writeLock().unlock(); // Unlock write, still hold read
     }
 
     use(data);
     rwl.readLock().unlock();
   }
 }
```

    一个Cache数据的例子，读取数据时首先拿读锁，如果cache是有效的（volatile boolean cacheValid），直接使用数据。

    如果失效了，那么释放读锁，获取写锁【这个类不支持upgrading】，然后double check一下是否cache有效，如果还是无效（说明它应该更新），那么更新数据，并且修改变量cacheValid，让其它线程看到。

#####    臭名昭著的double check

     前面提到了double check，这里也顺便讨论一下：

```
@NotThreadSafe
public class DoubleCheckedLocking {
    private static Resource resource;
 
    public static Resource getInstance() {
        if (resource == null) {
            synchronized (DoubleCheckedLocking.class) {
                if (resource == null)
                    resource = new Resource();
            }
        }
        return resource;
    }
}
```

很多“hacker”再提到延迟加载的时候都会提到它，上面的代码看起来没有什么问题：首先检查一些resource，如果为空，那么加锁，因为检查resource==null没有加锁，所以可能同时两个线程进入if并且请求加锁，所以第一个拿到锁的初始化一次，第二次拿锁的会再次check。这看起来很完美：大多数情况下resouce不为空，很少的情况（刚开始时）resource为空，那么再加锁，这比一上来就加锁要高效很多。

不过千万别高兴地太早了，因为编译器对引用的赋值可能会做优化，可能这个对象还没有正确的构造好，值已经赋好了（为什么要这么做？也许构造对象需要IO，io等待的时间把值赋好了能提高速度）。这个时候别的线程就惨了！

另外很多讲延迟加载的文章都比较早（早于jdk6），那个年代java的synchronized确实很不给力。如果你实在在乎这点性能的话，应该用jvm的静态类加载机制来实现：

```
@ThreadSafe
public class ResourceFactory {
     private static class ResourceHolder {
         public static Resource resource = new Resource();
     }
 
     public static Resource getResource() {
         return  ResourceHolder.resource ;
     }
}
```