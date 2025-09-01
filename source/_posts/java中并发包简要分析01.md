---
title: java中并发包简要分析01
id: 173
date: 2024-10-31 22:01:41
author: daichangya
excerpt: "参考《分布式java应用》一书，简单过一遍并发包（java.util.concurrent）ConcurrentHashMapConcurrentHashMap是线程安全的HashMap的实现。1）添加put(Object key , Object value)ConcurrentHashMap并没有采用synchronized进行控制，"
permalink: /archives/12954711/
categories:
 - 多线程-并发
---

参考《分布式java应用》一书，简单过一遍并发包（java.util.concurrent）

ConcurrentHashMap
ConcurrentHashMap是线程安全的HashMap的实现。

1）添加

put(Object key , Object value)

ConcurrentHashMap并没有采用synchronized进行控制，而是使用了ReentrantLock。
```
public V put(K key, V value) {
        if (value == null)
            throw new NullPointerException();
        int hash = hash(key.hashCode());
        return segmentFor(hash).put(key, hash, value, false);
    }
```
这里计算出key的hash值，根据hash值获取对应的数组中的segment对象。接下来的工作都交由segment完成。

segment可以看成是HashMap的一个部分，（ConcurrentHashMap基于concurrencyLevel划分出了多个segment来对key-value进行存储）每次操作都只对当前segment进行锁定，从而避免每次put操作锁住整个map。
```
V put(K key, int hash, V value, boolean onlyIfAbsent) {
            lock();
            try {
                int c = count;
                if (c++ > threshold) // ensure capacity
                    rehash();
                HashEntry<K,V>[] tab = table;
                int index = hash & (tab.length - 1);
                HashEntry<K,V> first = tab[index];
                HashEntry<K,V> e = first;
                while (e != null && (e.hash != hash || !key.equals(e.key)))
                    e = e.next;
 
                V oldValue;
                if (e != null) {
                    oldValue = e.value;
                    if (!onlyIfAbsent)
                        e.value = value;
                }
                else {
                    oldValue = null;
                    ++modCount;
                    tab[index] = new HashEntry<K,V>(key, hash, first, value);
                    count = c; // write-volatile
                }
                return oldValue;
            } finally {
                unlock();
            }
        }
```
这个方法进来就上锁（lock），并在finally中确保释放锁（unlock）。

添加key-value的过程中，先判断当前存储对象个数加1后是否大于threshold，如果大于则进行扩容（对象数组扩大两倍，进行重新hash，转移到新数组）。

如果不大于，则进行后续操作。通过对hash值和对象数组大小减1的值进行按位与操作（取余），得到当前key需要放入数组的位置，接着寻找对应位置上的hashEntry对象链表，并进行遍历。

如果找到相同key值的Entry，则替换该Entry对象的value。

如果没有找到就创建一个Entry对象，赋值给对应位置的数组对象，并构成链表。

注意：采用segment这种方式，在并发操作过程中，可以在很多程度上减少阻塞现象。

 

2）删除

remove(Object key)
```
public V remove(Object key) {
    int hash = hash(key.hashCode());
        return segmentFor(hash).remove(key, hash, null);
    }
```
和put类似，删除也要根据hash先获得segment，然后在segment上执行remove操作。
```
V remove(Object key, int hash, Object value) {
            lock();
            try {
                int c = count - 1;
                HashEntry<K,V>[] tab = table;
                int index = hash & (tab.length - 1);
                HashEntry<K,V> first = tab[index];
                HashEntry<K,V> e = first;
                while (e != null && (e.hash != hash || !key.equals(e.key)))
                    e = e.next;
 
                V oldValue = null;
                if (e != null) {
                    V v = e.value;
                    if (value == null || value.equals(v)) {
                        oldValue = v;
                        // All entries following removed node can stay
                        // in list, but all preceding ones need to be
                        // cloned.
                        ++modCount;
                        HashEntry<K,V> newFirst = e.next;
                        for (HashEntry<K,V> p = first; p != e; p = p.next)
                            newFirst = new HashEntry<K,V>(p.key, p.hash,
                                                          newFirst, p.value);
                        tab[index] = newFirst;
                        count = c; // write-volatile
                    }
                }
                return oldValue;
            } finally {
                unlock();
            }
        }
```
segment的remove操作，首先加锁，然后对hash值与数组大小减1的值按位与操作，得到数组对应位置上的HashEntry对象，接下来遍历此链表，查找hash值相等并且key相等（equals）的对象。

如果没有找到，返回null，释放锁。

如果找到了，则重新创建位于删除元素之前的所有HashEntry，位于其后的不用处理。释放锁！

 

