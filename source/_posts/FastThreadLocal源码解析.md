---
title: FastThreadLocal源码解析
id: 1537
date: 2024-10-31 22:02:00
author: daichangya
permalink: /archives/fastthreadlocal%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/
categories:
 - netty
---



## 1\. 前言

netty自行封装了FastThreadLocal以替换jdk提供的ThreadLocal，结合封装的FastThreadLocalThread,在多线程环境下的变量提高了ThreadLocal对象的查询以及更新效率.  
下文，将通过对比ThreadLocal与FastThreadLocal，通过源码解析，探究FastThreadLocal与FastThreadLocalThread的搭配使用后性能的奥秘.

## 2\. ThreadLocalMap

ThreadLocalMap是TharedLocal中定义的静态类，其作用是保存Thared中引用的ThreadLocal对象.  
jdk中，每一个Thread对象中均会包含以下两个变量:

```java
public
class Thread implements Runnable {

    // 此处省略若干代码

    // 存储ThreadLocal变量，通过每个Thread存储一个ThreadLocalMap，实现了变量的线程隔离
    ThreadLocal.ThreadLocalMap threadLocals = null;

    ThreadLocal.ThreadLocalMap inheritableThreadLocals = null;
}

```

编程实践中，线程中可能包含多个ThreadLocal去进行引用，它们均保存在ThreadLocal.ThreadLocalMap threadLocals中(每个线程中均包含自己的ThreadLocalMap,避免多线程争用).

```java
 static class ThreadLocalMap {

        // 需要注意，此处Entry使用WeakReference
        (软引用),这样在资源紧张的时候可以回收部分不再引用的ThreadLocal变量
        static class Entry extends WeakReference<ThreadLocal<?>> {
            /** The value associated with this ThreadLocal. */
            Object value;

            Entry(ThreadLocal<?> k, Object v) {
                super(k);
                value = v;
            }
        }
        
        // ThreadLocal对象存储数组的初始化长度
        private static final int INITIAL_CAPACITY = 16;
        
        // ThreadLocal对象存储数组
        private Entry[] table;
        
        // 初始化ThreadLocalMap，使用数组存放ThreadLocal资源，使用ThreadLocal对象的threadLocalHashCode进行hash得到索引
        // 此处使用对象数组存放ThreadLocal对象，操作类似于HashMap，感兴趣的读者可以查看HashMap的源码进行比较
        ThreadLocalMap(ThreadLocal<?> firstKey, Object firstValue) {
            table = new Entry[INITIAL_CAPACITY];
            int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);
            table[i] = new Entry(firstKey, firstValue);
            size = 1;
            setThreshold(INITIAL_CAPACITY);
        }
        
        // 获取ThreadLocal对象，此处需要根据threadLocalHashCode进行hash操作得到索引
        private Entry getEntry(ThreadLocal<?> key) {
            int i = key.threadLocalHashCode & (table.length - 1);
            Entry e = table[i];
            if (e != null && e.get() == key)
                return e;
            else
                return getEntryAfterMiss(key, i, e);
        }
    }

```

由以上代码可知，在ThreadLocalMap初始化时，会创建一个对象数组.  
对象数组的初始长度为16，在后续的扩张中，数组长度会保持在2^n级别，以便进行hash操作确定ThradLocal对象的索引.  
在每次获取ThreadLocal对象的时候，会根据对象的threadLocalHashCode与对象数组长度减一的求与值，确定对象索引，从而快速获取value.

使用hash确定数组下标，存在以下几个问题：

*   解决hash冲突；
*   对象数组扩容带来的rehash.  
    ThreadLocal是jdk提供的通用类，在大部分场景下，线程中的ThreadLocal变量较少，因此hash冲突以及rehash较少.  
    即使,偶尔发生的hash冲突以及rehash，也不会给应用程序带来较大的性能损耗.

## 3\. FastThreadLocalThread

Netty对ThreadLocal改造为FastThreadLocal，以应对自身的大并发量，数据吞吐量大的应用场景.  
为了更好的使用，Netty亦继承Thread，构建了FastThreadLocalThread.  
当且仅当FastThreadLocal与FastThreadLocalThread合并使用，方能真正起到提速的作用.

