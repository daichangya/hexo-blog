---
title: Recycler对象池分析
id: 1538
date: 2024-10-31 22:02:00
author: daichangya
excerpt: "publicclassRecyclerTest{staticclassWrapRecycler{privatebooleantmp;privatefinalstaticRecycler&lt;WrapRecycler&gt;RECYCLER=newRecycler&lt;WrapRecycler&g"
permalink: /archives/recycler%E5%AF%B9%E8%B1%A1%E6%B1%A0%E5%88%86%E6%9E%90/
categories:
 - netty
---



```

public class RecyclerTest {
    static class WrapRecycler{

        private boolean tmp ;
        private final static Recycler<WrapRecycler> RECYCLER = new Recycler<WrapRecycler>() {
            @Override
            protected WrapRecycler newObject(Handle<WrapRecycler> handle) {
                return new WrapRecycler(handle);
            }
        };

        Recycler.Handle<WrapRecycler> handle;
        WrapRecycler(Recycler.Handle<WrapRecycler> handle){
            this.handle = handle;
            this.tmp = false;
        }

        static WrapRecycler getInstance(){
            return RECYCLER.get();
        }

        void recycle(){
            this.tmp = false;
            handle.recycle(this);
        }

        public boolean getTmp(){
            return tmp;
        }

        public void setTmp(boolean tmp){
            this.tmp = tmp;
        }
    }


    public static void main(String[] args) {
        WrapRecycler instance = WrapRecycler.getInstance();
        System.out.println(instance.hashCode());
        System.out.println(instance.getTmp());
        instance.setTmp(true);
        System.out.println(instance.getTmp());
        instance.recycle();
        instance = WrapRecycler.getInstance();
        System.out.println(instance.hashCode());
        System.out.println(instance.getTmp());
    }
}
```

*   运行结果，两次获取的对象的hashcode哈希值相同说明是同一个对象

```

41359092
false
true
41359092
false

```

## (1) Recycler类结构

*   Recycler是一个抽象类，在目标类中创建Recycler对象池实例时需要实现newObject(Handler handler)方法用来创建特定类的实例；
    
*   Recycler对象池内部是用一个对象数组维护对象池中的对象实例，对外提供统一的对象创建和回收接口：
    
    *   Recycler#get方法 : 是获取对象池中对象的入口, 如果有可用对象,直接返回, 没有就调用newObject()方法创建一个.
        
    *   Recycler#recycle方法: 是对象使用完毕后回收对象,只能回收当前线程创建的对象 现在已经标记@Deprecated不建议使用了, 建议使用Recycler.Handle#recycler方法，可以回收不是当前线程创建的对象, 复用性和性能更好了.
        
*   Recycler对象池的实现主要是通过三个核心组件：Handler，WeakOrderQueue和Stack
    

### 1\. Handler组件

*   Handler组件主要用来对外提供一个recycle()对象回收接口

```

static final class DefaultHandle<T> implements Handle<T> {
    private int lastRecycledId;
    private int recycleId;

    boolean hasBeenRecycled;

    private Stack<?> stack;
    private Object value;

    DefaultHandle(Stack<?> stack) {
        this.stack = stack;
    }

    @Override
    public void recycle(Object object) {
        if (object != value) {
            throw new IllegalArgumentException("object does not belong to handle");
        }
        stack.push(this);
    }
}
```

*   每个池化对象在newObject()创建时都会绑定一个Handler用作该对象的回收；

```

protected WrapRecycler newObject(Handle<WrapRecycler> handle) {
    return new WrapRecycler(handle);
}    
```

*   每个Handle关联一个value字段，用于存放具体的池化对象，在对象池中，所有的池化对象都被这个Handle包装，Handle是对象池管理的基本单位，Stack中存储管理的也是Handler类；
    
    *   调用get()方法从对象池中获取复用对象，如果对象池为空则在stack中创建新的Handler实例，并通过newObject()方法创建对象赋给handler.value属性；

```

public final T get() {
    if (maxCapacityPerThread == 0) {
        return newObject((Handle<T>) NOOP_HANDLE);
    }
    Stack<T> stack = threadLocal.get();
    DefaultHandle<T> handle = stack.pop();
    if (handle == null) {
        handle = stack.newHandle();
        handle.value = newObject(handle);
    }
    return (T) handle.value;
}
```

### 2\. Stack组件

*   通过FastThreadLocal类每个线程维护着一个与线程绑定的stack，用来存储复用的对象

```

private final FastThreadLocal<Stack<T>> threadLocal = new FastThreadLocal<Stack<T>>() {
    @Override
    protected Stack<T> initialValue() {
        return new Stack<T>(Recycler.this, Thread.currentThread(), maxCapacityPerThread, maxSharedCapacityFactor,
                ratioMask, maxDelayedQueuesPerThread);
    }
};
```

*   线程在通过Recycler的get()方法获取复用对象时，首先获取与当前线程绑定的stack，再从Stack中pop出Handler包装实例

