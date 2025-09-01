---
title: Spring 执行存储过程示例
id: 1595
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/spring%E6%89%A7%E8%A1%8C%E5%AD%98%E5%82%A8%E8%BF%87%E7%A8%8B%E7%A4%BA%E4%BE%8B/
categories:
 - spring
tags: 
 - 存储过程
---


在Spring中执行存储过程的方法：

1.  JDBC Template
2.  NamedParameterJdbcTemplate
3.  SimpleJdbcCall

JDBC Template示例：

```
String procedureCall = "{call proc_name(?, ?)}";
Map<String, Object> inParams = new HashMap<>();
inParams.put("inParam1", 1);
Map<String, Object> outParams = jdbcTemplate.call(con -> {
   CallableStatement callableStatement = con.prepareCall(procedureCall);
   callableStatement.setInt(1, (Integer) inParams.get("inParam1"));
   callableStatement.registerOutParameter(2, Types.INTEGER);
   return callableStatement;
}, outParams);
int result = (int) outParams.get("outParam1");
System.out.println("Result : " + result);
```

NamedParameterJdbcTemplate示例：

```
String procedureCall = "{call proc_name(:inParam1, :outParam1)}";
Map<String, Object> inParams = new HashMap<>();
inParams.put("inParam1", 1);
Map<String, Object> outParams = new HashMap<>();
outParams.put("outParam1", Types.INTEGER);
Map<String, Object> result = namedParameterJdbcTemplate.call(procedureCall, inParams, outParams);
System.out.println("Result : " + result.get("outParam1"));
```

SimpleJdbcCall示例：

```
SimpleJdbcCall simpleJdbcCall = new SimpleJdbcCall(jdbcTemplate).withProcedureName("proc_name");
SqlParameterSource in = new MapSqlParameterSource().addValue("inParam1", 1);
Map<String, Object> out = simpleJdbcCall.execute(in);
int result = (int) out.get("outParam1");
System.out.println("Result : " + result);
```