```java
// 限于篇幅，省略较多函数
public class FastThreadLocalThread extends Thread {

    // 相对于Thread中使用ThreadLocal.ThreadLocalMap存放ThreadLocal资源，FastThreadLocalThread使用InternalThreadLocalMap存放ThreadLocal资源
    private InternalThreadLocalMap threadLocalMap;

    public final InternalThreadLocalMap threadLocalMap() {
        return threadLocalMap;
    }

    public final void setThreadLocalMap(InternalThreadLocalMap threadLocalMap) {
        this.threadLocalMap = threadLocalMap;
    }
    
    @UnstableApi
    public boolean willCleanupFastThreadLocals() {
        return cleanupFastThreadLocals;
    }

    @UnstableApi
    public static boolean willCleanupFastThreadLocals(Thread thread) {
        return thread instanceof FastThreadLocalThread &&
                ((FastThreadLocalThread) thread).willCleanupFastThreadLocals();
    }
}

```

由以上代码可以看出，相对于Thread,FastThreadLocalThread添加了threadLocalMap对象，以及threadLocalMap的清理标志获取函数.

ThreadLocal即使使用了WeakReference以保证资源释放，但是仍会存在内存泄漏可能.  
FastThreadLocalThread与FastThreadLocal均为Netty定制，可以在线程任务执行后，强制执行InternalThreadLocalMap的清理函数removeAll(详情见下文).

## 4\. FastThreadLocal

### 4.1 InternalThreadLocalMap

前情提要：

FastThreadLocalThread中声明了InternalThreadLocalMap对象threadLocalMap.

```java
public final class InternalThreadLocalMap extends UnpaddedInternalThreadLocalMap{
    
}

```

从以上代码可知，InternalThreadLocalMap继承于UnpaddedInternalThreadLocalMap.  
因此，我们需要先探究下UnpaddedInternalThreadLocalMap的定义.

```java
//
class UnpaddedInternalThreadLocalMap {

    // 如果在`Thread`中使用`FastThreadLocal`，则实际上使用`ThreadLocal`存放资源
    static final ThreadLocal<InternalThreadLocalMap> slowThreadLocalMap = new ThreadLocal<InternalThreadLocalMap>();
    // 资源索引，每一个FastThreadLocal对象都会有对应的ID，即通过nextIndex自增得到
    static final AtomicInteger nextIndex = new AtomicInteger();

    // FastThreadLocal的资源存放地址，ThreadLocal中是通过ThreadLocalMap存放资源，索引是ThreadLocal对象的threadLocalHashCode进行hash得到
    // FastThreadLocal使用Object[]数组，使用通过nextIndex自增得到的数值作为索引，保证每次查询数值都是O(1)操作
    // 需要注意，FastThreadLocal对象为了避免伪共享带来的性能损耗，使用padding使得FastThreadLocal的对象大小超过128byte
    // 避免伪共享的情况下，indexedVariables的多个连续数值在不更新的前提下可以被缓存至cpu chache line中，这样大大的提高了查询效率
    Object[] indexedVariables;

    // Core thread-locals
    int futureListenerStackDepth;
    int localChannelReaderStackDepth;
    Map<Class<?>, Boolean> handlerSharableCache;
    IntegerHolder counterHashCode;
    ThreadLocalRandom random;
    Map<Class<?>, TypeParameterMatcher> typeParameterMatcherGetCache;
    Map<Class<?>, Map<String, TypeParameterMatcher>> typeParameterMatcherFindCache;

    // String-related thread-locals
    StringBuilder stringBuilder;
    Map<Charset, CharsetEncoder> charsetEncoderCache;
    Map<Charset, CharsetDecoder> charsetDecoderCache;

    // ArrayList-related thread-locals
    ArrayList<Object> arrayList;

    // 构造函数，后续需要关注
    UnpaddedInternalThreadLocalMap(Object[] indexedVariables) {
        this.indexedVariables = indexedVariables;
    }
}

```

以上代码中，需要注意：

```java
    static final ThreadLocal<InternalThreadLocalMap> slowThreadLocalMap = new ThreadLocal<InternalThreadLocalMap>();

```