```

public final T get() {
    if (maxCapacityPerThread == 0) {
        return newObject((Handle<T>) NOOP_HANDLE);
    }
    Stack<T> stack = threadLocal.get();
    DefaultHandle<T> handle = stack.pop();
    if (handle == null) {
        handle = stack.newHandle();
        handle.value = newObject(handle);
    }
    return (T) handle.value;
}
```

### 3\. WeakOrderQueue组件

*   WeakOrderQueue是Recycler的一个内部私有类，用来暂存待回收的对象；Handler.recycler()可以回收不是当前线程创建的对象主要依靠WeakOrderQueue实现；

```

private static final FastThreadLocal<Map<Stack<?>, WeakOrderQueue>> DELAYED_RECYCLED =
        new FastThreadLocal<Map<Stack<?>, WeakOrderQueue>>() {
    @Override
    protected Map<Stack<?>, WeakOrderQueue> initialValue() {
        return new WeakHashMap<Stack<?>, WeakOrderQueue>();
    }
};
```

*   如果是当前线程创建的对象, 直接就把对象放到当前线程对应的Stack中. 如果不是, 则放入WeakOrderQueue中；每个线程维护着一个ＷeakHashmap

```

public void recycle(Object object) {
    if (object != value) {
        throw new IllegalArgumentException("object does not belong to handle");
    }
    stack.push(this);
}
```

```

void push(DefaultHandle<?> item) {
    Thread currentThread = Thread.currentThread();
    if (thread == currentThread) {
        pushNow(item);
    } else {
        pushLater(item, currentThread);
    }
}
```

```

private void pushLater(DefaultHandle<?> item, Thread thread) {
    Map<Stack<?>, WeakOrderQueue> delayedRecycled = DELAYED_RECYCLED.get();
    WeakOrderQueue queue = delayedRecycled.get(this);
    if (queue == null) {
        if (delayedRecycled.size() >= maxDelayedQueues) {
            delayedRecycled.put(this, WeakOrderQueue.DUMMY);
            return;
        }

        if ((queue = WeakOrderQueue.allocate(this, thread)) == null) {
            return;
        }
        delayedRecycled.put(this, queue);
    } else if (queue == WeakOrderQueue.DUMMY) {
        return;
    }

    queue.add(item);
}
```

*   在从Stack获取对象池时,如果Stack中可用对象为空,会尝试遍历多线程对应的WeakOrderQueue链表中回收恢复对象；

```

public final T get() {
    if (maxCapacityPerThread == 0) {
        return newObject((Handle<T>) NOOP_HANDLE);
    }
    Stack<T> stack = threadLocal.get();
    DefaultHandle<T> handle = stack.pop();
    if (handle == null) {
        handle = stack.newHandle();
        handle.value = newObject(handle);
    }
    return (T) handle.value;
}
```

```

DefaultHandle<T> pop() {
    int size = this.size;
    if (size == 0) {
        if (!scavenge()) {
            return null;
        }
        size = this.size;
    }
    size --;
    DefaultHandle ret = elements[size];
    elements[size] = null;
    if (ret.lastRecycledId != ret.recycleId) {
        throw new IllegalStateException("recycled multiple times");
    }
    ret.recycleId = 0;
    ret.lastRecycledId = 0;
    this.size = size;
    return ret;
}
```

```

boolean scavengeSome() {
    WeakOrderQueue prev;
    WeakOrderQueue cursor = this.cursor;
    if (cursor == null) {
        prev = null;
        cursor = head;
        if (cursor == null) {
            return false;
        }
    } else {
        prev = this.prev;
    }

    boolean success = false;
    do {
        if (cursor.transfer(this)) {
            success = true;
            break;
        }
        WeakOrderQueue next = cursor.next;
        if (cursor.owner.get() == null) {
            if (cursor.hasFinalData()) {
                for (;;) {
                    if (cursor.transfer(this)) {
                        success = true;
                    } else {
                        break;
                    }
                }
            }

            if (prev != null) {
                prev.setNext(next);
            }
        } else {
            prev = cursor;
        }

        cursor = next;

    } while (cursor != null && !success);

    this.prev = prev;
    this.cursor = cursor;
    return success;
}
```
![20171124194628835.png](https://images.jsdiff.com/20171124194628835_1726491737441.png)

## 总结

*   Netty实现的轻量级的对象池实现了对象的复用和回收，核心组件包括Stack，WeakOrderQueue和Handler
    
*   Stack相当于MyBatis的一级缓存，与线程绑定，线程内对象的获取和回收都使用绑定的Stack；复用对象时直接从Stack中申请，使用完后如果对象是自己创建的则放入Stack；
    
*   在对象回收时候如果对象不是当前线程创建的则不能放入Stack中回收，而是放入WeakOrderQueue中，所有的Queue组成一个链表作为对象回收的仓库，当Stack中无可用的对象时会遍历链表回收对象，实现了多线程之间对象回收的共享；
    

![20171124194642988.png](https://images.jsdiff.com/20171124194642988_1726491746947.png)