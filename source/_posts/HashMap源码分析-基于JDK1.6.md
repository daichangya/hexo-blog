---
title: HashMap源码分析（基于JDK1.6）
id: 965
date: 2024-10-31 22:01:47
author: daichangya
excerpt: "在Java集合类中最常用的除了ArrayList外，就是HashMap了。本文尽自己所能，尽量详细的解释HashMap的源码。一山还有一山高，有不足之处请之处，定感谢指定并及时修正。

    在看HashMap源码之前先复习一下数据结构。

    Java最基本的数据结构有数组和链表。数组的特点是空间连续（大小固定）、寻址迅速，但是插入和删除时需要移动元素，所以查询快，增加删除慢。链表"
permalink: /archives/10082469/
categories:
 - java源码分析
---

 在Java集合类中最常用的除了ArrayList外，就是HashMap了。本文尽自己所能，尽量详细的解释HashMap的源码。一山还有一山高，有不足之处请之处，定感谢指定并及时修正。

    在看HashMap源码之前先复习一下数据结构。

    Java最基本的数据结构有数组和链表。数组的特点是空间连续（大小固定）、寻址迅速，但是插入和删除时需要移动元素，所以查询快，增加删除慢。链表恰好相反，可动态增加或减少空间以适应新增和删除元素，但查找时只能顺着一个个节点查找，所以增加删除快，查找慢。有没有一种结构综合了数组和链表的优点呢？当然有，那就是哈希表（虽说是综合优点，但实际上查找肯定没有数组快，插入删除没有链表快，一种折中的方式吧）。一般采用拉链法实现哈希表。哈希表？拉链法？可能一下想不起来，不过放张图就了然了。