3）获取

get(Object key)

直接看看segment中的get操作，如下：
```
V get(Object key, int hash) {
           if (count != 0) { // read-volatile
               HashEntry<K,V> e = getFirst(hash);
               while (e != null) {
                   if (e.hash == hash && key.equals(e.key)) {
                       V v = e.value;
                       if (v != null)
                           return v;
                       return readValueUnderLock(e); // recheck
                   }
                   e = e.next;
               }
           }
           return null;
       }
```
可以看出并没有加锁操作，只有v==null时，进入readValueUnderLock才有加锁操作。

这里假设一种情况，例如两条线程a、b，a执行get操作，b执行put操作。

当a执行到getFirst，与当前数组长度减1按位与操作后得到指定位置index，此时cpu将执行权交给b，b线程put一对key-value，导致扩容并重新hash排列，然后cpu又将执行权还给a，a然后根据之前的index去获取HashEntry就会发生问题。

当然这种情况发生的概率很小。

 

4）遍历

其实这个过程和读取过程类似，读取所有分段中的数据即可。

 

ConcurrentHashMap默认情况下采用将数据分为16个段进行存储，并且每个段各自拥有自己的锁，锁仅用于put和remove等改变集合对象的操作，基于voliate及hashEntry链表的不变性实现读取的不加锁。

这些方式使得ConcurrentHashMap能够保持极好的并发操作，尤其是对于读远比插入和删除频繁的map而言，而它采用的这些方法也可谓是对于java内存模型、并发机制深刻掌握的体现，是一个设计得非常不错的支持高并发的集合对象。

——摘自《分布式java应用》

 

CopyOnWriteArrayList
CopyOnWriteArrayList是一个线程安全、并且在读操作时无锁的ArrayList。

1）添加

add(E e)
```
public boolean add(E e) {
    final ReentrantLock lock = this.lock;
    lock.lock();
    try {
        Object[] elements = getArray();
        int len = elements.length;
        Object[] newElements = Arrays.copyOf(elements, len + 1);//复制数组
        newElements[len] = e;//添加到末尾
        setArray(newElements);
        return true;
    } finally {
        lock.unlock();
    }
    }
```
这里同样没有使用synchronized关键字，而是使用ReentrantLock。

和ArrayList不同的是，这里每次都会创建一个新的object数组，大小比之前数组大1。将之前的数组复制到新数组，并将新加入的元素加到数组末尾。

 

2）删除

remove(Object o)
```
public boolean remove(Object o) {
    final ReentrantLock lock = this.lock;
    lock.lock();
    try {
        Object[] elements = getArray();
        int len = elements.length;
        if (len != 0) {
        // Copy while searching for element to remove
        // This wins in the normal case of element being present
        int newlen = len - 1;
        Object[] newElements = new Object[newlen];//新建数组
 
        for (int i = 0; i < newlen; ++i) {
            if (eq(o, elements[i])) {
            // found one;  copy remaining and exit
            for (int k = i + 1; k < len; ++k)
                newElements[k-1] = elements[k];
            setArray(newElements);
            return true;
            } else
            newElements[i] = elements[i];
        }
 
        // special handling for last cell
        if (eq(o, elements[newlen])) {
            setArray(newElements);
            return true;
        }
        }
        return false;
    } finally {
        lock.unlock();
    }
    }
```
此方法为什么这么直接进行数组的复制呢？为何不适用system的arrayCopy来完成？

 

3）获取

get(int index)
```
public E get(int index) {
        return (E)(getArray()[index]);
    }
```
这里有可能脏读。但是销量非常高。

//通过看集合包和并发包可以看出一些不同的编程思路。这里为什么就不事先做范围的检查？

 

从上可见，CopyOnWriteArrayList基于ReentrantLock保证了增加元素和删除元素动作的互斥。在读操作上没有任何锁，这样就保证了读的性能，带来的副作用是有时候可能会读取到脏数据。

 

CopyOnWriteArraySet
CopyOnWriteArraySet是基于CopyOnWriteArrayList的，可以知道set是不容许重复数据的，因此add操作和CopyOnWriteArrayList有所区别，他是调用CopyOnWriteArrayList的addIfAbsent方法。
```
public boolean addIfAbsent(E e) {
   final ReentrantLock lock = this.lock;
   lock.lock();
   try {
       // Copy while checking if already present.
       // This wins in the most common case where it is not present
       Object[] elements = getArray();
       int len = elements.length;
       Object[] newElements = new Object[len + 1];
       for (int i = 0; i < len; ++i) {
       if (eq(e, elements[i])) //如果存在，直接返回！
           return false; // exit, throwing away copy
       else
           newElements[i] = elements[i];
       }
       newElements[len] = e;
       setArray(newElements);
       return true;
   } finally {
       lock.unlock();
   }
   }
```
由此可见，addIfAbsent需要每次都遍历，在add方面，CopyOnWriteArraySet效率要比CopyOnWriteArrayList低一点。

 