声明slowThreadLocalMap的原因在于，用户可能在Thread而非FastThreadLocalThread中调用FastThreadLocal.  
因此，为了保证程序的兼容性，声明此变量保存普通的ThreadLocal相关变量(具体使用详见后面说明).

```java

// 出于篇幅考虑，删除部分函数
public final class InternalThreadLocalMap extends UnpaddedInternalThreadLocalMap {

    private static final int DEFAULT_ARRAY_LIST_INITIAL_CAPACITY = 8;
    
    // 资源未赋值变质量
    public static final Object UNSET = new Object();

    // 获取ThreadLocal对象，此处会判断当前调用线程的类型分别调用不同的资源
    public static InternalThreadLocalMap getIfSet() {
        Thread thread = Thread.currentThread();
        if (thread instanceof FastThreadLocalThread) {
            return ((FastThreadLocalThread) thread).threadLocalMap();
        }
        return slowThreadLocalMap.get();
    }

    // 获取ThreadLocal对象，此处会判断当前调用线程的类型，从而判断调用fastGet或是slowGet
    public static InternalThreadLocalMap get() {
        Thread thread = Thread.currentThread();
        if (thread instanceof FastThreadLocalThread) {
            return fastGet((FastThreadLocalThread) thread);
        } else {
            return slowGet();
        }
    }

    // 如果当前调用FastThreadLocal对象的是FastThreadLocalThread，则调用FastThreadLocalThread的threadLocalMap对象获取相关资源
    private static InternalThreadLocalMap fastGet(FastThreadLocalThread thread) {
        InternalThreadLocalMap threadLocalMap = thread.threadLocalMap();
        if (threadLocalMap == null) {
            thread.setThreadLocalMap(threadLocalMap = new InternalThreadLocalMap());
        }
        return threadLocalMap;
    }

    // 如果当前调用FastThreadLocal对象的是Thread，则调用slowThreadLocalMap对象获取相关资源(slowThreadLocalMap其实是调用jdk提供的ThreadLocalMap)
    private static InternalThreadLocalMap slowGet() {
        ThreadLocal<InternalThreadLocalMap> slowThreadLocalMap = UnpaddedInternalThreadLocalMap.slowThreadLocalMap;
        InternalThreadLocalMap ret = slowThreadLocalMap.get();
        if (ret == null) {
            ret = new InternalThreadLocalMap();
            slowThreadLocalMap.set(ret);
        }
        return ret;
    }

    // 保证FastThreadLocal的实体对象大小超过128byte，以避免伪共享发生
    // 如果资源能够避免伪共享，则FastThreadLocal的实体对象能够部分缓存至L1缓存，通过提高缓存命中率加快查询速度(查询L1缓存的速度要远快于查询主存速度)
    // 更多解释，详见
    public long rp1, rp2, rp3, rp4, rp5, rp6, rp7, rp8, rp9;

    private InternalThreadLocalMap() {
        super(newIndexedVariableTable());
    }

    // 初始化资源，初始化的长度为32，并初始化为UNSET
    private static Object[] newIndexedVariableTable() {
        Object[] array = new Object[32];
        Arrays.fill(array, UNSET);
        return array;
    }
}

```

以上代码为InternalThreadLocalMap的主要实现，对于使用者来说，需要关注以下几个函数:

*   getIfSet();
*   get();
*   fastGet();
*   slowGet();  
    存在以下两种情况:

(1) 在Thread中调用FastThreadLocal;  
(2) 在FastThreadLocalThread中调用FastThreadLocal.

因为存在以上两种调用场景，在获取InternalThreadLocalMap时，会使用instanceof进行判断，如下所示：

```java
        if (thread instanceof FastThreadLocalThread) {
            // 对应fastGet等操作
        } else {
            // 对应slowGet等操作
        }

```

如果调用线程是

Thread: 调用UnpaddedInternalThreadLocalMap中的slowThreadLocalMap变量;  
FastThreadLocalThread: 调用FastThreadLocalThread中的threadLocalMap变量.  
因为InternalThreadLocalMap构造函数为私有函数，所以在getIfSet/fastGet函数中均是获取FastThreadLocalThread的threadLocalMap变量.若变量为空，则调用私有构造函数进行赋值操作.

