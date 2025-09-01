---
title: ibatis源码分析
id: 1135
date: 2024-10-31 22:01:49
author: daichangya
excerpt: 背景：调试模式下，单步运行一个查询订单协议操作，记录了ibatis框架的执行动作，侧面剖析其原理。一、简介：1. dal 层的dao接口实现类通常会继承SqlMapClientDaoSupport。spring容器在初始化一个dao
  bean实例时，通常会注入两块信息DataSource（数据源）和sqlMapClient（主要是sql语句），这两块信息会封装到SqlM
permalink: /archives/ibatis-yuan-ma-fen-xi/
tags:
- mybatis
---

 

背景：调试模式下，单步运行一个查询订单协议操作，记录了ibatis框架的执行动作，侧面剖析其原理。

  

一、简介：

1\. dal 层的dao接口实现类通常会继承SqlMapClientDaoSupport。spring容器在初始化一个dao bean实例时，通常会注入两块信息DataSource（数据源）和sqlMapClient（主要是sql语句），这两块信息会封装到SqlMapClientTemplate

![](https://img-blog.csdn.net/20130626103301343?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYWFsYW5zZWhhaXlhbmc1Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

  

2\. 其中数据源的实例通常采用apache的开源项目dbcp

代码配置如下：



      <beanid="dataSource"class="org.apache.commons.dbcp.BasicDataSource"destroy-method="close">
          <propertyname="driverClassName"value="com.mysql.jdbc.Driver"/>
          <propertyname="url"value="xxxx"/>
          <propertyname="username"><value>xxxx</value></property>
              <propertyname="password"><value>xxxxx</value></property>
              <propertyname="maxActive"><value>20</value></property>
              <propertyname="initialSize"><value>1</value></property>
              <propertyname="maxWait"><value>60000</value></property>
              <propertyname="maxIdle"><value>20</value></property>
              <propertyname="minIdle"><value>3</value></property>
              <propertyname="removeAbandoned"><value>true</value></property>
              <propertyname="removeAbandonedTimeout"><value>180</value></property>
              <propertyname="connectionProperties"><value>clientEncoding=GBK</value></property>
      </bean>

各配置参数的具体含义可参照：[dbcp基本配置和重连配置](http://agapple.iteye.com/blog/772507)

  

3\. sqlMapClient



      <beanid="sqlMapClient"class="org.springframework.orm.ibatis.SqlMapClientFactoryBean">
              <propertyname="configLocation">
                  <value>classpath:sqlmap.xml</value>
              </property>
          </bean>

          <beanid="sqlMapClientTddl"class="org.springframework.orm.ibatis.SqlMapClientFactoryBean">
              <propertyname="dataSource"ref="tGroupDataSource"/>
              <propertyname="configLocation"value="classpath:sqlmap.xml"/>
          </bean>

sqlMapClient，主要是借助于实现FactoryBean和InitializingBean两个接口，加载sql.xml文件资源信息，得到sqlMapClient组件

注：上面的sqlMapClient默认不配置数据源，后面的SqlMapClientTemplate优先从全局变量中取，如果没有再从sqlMapClient中查找。



      public DataSource getDataSource() {  
              DataSource ds = super.getDataSource();  
              return (ds != null ? ds : this.sqlMapClient.getDataSource());  
          }  

构造sqlMapClient组件的代码块。  



      public void afterPropertiesSet() throws Exception {  
              if (this.lobHandler != null) {  
                  // Make given LobHandler available for SqlMapClient configuration.  
                  // Do early because because mapping resource might refer to custom types.  
                  configTimeLobHandlerHolder.set(this.lobHandler);  
              }  

              try {  
                  this.sqlMapClient = buildSqlMapClient(this.configLocations, this.mappingLocations, this.sqlMapClientProperties);  

                  // Tell the SqlMapClient to use the given DataSource, if any.  
                  if (this.dataSource != null) {  
                      TransactionConfig transactionConfig = (TransactionConfig) this.transactionConfigClass.newInstance();  
                      DataSource dataSourceToUse = this.dataSource;  
                      if (this.useTransactionAwareDataSource && !(this.dataSource instanceof TransactionAwareDataSourceProxy)) {  
                          dataSourceToUse = new TransactionAwareDataSourceProxy(this.dataSource);  
                      }  
                      transactionConfig.setDataSource(dataSourceToUse);  
                      transactionConfig.initialize(this.transactionConfigProperties);  
                      applyTransactionConfig(this.sqlMapClient, transactionConfig);  
                  }  
              }  

              finally {  
                  if (this.lobHandler != null) {  
                      // Reset LobHandler holder.  
                      configTimeLobHandlerHolder.set(null);  
                  }  
              }  
          }  

  

4\. SqlMapExecutor 

该接口是对SQL操作行为的抽象，提供了SQL单条执行和批处理涉及的所有操作方法  

![](https://img-blog.csdn.net/20130626203330046?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYWFsYW5zZWhhaXlhbmc1Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

5\. SqlMapTransactionManager   
该接口是对事务行为的抽象，提供了事务执行过程中涉及的所有方法。   
 ![](https://img-blog.csdn.net/20130626203703109?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYWFsYW5zZWhhaXlhbmc1Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  
6\. SqlMapClient   
该接口定位是SQL执行客户端，是线程安全的，用于处理多个线程的sql执行。它继承了上面两个接口，这意味着该接口具有SQL执行和事务处理的能力，该接口的核心实现类是SqlMapClientImpl。   
  
7\. SqlMapSession   
该接口在继承关系上和SqlMapClient一致，但它的定位是保存单线程sql执行过程的session信息。该接口的核心实现类是SqlMapSessionImpl

  
8\. MappedStatement   
该接口定位是单条SQL执行时的上下文环境信息，如SQL标识、SQL、参数信息、返回结果、操作行为等。   
  
9\. ParameterMap/ResultMap   
该接口用于在SQL执行的前后提供参数准备和执行结果集的处理。   

整体类图：

![](https://img-blog.csdn.net/20130626211839046?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYWFsYW5zZWhhaXlhbmc1Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  

  

二、具体调用

接下来就到了数据持久层的代码调用，所有的数据库DML操作（增、删、改、查）都是借助于SqlMapClientTemplate来实现的。

![](https://img-blog.csdn.net/20130626111907734?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYWFsYW5zZWhhaXlhbmc1Mg==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)  



      public OrderEnsureProtocolDO getOrderEnsureProtocolByOrderId(Long orderId) {  
              if (orderId == null) {  
                  return null;  
              }  
              return (OrderEnsureProtocolDO) this.getSqlMapClientTemplate().queryForObject("MS-FIND-ORDERENSUREPROTOCOL-BY-ORDERID",  
                                                                                           orderId);  
          }  

如果一次执行的sql较多，我们会采用批处理的形式



      public void batchDeleteOfferSaleRecord(final List<Long> orderEntryIds) throws Exception {  
             if (orderEntryIds == null || orderEntryIds.size() <1 || orderEntryIds.size() > 50) {  
                 return;  
             }  

             this.getSqlMapClientTemplate().execute(new SqlMapClientCallback() {  

                 @Override  
                 public Object doInSqlMapClient(SqlMapExecutor executor) throws SQLException {  
                     executor.startBatch();  
                     for (Long entryId : orderEntryIds) {  
                         executor.insert(MS\_DELETE\_SALE_RECORD, entryId);  
                     }  

                     return executor.executeBatch();  
                 }  
             });  
         }  

不管采用上面哪种方式，查看源代码会发现，最后都是在调用execute(SqlMapClientCallback action)方法



      public Object queryForObject(final String statementName, final Object parameterObject)  
                  throws DataAccessException {  

              return execute(new SqlMapClientCallback() {  
                  public Object doInSqlMapClient(SqlMapExecutor executor) throws SQLException {  
                      return executor.queryForObject(statementName, parameterObject);  
                  }  
              });  
          }  

  



      public Object execute(SqlMapClientCallback action) throws DataAccessException {  
              Assert.notNull(action, "Callback object must not be null");  
              Assert.notNull(this.sqlMapClient, "No SqlMapClient specified");  
              //获取session信息(SqlMapSessionImpl实例)  
              SqlMapSession session = this.sqlMapClient.openSession();  
              if (logger.isDebugEnabled()) {  
                  logger.debug("Opened SqlMapSession \[" + session + "\] for iBATIS operation");  
              }  
              Connection ibatisCon = null;  

              try {  
                  Connection springCon = null;//数据库连接  
                  DataSource dataSource = getDataSource();  
                  boolean transactionAware = (dataSource instanceof TransactionAwareDataSourceProxy);  

                  try {  
                      //获取数据获连接  
                      ibatisCon = session.getCurrentConnection();  
                      if (ibatisCon == null) {  
                          springCon = (transactionAware ?  
                                  dataSource.getConnection() : DataSourceUtils.doGetConnection(dataSource));  
                          //将数据源set到session会话中  
                          session.setUserConnection(springCon);  
                          if (logger.isDebugEnabled()) {  
                              logger.debug("Obtained JDBC Connection \[" + springCon + "\] for iBATIS operation");  
                          }  
                      }  
                      else {  
                          if (logger.isDebugEnabled()) {  
                              logger.debug("Reusing JDBC Connection \[" + ibatisCon + "\] for iBATIS operation");  
                          }  
                      }  
                  }  
                  catch (SQLException ex) {  
                      throw new CannotGetJdbcConnectionException("Could not get JDBC Connection", ex);  
                  }  
                  try {  
                      //执行SQL   
                      return action.doInSqlMapClient(session);  
                  }  
                  catch (SQLException ex) {  
                      throw getExceptionTranslator().translate("SqlMapClient operation", null, ex);  
                  }  
                  finally {  
                      省略。。。一系列的关闭工作  
              }  
          }  

  

SqlMapSessionImpl().queryForObject()的方法很简单，直接交给代理对象SqlMapExecutorDelegate处理（里面注入了很多功能对象，负责具体的sql执行）



      public Object queryForObject(String id, Object paramObject) throws SQLException {  
        return delegate.queryForObject(session, id, paramObject);  
      }  

经过N层重载，最后调用内部的通用方法



       入参：   
       id=MS-FIND-ORDERENSUREPROTOCOL-BY-ORDERID  
       paramObject=26749329

       public Object queryForObject(SessionScope session, String id, Object paramObject, Object resultObject) throws SQLException {  
         Object object = null;  

      //MappedStatement对象集是上文中提及的初始化方法SqlMapClientFactoryBean.afterPropertiesSet()中，由配置文件构建而成  
      //调试中的ms为SelectStatement，具体的执行器  
         MappedStatement ms = getMappedStatement(id);   
      // 用于事务执行  
         Transaction trans = getTransaction(session);   
         boolean autoStart = trans == null;  

         try {  
           trans = autoStartTransaction(session, autoStart, trans);  
        // 从RequestScope池中获取该次sql执行中的上下文环境RequestScope   
           RequestScope request = popRequest(session, ms);    
           try {  
          // 执行sql  
             object = ms.executeQueryForObject(request, trans, paramObject, resultObject);     
           } finally {  
             pushRequest(request);  //归还RequestScope  
           }  

           autoCommitTransaction(session, autoStart);  
         } finally {  
           autoEndTransaction(session, autoStart);  
         }  

         return object;  
       }  

  
接下来由MappedStatement.executeQueryForObject()来执行  



      public Object executeQueryForObject(RequestScope request, Transaction trans, Object parameterObject, Object resultObject)  
           throws SQLException {  
         try {  
           Object object = null;  

           DefaultRowHandler rowHandler = new DefaultRowHandler();  
         //执行sql语句  
           executeQueryWithCallback(request, trans.getConnection(), parameterObject, resultObject, rowHandler, SqlExecutor.NO\_SKIPPED\_RESULTS, SqlExecutor.NO\_MAXIMUM\_RESULTS);  

           //结果处理，返回结果  
           List list = rowHandler.getList();   
           if (list.size() > 1) {  
             throw new SQLException("Error: executeQueryForObject returned too many results.");  
           } else if (list.size() > 0) {  
             object = list.get(0);  
           }  
         。。。。。。。。。  
       }  

MappedStatement.executeQueryWithCallback()方法包含了参数值映射、sql准备和sql执行等关键过程



      protected void executeQueryWithCallback(RequestScope request, Connection conn, Object parameterObject, Object resultObject, RowHandler rowHandler, int skipResults, int maxResults)  
          throws SQLException {  
      //预先封装错误信息，如果报错时便于排查问题  
        ErrorContext errorContext = request.getErrorContext();  
        errorContext.setActivity("preparing the mapped statement for execution");  
        errorContext.setObjectId(this.getId());  
        errorContext.setResource(this.getResource());  
        try {  
       //验证入参  
          parameterObject = validateParameter(parameterObject);    

       //获取SQL对象  
          Sql sql = getSql();    

          errorContext.setMoreInfo("Check the parameter map.");  
       // 入参映射  
          ParameterMap parameterMap = sql.getParameterMap(request, parameterObject);  

          errorContext.setMoreInfo("Check the result map.");  
       //获取结果  
          ResultMap resultMap = sql.getResultMap(request, parameterObject);   

          request.setResultMap(resultMap);  
          request.setParameterMap(parameterMap);  

          errorContext.setMoreInfo("Check the parameter map.");  
       //获取参数值  
          Object\[\] parameters = parameterMap.getParameterObjectValues(request, parameterObject);    

          errorContext.setMoreInfo("Check the SQL statement.");  
       //获取拼装后的sql语句  
          String sqlString = sql.getSql(request, parameterObject);    

          errorContext.setActivity("executing mapped statement");  
          errorContext.setMoreInfo("Check the SQL statement or the result map.");  
          RowHandlerCallback callback = new RowHandlerCallback(resultMap, resultObject, rowHandler);  
        //sql执行  
          sqlExecuteQuery(request, conn, sqlString, parameters, skipResults, maxResults, callback);   

          ....省略  
      }  

  
最后调用com.ibatis.sqlmap.engine.execution.SqlExecutor.executeQuery(RequestScope, Connection, String, Object\[\], int, int, RowHandlerCallback)



      public void executeQuery(RequestScope request, Connection conn, String sql, Object\[\] parameters, int skipResults, int maxResults, RowHandlerCallback callback) throws SQLException {  
        ...省略  
        PreparedStatement ps = null;  
        ResultSet rs = null;  
        setupResultObjectFactory(request);  
        try {  
          errorContext.setMoreInfo("Check the SQL Statement (preparation failed).");  
          Integer rsType = request.getStatement().getResultSetType();  
          //初始化PreparedStatement，设置sql、参数值等  
          if (rsType != null) {  
            ps = prepareStatement(request.getSession(), conn, sql, rsType);  
          } else {  
            ps = prepareStatement(request.getSession(), conn, sql);  
          }  
          setStatementTimeout(request.getStatement(), ps);  
          Integer fetchSize = request.getStatement().getFetchSize();  
          if (fetchSize != null) {  
            ps.setFetchSize(fetchSize.intValue());  
          }  
          errorContext.setMoreInfo("Check the parameters (set parameters failed).");  
          request.getParameterMap().setParameters(request, ps, parameters);  
          errorContext.setMoreInfo("Check the statement (query failed).");  
        //执行  
          ps.execute();  
          errorContext.setMoreInfo("Check the results (failed to retrieve results).");  

          //结果集处理  
          rs = handleMultipleResults(ps, request, skipResults, maxResults, callback);  

          。。。省略  

      }