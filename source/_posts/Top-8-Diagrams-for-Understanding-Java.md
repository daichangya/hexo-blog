---
title: Top 8 Diagrams for Understanding Java
id: 332
date: 2024-10-31 22:01:42
author: daichangya
excerpt: A diagram is sometimes worth 1000 words. The following diagrams are from Java
  tutorials on Program Creek, they have received the most votes so far. Hopefully,
  they can help you review what you alrea
permalink: /archives/Top-8-Diagrams-for-Understanding-Java/
categories:
- java基础
---

A diagram is sometimes worth 1000 words. The following diagrams are from [Java tutorials](http://www.programcreek.com/java-tutorials/) on Program Creek, they have received the most votes so far. Hopefully, they can help you review what you already know. If the problem is not clear by the diagram itself, you may want to go to each article to take a further took.

1. [String Immutability](http://www.programcreek.com/2009/02/diagram-to-show-java-strings-immutability/)

The following diagram shows what happens for the following code:

```
String s = "abcd";
s = s.concat("ef");
```

![string-immutability](http://www.programcreek.com/wp-content/uploads/2009/02/string-immutability-650x279.jpeg)

2. [The equals() and hashCode() Contract](http://www.programcreek.com/2011/07/java-equals-and-hashcode-contract/)

HashCode is designed to improve performance. The contract between equals() and hasCode() is that:  
1\. If two objects are equal, then they must have the same hash code.  
2\. If two objects have the same hashcode, they may or may not be equal.

![java-hashcode](http://www.programcreek.com/wp-content/uploads/2011/07/java-hashcode-650x369.jpeg)

3. [Java Exception Class Hierarchy](http://www.programcreek.com/2009/02/diagram-for-hierarchy-of-exception-classes/)

Red colored are checked exceptions which must either be caught or declared in the method’s throws clause.

![Exception-Hierarchy-Diagram](http://www.programcreek.com/wp-content/uploads/2009/02/Exception-Hierarchy-Diagram.jpeg)

4. [Collections Class Hierarchy](http://www.programcreek.com/2009/02/the-interface-and-class-hierarchy-for-collections/)

Note the difference between Collections and Collection.

![](http://www.programcreek.com/wp-content/uploads/2009/02/CollectionVsCollections.jpeg "CollectionVsCollections")  
![](http://www.programcreek.com/wp-content/uploads/2009/02/java-collection-hierarchy.jpeg "java-collection-hierarchy")

5. [Java synchronization](http://www.programcreek.com/2011/12/monitors-java-synchronization-mechanism/)

Java synchronization mechanism can be illustrated by an analogy to a building.

![](http://www.programcreek.com/wp-content/uploads/2011/12/Java-Monitor.jpg "Java-Monitor")

6. [Aliasing](http://www.programcreek.com/2012/12/how-does-java-handle-aliasing/)

Aliasing means there are multiple aliases to a location that can be updated, and these aliases have different types.

![Java Aliasing](http://www.programcreek.com/wp-content/uploads/2012/12/JavaAliasing.jpeg)

7. [Stack and Heap](http://www.programcreek.com/2013/04/what-does-a-java-array-look-like-in-memory/)

This diagram shows where methods and objects are in run-time memory.

![Java-array-in-memory](http://www.programcreek.com/wp-content/uploads/2013/04/Java-array-in-memory.png)

8. [JVM Run-Time Data Areas](http://www.programcreek.com/2013/04/jvm-run-time-data-areas/)

This diagram shows overall JVM run-time data areas.

![JVM runtime data area](http://www.programcreek.com/wp-content/uploads/2013/04/JVM-runtime-data-area.jpg)