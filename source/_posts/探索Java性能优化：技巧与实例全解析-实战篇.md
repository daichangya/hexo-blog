---
title: 探索Java性能优化：技巧与实例全解析-实战篇
id: 126c594b-7f66-41d0-9b05-f4fefe59d477
date: 2024-12-12 18:25:54
author: daichangya
cover: https://images.jsdiff.com/Java%20Performance.jpg
excerpt: "4. 代码优化案例剖析 4.1 电商系统库存管理模块优化 在电商系统中，库存管理模块的性能至关重要。假设原始代码在处理高并发的库存扣减操作时存在性能瓶颈。 原始代码问题分析： 库存扣减操作直接在业务逻辑层频繁操作数据库，没有有效的缓存策略，导致数据库 I/O 压力过大。 对于库存数量的校验和扣减操作"
permalink: /archives/tan-suo-javaxing-neng-you-hua-ji-qiao-yu-shi-li-quan-jie-xi-shi-zhan-pian/
categories:
 - java
---

## 4. 代码优化案例剖析
### 4.1 电商系统库存管理模块优化
在电商系统中，库存管理模块的性能至关重要。假设原始代码在处理高并发的库存扣减操作时存在性能瓶颈。

**原始代码问题分析**：
- 库存扣减操作直接在业务逻辑层频繁操作数据库，没有有效的缓存策略，导致数据库 I/O 压力过大。
- 对于库存数量的校验和扣减操作未进行原子性处理，在高并发场景下可能出现超卖现象。

**优化方案**：
- **引入缓存**：使用 Redis 作为库存缓存，在商品详情页面浏览等读取库存操作时，优先从 Redis 中获取库存数量。只有当库存发生变化（如订单支付成功后）且缓存中库存数量低于一定阈值时，才异步更新数据库并重新加载缓存。
```java
import redis.clients.jedis.Jedis;

public class InventoryCache {
    private static final String INVENTORY_KEY_PREFIX = "inventory:";

    public static int getInventory(String productId) {
        try (Jedis jedis = new Jedis("localhost", 6379)) {
            String inventoryKey = INVENTORY_KEY_PREFIX + productId;
            String inventoryStr = jedis.get(inventoryKey);
            if (inventoryStr!= null) {
                return Integer.parseInt(inventoryStr);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        // 如果缓存中没有，从数据库获取并设置到缓存
        int inventoryFromDB = getInventoryFromDB(productId);
        setInventory(productId, inventoryFromDB);
        return inventoryFromDB;
    }

    public static void setInventory(String productId, int inventory) {
        try (Jedis jedis = new Jedis("localhost", 6379)) {
            String inventoryKey = INVENTORY_KEY_PREFIX + productId;
            jedis.set(inventoryKey, String.valueOf(inventory));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static int getInventoryFromDB(String productId) {
        // 这里模拟从数据库获取库存数量的操作
        return 100; 
    }
}
```
- **原子性操作保障**：利用数据库的事务特性或分布式锁（如基于 Redis 的分布式锁），确保库存校验和扣减操作的原子性。例如，在扣减库存的方法中：
```java
import redis.clients.jedis.Jedis;

public class InventoryManager {
    private static final String LOCK_KEY_PREFIX = "inventory_lock:";

    public static boolean deductInventory(String productId, int quantity) {
        try (Jedis jedis = new Jedis("localhost", 6379)) {
            String lockKey = LOCK_KEY_PREFIX + productId;
            // 获取分布式锁
            while (!jedis.setnx(lockKey, "locked").equals(1L)) {
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            try {
                int currentInventory = InventoryCache.getInventory(productId);
                if (currentInventory >= quantity) {
                    // 模拟数据库事务中的库存扣减操作
                    // 这里可以替换为真实的数据库更新语句
                    InventoryCache.setInventory(productId, currentInventory - quantity);
                    return true;
                }
            } finally {
                // 释放分布式锁
                jedis.del(lockKey);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }
}
```

### 4.2 社交网络消息推送模块优化
社交网络的消息推送模块需要处理大量用户的消息发送任务，原始代码可能存在效率低下的问题。
<separator></separator>
**原始代码问题分析**：
- 消息推送采用同步方式，逐个向用户发送消息，当用户数量庞大时，发送时间过长。
- 没有对消息队列进行合理的优化和管理，可能导致消息积压和丢失。

**优化方案**：
- **异步消息发送**：引入消息队列（如 Kafka），将消息先发送到消息队列中，由后台的消费者线程进行异步发送。这样可以快速响应消息推送请求，提高系统的吞吐量。
```java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Properties;

public class MessageProducer {
    private static final String TOPIC = "message_push";
    private static KafkaProducer<String, String> producer;

    static {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("acks", "all");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        producer = new KafkaProducer<>(props);
    }

    public static void sendMessage(String userId, String message) {
        ProducerRecord<String, String> record = new ProducerRecord<>(TOPIC, userId, message);
        producer.send(record);
    }

    public static void close() {
        producer.close();
    }
}
```
- **消息队列优化**：合理设置 Kafka 的分区数量，根据用户数量和消息发送的负载均衡需求进行调整。同时，设置消息的过期时间和重试策略，确保消息的可靠性和及时性。例如：
```java
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.util.Collections;
import java.util.Properties;

public class MessageConsumer {
    private static final String TOPIC = "message_push";
    private static KafkaConsumer<String, String> consumer;

    static {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "message_push_group");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        // 设置自动提交偏移量为 false，以便手动控制消息消费的确认
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList(TOPIC));
    }

    public static void consumeMessages() {
        while (true) {
            // 拉取消息并处理
            consumer.poll(100).forEach(record -> {
                // 这里进行消息的实际推送操作，例如调用推送接口向用户发送消息
                System.out.println("Sending message to user " + record.key() + ": " + record.value());
                // 手动提交偏移量，确认消息已处理
                consumer.commitSync();
            });
        }
    }

    public static void close() {
        consumer.close();
    }
}
```
通过以上对电商库存管理模块和社交网络消息推送模块的优化案例剖析，可以看到针对具体业务场景进行代码优化的重要性和实际操作方法。开发者在面对不同的应用场景时，需要深入分析问题，运用合适的优化技术和工具，才能有效提升系统性能。 