ArrayBlockingQueue
ArrayBlockingQueue是一个基于数组、先进先出、线程安全的集合类，其特点是实现指定时间的阻塞读写，并且容量是可以限制的。

1）创建
```
public ArrayBlockingQueue(int capacity, boolean fair) {
        if (capacity <= 0)
            throw new IllegalArgumentException();
        this.items = (E[]) new Object[capacity];
        lock = new ReentrantLock(fair);
        notEmpty = lock.newCondition();
        notFull =  lock.newCondition();
    }
```
初始化锁和两个锁上的Condition，一个为notEmpty，一个为notFull。

 

2）添加

offer(E e , long timeout , TimeUtil unit)
```
public boolean offer(E e, long timeout, TimeUnit unit)
        throws InterruptedException {
 
        if (e == null) throw new NullPointerException();
    long nanos = unit.toNanos(timeout);
        final ReentrantLock lock = this.lock;
        lock.lockInterruptibly();
        try {
            for (;;) {
                if (count != items.length) {
                    insert(e);
                    return true;
                }
                if (nanos <= 0)
                    return false;
                try {
                    nanos = notFull.awaitNanos(nanos);
                } catch (InterruptedException ie) {
                    notFull.signal(); // propagate to non-interrupted thread
                    throw ie;
                }
            }
        } finally {
            lock.unlock();
        }
    }
```
这个方法将元素插入数组的末尾，如果数组满，则进入等待，只到以下三种情况发生才继续：

被唤醒、达到指定的时间、当前线程被中断。

该方法首先将等待时间转换成纳秒。然后加锁，如果数组未满，则在末尾插入数据，如果数组已满，则调用notFull.awaitNanos进行等待。如果被唤醒或超时，重新判断是否满。如果线程被interrupt，则直接抛出异常。

 

另外一个不带时间的offer方法在数组满的情况下不进去等待，而是直接返回false。
```
public boolean offer(E e) {
       if (e == null) throw new NullPointerException();
       final ReentrantLock lock = this.lock;
       lock.lock();
       try {
           if (count == items.length)
               return false;
           else {
               insert(e);
               return true;
           }
       } finally {
           lock.unlock();
       }
   }
```
同时还可以选择put方法，此方法在数组已满的情况下会一直等待，知道数组不为空或线程被interrupt。
```
public void put(E e) throws InterruptedException {
        if (e == null) throw new NullPointerException();
        final E[] items = this.items;
        final ReentrantLock lock = this.lock;
        lock.lockInterruptibly();
        try {
            try {
                while (count == items.length)
                    notFull.await();
            } catch (InterruptedException ie) {
                notFull.signal(); // propagate to non-interrupted thread
                throw ie;
            }
            insert(e);
        } finally {
            lock.unlock();
        }
    }
 ```

3）获取

poll(long timeout, TimeUnit unit)
```
public E poll(long timeout, TimeUnit unit) throws InterruptedException {
    long nanos = unit.toNanos(timeout);
        final ReentrantLock lock = this.lock;
        lock.lockInterruptibly();
        try {
            for (;;) {
                if (count != 0) {
                    E x = extract();
                    return x;
                }
                if (nanos <= 0)
                    return null;
                try {
                    nanos = notEmpty.awaitNanos(nanos);
                } catch (InterruptedException ie) {
                    notEmpty.signal(); // propagate to non-interrupted thread
                    throw ie;
                }
 
            }
        } finally {
            lock.unlock();
        }
    }
```
poll获取队列中的第一个元素，如果队列中没有元素，则进入等待。

poll首先将制定timeout转换成纳秒，然后加锁，如果数组个数不为0，则从当前对象数组中获取最后一个元素，在获取后将位置上的元素置为null。

如果数组中的元素个数为0，首先判断timeout是否小于等于0，若小于0则直接返回null。若大于则进行等待，如果被唤醒或者超时，重新判断数据元素个数是否大于0。

如果线程被interrupt，则直接抛出InterruptedException。

和offer一样，不带时间的poll方法在数组元素个数为0直接返回null，不进行等待。

take方法在数据为空的情况下会一直等待，只到数组不为空或者interrupt。