![](http://pic002.cnblogs.com/images/2012/471426/2012122409394770.png)

    （图片google来的，好多都用了文章用了这张图了，不知道出处了就没申明作者了）

    学计算机的肯定学过这玩意儿，也不需要解释，都懂的。

    铺垫了这么多，又是数组又是链表，还有哈希表，拉链法，该入正题了，我们什么时候用到了这些内容，具体它是怎么实现的？

    其实我们一直在用（别告诉我你没用过HashMap什么的），可能你一直没去深究，没看到它如何实现的，所以一直没感受到。这里主要分析HashMap的源码，就不再多扯其他的了。

    HashMap继承自AbstractMap，实现了Map接口（这些内容可以参考[《Java集合类》](http://www.cnblogs.com/hzmark/archive/2012/12/17/CollectionBase.html)）。来看类的定义。

```
 public class HashMap<K,V> extends AbstractMap<K,V> implements Map<K,V>, Cloneable, Serializable
```

    Map接口定义了所有Map子类必须实现的方法。Map接口中还定义了一个内部接口Entry（为什么要弄成内部接口？改天还要学习学习）。Entry将在后面有详细的介绍。

    AbstractMap也实现了Map接口，并且提供了两个实现Entry的内部类：SimpleEntry和SimpleImmutableEntry。

    定义了接口，接口中又有内部接口，然后有搞了个抽象类实现接口，抽象类里面又搞了两个内部类实现接口的内部接口，有没有点绕，为什么搞成这样呢？先不管了，先看HashMap吧。

    HashMap中定义的属性（应该都能看明白，不过还是解释一下）：

```
 /**
      * 默认的初始容量，必须是2的幂。
      */
     static final int DEFAULT_INITIAL_CAPACITY = 16;
     /**
      * 最大容量（必须是2的幂且小于2的30次方，传入容量过大将被这个值替换）
      */
     static final int MAXIMUM_CAPACITY = 1 << 30;
     /**
      * 默认装载因子，这个后面会做解释
      */
     static final float DEFAULT_LOAD_FACTOR = 0.75f;
     /**
      * 存储数据的Entry数组，长度是2的幂。看到数组的内容了，接着看数组中存的内容就明白为什么博文开头先复习数据结构了
      */
     transient Entry[] table;
     /**
      * map中保存的键值对的数量
      */
     transient int size;
     /**
      * 需要调整大小的极限值（容量*装载因子）
      */
     int threshold;
     /**
      *装载因子
      */
     final float loadFactor;
     /**
      * map结构被改变的次数
      */
     transient volatile int modCount;
```

    接着是HashMap的构造方法。

```
/**
     *使用默认的容量及装载因子构造一个空的HashMap
     */
    public HashMap() {
        this.loadFactor = DEFAULT_LOAD_FACTOR;
        threshold = (int)(DEFAULT_INITIAL_CAPACITY * DEFAULT_LOAD_FACTOR);//计算下次需要调整大小的极限值
        table = new Entry[DEFAULT_INITIAL_CAPACITY];//根据默认容量（16）初始化table
        init();
    }
/**
     * 根据给定的初始容量的装载因子创建一个空的HashMap
     * 初始容量小于0或装载因子小于等于0将报异常 
     */
    public HashMap(int initialCapacity, float loadFactor) {
        if (initialCapacity < 0)
            throw new IllegalArgumentException("Illegal initial capacity: " +
                                               initialCapacity);
        if (initialCapacity > MAXIMUM_CAPACITY)//调整最大容量
            initialCapacity = MAXIMUM_CAPACITY;
        if (loadFactor <= 0 || Float.isNaN(loadFactor))
            throw new IllegalArgumentException("Illegal load factor: " +
                                               loadFactor);
        int capacity = 1;
        //设置capacity为大于initialCapacity且是2的幂的最小值
        while (capacity < initialCapacity)
            capacity <<= 1;
        this.loadFactor = loadFactor;
        threshold = (int)(capacity * loadFactor);
        table = new Entry[capacity];
        init();
    }
/**
     *根据指定容量创建一个空的HashMap
     */
    public HashMap(int initialCapacity) {
        this(initialCapacity, DEFAULT_LOAD_FACTOR);//调用上面的构造方法，容量为指定的容量，装载因子是默认值
    }
/**
     *通过传入的map创建一个HashMap，容量为默认容量（16）和(map.zise()/DEFAULT_LOAD_FACTORY)+1的较大者，装载因子为默认值
     */
    public HashMap(Map<? extends K, ? extends V> m) {
        this(Math.max((int) (m.size() / DEFAULT_LOAD_FACTOR) + 1,
                      DEFAULT_INITIAL_CAPACITY), DEFAULT_LOAD_FACTOR);
        putAllForCreate(m);
    }
```

    上面的构造方法中调用到了init()方法，最后一个方法还调用了putAllForCreate(Map<? extends K, ? extends V> m)。init方法是一个空方法，里面没有任何内容。putAllForCreate看方法名就是创建的时候将传入的map全部放入新创建的对象中。该方法中还涉及到其他方法，将在后面介绍。

    先看初始化table时均使用了Entry，这是HashMap的一个内部类，实现了Map接口的内部接口Entry。

    下面给出Map.Entry接口及HashMap.Entry类的内容。

    Map.Entry接口定义的方法

```
 K getKey();//获取Key
 V getValue();//获取Value
 V setValue();//设置Value，至于具体返回什么要看具体实现
 boolean equals(Object o);//定义equals方法用于判断两个Entry是否相同
 int hashCode();//定义获取hashCode的方法
```

    HashMap.Entry类的具体实现

```
 static class Entry<K,V> implements Map.Entry<K,V> {
         final K key;
         V value;
         Entry<K,V> next;//对下一个节点的引用（看到链表的内容，结合定义的Entry数组，是不是想到了哈希表的拉链法实现？！）
         final int hash;//哈希值
 
         Entry(int h, K k, V v, Entry<K,V> n) {
             value = v;
             next = n;
             key = k;
             hash = h;
         }
 
         public final K getKey() {
             return key;
         }
 
         public final V getValue() {
             return value;
         }
 
         public final V setValue(V newValue) {
         V oldValue = value;
             value = newValue;
             return oldValue;//返回的是之前的Value
         }
 
         public final boolean equals(Object o) {
             if (!(o instanceof Map.Entry))//先判断类型是否一致
                 return false;
             Map.Entry e = (Map.Entry)o;
             Object k1 = getKey();
             Object k2 = e.getKey();
 // Key相等且Value相等则两个Entry相等
             if (k1 == k2 || (k1 != null && k1.equals(k2))) {
                 Object v1 = getValue();
                 Object v2 = e.getValue();
                 if (v1 == v2 || (v1 != null && v1.equals(v2)))
                     return true;
             }
             return false;
         }
         // hashCode是Key的hashCode和Value的hashCode的异或的结果
         public final int hashCode() {
             return (key==null   ? 0 : key.hashCode()) ^
                    (value==null ? 0 : value.hashCode());
         }
         // 重写toString方法，是输出更清晰
         public final String toString() {
             return getKey() + "=" + getValue();
         }
 
         /**
          *当调用put(k,v)方法存入键值对时，如果k已经存在，则该方法被调用（为什么没有内容？）
          */
         void recordAccess(HashMap<K,V> m) {
         }
 
         /**
          * 当Entry被从HashMap中移除时被调用（为什么没有内容？）
          */
         void recordRemoval(HashMap<K,V> m) {
         }
     }
```

    看完属性和构造方法，接着看HashMap中的其他方法，一个个分析，从最常用的put和get说起吧。

    put()

```
 public V put(K key, V value) {
         if (key == null)
             return putForNullKey(value);
         int hash = hash(key.hashCode());
         int i = indexFor(hash, table.length);
         for (Entry<K,V> e = table[i]; e != null; e = e.next) {
             Object k;
             if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {
                 V oldValue = e.value;
                 e.value = value;
                 e.recordAccess(this);
                 return oldValue;
             }
         }
 
         modCount++;
         addEntry(hash, key, value, i);
         return null;
     }
```

    当存入的key是null的时候将调用putForNUllKey方法，暂时将这段逻辑放一边，看key不为null的情况。先调用了hash(int h)方法获取了一个hash值。

```
 static int hash(int h) {
         // This function ensures that hashCodes that differ only by
         // constant multiples at each bit position have a bounded
         // number of collisions (approximately 8 at default load factor).
         h ^= (h >>> 20) ^ (h >>> 12);
         return h ^ (h >>> 7) ^ (h >>> 4);
     }
```

    这个方法的主要作用是防止质量较差的哈希函数带来过多的冲突（碰撞）问题。Java中int值占4个字节，即32位。根据这32位值进行移位、异或运算得到一个值。

```
 static int indexFor(int h, int length) {
         return h & (length-1);
     }
```

    indexFor返回hash值和table数组长度减1的与运算结果。为什么使用的是length-1？应为这样可以保证结果的最大值是length-1，不会产生数组越界问题。

    获取索引位置之后做了什么？探测table\[i\]所在的链表，所发现key值与传入的key值相同的对象，则替换并返回oldValue。若找不到，则通过addEntry(hash,key,value,i)添加新的对象。来看addEntry(hash,key,value,i)方法。

```
 void addEntry(int hash, K key, V value, int bucketIndex) {
     Entry<K,V> e = table[bucketIndex];
         table[bucketIndex] = new Entry<K,V>(hash, key, value, e);
         if (size++ >= threshold)
             resize(2 * table.length);
     }
```

    这就是在一个链表头部插入一个节点的过程。获取table\[i\]的对象e，将table\[i\]的对象修改为新增对象，让新增对象的next指向e。之后判断size是否到达了需要扩充table数组容量的界限并让size自增1，如果达到了则调用resize(int capacity)方法将数组容量拓展为原来的两倍。

```
 void resize(int newCapacity) {
         Entry[] oldTable = table;
         int oldCapacity = oldTable.length;
         // 这个if块表明，如果容量已经到达允许的最大值，即MAXIMUN_CAPACITY，则不再拓展容量，而将装载拓展的界限值设为计算机允许的最大值。
         // 不会再触发resize方法，而是不断的向map中添加内容，即table数组中的链表可以不断变长，但数组长度不再改变
         if (oldCapacity == MAXIMUM_CAPACITY) {
             threshold = Integer.MAX_VALUE;
             return;
         }
         // 创建新数组，容量为指定的容量
         Entry[] newTable = new Entry[newCapacity];
         transfer(newTable);
         table = newTable;
         // 设置下一次需要调整数组大小的界限
         threshold = (int)(newCapacity * loadFactor);
     }
```

    结合上面给出的注释，调整数组容量的内容仅剩下将原table中的内容复制到newTable中并将newTable返回给原table。即上面代码中的“transfer(newTable);table = newTable;”。来看transfer(Entry\[\] newTable)方法。

```
 void transfer(Entry[] newTable) {
         // 保留原数组的引用到src中，
         Entry[] src = table;
         // 新容量使新数组的长度
         int newCapacity = newTable.length;
 // 遍历原数组
         for (int j = 0; j < src.length; j++) {
             // 获取元素e
             Entry<K,V> e = src[j];
             if (e != null) {
                 // 将原数组中的元素置为null
                 src[j] = null;
                 // 遍历原数组中j位置指向的链表
                 do {
                     Entry<K,V> next = e.next;
                     // 根据新的容量计算e在新数组中的位置
                     int i = indexFor(e.hash, newCapacity);
                     // 将e插入到newTable[i]指向的链表的头部
                     e.next = newTable[i];
                     newTable[i] = e;
                     e = next;
                 } while (e != null);
             }
         }
     }
```

    从上面的代码可以看出，HashMap之所以不能保持元素的顺序有以下几点原因：第一，插入元素的时候对元素进行哈希处理，不同元素分配到table的不同位置；第二，容量拓展的时候又进行了hash处理；第三，复制原表内容的时候链表被倒置。

    一个put方法带出了这么多内容，接着看看putAll吧。

```
 public void putAll(Map<? extends K, ? extends V> m) {
         int numKeysToBeAdded = m.size();
         if (numKeysToBeAdded == 0)
             return;
         // 为什么判断条件是numKeysToBeAdded，不是(numKeysToBeAdded+table.length)>threshold???
         if (numKeysToBeAdded > threshold) {
             int targetCapacity = (int)(numKeysToBeAdded / loadFactor + 1);
             if (targetCapacity > MAXIMUM_CAPACITY)
                 targetCapacity = MAXIMUM_CAPACITY;
             int newCapacity = table.length;
             while (newCapacity < targetCapacity)
                 newCapacity <<= 1;
             if (newCapacity > table.length)
                 resize(newCapacity);
         }
 
         for (Iterator<? extends Map.Entry<? extends K, ? extends V>> i = m.entrySet().iterator(); i.hasNext(); ) {
             Map.Entry<? extends K, ? extends V> e = i.next();
             put(e.getKey(), e.getValue());
         }
     }
```

    先回答上面的问题：为什么判断条件是numKeysToBeAdded，不是(numKeysToBeAdded+table.length)>threshold???

    这是一种保守的做法，明显地，我们应该在(numKeysToBeAdded+table.length)>threshold的时候去拓展容量，但是考虑到将被添加的元素可能会有Key与原本存在的Key相同的情况，所以采用保守的做法，避免拓展到过大的容量。

    接着是遍历m中的内容，然后调用put方法将元素添加到table数组中。

    遍历的时候涉及到了entrySet方法，这个方法定义在Map接口中，HashMap中也有实现，后面会解释HashMap的这个方法，其它Map的实现暂不解释。

    下面介绍在put方法中被调用到的putForNullKey方法。

```
 private V putForNullKey(V value) {
         for (Entry<K,V> e = table[0]; e != null; e = e.next) {
             if (e.key == null) {
                 V oldValue = e.value;
                 e.value = value;
                 e.recordAccess(this);
                 return oldValue;
             }
         }
         modCount++;
         addEntry(0, null, value, 0);
         return null;
     }
```

    这是一个私有方法，在put方法中被调用。它首先遍历table数组，如果找到key为null的元素，则替换元素值并返回oldValue；否则通过addEntry方法添加元素，之后返回null。

    还记得上面构造方法中调用到的putAllForCreate吗？一口气将put操作的方法看完吧。

```
 private void putAllForCreate(Map<? extends K, ? extends V> m) {
         for (Iterator<? extends Map.Entry<? extends K, ? extends V>> i = m.entrySet().iterator(); i.hasNext(); ) {
             Map.Entry<? extends K, ? extends V> e = i.next();
             putForCreate(e.getKey(), e.getValue());
         }
     }
```

    先将遍历的过程放在一边，因为它同样涉及到了entrySet()方法。剩下的代码很简单，只是调用putForCreate方法逐个元素加入。

```
 private void putForCreate(K key, V value) {
         int hash = (key == null) ? 0 : hash(key.hashCode());
         int i = indexFor(hash, table.length);
         for (Entry<K,V> e = table[i]; e != null; e = e.next) {
             Object k;
             if (e.hash == hash &&
                 ((k = e.key) == key || (key != null && key.equals(k)))) {
                 e.value = value;
                 return;
             }
         }
         createEntry(hash, key, value, i);
     }
```

    该方法先计算需要添加的元素的hash值和在table数组中的索引i。接着遍历table\[i\]的链表，若有元素的key值与传入key值相等，则替换value，结束方法。若不存在key值相同的元素，则调用createEntry创建并添加元素。

```
 void createEntry(int hash, K key, V value, int bucketIndex) {
     Entry<K,V> e = table[bucketIndex];
         table[bucketIndex] = new Entry<K,V>(hash, key, value, e);
         size++;
     }
```

    这个方法的内容就不解释了，上面都解释过。

    至此所有put相关操作都解释完毕了。put之外，另一个常用的操作就是get，下面就来看get方法。

```
 public V get(Object key) {
         if (key == null)
             return getForNullKey();
         int hash = hash(key.hashCode());
         for (Entry<K,V> e = table[indexFor(hash, table.length)];
              e != null;
              e = e.next) {
             Object k;
             if (e.hash == hash && ((k = e.key) == key || key.equals(k)))
                 return e.value;
         }
         return null;
     }
```

    该方法分为key为null和不为null两块。先看不为null的情况。先获取key的hash值，之后通过hash值及table.length获取key对应的table数组的索引，遍历索引的链表，所找到key相同的元素，则返回元素的value，否者返回null。不为null的情况调用了getForNullKey()方法。

```
 private V getForNullKey() {
         for (Entry<K,V> e = table[0]; e != null; e = e.next) {
             if (e.key == null)
                 return e.value;
         }
         return null;
     }
```

    这是一个私有方法，只在get中被调用。该方法判断table\[0\]中的链表是否包含key为null的元素，包含则返回value，不包含则返回null。为什么是遍历table\[0\]的链表？因为key为null的时候获得的hash值都是0。

    添加（put）和获取（get）都结束了，接着看如何判断一个元素是否存在。

    HashMap没有提供判断元素是否存在的方法，只提供了判断Key是否存在及Value是否存在的方法，分别是containsKey(Object key)、containsValue(Object value)。

    containsKey(Object key)方法很简单，只是判断getEntry(key)的结果是否为null，是则返回false，否返回true。

```
 public boolean containsKey(Object key) {
         return getEntry(key) != null;
     }
 final Entry<K,V> getEntry(Object key) {
         int hash = (key == null) ? 0 : hash(key.hashCode());
         for (Entry<K,V> e = table[indexFor(hash, table.length)];
              e != null;
              e = e.next) {
             Object k;
             if (e.hash == hash &&
                 ((k = e.key) == key || (key != null && key.equals(k))))
                 return e;
         }
         return null;
     }
```

    getEntry(Object key)也没什么内容，只是根据key对应的hash值计算在table数组中的索引位置，然后遍历该链表判断是否存在相同的key值。

```
 public boolean containsValue(Object value) {
     if (value == null)
             return containsNullValue();
 
     Entry[] tab = table;
         for (int i = 0; i < tab.length ; i++)
             for (Entry e = tab[i] ; e != null ; e = e.next)
                 if (value.equals(e.value))
                     return true;
     return false;
     }
 private boolean containsNullValue() {
     Entry[] tab = table;
         for (int i = 0; i < tab.length ; i++)
             for (Entry e = tab[i] ; e != null ; e = e.next)
                 if (e.value == null)
                     return true;
     return false;
     }
```

    判断一个value是否存在比判断key是否存在还要简单，就是遍历所有元素判断是否有相等的值。这里分为两种情况处理，value为null何不为null的情况，但内容差不多，只是判断相等的方式不同。

    这个判断是否存在必须遍历所有元素，是一个双重循环的过程，因此是比较耗时的操作。

    接着看HashMap中“删除”相关的操作，有remove(Object key)和clear()两个方法。

    remove(Object key)

```
 public V remove(Object key) {
         Entry<K,V> e = removeEntryForKey(key);
         return (e == null ? null : e.value);
     }
```

    看这个方法，removeEntryKey(key)的返回结果应该是被移除的元素，如果不存在这个元素则返回为null。remove方法根据removeEntryKey返回的结果e是否为null返回null或e.value。

    removeEntryForKey(Object key)

```
 final Entry<K,V> removeEntryForKey(Object key) {
         int hash = (key == null) ? 0 : hash(key.hashCode());
         int i = indexFor(hash, table.length);
         Entry<K,V> prev = table[i];
         Entry<K,V> e = prev;
 
         while (e != null) {
             Entry<K,V> next = e.next;
             Object k;
             if (e.hash == hash &&
                 ((k = e.key) == key || (key != null && key.equals(k)))) {
                 modCount++;
                 size--;
                 if (prev == e)
                     table[i] = next;
                 else
                     prev.next = next;
                 e.recordRemoval(this);
                 return e;
             }
             prev = e;
             e = next;
         }
 
         return e;
     }
```

    上面的这个过程就是先找到table数组中对应的索引，接着就类似于一般的链表的删除操作，而且是单向链表删除节点，很简单。在C语言中就是修改指针，这个例子中就是将要删除节点的前一节点的next指向删除被删除节点的next即可。

    clear()

```
 public void clear() {
         modCount++;
         Entry[] tab = table;
         for (int i = 0; i < tab.length; i++)
             tab[i] = null;
         size = 0;
     }
```

    clear()方法删除HashMap中所有的元素，这里就不用一个个删除节点了，而是直接将table数组内容都置空，这样所有的链表都已经无法访问，Java的垃圾回收机制会去处理这些链表。table数组置空后修改size为0。

    这里为什么不直接操作table而是通过tab呢？希望有知道的大侠指点一二。

    主要方法看的差不多了，接着看一个上面提到了好几次但是都搁在一边没有分析的方法：entrySet()。 

    entrySet()

```
 public Set<Map.Entry<K,V>> entrySet() {
     return entrySet0();
     }
 
     private Set<Map.Entry<K,V>> entrySet0() {
         Set<Map.Entry<K,V>> es = entrySet;
         return es != null ? es : (entrySet = new EntrySet());
     }
```

    为什么会有这样的方法，只是调用了一下entrySet0，而且entrySet0的名称看着就很奇怪。再看entrySet0方法中为什么不直接return entrySet!=null?entrySet:(entrySet = new EntrySet)呢？

    上面的疑问还没解开，但是先看entrySet这个属性吧，在文章开头的属性定义中并没有给出这个属性，下面先看一下它的定义：

```
 private transient Set<Map.Entry<K,V>> entrySet = null;
```

    它是一个内容为Map.Entry<K,V>的Set。看看在哪些地方往里面添加了元素。 

    为什么上面的那句话我要把它标成红色？因为这是一个陷阱，在看代码的时候我就陷进去了。

    仔细看EntrySet这个类。

```
 private final class EntrySet extends AbstractSet<Map.Entry<K,V>> {
         public Iterator<Map.Entry<K,V>> iterator() {
             return newEntryIterator();
         }
         public boolean contains(Object o) {
             if (!(o instanceof Map.Entry))
                 return false;
             Map.Entry<K,V> e = (Map.Entry<K,V>) o;
             Entry<K,V> candidate = getEntry(e.getKey());
             return candidate != null && candidate.equals(e);
         }
         public boolean remove(Object o) {
             return removeMapping(o) != null;
         }
         public int size() {
             return size;
         }
         public void clear() {
             HashMap.this.clear();
         }
     }
```

    看到了什么？这个类根本就没属性，它只是个代理。因为它内部类，可以访问外部类的内容，debug的时候能看到的属性都是继承或者外部类的属性，输出的时候其实也是调用到了父类的toString方法将HashMap中的内容输出了。

    keySet()

```
 public Set<K> keySet() {
         Set<K> ks = keySet;
         return (ks != null ? ks : (keySet = new KeySet()));
     }
```

    是不是和entrySet0()方法很像！

```
 private final class KeySet extends AbstractSet<K> {
         public Iterator<K> iterator() {
             return newKeyIterator();
         }
         public int size() {
             return size;
         }
         public boolean contains(Object o) {
             return containsKey(o);
         }
         public boolean remove(Object o) {
             return HashMap.this.removeEntryForKey(o) != null;
         }
         public void clear() {
             HashMap.this.clear();
         }
     }
```

    同样是个代理类，contains、remove、clear方法都是调用的HashMap的方法。 

    values()

```
 public Collection<V> values() {
         Collection<V> vs = values;
         return (vs != null ? vs : (values = new Values()));
     }
 
     private final class Values extends AbstractCollection<V> {
         public Iterator<V> iterator() {
             return newValueIterator();
         }
         public int size() {
             return size;
         }
         public boolean contains(Object o) {
             return containsValue(o);
         }
         public void clear() {
             HashMap.this.clear();
         }
     }
```

    values()方法也一样是代理。只是Values类继承自AbstractCollention类，而不是AbstractSet。

    还有一个重要的内容没有进行说明，那就是迭代器。HashMap中的entrySet()、keySet()、values()等方法都使用到了迭代器Iterator的知识。其他集合类也有使用到迭代器，将另写博文总结讨论集合类的迭代器。