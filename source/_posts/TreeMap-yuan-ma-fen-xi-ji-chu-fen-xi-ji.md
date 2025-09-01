---
title: TreeMap源码分析——基础分析（基于JDK1.6）
id: 406
date: 2024-10-31 22:01:43
author: daichangya
excerpt: '常见的数据结构有数组、链表，还有一种结构也很常见，那就是树。前面介绍的集合类有基于数组的ArrayList，有基于链表的LinkedList，还有链表和数组结合的HashMap，今天介绍基于树的TreeMap。

       TreeMap基于红黑树（点击查看树、红黑树相关内容）实现。查看“键”或“键值对”时，它们会被排序（次序由Comparable或Comparator决定）。TreeMap的'
permalink: /archives/TreeMap-yuan-ma-fen-xi-ji-chu-fen-xi-ji/
categories:
- java基础
- java源码分析
---


常见的数据结构有数组、链表，还有一种结构也很常见，那就是树。前面介绍的集合类有基于数组的ArrayList，有基于链表的LinkedList，还有链表和数组结合的HashMap，今天介绍基于树的TreeMap。 TreeMap基于红黑树（点击查看树、红黑树相关内容）实现。查看“键”或“键值对”时，它们会被排序（次序由Comparable或Comparator决定）。TreeMap的特点在于，所得到的结果是经过排序的。TreeMap是唯一的带有subMap()方法的Map，它可以返回一个子树。

      常见的数据结构有数组、链表，还有一种结构也很常见，那就是树。前面介绍的集合类有基于数组的ArrayList，有基于链表的LinkedList，还有链表和数组结合的HashMap，今天介绍基于树的TreeMap。

     TreeMap基于红黑树（[点击查看树、红黑树相关内容](http://www.cnblogs.com/hzmark/archive/2012/12/31/Tree.html)）实现。查看“键”或“键值对”时，它们会被排序（次序由Comparable或Comparator决定）。TreeMap的特点在于，所得到的结果是经过排序的。TreeMap是唯一的带有subMap()方法的Map，它可以返回一个子树。 

     在介绍TreeMap前先介绍Comparable和Comparator接口。 

     Comparable接口：

```
 public interface Comparable<T> {
     public int compareTo(T o);
 }
```

     Comparable接口支持泛型，只有一个方法，该方法返回负数、零、正数分别表示当前对象“小于”、“等于”、“大于”传入对象o。

     Comparamtor接口：

```
 public interface Comparator<T> {
 int compare(T o1, T o2);
 boolean equals(Object obj);
 }
```

     compare(T o1,T o2)方法比较o1和o2两个对象，o1“大于”o2，返回正数，相等返回零，“小于”返回负数。

     equals(Object obj)返回true的唯一情况是obj也是一个比较器（Comparator）并且比较结果和此比较器的结果的大小次序是一致的。即comp1.equals(comp2)意味着sgn(comp1.compare(o1, * o2))==sgn(comp2.compare(o1, o2))。

     补充：符号sgn(expression)表示数学上的signum函数，该函数根据expression的值是负数、零或正数，分别返回-1、0或1。

     小结一下，实现Comparable结构的类可以和其他对象进行比较，即实现Comparable可以进行比较的类。而实现Comparator接口的类是比较器，用于比较两个对象的大小。

     下面正式分析TreeMap的源码。

     既然TreeMap底层使用的是树结构，那么必然有表示节点的对象。下面先看TreeMap中表示节点的内部类Entry。

```
 static final class Entry<K,V> implements Map.Entry<K,V> {
 // 键值对的“键”
 K key;
 // 键值对的“值”
     V value;
     // 左孩子
     Entry<K,V> left = null;
     // 右孩子
     Entry<K,V> right = null;
     // 父节点
     Entry<K,V> parent;
     // 红黑树的节点表示颜色的属性
     boolean color = BLACK;
     /**
      * 根据给定的键、值、父节点构造一个节点，颜色为默认的黑色
      */
     Entry(K key, V value, Entry<K,V> parent) {
         this.key = key;
         this.value = value;
         this.parent = parent;
     }
     // 获取节点的key
     public K getKey() {
         return key;
     }
     // 获取节点的value
     public V getValue() {
         return value;
     }
     /**
      * 修改并返回当前节点的value
      */
     public V setValue(V value) {
         V oldValue = this.value;
         this.value = value;
         return oldValue;
     }
     // 判断节点相等的方法（两个节点为同一类型且key值和value值都相等时两个节点相等）
     public boolean equals(Object o) {
         if (!(o instanceof Map.Entry))
             return false;
         Map.Entry<?,?> e = (Map.Entry<?,?>)o;
         return valEquals(key,e.getKey()) && valEquals(value,e.getValue());
     }
     // 节点的哈希值计算方法
     public int hashCode() {
         int keyHash = (key==null ? 0 : key.hashCode());
         int valueHash = (value==null ? 0 : value.hashCode());
         return keyHash ^ valueHash;
     }
     public String toString() {
         return key + "=" + value;
     }
 }
```

    上面的Entry类比较简单，实现了树节点的必要内容，提供了hashCode方法等。下面看TreeMap类的定义。

```
 public class TreeMap<K,V>
     extends AbstractMap<K,V>
     implements NavigableMap<K,V>, Cloneable, java.io.Serializable
```

     上面只有一个接口需要说明，那就是NavigableMap接口。

     NavigableMap接口扩展的SortedMap，具有了针对给定搜索目标返回最接近匹配项的导航方法。方法lowerEntry、floorEntry、ceilingEntry和higherEntry分别返回与小于、小于等于、大于等于、大于给定键的键关联的Map.Entry对象，如果不存在这样的键，则返回null。类似地，方法lowerKey、floorKey、ceilingKey和higherKey只返回关联的键。所有这些方法是为查找条目而不是遍历条目而设计的（后面会逐个介绍这些方法）。

     下面是TreeMap的属性：

```
      // 用于保持顺序的比较器，如果为空的话使用自然顺保持Key的顺序
     private final Comparator<? super K> comparator;
     // 根节点
     private transient Entry<K,V> root = null;
     // 树中的节点数量
     private transient int size = 0;
     // 多次在集合类中提到了，用于举了结构行的改变次数
     private transient int modCount = 0;
```

    注释中已经给出了属性的解释，下面看TreeMap的构造方法。

```
 // 构造方法一，默认的构造方法，comparator为空，即采用自然顺序维持TreeMap中节点的顺序
 public TreeMap() {
     comparator = null;
 }
 // 构造方法二，提供指定的比较器
 public TreeMap(Comparator<? super K> comparator) {
     this.comparator = comparator;
 }
 // 构造方法三，采用自然序维持TreeMap中节点的顺序，同时将传入的Map中的内容添加到TreeMap中
 public TreeMap(Map<? extends K, ? extends V> m) {
     comparator = null;
     putAll(m);
 }
 /** 
 *构造方法四，接收SortedMap参数，根据SortedMap的比较器维持TreeMap中的节点顺序，* 同时通过buildFromSorted(int size, Iterator it, java.io.ObjectInputStream str, V defaultVal)方* 法将SortedMap中的内容添加到TreeMap中
 */
 public TreeMap(SortedMap<K, ? extends V> m) {
     comparator = m.comparator();
     try {
         buildFromSorted(m.size(), m.entrySet().iterator(), null, null);
     } catch (java.io.IOException cannotHappen) {
     } catch (ClassNotFoundException cannotHappen) {
     }
 }
```

     TreeMap提供了四个构造方法，已经在注释中给出说明。构造方法中涉及到的方法在下文中会有介绍。

     下面从put/get方法开始，逐个分析TreeMap的方法。

**     put(K key, V value)**

```
     public V put(K key, V value) {
         Entry<K,V> t = root;
         if (t == null) {
         //如果根节点为null，将传入的键值对构造成根节点（根节点没有父节点，所以传入的父节点为null）
             root = new Entry<K,V>(key, value, null);
             size = 1;
             modCount++;
             return null;
         }
         // 记录比较结果
         int cmp;
         Entry<K,V> parent;
         // 分割比较器和可比较接口的处理
         Comparator<? super K> cpr = comparator;
         // 有比较器的处理
         if (cpr != null) {
             // do while实现在root为根节点移动寻找传入键值对需要插入的位置
             do {
                 // 记录将要被掺入新的键值对将要节点(即新节点的父节点)
                 parent = t;
                 // 使用比较器比较父节点和插入键值对的key值的大小
                 cmp = cpr.compare(key, t.key);
                 // 插入的key较大
                 if (cmp < 0)
                     t = t.left;
                 // 插入的key较小
                 else if (cmp > 0)
                     t = t.right;
                 // key值相等，替换并返回t节点的value(put方法结束)
                 else
                     return t.setValue(value);
             } while (t != null);
         }
         // 没有比较器的处理
         else {
             // key为null抛出NullPointerException异常
             if (key == null)
                 throw new NullPointerException();
             Comparable<? super K> k = (Comparable<? super K>) key;
             // 与if中的do while类似，只是比较的方式不同
             do {
                 parent = t;
                 cmp = k.compareTo(t.key);
                 if (cmp < 0)
                     t = t.left;
                 else if (cmp > 0)
                     t = t.right;
                 else
                     return t.setValue(value);
             } while (t != null);
         }
         // 没有找到key相同的节点才会有下面的操作
         // 根据传入的键值对和找到的“父节点”创建新节点
         Entry<K,V> e = new Entry<K,V>(key, value, parent);
         // 根据最后一次的判断结果确认新节点是“父节点”的左孩子还是又孩子
         if (cmp < 0)
             parent.left = e;
         else
             parent.right = e;
         // 对加入新节点的树进行调整
         fixAfterInsertion(e);
         // 记录size和modCount
         size++;
         modCount++;
         // 因为是插入新节点，所以返回的是null
         return null;
     }
```

     首先一点通性是TreeMap的put方法和其他Map的put方法一样，向Map中加入键值对，若原先“键（key）”已经存在则替换“值（value）”，并返回原先的值。

     在put(K key,V value)方法的末尾调用了fixAfterInsertion(Entry<K,V> x)方法，这个方法负责在插入节点后调整树结构和着色，以满足[红黑树](http://www.cnblogs.com/hzmark/archive/2012/12/31/Tree.html)的要求。

.  每一个节点或者着成红色，或者着成黑色。
.  根是黑色的。
.  如果一个节点是红色的，那么它的子节点必须是黑色的。
.  一个节点到一个null引用的每一条路径必须包含相同数量的黑色节点。

     在看fixAfterInsertion(Entry<K,V> x)方法前先看一个红黑树的内容：红黑树不是严格的平衡二叉树，它并不严格的保证左右子树的高度差不超过1，但红黑树高度依然是平均log(n)，且最坏情况高度不会超过2log(n)，所以它算是平衡树。

     下面看具体实现代码。

     **fixAfterInsertion(Entry<K,V> x)**

```
 private void fixAfterInsertion(Entry<K,V> x) {
     // 插入节点默认为红色
     x.color = RED;
     // 循环条件是x不为空、不是根节点、父节点的颜色是红色（如果父节点不是红色，则没有连续的红色节点，不再调整）
     while (x != null && x != root && x.parent.color == RED) {
         // x节点的父节点p（记作p）是其父节点pp（p的父节点，记作pp）的左孩子（pp的左孩子）
         if (parentOf(x) == leftOf(parentOf(parentOf(x)))) {
             // 获取pp节点的右孩子r
             Entry<K,V> y = rightOf(parentOf(parentOf(x)));
             // pp右孩子的颜色是红色（colorOf(Entry e)方法在e为空时返回BLACK），不需要进行旋转操作（因为红黑树不是严格的平衡二叉树）
             if (colorOf(y) == RED) {
                 // 将父节点设置为黑色
                 setColor(parentOf(x), BLACK);
                 // y节点，即r设置成黑色
                 setColor(y, BLACK);
                 // pp节点设置成红色
                 setColor(parentOf(parentOf(x)), RED);
                 // x“移动”到pp节点
                 x = parentOf(parentOf(x));
             } else {//父亲的兄弟是黑色的，这时需要进行旋转操作，根据是“内部”还是“外部”的情况决定是双旋转还是单旋转
                 // x节点是父节点的右孩子（因为上面已近确认p是pp的左孩子，所以这是一个“内部，左-右”插入的情况，需要进行双旋转处理）
                 if (x == rightOf(parentOf(x))) {
                     // x移动到它的父节点
                     x = parentOf(x);
                     // 左旋操作
                     rotateLeft(x);
                 }
                 // x的父节点设置成黑色
                 setColor(parentOf(x), BLACK);
                 // x的父节点的父节点设置成红色
                 setColor(parentOf(parentOf(x)), RED);
                 // 右旋操作
                 rotateRight(parentOf(parentOf(x)));
             }
         } else {
             // 获取x的父节点（记作p）的父节点（记作pp）的左孩子
             Entry<K,V> y = leftOf(parentOf(parentOf(x)));
             // y节点是红色的
             if (colorOf(y) == RED) {
                 // x的父节点，即p节点，设置成黑色
                 setColor(parentOf(x), BLACK);
                 // y节点设置成黑色
                 setColor(y, BLACK);
                 // pp节点设置成红色
                 setColor(parentOf(parentOf(x)), RED);
                 // x移动到pp节点
                 x = parentOf(parentOf(x));
             } else {
                 // x是父节点的左孩子（因为上面已近确认p是pp的右孩子，所以这是一个“内部，右-左”插入的情况，需要进行双旋转处理），
                 if (x == leftOf(parentOf(x))) {
                     // x移动到父节点
                     x = parentOf(x);
                     // 右旋操作
                     rotateRight(x);
                 }
                 // x的父节点设置成黑色
                 setColor(parentOf(x), BLACK);
                 // x的父节点的父节点设置成红色
                 setColor(parentOf(parentOf(x)), RED);
                 // 左旋操作
                 rotateLeft(parentOf(parentOf(x)));
             }
         }
     }
     // 根节点为黑色
     root.color = BLACK;
 }
```

     fixAfterInsertion(Entry<K,V> x)方法涉及到了左旋和右旋的操作，下面是左旋的代码及示意图（右旋操作类似，就不给出代码和示意图了）。

```
 // 左旋操作
 private void rotateLeft(Entry<K,V> p) {
     if (p != null) {
         Entry<K,V> r = p.right;
         p.right = r.left;
         if (r.left != null)
             r.left.parent = p;
         r.parent = p.parent;
         if (p.parent == null)
             root = r;
         else if (p.parent.left == p)
             p.parent.left = r;
         else
             p.parent.right = r;
         r.left = p;
         p.parent = r;
     }
 }
```

![](https://pic002.cnblogs.com/images/2013/471426/2013010120451182.jpg)

     看完put操作，下面来看get操作相关的内容。

     **get(Object key)**

```
 public V get(Object key) {
     Entry<K,V> p = getEntry(key);
     return (p==null ? null : p.value);
 }
```

     get(Object key)通过key获取对应的value，它通过调用getEntry(Object key)获取节点，若节点为null则返回null，否则返回节点的value值。下面是getEntry(Object key)的内容，来看它是怎么寻找节点的。

     **getEntry(Object key)**

```
 final Entry<K,V> getEntry(Object key) {
     // 如果有比较器，返回getEntryUsingComparator(Object key)的结果
     if (comparator != null)
         return getEntryUsingComparator(key);
     // 查找的key为null，抛出NullPointerException
     if (key == null)
         throw new NullPointerException();
     // 如果没有比较器，而是实现了可比较接口
     Comparable<? super K> k = (Comparable<? super K>) key;
     // 获取根节点
     Entry<K,V> p = root;
     // 对树进行遍历查找节点
     while (p != null) {
         // 把key和当前节点的key进行比较
         int cmp = k.compareTo(p.key);
         // key小于当前节点的key
         if (cmp < 0)
             // p “移动”到左节点上
             p = p.left;
         // key大于当前节点的key
         else if (cmp > 0)
             // p “移动”到右节点上
 p = p.right;
         // key值相等则当前节点就是要找的节点
         else
             // 返回找到的节点
             return p;
         }
     // 没找到则返回null
     return null;
 }
```

     上面主要是处理实现了可比较接口的情况，而有比较器的情况在getEntryUsingComparator(Object key)中处理了，下面来看处理的代码。

     **getEntryUsingComparator(Object key)**

```
 final Entry<K,V> getEntryUsingComparator(Object key) {
     K k = (K) key;
     // 获取比较器
 Comparator<? super K> cpr = comparator;
 // 其实在调用此方法的get(Object key)中已经对比较器为null的情况进行判断，这里是防御性的判断
 if (cpr != null) {
     // 获取根节点
         Entry<K,V> p = root;
         // 遍历树
         while (p != null) {
             // 获取key和当前节点的key的比较结果
             int cmp = cpr.compare(k, p.key);
             // 查找的key值较小
             if (cmp < 0)
                 // p“移动”到左孩子
                 p = p.left;
             // 查找的key值较大
             else if (cmp > 0)
                 // p“移动”到右节点
                 p = p.right;
             // key值相等
             else
                 // 返回找到的节点
                 return p;
         }
 }
 // 没找到key值对应的节点，返回null
     return null;
 }
```

     看完添加（put）和获取（get），下面来看删除（remove、clear）。

     **remove(Object key)**

```
 public V remove(Object key) {
     // 通过getEntry(Object key)获取节点 getEntry(Object key)方法已经在上面介绍过了
 Entry<K,V> p = getEntry(key);
 // 指定key的节点不存在，返回null
     if (p == null)
         return null;
     // 获取节点的value
 V oldValue = p.value;
 // 删除节点
 deleteEntry(p);
 // 返回节点的内容
     return oldValue;
 }
```

     真正实现删除节点的内容在deleteEntry(Entry e)中，涉及到树结构的调整等。remove(Object key)只是获取要删除的节点并返回被删除节点的value。下面来看deleteEntry(Entry e)的内容。

     **deleteEntry(Entry e)**

```
 private void deleteEntry(Entry<K,V> p) {
 // 记录树结构的修改次数
 modCount++;
 // 记录树中节点的个数
     size--;
 
 // p有左右两个孩子的情况  标记①
 if (p.left != null && p.right != null) {
         // 获取继承者节点（有两个孩子的情况下，继承者肯定是右孩子或右孩子的最左子孙）
         Entry<K,V> s = successor (p);
         // 使用继承者s替换要被删除的节点p，将继承者的key和value复制到p节点，之后将p指向继承者
         p.key = s.key;
         p.value = s.value;
         p = s;
     } 
 
 // Start fixup at replacement node, if it exists.
 // 开始修复被移除节点处的树结构
 // 如果p有左孩子，取左孩子，否则取右孩子    标记②
     Entry<K,V> replacement = (p.left != null ? p.left : p.right);
     if (replacement != null) {
         // Link replacement to parent
         replacement.parent = p.parent;
         // p节点没有父节点，即p节点是根节点
         if (p.parent == null)
             // 将根节点替换为replacement节点
             root = replacement;
         // p是其父节点的左孩子
         else if (p == p.parent.left)
             // 将p的父节点的left引用指向replacement
             // 这步操作实现了删除p的父节点到p节点的引用
             p.parent.left  = replacement;
         else
             // 如果p是其父节点的右孩子，将父节点的right引用指向replacement
             p.parent.right = replacement;
         // 解除p节点到其左右孩子和父节点的引用
         p.left = p.right = p.parent = null;
         if (p.color == BLACK)
             // 在删除节点后修复红黑树的颜色分配
             fixAfterDeletion(replacement);
 } else if (p.parent == null) { 
 /* 进入这块代码则说明p节点就是根节点（这块比较难理解，如果标记①处p有左右孩子，则找到的继承节点s是p的一个祖先节点或右孩子或右孩子的最左子孙节点，他们要么有孩子节点，要么有父节点，所以如果进入这块代码，则说明标记①除的p节点没有左右两个孩子。没有左右孩子，则有没有孩子、有一个右孩子、有一个左孩子三种情况，三种情况中只有没有孩子的情况会使标记②的if判断不通过，所以p节点只能是没有孩子，加上这里的判断，p没有父节点，所以p是一个独立节点，也是树种的唯一节点……有点难理解，只能解释到这里了，读者只能结合注释慢慢体会了），所以将根节点设置为null即实现了对该节点的删除 */
         root = null;
 } else { /* 标记②的if判断没有通过说明被删除节点没有孩子，或它有两个孩子但它的继承者没有孩子。如果是被删除节点没有孩子，说明p是个叶子节点，则不需要找继承者，直接删除该节点。如果是有两个孩子，那么继承者肯定是右孩子或右孩子的最左子孙 */
         if (p.color == BLACK)
             // 调整树结构
             fixAfterDeletion(p);
         // 这个判断也一定会通过，因为p.parent如果不是null则在上面的else if块中已经被处理
         if (p.parent != null) {
             // p是一个左孩子
             if (p == p.parent.left)
                 // 删除父节点对p的引用
                 p.parent.left = null;
             else if (p == p.parent.right)// p是一个右孩子
                 // 删除父节点对p的引用
                 p.parent.right = null;
             // 删除p节点对父节点的引用
             p.parent = null;
         }
     }
 }
```

     deleteEntry(Entry e)方法中主要有两个方法调用需要分析：successor(Entry<K,V> t)和fixAfterDeletion(Entry<K,V> x)。

     successor(Entry<K,V> t)返回指定节点的继承者。分三种情况处理，第一。t节点是个空节点：返回null；第二，t有右孩子：找到t的右孩子中的最左子孙节点，如果右孩子没有左孩子则返回右节点，否则返回找到的最左子孙节点；第三，t没有右孩子：沿着向上（向跟节点方向）找到第一个自身是一个左孩子的节点或根节点，返回找到的节点。下面是具体代码分析的注释。

```
 static <K,V> TreeMap.Entry<K,V> successor(Entry<K,V> t) {
     // 如果t本身是一个空节点，返回null
     if (t == null)
         return null;
     // 如果t有右孩子，找到右孩子的最左子孙节点
     else if (t.right != null) {
         Entry<K,V> p = t.right;
         // 获取p节点最左的子孙节点，如果存在的话
         while (p.left != null)
             p = p.left;
         // 返回找到的继承节点
         return p;
     } else {//t不为null且没有右孩子
         Entry<K,V> p = t.parent;
         Entry<K,V> ch = t;
        // // 沿着右孩子向上查找继承者，直到根节点或找到节点ch是其父节点的左孩子的节点
         while (p != null && ch == p.right) {
             ch = p;
             p = p.parent;
         }
         return p;
     }
 }
```

     与添加节点之后的修复类似的是，TreeMap 删除节点之后也需要进行类似的修复操作，通过这种修复来保证该排序二叉树依然满足红黑树特征。大家可以参考插入节点之后的修复来分析删除之后的修复。TreeMap 在删除之后的修复操作由 fixAfterDeletion(Entry<K,V> x) 方法提供，该方法源代码如下：

```
 private void fixAfterDeletion(Entry<K,V> x) {
     // 循环处理，条件为x不是root节点且是黑色的（因为红色不会对红黑树的性质造成破坏，所以不需要调整）
 while (x != root && colorOf(x) == BLACK) {
     // x是一个左孩子
         if (x == leftOf(parentOf(x))) {
             // 获取x的兄弟节点sib
             Entry<K,V> sib = rightOf(parentOf(x));
             // sib是红色的
             if (colorOf(sib) == RED) {
                 // 将sib设置为黑色
                 setColor(sib, BLACK);
                 // 将父节点设置成红色
                 setColor(parentOf(x), RED);
                 // 左旋父节点
                 rotateLeft(parentOf(x));
                 // sib移动到旋转后x的父节点p的右孩子（参见左旋示意图，获取的节点是旋转前p的右孩子r的左孩子rl）
                 sib = rightOf(parentOf(x));
             }
             // sib的两个孩子的颜色都是黑色（null返回黑色）
             if (colorOf(leftOf(sib))  == BLACK &&
                 colorOf(rightOf(sib)) == BLACK) {
                 // 将sib设置成红色
                 setColor(sib, RED);
                 // x移动到x的父节点
                 x = parentOf(x);
             } else {// sib的左右孩子都是黑色的不成立
                 // sib的右孩子是黑色的
                 if (colorOf(rightOf(sib)) == BLACK) {
                     // 将sib的左孩子设置成黑色
                     setColor(leftOf(sib), BLACK);
                     // sib节点设置成红色
                     setColor(sib, RED);
                     // 右旋操作
                     rotateRight(sib);
                     // sib移动到旋转后x父节点的右孩子
                     sib = rightOf(parentOf(x));
                 }
                 // sib设置成和x的父节点一样的颜色
                 setColor(sib, colorOf(parentOf(x)));
                 // x的父节点设置成黑色
                 setColor(parentOf(x), BLACK);
                 // sib的右孩子设置成黑色
                 setColor(rightOf(sib), BLACK);
                 // 左旋操作
                 rotateLeft(parentOf(x));
                 // 设置调整完的条件：x = root跳出循环
                 x = root;
             }
         } else { // x是一个右孩子
             // 获取x的兄弟节点
             Entry<K,V> sib = leftOf(parentOf(x));
             // 如果sib是红色的
             if (colorOf(sib) == RED) {
                 // 将sib设置为黑色
                 setColor(sib, BLACK);
                 // 将x的父节点设置成红色
                 setColor(parentOf(x), RED);
                 // 右旋
                 rotateRight(parentOf(x));
                 // sib移动到旋转后x父节点的左孩子
                 sib = leftOf(parentOf(x));
             }
             // sib的两个孩子的颜色都是黑色（null返回黑色）
             if (colorOf(rightOf(sib)) == BLACK &&
                 colorOf(leftOf(sib)) == BLACK) {
                 // sib设置为红色
                 setColor(sib, RED);
                 // x移动到x的父节点
                 x = parentOf(x);
             } else { // sib的两个孩子的颜色都是黑色（null返回黑色）不成立
                 // sib的左孩子是黑色的，或者没有左孩子
                 if (colorOf(leftOf(sib)) == BLACK) {
                     // 将sib的右孩子设置成黑色
                     setColor(rightOf(sib), BLACK);
                     // sib节点设置成红色
                     setColor(sib, RED);
                     // 左旋
                     rotateLeft(sib);
                     // sib移动到x父节点的左孩子
                     sib = leftOf(parentOf(x));
                 }
                 // sib设置成和x的父节点一个颜色
                 setColor(sib, colorOf(parentOf(x)));
                 // x的父节点设置成黑色
                 setColor(parentOf(x), BLACK);
                 // sib的左孩子设置成黑色
                 setColor(leftOf(sib), BLACK);
                 // 右旋
                 rotateRight(parentOf(x));
                 // 设置跳出循环的标识
                 x = root;
             }
         }
     }
     // 将x设置为黑色
     setColor(x, BLACK);
 }
```

     光看调整的代码，一大堆设置颜色，还有左旋和右旋，非常的抽象，下面是一个构造红黑树的视屏，包括了着色和旋转。

      [http://v.youku.com/v\_show/id\_XMjI3NjM0MTgw.html](http://v.youku.com/v_show/id_XMjI3NjM0MTgw.html)

     **clear()**

```
 public void clear() {
     modCount++;
     size = 0;
     root = null;
 }
```

     clear()方法很简单，只是记录结构修改次数，将size修改为0，将root设置为null，这样就没法通过root访问树的其他节点，所以数的内容会被GC回收。

     添加（修改）、获取、删除的原码都已经看了，下面看判断是否包含的方法。

     **containKey(Object key)**

```
 public boolean containsKey(Object key) {
     return getEntry(key) != null;
 }
```

     这个方法判断获取key对应的节点是否为空，getEntry(Object key)方法已经在上面介绍过了。

     **contain(Object value)**

```
 public boolean containsValue(Object value) {
     // 通过e = successor(e)实现对树的遍历
     for (Entry<K,V> e = getFirstEntry(); e != null; e = successor(e))
     // 判断节点值是否和value相等
         if (valEquals(value, e.value))
             return true;
     // 默认返回false
     return false;
 }
```

     contain(Object value)涉及到了getFirstEntry()方法和successor(Entry<K,V> e)。getFirstEntry()是获取第一个节点，successor(Entry<K,V> e)是获取节点e的继承者，在for循环中配合使用getFirstEntry()方法和successor(Entry<K,V> e)及e!=null是遍历树的一种方法。

     下面介绍getFirstEntry()方法。

     **getFirstEntry()**

```
 final Entry<K,V> getFirstEntry() {
     Entry<K,V> p = root;
     if (p != null)
         while (p.left != null)
             p = p.left;
     return p;
 }
```

     从名字上看是获取第一个节点，实际是获取的整棵树中“最左”的节点（第一个节点具体指哪一个节点和树的遍历次序有关，如果是先根遍历，则第一个节点是根节点）。又因为红黑树是排序的树，所以“最左”的节点也是值最小的节点。

     上面是getFirstEntry()方法，下面介绍getLastEntry()方法。

     **getLastEntry()**

```
 final Entry<K,V> getLastEntry() {
     Entry<K,V> p = root;
     if (p != null)
         while (p.right != null)
             p = p.right;
     return p;
 }
```

     getLastEntry()和getFirstEntry()对应，获取的是“最右”的节点。

     TreeMap中提供了获取并移除最小和最大节点的两个方法：pollFirstEntry()和pollLastEntry()。

     **pollFirstEntry()**

```
 public Map.Entry<K,V> pollFirstEntry() {
     Entry<K,V> p = getFirstEntry();
     Map.Entry<K,V> result = exportEntry(p);
     if (p != null)
         deleteEntry(p);
     return result;
 }
```

     **pollLastEntry()**

```
 public Map.Entry<K,V> pollLastEntry() {
     Entry<K,V> p = getLastEntry();
     Map.Entry<K,V> result = exportEntry(p);
     if (p != null)
         deleteEntry(p);
     return result;
 }
```

     pollFirstEntry()和pollLastEntry()分别通过getFirstEntry()和getLastEntry()获取节点，exportEntry(TreeMap.Entry<K,V> e)应该是保留这个对象用于在删除这个节点后返回。具体实现看下面的代码。

```
 static <K,V> Map.Entry<K,V> exportEntry(TreeMap.Entry<K,V> e) {
     return e == null? null :
         new AbstractMap.SimpleImmutableEntry<K,V>(e);
 }
```

     返回了一个SimpleImmutableEntry对象，调用的构造方法如下：

```
 public SimpleImmutableEntry(Entry<? extends K, ? extends V> entry) {
     this.key   = entry.getKey();
     this.value = entry.getValue();
 }
```

     可以看到返回的节点内容只包含key和value。

     下面看其他具体的获取键、值、键值对的方法。

```
 public Map.Entry<K,V> ceilingEntry(K key) {
     return exportEntry(getCeilingEntry(key));
 }
 public K ceilingKey(K key) {
     return keyOrNull(getCeilingEntry(key));
 }
```

     上面这两个方法很简单，只是对exportEntry和keyOrNull的调用。keyOrNull根据传入的Entry是否为null，选择方法null或Entry的key。

```
 // 获取最小的节点的key
 public K firstKey() {
     return key(getFirstEntry());
 }
 // 获取最大节点的key
 public K lastKey() {
     return key(getLastEntry());
 }
 // 获取最小的键值对
 public Map.Entry<K,V> firstEntry() {
     return exportEntry(getFirstEntry());
 }
 // 获取最大的键值对
 public Map.Entry<K,V> lastEntry() {
     return exportEntry(getLastEntry());
 }
```

     这几个方法涉及到的内容都在上面介绍过了，就不在说明了。

```
 public Map.Entry<K,V> floorEntry(K key) {
     return exportEntry(getFloorEntry(key));
 }
 public K floorKey(K key) {
     return keyOrNull(getFloorEntry(key));
 }
 public Map.Entry<K,V> higherEntry(K key) {
     return exportEntry(getHigherEntry(key));
 }
 public K higherKey(K key) {
     return keyOrNull(getHigherEntry(key));
 }
```

     这几个获取key的Entry的方法都是对getFloorEntry和getHigherEntry的处理。下面介绍这两个方法。

     **getFloorEntry(K key)**

```
 final Entry<K,V> getFloorEntry(K key) {
     // 获取根节点
 Entry<K,V> p = root;
 // 不是空树，最树进行遍历
     while (p != null) {
         int cmp = compare(key, p.key);
         // key较大
         if (cmp > 0) {
             // 找到节点有右孩子，则继续向右孩子遍历
             if (p.right != null)
                 p = p.right;
             else// 没有右孩子，那么p节点就是树中比key值比传入key值小且最接近传入key的节点，就是要找的节点
                 return p;
         } else if (cmp < 0) {// key值较小
             // 有左孩子向左孩子遍历
             if (p.left != null) {
                 p = p.left;
             } else {// 没有左孩子，这个节点比key值大，返回内容是向上寻找到的根节点或比传入key值小的最后一个节点（这块比较难理解，仔细模拟寻找节点的过程就会明白）
                 Entry<K,V> parent = p.parent;
                 Entry<K,V> ch = p;
                 while (parent != null && ch == parent.left) {
                     ch = parent;
                     parent = parent.parent;
                 }
                 return parent;
             }
         } else // key值相等
             return p;
     }
     return null;
 }
```

     **getHigherEntry(K key)**

```
 final Entry<K,V> getHigherEntry(K key) {
     Entry<K,V> p = root;
     while (p != null) {
         int cmp = compare(key, p.key);
         if (cmp < 0) {
             if (p.left != null)
                 p = p.left;
             else
                 return p;
         } else {
             if (p.right != null) {
                 p = p.right;
             } else {
                 Entry<K,V> parent = p.parent;
                 Entry<K,V> ch = p;
                 while (parent != null && ch == parent.right) {
                     ch = parent;
                     parent = parent.parent;
                 }
                 return parent;
             }
         }
     }
     return null;
 }
```

     getFloorEntry和getHigherEntry方法遍历和寻找节点的方法类似，区别在于getFloorEntry寻找的是小于等于，优先返回小于的节点，而getHigherEntry寻找的是严格大于的节点，不包括等于的情况。

     以上内容是TreeMap的基础方法，TreeMap的内部类及涉及到内部类的方法等都将在[《TreeMap源码分析——深入分析》](https://blog.jsdiff.com/archives/TreeMap-Deep)中给出。