```java
    // Cache line padding (must be public)
    // With CompressedOops enabled, an instance of this class should occupy at least 128 bytes.
    public long rp1, rp2, rp3, rp4, rp5, rp6, rp7, rp8, rp9;

    private InternalThreadLocalMap() {
        super(newIndexedVariableTable());
    }

    private static Object[] newIndexedVariableTable() {
        Object[] array = new Object[32];
        Arrays.fill(array, UNSET);
        return array;
    }

```

构造函数，会创建一个Object数组(初始化长度为32)，并逐个初始化数值为UNSET，为后续的赋值操作提供判断依据(详见removeIndexedVariable以及isIndexedVariableSet函数).

Tips:

构造函数存在一段代码public long rp1, rp2, rp3, rp4, rp5, rp6, rp7, rp8, rp9;.  
此段代码无实际实用意义，其存在是为了保证InternalThreadLocalMap的实例大小超过128字节(以上long变量72字节，InternalThreadLocalMap的基类UnpaddedInternalThreadLocalMap亦存在若干变量).  
cpu cache line的大小一般为64k或者128k，变量的大小超过128byte，则会极大的减少伪共享情况.  
(当前Netty的版本号是4.1.38，InternalThreadLocalMap的实例大小是136byte，这是因为在Netty的4.0.33版本后，引入了cleanerFlags以及arrayList变量，忘记去除rp9变量导致的).  
关于伪共享，可关注JAVA 拾遗 — CPU Cache 与缓存行一文.

## 4.2 FastThreadLocal初始化

```java
public class FastThreadLocal<V> {
    
    private final int index;

    // 原子变量自增，获取ID，作为FastThreadLocal的存放索引
    // public static int nextVariableIndex() {
    //     int index = nextIndex.getAndIncrement();
    //     if (index < 0) {
    //         nextIndex.decrementAndGet();
    //         throw new IllegalStateException("too many thread-local indexed variables");
    //     }
    //     return index;
    // }
    public FastThreadLocal() {
        index = InternalThreadLocalMap.nextVariableIndex();
    }
    
    // 设置FastThreadLocal资源
    public final void set(V value) {
        if (value != InternalThreadLocalMap.UNSET) {
            InternalThreadLocalMap threadLocalMap = InternalThreadLocalMap.get();
            setKnownNotUnset(threadLocalMap, value);
        } else {
            // 如果设置的资源为UNSET，则销毁当前FastThreadLocal对应的资源对象
            remove();
        }
    }
    
    // 设置资源，并将设置好的FastThreadLocal变量添加至待销毁资源列表中，待后续进行销毁操作
    private void setKnownNotUnset(InternalThreadLocalMap threadLocalMap, V value) {
        if (threadLocalMap.setIndexedVariable(index, value)) {
            addToVariablesToRemove(threadLocalMap, this);
        }
    }
    
    // 根据FastThreadLocal初始化的index，确定其在资源列表中的位置，后续查询资源就可以根据索引快速确定位置
    public boolean setIndexedVariable(int index, Object value) {
        Object[] lookup = indexedVariables;
        if (index < lookup.length) {
            Object oldValue = lookup[index];
            lookup[index] = value;
            return oldValue == UNSET;
        } else {
            expandIndexedVariableTableAndSet(index, value);
            return true;
        }
    }
    
    // 按照2的倍数，扩张资源池数组长度
    private void expandIndexedVariableTableAndSet(int index, Object value) {
        Object[] oldArray = indexedVariables;
        final int oldCapacity = oldArray.length;
        int newCapacity = index;
        newCapacity |= newCapacity >>>  1;
        newCapacity |= newCapacity >>>  2;
        newCapacity |= newCapacity >>>  4;
        newCapacity |= newCapacity >>>  8;
        newCapacity |= newCapacity >>> 16;
        newCapacity ++;

        Object[] newArray = Arrays.copyOf(oldArray, newCapacity);
        Arrays.fill(newArray, oldCapacity, newArray.length, UNSET);
        newArray[index] = value;
        indexedVariables = newArray;
    }
}

```

