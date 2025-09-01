---
title: TreeMap源码分析——深入分析（基于JDK1.6）
id: 330
date: 2024-10-31 22:01:42
author: daichangya
excerpt: TreeMap有Values、EntrySet、KeySet、PrivateEntryIterator、EntryIterator、ValueIterator、KeyIterator、DescendingKeyIterator、NavigableSubMap、AscendingSubMap、DescendingSubMap、SubMap、Entry共十三个内部类。Entry是在TreeMap中用于
permalink: /archives/TreeMap-yuan-ma-fen-xi-shen-ru-fen-xi/
categories:
- java基础
- java源码分析
---



TreeMap有Values、EntrySet、KeySet、PrivateEntryIterator、EntryIterator、ValueIterator、KeyIterator、DescendingKeyIterator、NavigableSubMap、AscendingSubMap、DescendingSubMap、SubMap、Entry共十三个内部类。Entry是在TreeMap中用于表示树的节点的内部类，已经在《TreeMap源码分析——基础分析》中分析过。下面逐一介绍上面的内部类以及TreeMap中提供的和内部类相关的方法。

     TreeMap有Values、EntrySet、KeySet、PrivateEntryIterator、EntryIterator、ValueIterator、KeyIterator、DescendingKeyIterator、NavigableSubMap、AscendingSubMap、DescendingSubMap、SubMap、Entry共十三个内部类。Entry是在TreeMap中用于表示树的节点的内部类，已经在[《TreeMap源码分析——基础分析》](https://blog.jsdiff.com/archives/TreeMap-Base)中分析过。下面逐一介绍上面的内部类以及TreeMap中提供的和内部类相关的方法。

     先看Values。

```
 // 从类的定义可以看出，Values是一个集合类
 class Values extends AbstractCollection<V> {
     // 提供集合类Values的迭代器
     public Iterator<V> iterator() {
         return new ValueIterator(getFirstEntry());
     }
     // 返回TreeMap中保存的节点数
     public int size() {
         return TreeMap.this.size();
     }
     // 判断TreeMap中是否存在Value为o的节点
     public boolean contains(Object o) {
         return TreeMap.this.containsValue(o);
     }
     // 删除一个对象
     public boolean remove(Object o) {
         // 遍历TreeMap
         for (Entry<K,V> e = getFirstEntry(); e != null; e = successor(e)) {
             // 寻找值相等的节点
             if (valEquals(e.getValue(), o)) {
                 // 删除找到的节点
                 deleteEntry(e);
                 return true;
             }
         }
         return false;
     }
     // 清空TreeMap
     public void clear() {
         TreeMap.this.clear();
     }
 }
```

     Values类实际上是一个代理，多数方法都是调用TreeMap的方法。在Values的iterator()方法中返回了一个ValuesIterator对象，下面来看和迭代器相关的内部类。PrivateEntryIterator是TreeMap中和迭代器相关的类的基础，以下是PrivateEntryIterator的内容。

```
 abstract class PrivateEntryIterator<T> implements Iterator<T> {
     // 指向next的引用
 Entry<K,V> next;
 // 保留对上一次返回节点的引用
     Entry<K,V> lastReturned;
     int expectedModCount;
     // 构造方法，lastReturned置空，next指向传入的节点
     PrivateEntryIterator(Entry<K,V> first) {
         expectedModCount = modCount;
         lastReturned = null;
         next = first;
     }
     // 判断是否还有下一个节点
     public final boolean hasNext() {
         return next != null;
     }
     // 返回下一个节点
     final Entry<K,V> nextEntry() {
         Entry<K,V> e = next;
         if (e == null)
             throw new NoSuchElementException();
         if (modCount != expectedModCount)
             throw new ConcurrentModificationException();
         // next移动到它的继承者
         next = successor(e);
         // 记录被返回的节点
         lastReturned = e;
         // 返回原先记录的next节点
         return e;
     }
     // 前一个节点
     final Entry<K,V> prevEntry() {
         Entry<K,V> e = next;
         if (e == null)
             throw new NoSuchElementException();
         if (modCount != expectedModCount)
             throw new ConcurrentModificationException();
         // 获取指定节点的“前任”（按遍历次序的前一个节点）
         next = predecessor(e);
         // 记录被返回的节点
         lastReturned = e;
         return e;
     }
     // 移除最近一次被返回的节点
     public void remove() {
         if (lastReturned == null)
             throw new IllegalStateException();
         if (modCount != expectedModCount)
             throw new ConcurrentModificationException();
         // deleted entries are replaced by their successors
         if (lastReturned.left != null && lastReturned.right != null)
             /* 如果被删除节点有两个孩子，删除节点e的时候e的引用会被修改为指向原节点的继承者，所以这里先保留next对lastReturned的引用，这样在删除节点后就能获取到继承者的引用，继而继续遍历树 */
             next = lastReturned;
         // 删除节点
         deleteEntry(lastReturned);
         expectedModCount = modCount;
         lastReturned = null;
     }
 }
```

     PrivateEntryIterator类的prevEntry()方法用到了predecessor(Entry<K,V> t)方法，下面对这个方法进行介绍。

     predecessor(Entry<K,V> t)方法返回传入节点的“前一个”节点，至于前一个节点是哪个节点，这和树的遍历次序相关。根据successor(Entry<K,V> t)和predecessor(Entry<K,V> t)方法可以推出TreeMap中树的遍历次序是中根遍历（左孩子-根-右孩子）。

```
 static <K,V> Entry<K,V> predecessor(Entry<K,V> t) {
     if (t == null)
         return null;
 else if (t.left != null) {
     // 获得左孩子
         Entry<K,V> p = t.left;
         // 对左孩子进行遍历，获取左孩子最右的子孙
         while (p.right != null)
             p = p.right;
         return p;
 } else {
     // 获取t的父节点
         Entry<K,V> p = t.parent;
         Entry<K,V> ch = t; 
 // 沿着右孩子向上查找继承者，直到根节点或找到节点ch是其父节点的右孩子的节点
         while (p != null && ch == p.left) {
             ch = p;
             p = p.parent;
         }
         return p;
     }
 }
```

     下面是TreeMap中其它和迭代器相关的内部类。

```
 // EntryIterator就是树节点的迭代器，和PrivateEntryIterator完全一样，因为提供的方法都直接的调用而来父类的方法。
 final class EntryIterator extends PrivateEntryIterator<Map.Entry<K,V>> {
     EntryIterator(Entry<K,V> first) {
         super(first);
     }
     public Map.Entry<K,V> next() {
         return nextEntry();
     }
 }
 /** Value的迭代器 */
 final class ValueIterator extends PrivateEntryIterator<V> {
     ValueIterator(Entry<K,V> first) {
         super(first);
 }
 // next()方法返回的是节点的value值
     public V next() {
         return nextEntry().value;
     }
 }
 /** Key迭代器 */
 final class KeyIterator extends PrivateEntryIterator<K> {
     KeyIterator(Entry<K,V> first) {
         super(first);
 }
 // next()方法返回的是节点的key
     public K next() {
         return nextEntry().key;
     }
 }
 /** 逆序的Key迭代器 */
 final class DescendingKeyIterator extends PrivateEntryIterator<K> {
     DescendingKeyIterator(Entry<K,V> first) {
         super(first);
 }
 // next()方法返回的是节点的“前任”（按照遍历次序的前一个节点）的key
     public K next() {
         return prevEntry().key;
     }
 }
```

     除了迭代器相关的内部类，TreeMap还有两个和Set相关的内部类，分别是EntrySet和KeySet。两个类分别表示节点的集合和键的集合。下面具体看这两个类的实现。

```
 // 继承自AbstractSet说明是一个Set
 class EntrySet extends AbstractSet<Map.Entry<K,V>> {
     // iterator()方法返回的是上面介绍过的EntryIterator对象
     public Iterator<Map.Entry<K,V>> iterator() {
         return new EntryIterator(getFirstEntry());
     }
     // 判断是否包含某个节点的方法
     public boolean contains(Object o) {
         if (!(o instanceof Map.Entry))
             return false;
         Map.Entry<K,V> entry = (Map.Entry<K,V>) o;
         V value = entry.getValue();
         Entry<K,V> p = getEntry(entry.getKey());
         // 判断是否包含某个对象的标准是存在节点的key的与传入对象的key值，且该节点的value也与存入对象的value值相等
         return p != null && valEquals(p.getValue(), value);
     }
     // 删除一个对象
     public boolean remove(Object o) {
         if (!(o instanceof Map.Entry))
             return false;
         Map.Entry<K,V> entry = (Map.Entry<K,V>) o;
         V value = entry.getValue();
         Entry<K,V> p = getEntry(entry.getKey());
         // 如果存在该对象，则进行删除操作并返回true
         if (p != null && valEquals(p.getValue(), value)) {
             deleteEntry(p);
             return true;
         }
         // 不存在直接返回false
         return false;
     }
     // size()返回的是TreeMap中包含的节点的数量
     public int size() {
         return TreeMap.this.size();
     }
     // clear()方法实际调用了TreeMap的clear()方法，和size()方法都是代理方法
     public void clear() {
         TreeMap.this.clear();
     }
 }
```

```
 // KeySet同样继承自AbstractSet。KeySet实现了NavigableSet接口，意味着是“可导航”的Set，包含更多的获取指定节点的方法
 static final class KeySet<E> extends AbstractSet<E> implements NavigableSet<E> {
 private final NavigableMap<E, Object> m;
 // 构造方法
     KeySet(NavigableMap<E,Object> map) { m = map; }
     // 
     public Iterator<E> iterator() {
         if (m instanceof TreeMap)
             return ((TreeMap<E,Object>)m).keyIterator();
         else
             // 这里涉及到的NavigableSubMap将在后面介绍
             return (Iterator<E>)(((TreeMap.NavigableSubMap)m).keyIterator());
     }
 
     public Iterator<E> descendingIterator() {
         if (m instanceof TreeMap)
             return ((TreeMap<E,Object>)m).descendingKeyIterator();
         else
             return (Iterator<E>)(((TreeMap.NavigableSubMap)m).descendingKeyIterator());
     }
     // size()方法返回的是通过构造方法传入的map的大小
 public int size() { return m.size(); }
 // isEmpty()判断是否为空也是判断的传入的map是否为空
 public boolean isEmpty() { return m.isEmpty(); }
 // contains(Object o)方法判断传入map中是否包含这个key
     public boolean contains(Object o) { return m.containsKey(o); }
 public void clear() { m.clear(); }
 // 因为传入的map是NavigableMap，所以下面这几个方法都是代理方法，调用map中相应的方法
     public E lower(E e) { return m.lowerKey(e); }
     public E floor(E e) { return m.floorKey(e); }
     public E ceiling(E e) { return m.ceilingKey(e); }
     public E higher(E e) { return m.higherKey(e); }
     public E first() { return m.firstKey(); }
 public E last() { return m.lastKey(); }
 // 获取传入map的比较器
 public Comparator<? super E> comparator() { return m.comparator(); }
 // 获取map中第一个节点的key
     public E pollFirst() {
         Map.Entry<E,Object> e = m.pollFirstEntry();
         return e == null? null : e.getKey();
 }
 // 获取map中最后一个节点的key
     public E pollLast() {
         Map.Entry<E,Object> e = m.pollLastEntry();
         return e == null? null : e.getKey();
 }
 // 删除一个对象，实际上是删除map中以这个对象为key的一个节点
     public boolean remove(Object o) {
         int oldSize = size();
         m.remove(o);
         return size() != oldSize;
 }
 // 下面的方法都是通过NavigableMap和TreeSet实现的，NavigableMap将在下文介绍，TreeSet将另开博文介绍
     public NavigableSet<E> subSet(E fromElement, boolean fromInclusive,
                                       E toElement,   boolean toInclusive) {
         return new TreeSet<E>(m.subMap(fromElement, fromInclusive,
                                            toElement,   toInclusive));
     }
     public NavigableSet<E> headSet(E toElement, boolean inclusive) {
         return new TreeSet<E>(m.headMap(toElement, inclusive));
     }
     public NavigableSet<E> tailSet(E fromElement, boolean inclusive) {
         return new TreeSet<E>(m.tailMap(fromElement, inclusive));
     }
     public SortedSet<E> subSet(E fromElement, E toElement) {
         return subSet(fromElement, true, toElement, false);
     }
     public SortedSet<E> headSet(E toElement) {
         return headSet(toElement, false);
     }
     public SortedSet<E> tailSet(E fromElement) {
         return tailSet(fromElement, true);
     }
     public NavigableSet<E> descendingSet() {
         return new TreeSet(m.descendingMap());
     }
 }
```

     介绍完了两个和Set相关的内部类，现在还剩下四个和SubMap相关的内部类：NavigableSubMap、AscendingSubMap、DescendingSubMap、SubMap。

     首先看NavigableSubMap，它足足有400多行代码，相当的多，需要耐心啊。

```
 // NavigableSubMap是一个抽象类，继承了AbstractMap，实现了NavigableMap接口
 static abstract class NavigableSubMap<K,V> extends AbstractMap<K,V>
         implements NavigableMap<K,V>, java.io.Serializable {
     // 存储内容的Map
     final TreeMap<K,V> m;
     // lowKey、highKey
     final K lo, hi;
     // 标识map的边界是否是map的第一个节点和最后一个节点
     final boolean fromStart, toEnd;
     // 是否包含最低lo、最高位置hi
     final boolean loInclusive, hiInclusive;
     // 通过上面的三组变量可以组成两个三元组表示一个集合的两个端点
     // 构造方法
     NavigableSubMap(TreeMap<K,V> m,
                         boolean fromStart, K lo, boolean loInclusive,
                         boolean toEnd,     K hi, boolean hiInclusive) {
         if (!fromStart && !toEnd) {
             // lo>hi抛出异常
             if (m.compare(lo, hi) > 0)
                 throw new IllegalArgumentException("fromKey > toKey");
         } else {
             if (!fromStart) // type check
                 m.compare(lo, lo);
             if (!toEnd)
                 m.compare(hi, hi);
         }
 
         this.m = m;
         this.fromStart = fromStart;
         this.lo = lo;
         this.loInclusive = loInclusive;
         this.toEnd = toEnd;
         this.hi = hi;
         this.hiInclusive = hiInclusive;
     }
 
     // tooLow 判断传入的key是否太小
     final boolean tooLow(Object key) {
         // 如果fromStart为false，需要判断最低边界 
         if (!fromStart) {
             int c = m.compare(key, lo);
             // 如果key<lo或者相等但是map的边界不包含lo，那么key越界了，即小于最小值
             if (c < 0 || (c == 0 && !loInclusive))
                 return true;
         }
         // 默认返回false
         return false;
     }
     // 与上面的tooLow类似
     final boolean tooHigh(Object key) {
         if (!toEnd) {
             int c = m.compare(key, hi);
             if (c > 0 || (c == 0 && !hiInclusive))
                 return true;
         }
         return false;
     }
     // 判断是否在范围内，即满足最低最高限制，结合tooLow和tooHigh即可
     final boolean inRange(Object key) {
         return !tooLow(key) && !tooHigh(key);
     }
     // 是否在封闭的区间内
     final boolean inClosedRange(Object key) {
         return (fromStart || m.compare(key, lo) >= 0)
                 && (toEnd || m.compare(hi, key) >= 0);
     }
     // 判断是否是在一个区间内
     final boolean inRange(Object key, boolean inclusive) {
         return inclusive ? inRange(key) : inClosedRange(key);
     }
     // 获取绝对的最低的节点
 final TreeMap.Entry<K,V> absLowest() {
 /* 如果fromStart为true，获取第一个节点，否则根据loInclusive是否为true，即是否包含lo来决定获取Ceiling节点或Higher节点；getCeilingEntry意为获取指定key的节点或者比指定key大的最小节点，如果不存在则返回null；getHigherEntry意为获取比指定key大的最小节点，如果不存在，返回null */
     TreeMap.Entry<K,V> e =
                 (fromStart ?  m.getFirstEntry() :
                  (loInclusive ? m.getCeilingEntry(lo) :
                                 m.getHigherEntry(lo)));
         // 判断得到的节点是否为空或者key过大
         return (e == null || tooHigh(e.key)) ? null : e;
     }
     // 与absLowest类似
     final TreeMap.Entry<K,V> absHighest() {
     TreeMap.Entry<K,V> e =
                 (toEnd ?  m.getLastEntry() :
                  (hiInclusive ?  m.getFloorEntry(hi) :
                                  m.getLowerEntry(hi)));
         return (e == null || tooLow(e.key)) ? null : e;
     }
     // 寻找大于等于key的最小的节点
 final TreeMap.Entry<K,V> absCeiling(K key) {
     // 如果key太小，返回绝对的最小的节点
         if (tooLow(key))
             return absLowest();
         // 获取允许的key的极限节点（满足要求的最小的节点）
         TreeMap.Entry<K,V> e = m.getCeilingEntry(key);
         return (e == null || tooHigh(e.key)) ? null : e;
     }
     // 和absCeiling类似，只是获取的不包含相等的情况，而是寻找大于key的最小节点
     final TreeMap.Entry<K,V> absHigher(K key) {
         if (tooLow(key))
             return absLowest();
         TreeMap.Entry<K,V> e = m.getHigherEntry(key);
         return (e == null || tooHigh(e.key)) ? null : e;
     }
     // 获取绝对的小于等于key的节点
 final TreeMap.Entry<K,V> absFloor(K key) {
     // 指定的key超出了hi，直接返回绝对的允许的最大的节点
         if (tooHigh(key))
             return absHighest();
         /* getFloorEntry 获取的是指定key的节点，如果不存在这样的节点，就去获取比指定key小的最大的节点，如果这样的节点也不存在，返回null*/
         TreeMap.Entry<K,V> e = m.getFloorEntry(key);
         return (e == null || tooLow(e.key)) ? null : e;
     }
     // 与上面的absFloor类似，只是不包含等于的情况
     final TreeMap.Entry<K,V> absLower(K key) {
         if (tooHigh(key))
             return absHighest();
         TreeMap.Entry<K,V> e = m.getLowerEntry(key);
         return (e == null || tooLow(e.key)) ? null : e;
     }
 
     // 返回比最大的节点“还要大”的节点（Fence是栅栏、围栏的意思）
 final TreeMap.Entry<K,V> absHighFence() {
     /* 如果toEnd是true，那么“围在”它外面的是null，如果是false，根据hi是否被包含返回getHigherEntry或getCeilingEntry，这两个方法意思在上面的方法中说明过了 */
         return (toEnd ? null : (hiInclusive ?
                                     m.getHigherEntry(hi) :
                                     m.getCeilingEntry(hi)));
     }
 
     // 与absHighFence类似
     final TreeMap.Entry<K,V> absLowFence() {
             return (fromStart ? null : (loInclusive ?
                                         m.getLowerEntry(lo) :
                                         m.getFloorEntry(lo)));
     }
 
     abstract TreeMap.Entry<K,V> subLowest();
     abstract TreeMap.Entry<K,V> subHighest();
     abstract TreeMap.Entry<K,V> subCeiling(K key);
     abstract TreeMap.Entry<K,V> subHigher(K key);
     abstract TreeMap.Entry<K,V> subFloor(K key);
     abstract TreeMap.Entry<K,V> subLower(K key);
     abstract Iterator<K> keyIterator();
     abstract Iterator<K> descendingKeyIterator();
 
     // 如果fromStart、toEnd都是true，那么判断空、获取大小都是直接通过m，不然就必须使用entrySet()先获取节点集
     public boolean isEmpty() {
         return (fromStart && toEnd) ? m.isEmpty() : entrySet().isEmpty();
     }
 
     public int size() {
         return (fromStart && toEnd) ? m.size() : entrySet().size();
     }
     // 判断是否存在key先判断范围，在通过TreeMap的containKey方法来判断
     public final boolean containsKey(Object key) {
         return inRange(key) && m.containsKey(key);
     }
     // 添加节点
 public final V put(K key, V value) {
     // 判断要添加的key是否在范围内
         if (!inRange(key))
             throw new IllegalArgumentException("key out of range");
         return m.put(key, value);
     }
     public final V get(Object key) {
         return !inRange(key)? null :  m.get(key);
     }
     public final V remove(Object key) {
         return !inRange(key)? null  : m.remove(key);
 }
 public final Map.Entry<K,V> ceilingEntry(K key) {
         /* exportEntry(TreeMap.Entry<K,V> e)方法返回的是Map.Entry<K,V>对象，它的Key 和Value和传入的节点的Key 和Value相同 */
         return exportEntry(subCeiling(key));
     }
 public final K ceilingKey(K key) {
         // keyOrNull根据传入的节点是否为null返回null或节点的key（相当于提供了一个null安全的获取key的方法）
         return keyOrNull(subCeiling(key));
     }
     public final Map.Entry<K,V> higherEntry(K key) {
         return exportEntry(subHigher(key));
     }
     public final K higherKey(K key) {
        return keyOrNull(subHigher(key));
     }
     public final Map.Entry<K,V> floorEntry(K key) {
         return exportEntry(subFloor(key));
     }
     public final K floorKey(K key) {
         return keyOrNull(subFloor(key));
     }
     public final Map.Entry<K,V> lowerEntry(K key) {
         return exportEntry(subLower(key));
     }
     public final K lowerKey(K key) {
         return keyOrNull(subLower(key));
     }
     public final K firstKey() {
         return key(subLowest());
     }
     public final K lastKey() {
         return key(subHighest());
     }
     public final Map.Entry<K,V> firstEntry() {
         return exportEntry(subLowest());
     }
     public final Map.Entry<K,V> lastEntry() {
         return exportEntry(subHighest());
     }
     // 返回并删除第一个节点
     public final Map.Entry<K,V> pollFirstEntry() {
     TreeMap.Entry<K,V> e = subLowest();
         Map.Entry<K,V> result = exportEntry(e);
         if (e != null)
             m.deleteEntry(e);
         return result;
     }
     // 返回并删除最后一个节点
     public final Map.Entry<K,V> pollLastEntry() {
     TreeMap.Entry<K,V> e = subHighest();
         Map.Entry<K,V> result = exportEntry(e);
         if (e != null)
             m.deleteEntry(e);
         return result;
     }
 
     // 这些都是视图
     transient NavigableMap<K,V> descendingMapView = null;
     transient EntrySetView entrySetView = null;
     transient KeySet<K> navigableKeySetView = null;
     // 返回TreeMap的KeySet
     public final NavigableSet<K> navigableKeySet() {
         KeySet<K> nksv = navigableKeySetView;
         return (nksv != null) ? nksv :
             (navigableKeySetView = new TreeMap.KeySet(this));
     }
     public final Set<K> keySet() {
         return navigableKeySet();
     }
     // 逆序的KeySet
     public NavigableSet<K> descendingKeySet() {
         return descendingMap().navigableKeySet();
     }
     // 返回一个子Map
     public final SortedMap<K,V> subMap(K fromKey, K toKey) {
         return subMap(fromKey, true, toKey, false);
     }
     // 下面这几个方法会在后面给出分析
     public final SortedMap<K,V> headMap(K toKey) {
         return headMap(toKey, false);
     }
     public final SortedMap<K,V> tailMap(K fromKey) {
         return tailMap(fromKey, true);
     }
 
     // 视图类
     abstract class EntrySetView extends AbstractSet<Map.Entry<K,V>> {
         private transient int size = -1, sizeModCount;
         // 返回子Map的大小
         public int size() {
             // 如果fromStart和toEnd都是true，返回的是m的size
             if (fromStart && toEnd)
                 return m.size();
             // size=-1或标记size不同，重新计算一次size
             if (size == -1 || sizeModCount != m.modCount) {
                 sizeModCount = m.modCount;
                 size = 0;
                 Iterator i = iterator();
                 while (i.hasNext()) {
                     size++;
                     i.next();
                 }
             }
             return size;
         }
         // 判断EntrySet是否为空
         public boolean isEmpty() {
             TreeMap.Entry<K,V> n = absLowest();
             return n == null || tooHigh(n.key);
         }
         // 判断是否包含某个对象
         public boolean contains(Object o) {
             if (!(o instanceof Map.Entry))
                 return false;
             Map.Entry<K,V> entry = (Map.Entry<K,V>) o;
             K key = entry.getKey();
             // key不在范围内，返回false
             if (!inRange(key))
                 return false;
             // 判断是否有键和值如传入节点的键和值相等的节点
             TreeMap.Entry node = m.getEntry(key);
             return node != null &&
                 valEquals(node.getValue(), entry.getValue());
         }
         // 移除一个节点
         public boolean remove(Object o) {
             if (!(o instanceof Map.Entry))
                 return false;
             Map.Entry<K,V> entry = (Map.Entry<K,V>) o;
             K key = entry.getKey();
             if (!inRange(key))
                 return false;
             TreeMap.Entry<K,V> node = m.getEntry(key);
             // 找到节点并移除，返回true
             if (node!=null && valEquals(node.getValue(),entry.getValue())){
                 m.deleteEntry(node);
                 return true;
             }
             return false;
         }
     }
 
     //子类迭代器
     abstract class SubMapIterator<T> implements Iterator<T> {
         // 上一次被返回的节点
         TreeMap.Entry<K,V> lastReturned;
         // 下一个节点
         TreeMap.Entry<K,V> next;
         // “栅栏”key（如果是向大的方向遍历，不能访问key大于等于fenceKey的节点；如果是向小的方向遍历，不能访问key小于等于fenceKey的节点）
         final K fenceKey;
         int expectedModCount;
         // 构造方法
         SubMapIterator(TreeMap.Entry<K,V> first,
                        TreeMap.Entry<K,V> fence) {
             expectedModCount = m.modCount;
             lastReturned = null;
             next = first;
             fenceKey = fence == null ? null : fence.key;
         }
         // 判断是否还有下一个节点
         public final boolean hasNext() {
             // 与普通的hasNext的判断不同的是这里必须判断next的key是否超出了fenceKey
             return next != null && next.key != fenceKey;
         }
         // 获得下一个节点的方法，比较容易理解
         final TreeMap.Entry<K,V> nextEntry() {
             TreeMap.Entry<K,V> e = next;
             if (e == null || e.key == fenceKey)
                 throw new NoSuchElementException();
             if (m.modCount != expectedModCount)
                 throw new ConcurrentModificationException();
             next = successor(e);
 lastReturned = e;
             return e;
         }
         // 另一种遍历方法，向前遍历
         final TreeMap.Entry<K,V> prevEntry() {
             TreeMap.Entry<K,V> e = next;
             if (e == null || e.key == fenceKey)
                 throw new NoSuchElementException();
             if (m.modCount != expectedModCount)
                 throw new ConcurrentModificationException();
             next = predecessor(e);
 lastReturned = e;
             return e;
         }
         // 删除节点后可以继续遍历剩余的节点，因为删除前用next保留了lastReturned节点，而这个节点在删除操作的过程中被替换成了它的继承者
         final void removeAscending() {
             if (lastReturned == null)
                 throw new IllegalStateException();
             if (m.modCount != expectedModCount)
                 throw new ConcurrentModificationException();
             if (lastReturned.left != null && lastReturned.right != null)
                 // next指向lastReturned所指向的节点，这个节点的内容在删除lastReturned的时候被改变了
                 next = lastReturned;
             m.deleteEntry(lastReturned);
             lastReturned = null;
             expectedModCount = m.modCount;
         }
         // 删除之后next指向的节点其实被删除了，不能继续迭代访问
         final void removeDescending() {
             if (lastReturned == null)
                 throw new IllegalStateException();
             if (m.modCount != expectedModCount)
                 throw new ConcurrentModificationException();
             m.deleteEntry(lastReturned);
             lastReturned = null;
             expectedModCount = m.modCount;
         }
 
     }
     //下面的几个内部类很简单，都是对SubMapIterator的调用或间接调用，不再解释
     final class SubMapEntryIterator extends SubMapIterator<Map.Entry<K,V>> {
         SubMapEntryIterator(TreeMap.Entry<K,V> first,
                                 TreeMap.Entry<K,V> fence) {
             super(first, fence);
         }
         public Map.Entry<K,V> next() {
             return nextEntry();
         }
         public void remove() {
             removeAscending();
         }
     }
 
     final class SubMapKeyIterator extends SubMapIterator<K> {
         SubMapKeyIterator(TreeMap.Entry<K,V> first,
                               TreeMap.Entry<K,V> fence) {
             super(first, fence);
         }
         public K next() {
             return nextEntry().key;
         }
         public void remove() {
             removeAscending();
         }
     }
 
     final class DescendingSubMapEntryIterator extends SubMapIterator<Map.Entry<K,V>> {
         DescendingSubMapEntryIterator(TreeMap.Entry<K,V> last,
                                           TreeMap.Entry<K,V> fence) {
             super(last, fence);
         }
 
         public Map.Entry<K,V> next() {
             return prevEntry();
         }
         public void remove() {
             removeDescending();
         }
     }
 
     final class DescendingSubMapKeyIterator extends SubMapIterator<K> {
         DescendingSubMapKeyIterator(TreeMap.Entry<K,V> last,
                                         TreeMap.Entry<K,V> fence) {
             super(last, fence);
         }
         public K next() {
             return prevEntry().key;
         }
         public void remove() {
             removeDescending();
         }
     }
 }
```

     NavigableSubMap类算是看了一遍，很复杂，自身是个内部类，它里面还包含了好几个类。理解它的代码需要部分TreeMap中的其他代码的深入理解，如涉及到的deleteEntry等方法（见[《TreeMap源码分析——基础分析》](https://blog.jsdiff.com/archives/TreeMap-Base.html)）。

     下面看TreeMap的其他内部类，它们是NavigableSubMap的子类。

     **AscendingSubMap**

```
 // AscendingSubMap继承自NavigableSubMap
 static final class AscendingSubMap<K,V> extends NavigableSubMap<K,V> {
     private static final long serialVersionUID = 912986545866124060L;
     // 构造方法，直接调用父类构造方法
     AscendingSubMap(TreeMap<K,V> m,
                         boolean fromStart, K lo, boolean loInclusive,
                         boolean toEnd,     K hi, boolean hiInclusive) {
         super(m, fromStart, lo, loInclusive, toEnd, hi, hiInclusive);
     }
     // 获得比较器
     public Comparator<? super K> comparator() {
         return m.comparator();
     }
     // “截取”子Map
     public NavigableMap<K,V> subMap(K fromKey, boolean fromInclusive,
                                         K toKey,   boolean toInclusive) {
         // 截取之前判断是否超出范围
         if (!inRange(fromKey, fromInclusive))
             throw new IllegalArgumentException("fromKey out of range");
         if (!inRange(toKey, toInclusive))
             throw new IllegalArgumentException("toKey out of range");
         return new AscendingSubMap(m,
                                        false, fromKey, fromInclusive,
                                        false, toKey,   toInclusive);
     }
     // “截取”子Map，headMap通过构造方法便可以实现
     public NavigableMap<K,V> headMap(K toKey, boolean inclusive) {
         if (!inRange(toKey, inclusive))
             throw new IllegalArgumentException("toKey out of range");
         return new AscendingSubMap(m,
                                        fromStart, lo,    loInclusive,
                                        false,     toKey, inclusive);
     }
     // 和headMap类似
     public NavigableMap<K,V> tailMap(K fromKey, boolean inclusive){
         if (!inRange(fromKey, inclusive))
             throw new IllegalArgumentException("fromKey out of range");
         return new AscendingSubMap(m,
                                        false, fromKey, inclusive,
                                        toEnd, hi,      hiInclusive);
     }
     // 这个方法涉及到DescendingSubMap类的构造方法，在下面会介绍到
     public NavigableMap<K,V> descendingMap() {
         NavigableMap<K,V> mv = descendingMapView;
         return (mv != null) ? mv :
                 (descendingMapView =
                  new DescendingSubMap(m,
                                       fromStart, lo, loInclusive,
                                       toEnd,     hi, hiInclusive));
     }
     // 下面两个方法都是对上面提到过的构造方法的调用
     Iterator<K> keyIterator() {
         return new SubMapKeyIterator(absLowest(), absHighFence());
     }
     Iterator<K> descendingKeyIterator() {
         return new DescendingSubMapKeyIterator(absHighest(), absLowFence());
 }
     // AscendingEntrySetView是一个视图类，重写了父类的iterator()方法，调用SubMapEntryIterator构造迭代器
     final class AscendingEntrySetView extends EntrySetView {
         public Iterator<Map.Entry<K,V>> iterator() {
             return new SubMapEntryIterator(absLowest(), absHighFence());
         }
     }
     // 获取节点集合的方法
     public Set<Map.Entry<K,V>> entrySet() {
         EntrySetView es = entrySetView;
         return (es != null) ? es : new AscendingEntrySetView();
     }
     // 父类中抽象方法的实现，都很简单
     TreeMap.Entry<K,V> subLowest()       { return absLowest(); }
     TreeMap.Entry<K,V> subHighest()      { return absHighest(); }
     TreeMap.Entry<K,V> subCeiling(K key) { return absCeiling(key); }
     TreeMap.Entry<K,V> subHigher(K key)  { return absHigher(key); }
     TreeMap.Entry<K,V> subFloor(K key)   { return absFloor(key); }
     TreeMap.Entry<K,V> subLower(K key)   { return absLower(key); }
 }
```

     **DescendingSubMap**

```
 // DescendingSubMap也继承自NavigableSubMap，和上面的AscendingSubMap对应
 static final class DescendingSubMap<K,V>  extends NavigableSubMap<K,V> {
     private static final long serialVersionUID = 912986545866120460L;
     DescendingSubMap(TreeMap<K,V> m,
                         boolean fromStart, K lo, boolean loInclusive,
                         boolean toEnd,     K hi, boolean hiInclusive) {
         super(m, fromStart, lo, loInclusive, toEnd, hi, hiInclusive);
     }
     // 构造一个“相反”的比较器
     private final Comparator<? super K> reverseComparator =
         Collections.reverseOrder(m.comparator);
     // 获取的比较器是“相反”的比较器，比较结果会对调
     public Comparator<? super K> comparator() {
         return reverseComparator;
     }
     // subMap方法和AscendingSubMap类中类似
     public NavigableMap<K,V> subMap(K fromKey, boolean fromInclusive,
                                         K toKey,   boolean toInclusive) {
         if (!inRange(fromKey, fromInclusive))
             throw new IllegalArgumentException("fromKey out of range");
         if (!inRange(toKey, toInclusive))
             throw new IllegalArgumentException("toKey out of range");
         return new DescendingSubMap(m,
                                         false, toKey,   toInclusive,
                                         false, fromKey, fromInclusive);
     }
     // 与AscendingSubMap中其实是相反的
     public NavigableMap<K,V> headMap(K toKey, boolean inclusive) {
         if (!inRange(toKey, inclusive))
             throw new IllegalArgumentException("toKey out of range");
         // 因为DescendingSubMap表示的是逆序的map，所以其实是通过获取原序的尾部
         return new DescendingSubMap(m,
                                         false, toKey, inclusive,
                                         toEnd, hi,    hiInclusive);
     }
     // 与headMap对应，tailMap其实获取的是原序中的头部
     public NavigableMap<K,V> tailMap(K fromKey, boolean inclusive){
         if (!inRange(fromKey, inclusive))
             throw new IllegalArgumentException("fromKey out of range");
         return new DescendingSubMap(m,
                                         fromStart, lo, loInclusive,
                                         false, fromKey, inclusive);
     }
     // 逆序的逆序其实是正序
     public NavigableMap<K,V> descendingMap() {
         NavigableMap<K,V> mv = descendingMapView;
         return (mv != null) ? mv :
                 (descendingMapView =
                  new AscendingSubMap(m,
                                      fromStart, lo, loInclusive,
                                      toEnd,     hi, hiInclusive));
     }
     // 剩余内容和AscendingSubMap很类似，就不说了
     Iterator<K> keyIterator() {
         return new DescendingSubMapKeyIterator(absHighest(), absLowFence());
     }
     Iterator<K> descendingKeyIterator() {
         return new SubMapKeyIterator(absLowest(), absHighFence());
     }
     final class DescendingEntrySetView extends EntrySetView {
         public Iterator<Map.Entry<K,V>> iterator() {
             return new DescendingSubMapEntryIterator(absHighest(), absLowFence());
         }
     }
     public Set<Map.Entry<K,V>> entrySet() {
         EntrySetView es = entrySetView;
         return (es != null) ? es : new DescendingEntrySetView();
     }
     TreeMap.Entry<K,V> subLowest()       { return absHighest(); }
     TreeMap.Entry<K,V> subHighest()      { return absLowest(); }
     TreeMap.Entry<K,V> subCeiling(K key) { return absFloor(key); }
     TreeMap.Entry<K,V> subHigher(K key)  { return absLower(key); }
     TreeMap.Entry<K,V> subFloor(K key)   { return absCeiling(key); }
     TreeMap.Entry<K,V> subLower(K key)   { return absHigher(key); }
 }
```

     最后一个内部类是SubMap，它比较特别。这个类存在仅仅为了序列化兼容之前的版本不支持NavigableMap TreeMap。它被翻译成一个旧版本AscendingSubMap子映射到一个新版本。这个类是从来没有以其他方式使用。

```
 // SubMap 继承自AbstractMap；这个类存在仅仅为了序列化兼容之前的版本不支持NavigableMap TreeMap。它被翻译成一个旧版本AscendingSubMap子映射到一个新版本。这个类是从来没有以其他方式使用。
 private class SubMap extends AbstractMap<K,V>
     implements SortedMap<K,V>, java.io.Serializable {
     private static final long serialVersionUID = -6520786458950516097L;
     // 标识是否从map的开始到结尾都属于子map
     private boolean fromStart = false, toEnd = false;
     // 开始位置和结束位置的key
     private K fromKey, toKey;
     private Object readResolve() {
         return new AscendingSubMap(TreeMap.this,
                                        fromStart, fromKey, true,
                                        toEnd, toKey, false);
     }
     // 结合类定义和类的说明就明白为什么提供了这么多方法但是都不能用了
     public Set<Map.Entry<K,V>> entrySet() { throw new InternalError(); }
     public K lastKey() { throw new InternalError(); }
     public K firstKey() { throw new InternalError(); }
     public SortedMap<K,V> subMap(K fromKey, K toKey) { throw new InternalError(); }
     public SortedMap<K,V> headMap(K toKey) { throw new InternalError(); }
     public SortedMap<K,V> tailMap(K fromKey) { throw new InternalError(); }
     public Comparator<? super K> comparator() { throw new InternalError(); }
 }
```

     结合上面的内部类分析和《TreeMap源码分析——基础分析》，对TreeMap的实现应该有个大致轮廓。不过TreeMap的代码很长很复杂，不自己看一遍分析一边，很难想明白，很难理解进去。

     自己也理解的不是很好，如果有牛人有对TreeMap的看法，望多指点。
