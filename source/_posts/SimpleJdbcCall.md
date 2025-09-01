---
title: SimpleJdbcCall
id: 1590
date: 2024-10-31 22:02:02
author: daichangya
permalink: /archives/simplejdbccall/
tags: 
 - jdbc
---

```language
SimpleJdbcCall simpleJdbcCall = new SimpleJdbcCall(jdbcTemplate)

.withProcedureName("STORED_PROCEDURE_NAME");

Map<String, Object> inParamMap = new HashMap<String, Object>();
inParamMap.put("firstName", "FirstNameValue");
inParamMap.put("lastName", "LastNameValue");
SqlParameterSource in = new MapSqlParameterSource(inParamMap);


Map<String, Object> simpleJdbcCallResult = simpleJdbcCall.execute(in);
System.out.println(simpleJdbcCallResult);
```