以上是FastThreadLocal的部分函数节选.  
由构造函数可知，FastThreadLocal在初始化的时候，会使用InternalThreadLocalMap的nextVariableIndex获取一个唯一ID.  
此ID为原子变量自增获取，后续对此变量的更新或者删除操作，均是通过此index进行操作.  
在设置变量的时候，存在indexedVariables空间不足的情况(初始化长度为32),则会对此数组通过expandIndexedVariableTableAndSet进行扩容操作(>>>为无符号右移即若该数为正，则高位补0，而若该数为负数，则右移后高位同样补0).通过这样的位移操作，每次数组均会乘2（保持2^n）.  
因为使用常数索引index，因此Netty中查询FastThreadLocal变量的速度为O(1),扩容时采用Arrays.Copy也很简单(相较于jdk的ThreadLocal的rehash操作).

## 4.3 FastThreadLocal变量获取及删除

```java
public class FastThreadLocal<V> {

    private static final int variablesToRemoveIndex = InternalThreadLocalMap.nextVariableIndex();
    

    // 在线程执行完资源之后，需要根据业务场景，确定是否调用此函数以销毁线程中存在的FastThreadLocal资源
    public static void removeAll() {
        InternalThreadLocalMap threadLocalMap = InternalThreadLocalMap.getIfSet();
        if (threadLocalMap == null) {
            return;
        }

        try {
            Object v = threadLocalMap.indexedVariable(variablesToRemoveIndex);
            if (v != null && v != InternalThreadLocalMap.UNSET) {
                @SuppressWarnings("unchecked")
                Set<FastThreadLocal<?>> variablesToRemove = (Set<FastThreadLocal<?>>) v;
                FastThreadLocal<?>[] variablesToRemoveArray =
                        variablesToRemove.toArray(new FastThreadLocal[0]);
                for (FastThreadLocal<?> tlv: variablesToRemoveArray) {
                    tlv.remove(threadLocalMap);
                }
            }
        } finally {
            // 实际上仅仅是将FastThreadLocalThread中的threadLocalMap置为null，或者是将slowThreadLocalMap销毁
            InternalThreadLocalMap.remove();
        }
    }
    
    @SuppressWarnings("unchecked")
    public final V get(InternalThreadLocalMap threadLocalMap) {
        Object v = threadLocalMap.indexedVariable(index);
        if (v != InternalThreadLocalMap.UNSET) {
            return (V) v;
        }

        // 如果当前待获取资源为空，则进行初始操作，返回相应资源
        return initialize(threadLocalMap);
    }

    // 根据用户重载的initialValue函数，初始化待获取资源
    private V initialize(InternalThreadLocalMap threadLocalMap) {
        V v = null;
        try {
            v = initialValue();
        } catch (Exception e) {
            PlatformDependent.throwException(e);
        }

        threadLocalMap.setIndexedVariable(index, v);
        addToVariablesToRemove(threadLocalMap, this);
        return v;
    }
    
    // 将FastThreadLocal变量，添加至待删除的资源列表中
    @SuppressWarnings("unchecked")
    private static void addToVariablesToRemove(InternalThreadLocalMap threadLocalMap, FastThreadLocal<?> variable) {
        Object v = threadLocalMap.indexedVariable(variablesToRemoveIndex);
        Set<FastThreadLocal<?>> variablesToRemove;
        // 如果待删除资源列表为空，则初始化待删除资源列表(Set)
        if (v == InternalThreadLocalMap.UNSET || v == null) {
            variablesToRemove = Collections.newSetFromMap(new IdentityHashMap<FastThreadLocal<?>, Boolean>());
            threadLocalMap.setIndexedVariable(variablesToRemoveIndex, variablesToRemove);
        } else {
            variablesToRemove = (Set<FastThreadLocal<?>>) v;
        }

        variablesToRemove.add(variable);
    }
    

    @SuppressWarnings("unchecked")
    public final void remove(InternalThreadLocalMap threadLocalMap) {
        if (threadLocalMap == null) {
            return;
        }

        Object v = threadLocalMap.removeIndexedVariable(index);
        removeFromVariablesToRemove(threadLocalMap, this);
    
        // FastThreadLocal变量已经被赋值，则需要调用用户重载的onRemoval函数，销毁资源
        if (v != InternalThreadLocalMap.UNSET) {
            try {
                onRemoval((V) v);
            } catch (Exception e) {
                PlatformDependent.throwException(e);
            }
        }
    }
    
    // 确定资源的初始化函数(如果用户不进行重载，则返回null)
    protected V initialValue() throws Exception {
        return null;
    }

    // 用户需要重载次函数，以便销毁申请的资源
    protected void onRemoval(@SuppressWarnings("UnusedParameters") V value) throws Exception { }
}·

```

