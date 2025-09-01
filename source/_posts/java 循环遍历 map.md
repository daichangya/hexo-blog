---
title: java 循环遍历 map
id: 1593
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/java%E5%BE%AA%E7%8E%AF%E9%81%8D%E5%8E%86map/
tags: 
 - java
 - map
---



Java 中可以使用以下方法遍历 Map：

1.  for-each loop：

```

for (Map.Entry<Key, Value> entry : map.entrySet()) {
   Key key = entry.getKey();
   Value value = entry.getValue();
   // ...
} 
```
2.  Iterator：

```
Iterator<Map.Entry<Key, Value>> it = map.entrySet().iterator();
while (it.hasNext()) {
   Map.Entry<Key, Value> entry = it.next();
   Key key = entry.getKey();
   Value value = entry.getValue();
   // ...
}
```
3.  Stream API：

```
map.forEach((key, value) -> {
   // ...
}); 
```
4.  Java 8 forEach + Lambda：

```
map.entrySet().forEach(entry -> {
   Key key = entry.getKey();
   Value value = entry.getValue();
   // ...
});
```