用户在使用FastThreadLocal时，需要继承initialValue以及onRemoval函数（FastThreadLocal对象的初始化及销毁交由用户控制）.

initialValue: 在获取FastThreadLocal对象时，若对象未设置，则调用initialValue初始化资源(get等函数中判断对象为空，则调用initialize初始化资源);  
onRemoval: 在FastThreadLocal更新对象或最终销毁资源时，调用onRemoval销毁资源(set等函数中判断待设置对象已被设置过，则调用onRemoval销毁资源).

```java
    this.threadLocal = new FastThreadLocal<Recycler.Stack<T>>() {
        protected Recycler.Stack<T> initialValue() {
            return new Recycler.Stack(Recycler.this, Thread.currentThread(), Recycler.this.maxCapacityPerThread, Recycler.this.maxSharedCapacityFactor, Recycler.this.ratioMask, Recycler.this.maxDelayedQueuesPerThread);
        }

        protected void onRemoval(Recycler.Stack<T> value) {
            if (value.threadRef.get() == Thread.currentThread() && Recycler.DELAYED_RECYCLED.isSet()) {
                ((Map)Recycler.DELAYED_RECYCLED.get()).remove(value);
            }

        }
    };

```

以上代码，就是Recycler调用FastThreadLocal的使用示范(Recycler是Netty的轻量级对象池).  
需要注意，在FastThreadLocal中，存在一个静态变量variablesToRemoveIndex,其作用是在对象池中占据一个固定位置，存放一个集合Set<FastThreadLocal<?>> variablesToRemove.  
每次初始化变量的时候，均会将对应的FastThreadLocal存放至variablesToRemove中，在更新对象的时候(set等函数)或者清理FastThreadLocalThread中的变量时(removeAll函数)时，程序就会根据variablesToRemove进行相应的清理工作.  
这样，用户在使用FastThreadLocalThread时，就无须花费过多的经理关注线程安全问题(在Netty中，线程池的生命周期较长，无需过多的关注内存清理，然而如果用户在线程池等场景使用FastThreadLocalThread，就需要在执行完任务后，清理FastThreadLocal参数，以免对后续的业务产生影响).

## 总结

通过以上源码分析，可以得知Netty为了提升ThreadLocal性能，做了很多改善操作.

定制FastThreadLocalThread以及FastThreadLocal;  
使用padding手段扩充FastThreadLocal的实例大小，避免伪共享;  
使用原子变量自增获取的ID作为常数索引，优化查询速度至O(1)，避免了hash冲突以及扩容导致的rehash操作；  
提供initialValue以及onRemoval函数，用户可以自行重载函数，实现FastThreadLocal资源的高度定制化操作;  
FastThreadLocal对象数组的扩容(expandIndexedVariableTableAndSet)采用位操作，计算数组长度;  
针对在Thread中调用FastThreadLocal以及在FastThreadLocalThread中调用FastThreadLocal，分别采用不同的获取方式，增强了兼容性.  
更多细节，读者可以自己参照源码进行进一步分析.  
对于采用Object\[\]数组存放FastThreadLocal变量，是否存在牺牲空间换取性能，个人理解如下：  
Netty的默认启动线程是2 * cpu core,也就是两倍cpu核数，且此线程组会在Netty的生命周期中持续存在.  
Netty不存在创建过多线程导致内存占用过多的现象(用户手动调节Netty的boss group以及worker group线程数量都会很慎重).  
此外，Netty中对于FastThreadLocal存在较大的读取以及更新需求量，确实存在优化ThreadLocal的需求.  
因此，适当的浪费一些空间，换取查询和更新的性能提升，是恰当的操作.