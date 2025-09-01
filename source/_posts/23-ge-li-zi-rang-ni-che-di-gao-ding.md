---
title: 23 个例子让你彻底搞定 Elasticsearch 的搜索查询语法
id: 1388
date: 2024-10-31 22:01:53
author: daichangya
excerpt: 目录例子最基础的matchquery提高相关度布尔查询模糊查询通配符查询正则表达式查询短句查询QueryString简化的QueryStringTerm/Terms查询Term查询-排序范围查询筛选布尔查询相关度函数：FieldValueFactor相关度函数衰变函数相关度函数：自定义函数原文ht
permalink: /archives/23-ge-li-zi-rang-ni-che-di-gao-ding/
tags:
- elasticsearch
---

目录

*   [例子](#%E4%BE%8B%E5%AD%90)
*   [最基础的 match query](#%E6%9C%80%E5%9F%BA%E7%A1%80%E7%9A%84match%20query)
*   [提高相关度](#%E6%8F%90%E9%AB%98%E7%9B%B8%E5%85%B3%E5%BA%A6)
*   [布尔查询](#%E5%B8%83%E5%B0%94%E6%9F%A5%E8%AF%A2)
*   [模糊查询](#%E6%A8%A1%E7%B3%8A%E6%9F%A5%E8%AF%A2)
*   [通配符查询](#%E9%80%9A%E9%85%8D%E7%AC%A6%E6%9F%A5%E8%AF%A2)
*   [正则表达式查询](#%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%9F%A5%E8%AF%A2)
*   [短句查询](#%E7%9F%AD%E5%8F%A5%E6%9F%A5%E8%AF%A2)
*   [Query String](#Query%20String)
*   [简化的 Query String](#%E7%AE%80%E5%8C%96%E7%9A%84Query%20String)
*   [Term/Terms 查询](#Term/Terms%20%E6%9F%A5%E8%AF%A2)
*   [Term 查询 - 排序](#Term%20%E6%9F%A5%E8%AF%A2%20-%20%E6%8E%92%E5%BA%8F)
*   [范围查询](#%E8%8C%83%E5%9B%B4%E6%9F%A5%E8%AF%A2)
*   [筛选布尔查询](#%E7%AD%9B%E9%80%89%E5%B8%83%E5%B0%94%E6%9F%A5%E8%AF%A2)
*   [相关度函数： Field Value Factor](#%E7%9B%B8%E5%85%B3%E5%BA%A6%E5%87%BD%E6%95%B0%EF%BC%9A%20Field%20Value%20Factor)
*   [相关度函数: 衰变函数](#%E7%9B%B8%E5%85%B3%E5%BA%A6%E5%87%BD%E6%95%B0:%20%20%E8%A1%B0%E5%8F%98%E5%87%BD%E6%95%B0)
*   [相关度函数： 自定义函数](#%E7%9B%B8%E5%85%B3%E5%BA%A6%E5%87%BD%E6%95%B0%EF%BC%9A%20%E8%87%AA%E5%AE%9A%E4%B9%89%E5%87%BD%E6%95%B0)

原文 [https://dzone.com/articles/23-useful-elasticsearch-example-queries](https://dzone.com/articles/23-useful-elasticsearch-example-queries)

为了说明 Elasticsearch 里不同的搜索类型，我们将会搜索一张名为 book 的表，并且拥有以下几个字段: title, authors, summary, release, data 和 number of reviews

首先我们将使用[bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)来准备一些测试数据

    PUT /bookdb_index
        { "settings": { "number_of_shards": 1 }}
    

    POST /bookdb_index/book/_bulk
        { "index": { "_id": 1 }}
        { "title": "Elasticsearch: The Definitive Guide", "authors": ["clinton gormley", "zachary tong"], "summary" : "A distibuted real-time search and analytics engine", "publish_date" : "2015-02-07", "num_reviews": 20, "publisher": "oreilly" }
        { "index": { "_id": 2 }}
        { "title": "Taming Text: How to Find, Organize, and Manipulate It", "authors": ["grant ingersoll", "thomas morton", "drew farris"], "summary" : "organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization", "publish_date" : "2013-01-24", "num_reviews": 12, "publisher": "manning" }
        { "index": { "_id": 3 }}
        { "title": "Elasticsearch in Action", "authors": ["radu gheorge", "matthew lee hinman", "roy russo"], "summary" : "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms", "publish_date" : "2015-12-03", "num_reviews": 18, "publisher": "manning" }
        { "index": { "_id": 4 }}
    

例子
--

### 最基础的 match query

有两种方法可以执行一个基础的 full-text 查询：使用轻量的 Search Api，这种方式通过在 Url 中加入参数来进行简单的查询，或者通过 JSON 格式的 request body，这种方式可以使用完整的 Elasticsearch 搜索 DSL

这是一个基础的查询，搜索所有字段，匹配字符 “guide”

    GET /bookdb_index/book/_search?q=guide
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "4",
        "_score": 1.3278645,
        "_source": {
          "title": "Solr in Action",
          "authors": [
            "trey grainger",
            "timothy potter"
          ],
          "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
          "publish_date": "2014-04-05",
          "num_reviews": 23,
          "publisher": "manning"
        }
      },
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "1",
        "_score": 1.2871116,
        "_source": {
          "title": "Elasticsearch: The Definitive Guide",
          "authors": [
            "clinton gormley",
            "zachary tong"
          ],
          "summary": "A distibuted real-time search and analytics engine",
          "publish_date": "2015-02-07",
          "num_reviews": 20,
          "publisher": "oreilly"
        }
      }
    ]
    

下面是使用 DSL 的版本，和上面的效果相同

    GET /bookdb_index/book/_search
    
    {
        "query": {
            "multi_match" : {
                "query" : "guide",
                "fields" : ["title", "authors", "summary", "publish_date", "num_reviews", "publisher"]
            }
        }
    }
    

`multi_match`关键字的作用是可以使多个字段同时匹配一个关键字，`fields`属性声明需要查询哪些字段，在这个例子中，我们搜索了这张表的所有字段

**备注**：Elasticsearch6 之前的版本可以使用"\_all"，来代替你声明所有字段，"\_all"字段的原理是串联所有的字段到一个大的字段，并使用空格分割，然后再分析并索引字段, 从 Elasticsearch6 开始，这个功能将被弃用，Elasticsearch6 提供了"copy\_to"参数，你可以利用这个创建自定义的"\_all"字段，查看[Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/copy-to.html)获取更多信息

Url 的搜索方式也允许你声明你想要搜索的字段，比如，搜索 title 为 “in Action” 的 books

    GET /bookdb_index/book/_search?q=title:in action
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "3",
        "_score": 1.6323128,
        "_source": {
          "title": "Elasticsearch in Action",
          "authors": [
            "radu gheorge",
            "matthew lee hinman",
            "roy russo"
          ],
          "summary": "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms",
          "publish_date": "2015-12-03",
          "num_reviews": 18,
          "publisher": "manning"
        }
      },
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "4",
        "_score": 1.6323128,
        "_source": {
          "title": "Solr in Action",
          "authors": [
            "trey grainger",
            "timothy potter"
          ],
          "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
          "publish_date": "2014-04-05",
          "num_reviews": 23,
          "publisher": "manning"
        }
      }
    ]
    

然而，使用完整的 DSL 搜索可以创建更加复杂的查询（我们等会会看到）并且你可以声明你想要的返回的结果，在下面的例子中，我们声明了我们想要返回多少个结果，偏移量是多少（这可以用来做分页），返回哪些字段以及配置高亮，注意我们使用了 “match”，代替了 “multi\_match”，因为我们只想要搜索 title 这一个字段

    POST /bookdb_index/book/_search
    {
        "query": {
            "match" : {
                "title" : "in action"
            }
        },
        "size": 2,
        "from": 0,
        "_source": [ "title", "summary", "publish_date" ],
        "highlight": {
            "fields" : {
                "title" : {}
            }
        }
    }
    [Results]
    "hits": {
      "total": 2,
      "max_score": 1.6323128,
      "hits": [
        {
          "_index": "bookdb_index",
          "_type": "book",
          "_id": "3",
          "_score": 1.6323128,
          "_source": {
            "summary": "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms",
            "title": "Elasticsearch in Action",
            "publish_date": "2015-12-03"
          },
          "highlight": {
            "title": [
              "Elasticsearch <em>in</em> <em>Action</em>"
            ]
          }
        },
        {
          "_index": "bookdb_index",
          "_type": "book",
          "_id": "4",
          "_score": 1.6323128,
          "_source": {
            "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
            "title": "Solr in Action",
            "publish_date": "2014-04-05"
          },
          "highlight": {
            "title": [
              "Solr <em>in</em> <em>Action</em>"
            ]
          }
        }
      ]
    

**注意**： 对于多个单词的搜索，match 查询支持使用 “operator” 参数来声明多个单词之间的关系，可以使用 and 来代替默认的 or，你还能通过声明 “minimum\_should\_match” 参数去调整搜索结果的相关性，更多细节，查看[Elasticsearch guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/match-multi-word.html)

提高相关度
-----

在我们搜索多个字段的时候，我们也许想要提高某个字段的分数（相关度），在下面的例子里，我们将 summary 这个字段的分数提高到了 3，增加这个字段的重要性，反过来说，这增加了\_id 为 4 的这条数据的相关性

    POST /bookdb_index/book/_search
    {
        "query": {
            "multi_match" : {
                "query" : "elasticsearch guide",
                "fields": ["title", "summary^3"]
            }
        },
        "_source": ["title", "summary", "publish_date"]
    }
    [Results]
    "hits": {
      "total": 3,
      "max_score": 3.9835935,
      "hits": [
        {
          "_index": "bookdb_index",
          "_type": "book",
          "_id": "4",
          "_score": 3.9835935,
          "_source": {
            "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
            "title": "Solr in Action",
            "publish_date": "2014-04-05"
          }
        },
        {
          "_index": "bookdb_index",
          "_type": "book",
          "_id": "3",
          "_score": 3.1001682,
          "_source": {
            "summary": "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms",
            "title": "Elasticsearch in Action",
            "publish_date": "2015-12-03"
          }
        },
        {
          "_index": "bookdb_index",
          "_type": "book",
          "_id": "1",
          "_score": 2.0281231,
          "_source": {
            "summary": "A distibuted real-time search and analytics engine",
            "title": "Elasticsearch: The Definitive Guide",
            "publish_date": "2015-02-07"
          }
        }
      ]
    

**备注**：提升相关度并不仅仅意味着计算得分乘以提升因子。应用的实际增强值通过标准化和一些内部优化。有关原理以及更多信息 [Elasticsearch guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/query-time-boosting.html)

布尔查询
----

AND/OR/NOT 操作符可以用来微调我们的搜索，使得搜索结果更加的符合预期，在 search Api 中，这被称之为布尔查询，布尔查询 可以使用参数 `must`（等同于 AND），可以使用参数`must_not`（等同于 NOT）和参数`should`（等同于 OR），举例来说，如果我想要搜索 title 为 “Elasticsearch” 或者 “Solr”，并且 authored 为 “clinton gormley” 但又不等于 “radu gheorge” 的 books

    POST /bookdb_index/book/_search
    {
      "query": {
        "bool": {
          "must": {
            "bool" : { 
              "should": [
                { "match": { "title": "Elasticsearch" }},
                { "match": { "title": "Solr" }} 
              ],
              "must": { "match": { "authors": "clinton gormely" }} 
            }
          },
          "must_not": { "match": {"authors": "radu gheorge" }}
        }
      }
    }
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "1",
        "_score": 2.0749094,
        "_source": {
          "title": "Elasticsearch: The Definitive Guide",
          "authors": [
            "clinton gormley",
            "zachary tong"
          ],
          "summary": "A distibuted real-time search and analytics engine",
          "publish_date": "2015-02-07",
          "num_reviews": 20,
          "publisher": "oreilly"
        }
      }
    ]
    

**备注**：可以看到，一个布尔查询（bool）可以嵌套另一个布尔查询，并且可以支持无限层级嵌套

模糊查询
----

模糊查询可以在`Match`和`Multi-Match`查询里使用，来解决用户拼写错误，模糊查询的程度声明基于原单词的[莱温斯坦距离](https://en.wikipedia.org/wiki/Levenshtein_distance)，即：需要对一个字符串进行一个字符更改的数量，以使其与另一个字符串相同。

    POST /bookdb_index/book/_search
    {
        "query": {
            "multi_match" : {
                "query" : "comprihensiv guide",
                "fields": ["title", "summary"],
                "fuzziness": "AUTO"
            }
        },
        "_source": ["title", "summary", "publish_date"],
        "size": 1
    }
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "4",
        "_score": 2.4344182,
        "_source": {
          "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
          "title": "Solr in Action",
          "publish_date": "2014-04-05"
        }
      }
    ]
    

**备注**：除了 “AUTO”，还可以指定数字 0，1 或者 2 去声明，可以匹配到一个单词的最大字符数，使用 “AUTO” 的好处是它考虑了字符串的长度，对于一个只有三个字符的单词，指定模糊匹配的字符数量为 2，显然对于性能是有问题的，因此，大部分情况还是建议使用 “AUTO”

通配符查询
-----

通配符查询允许你使用一个通配符来代替完整匹配。`?`可匹配任意字符，`*`可以匹配 0 或者更多其他字符，比如，我们要查找一条 authors 是"t"开头的数据

    POST /bookdb_index/book/_search
    {
        "query": {
            "wildcard" : {
                "authors" : "t*"
            }
        },
        "_source": ["title", "authors"],
        "highlight": {
            "fields" : {
                "authors" : {}
            }
        }
    }
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "1",
        "_score": 1,
        "_source": {
          "title": "Elasticsearch: The Definitive Guide",
          "authors": [
            "clinton gormley",
            "zachary tong"
          ]
        },
        "highlight": {
          "authors": [
            "zachary <em>tong</em>"
          ]
        }
      },
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "2",
        "_score": 1,
        "_source": {
          "title": "Taming Text: How to Find, Organize, and Manipulate It",
          "authors": [
            "grant ingersoll",
            "thomas morton",
            "drew farris"
          ]
        },
        "highlight": {
          "authors": [
            "<em>thomas</em> morton"
          ]
        }
      },
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "4",
        "_score": 1,
        "_source": {
          "title": "Solr in Action",
          "authors": [
            "trey grainger",
            "timothy potter"
          ]
        },
        "highlight": {
          "authors": [
            "<em>trey</em> grainger",
            "<em>timothy</em> potter"
          ]
        }
      }
    ]
    

正则表达式查询
-------

正则表达式查询允许你声明比通配查询更加复杂的查询

    POST /bookdb_index/book/_search
    {
        "query": {
            "regexp" : {
                "authors" : "t[a-z]*y"
            }
        },
        "_source": ["title", "authors"],
        "highlight": {
            "fields" : {
                "authors" : {}
            }
        }
    }
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "4",
        "_score": 1,
        "_source": {
          "title": "Solr in Action",
          "authors": [
            "trey grainger",
            "timothy potter"
          ]
        },
        "highlight": {
          "authors": [
            "<em>trey</em> grainger",
            "<em>timothy</em> potter"
          ]
        }
      }
    ]
    

短句查询
----

短句查询需要匹配所有单词才能被搜索出来，按照指定的顺序并且是连续的，默认情况下单词之间必须是连续的，但是你可以通过改写 “slop” 的值来声明即便两个单词之间间隔多少个单词，该文档仍然能被匹配出来

    POST /bookdb_index/book/_search
    {
        "query": {
            "match_phrase_prefix" : {
                "summary": {
                    "query": "search en",
                    "slop": 3,
                    "max_expansions": 10
                }
            }
        },
        "_source": [ "title", "summary", "publish_date" ]
    }
    [Results]
    "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "4",
            "_score": 0.5161346,
            "_source": {
              "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
              "title": "Solr in Action",
              "publish_date": "2014-04-05"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "1",
            "_score": 0.37248808,
            "_source": {
              "summary": "A distibuted real-time search and analytics engine",
              "title": "Elasticsearch: The Definitive Guide",
              "publish_date": "2015-02-07"
            }
          }
        ]
    

**备注**：Query-time search-as-you-type 有一定的性能成本，更好的方案是 index-time search-as-you-type，查看[Completion Suggester API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters-completion.html)或者使用 [Edge-Ngram](https://www.elastic.co/guide/en/elasticsearch/guide/current/_index_time_search_as_you_type.html)查看更多信息

Query String
------------

`query_string`查询提供了一种将 “multi\_match 查询”，“布尔查询”，“boosting”，“模糊查询”，“通配查询”，“范围查询” 整合在一个短句里的方法，下面的查询，匹配 “grant ingersoll” 或者 “tom morton.” 且含有短句 “grant ingersoll”，然后还将 summary 字段的分数提到了 2

    POST /bookdb_index/book/_search
    {
        "query": {
            "query_string" : {
                "query": "(saerch~1 algorithm~1) AND (grant ingersoll)  OR (tom morton)",
                "fields": ["title", "authors" , "summary^2"]
            }
        },
        "_source": [ "title", "summary", "authors" ],
        "highlight": {
            "fields" : {
                "summary" : {}
            }
        }
    }
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "2",
        "_score": 3.571021,
        "_source": {
          "summary": "organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization",
          "title": "Taming Text: How to Find, Organize, and Manipulate It",
          "authors": [
            "grant ingersoll",
            "thomas morton",
            "drew farris"
          ]
        },
        "highlight": {
          "summary": [
            "organize text using approaches such as full-text <em>search</em>, proper name recognition, clustering, tagging"
          ]
        }
      }
    ]
    

简化的 Query String
----------------

`simple_query_string`是`query_string`的一个版本，更加适合用在一个单独的搜索框里暴露给用户使用，因为它将 AND/OR/NOT 分别变成了 +/|/-，并且这种查询将不会直接将查询的语法错误直接抛出

    POST /bookdb_index/book/_search
    {
        "query": {
            "simple_query_string" : {
                "query": "(saerch~1 algorithm~1) + (grant ingersoll)  | (tom morton)",
                "fields": ["title", "authors" , "summary^2"]
            }
        },
        "_source": [ "title", "summary", "authors" ],
        "highlight": {
            "fields" : {
                "summary" : {}
            }
        }
    }
    

Term/Terms 查询
-------------

以上的例子展示了`full-text`搜索，有时候我们也会想要一个精确的匹配，`term`以及`terms`查询可以帮助我们做到这一点，下面的例子中，我们搜索了所有发布者为 “Manning” 发布的 books

    POST /bookdb_index/book/_search
    {
        "query": {
            "term" : {
                "publisher": "manning"
            }
        },
        "_source" : ["title","publish_date","publisher"]
    }
    [Results]
    "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "2",
            "_score": 1.2231436,
            "_source": {
              "publisher": "manning",
              "title": "Taming Text: How to Find, Organize, and Manipulate It",
              "publish_date": "2013-01-24"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "3",
            "_score": 1.2231436,
            "_source": {
              "publisher": "manning",
              "title": "Elasticsearch in Action",
              "publish_date": "2015-12-03"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "4",
            "_score": 1.2231436,
            "_source": {
              "publisher": "manning",
              "title": "Solr in Action",
              "publish_date": "2014-04-05"
            }
          }
        ]
    

多个`terms`可以用关键字`terms`来代替，并且可以传入一个数组

    {
        "query": {
            "terms" : {
                "publisher": ["oreilly", "packt"]
            }
        }
    }
    

Term 查询 - 排序
------------

Term 查询的结果（也包括其他种类的查询）可以很轻松的进行排序，多级排序也是被允许的

    POST /bookdb_index/book/_search
    {
        "query": {
            "term" : {
                "publisher": "manning"
            }
        },
        "_source" : ["title","publish_date","publisher"],
        "sort": [
            { "publish_date": {"order":"desc"}}
        ]
    }
    [Results]
    "hits": [
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "3",
        "_score": null,
        "_source": {
          "publisher": "manning",
          "title": "Elasticsearch in Action",
          "publish_date": "2015-12-03"
        },
        "sort": [
          1449100800000
        ]
      },
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "4",
        "_score": null,
        "_source": {
          "publisher": "manning",
          "title": "Solr in Action",
          "publish_date": "2014-04-05"
        },
        "sort": [
          1396656000000
        ]
      },
      {
        "_index": "bookdb_index",
        "_type": "book",
        "_id": "2",
        "_score": null,
        "_source": {
          "publisher": "manning",
          "title": "Taming Text: How to Find, Organize, and Manipulate It",
          "publish_date": "2013-01-24"
        },
        "sort": [
          1358985600000
        ]
      }
    ]
    

**备注**：在 6 之后的版本，使用 text 类型的字段排序或者分组，比如 title，你需要为那个字段指定`fielddata`，更多细节查看[ElasticSearch Guide.](https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html)

范围查询
----

还有另一种查询的结构我们称之为范围查询，在下面的例子里，我们搜索了所有在 2015 年发布的 books

    POST /bookdb_index/book/_search
    {
        "query": {
            "range" : {
                "publish_date": {
                    "gte": "2015-01-01",
                    "lte": "2015-12-31"
                }
            }
        },
        "_source" : ["title","publish_date","publisher"]
    }
    [Results]
    "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "1",
            "_score": 1,
            "_source": {
              "publisher": "oreilly",
              "title": "Elasticsearch: The Definitive Guide",
              "publish_date": "2015-02-07"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "3",
            "_score": 1,
            "_source": {
              "publisher": "manning",
              "title": "Elasticsearch in Action",
              "publish_date": "2015-12-03"
            }
          }
        ]
    

**备注**：范围查询支持的字段类型有：日期，数字和字符串

筛选布尔查询
------

当我们使用布尔查询的时候，可以使用`filter`参数去筛掉一些结果，下面的例子中，我们查询了 title 或者 summary 字段含有 “Elasticsearch”,与此同时我们还需要 reviews 的数量大于等于 20

    POST /bookdb_index/book/_search
    {
        "query": {
            "filtered": {
                "query" : {
                    "multi_match": {
                        "query": "elasticsearch",
                        "fields": ["title","summary"]
                    }
                },
                "filter": {
                    "range" : {
                        "num_reviews": {
                            "gte": 20
                        }
                    }
                }
            }
        },
        "_source" : ["title","summary","publisher", "num_reviews"]
    }
    [Results]
    "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "1",
            "_score": 0.5955761,
            "_source": {
              "summary": "A distibuted real-time search and analytics engine",
              "publisher": "oreilly",
              "num_reviews": 20,
              "title": "Elasticsearch: The Definitive Guide"
            }
          }
        ]
    

多个 filters 可以再一个`bool`查询中结合起来使用，下一个例子中，filter 规定了结果必须含有最少 20 个 reviews，发布时间不能早于 2015 年，并且发布人应该是 Reilly

    POST /bookdb_index/book/_search
    {
        "query": {
            "filtered": {
                "query" : {
                    "multi_match": {
                        "query": "elasticsearch",
                        "fields": ["title","summary"]
                    }
                },
                "filter": {
                    "bool": {
                        "must": {
                            "range" : { "num_reviews": { "gte": 20 } }
                        },
                        "must_not": {
                            "range" : { "publish_date": { "lte": "2014-12-31" } }
                        },
                        "should": {
                            "term": { "publisher": "oreilly" }
                        }
                    }
                }
            }
        },
        "_source" : ["title","summary","publisher", "num_reviews", "publish_date"]
    }
    [Results]
    "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "1",
            "_score": 0.5955761,
            "_source": {
              "summary": "A distibuted real-time search and analytics engine",
              "publisher": "oreilly",
              "num_reviews": 20,
              "title": "Elasticsearch: The Definitive Guide",
              "publish_date": "2015-02-07"
            }
          }
        ]
    

相关度函数： Field Value Factor
-------------------------

有时候你可能想要根据结果的某个字段的值来提升这条数据在这次检索中的相关度，比较典型的是你希望根据数据的被关注的程度来提升检索相关度，在下面的例子中，我们希望通过 reviews 的数量来提升一条文档的相关度，可以通过`field_value_factor`函数实现

    POST /bookdb_index/book/_search
    {
        "query": {
            "function_score": {
                "query": {
                    "multi_match" : {
                        "query" : "search engine",
                        "fields": ["title", "summary"]
                    }
                },
                "field_value_factor": {
                    "field" : "num_reviews",
                    "modifier": "log1p",
                    "factor" : 2
                }
            }
        },
        "_source": ["title", "summary", "publish_date", "num_reviews"]
    }
    [Results]
    "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "1",
            "_score": 0.44831306,
            "_source": {
              "summary": "A distibuted real-time search and analytics engine",
              "num_reviews": 20,
              "title": "Elasticsearch: The Definitive Guide",
              "publish_date": "2015-02-07"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "4",
            "_score": 0.3718407,
            "_source": {
              "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
              "num_reviews": 23,
              "title": "Solr in Action",
              "publish_date": "2014-04-05"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "3",
            "_score": 0.046479136,
            "_source": {
              "summary": "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms",
              "num_reviews": 18,
              "title": "Elasticsearch in Action",
              "publish_date": "2015-12-03"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "2",
            "_score": 0.041432835,
            "_source": {
              "summary": "organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization",
              "num_reviews": 12,
              "title": "Taming Text: How to Find, Organize, and Manipulate It",
              "publish_date": "2013-01-24"
            }
          }
        ]
    

**备注 1**：我们可以使用`multi_match`来查询，再通过 reviews 数量来排序，但是这样我们就失去了相关度算法带来的好处

**备注 2**： 有一些额外的参数例如 “modifier”, “factor”, “boost\_mode” 等等，更多详情参考[Elasticsearch guide.](https://www.elastic.co/guide/en/elasticsearch/guide/current/boosting-by-popularity.html)

相关度函数: 衰变函数
-----------

除了通过某个字段提高一条文档的相关度之外，你也许还想要通过判断一个字段的某个值距离你想要的值的差来减少相关度，例如通过日期，在下面的例子里，我们希望文档的发布时间在 2014 年 6 月左右，越接近这个日期则相关越高，反之则越低

    POST /bookdb_index/book/_search
    {
        "query": {
            "function_score": {
                "query": {
                    "multi_match" : {
                        "query" : "search engine",
                        "fields": ["title", "summary"]
                    }
                },
                "functions": [
                    {
                        "exp": {
                            "publish_date" : {
                                "origin": "2014-06-15",
                                "offset": "7d",
                                "scale" : "30d"
                            }
                        }
                    }
                ],
                "boost_mode" : "replace"
            }
        },
        "_source": ["title", "summary", "publish_date", "num_reviews"]
    }
    [Results]
    "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "4",
            "_score": 0.27420625,
            "_source": {
              "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
              "num_reviews": 23,
              "title": "Solr in Action",
              "publish_date": "2014-04-05"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "1",
            "_score": 0.005920768,
            "_source": {
              "summary": "A distibuted real-time search and analytics engine",
              "num_reviews": 20,
              "title": "Elasticsearch: The Definitive Guide",
              "publish_date": "2015-02-07"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "2",
            "_score": 0.000011564,
            "_source": {
              "summary": "organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization",
              "num_reviews": 12,
              "title": "Taming Text: How to Find, Organize, and Manipulate It",
              "publish_date": "2013-01-24"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "3",
            "_score": 0.0000059171475,
            "_source": {
              "summary": "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms",
              "num_reviews": 18,
              "title": "Elasticsearch in Action",
              "publish_date": "2015-12-03"
            }
          }
        ]
    

相关度函数： 自定义函数
------------

如果内置的相关度函数无法满足你的需求，你可以使用自己定制的相关度函数，现在，我们想要写一个函数，根据发布时间来判断，reviews 数量越多的文档理所应当提高其相关度，但是对于一本新书来说，显然不应该适用这个规则，它们不应该因为 reviews 的数量而被 “惩罚”

脚本如下

    publish_date = doc['publish_date'].value
    num_reviews = doc['num_reviews'].value
    if (publish_date > Date.parse('yyyy-MM-dd', threshold).getTime()) {
      my_score = Math.log(2.5 + num_reviews)
    } else {
      my_score = Math.log(1 + num_reviews)
    }
    return my_score
    

使用动态脚本，我们要用到`script_score`选项

    POST /bookdb_index/book/_search
    {
        "query": {
            "function_score": {
                "query": {
                    "multi_match" : {
                        "query" : "search engine",
                        "fields": ["title", "summary"]
                    }
                },
                "functions": [
                    {
                        "script_score": {
                            "params" : {
                                "threshold": "2015-07-30"
                            },
                            "script": "publish_date = doc['publish_date'].value; num_reviews = doc['num_reviews'].value; if (publish_date > Date.parse('yyyy-MM-dd', threshold).getTime()) { return log(2.5 + num_reviews) }; return log(1 + num_reviews);"
                        }
                    }
                ]
            }
        },
        "_source": ["title", "summary", "publish_date", "num_reviews"]
    }
    [Results]
    "hits": {
        "total": 4,
        "max_score": 0.8463001,
        "hits": [
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "1",
            "_score": 0.8463001,
            "_source": {
              "summary": "A distibuted real-time search and analytics engine",
              "num_reviews": 20,
              "title": "Elasticsearch: The Definitive Guide",
              "publish_date": "2015-02-07"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "4",
            "_score": 0.7067348,
            "_source": {
              "summary": "Comprehensive guide to implementing a scalable search engine using Apache Solr",
              "num_reviews": 23,
              "title": "Solr in Action",
              "publish_date": "2014-04-05"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "3",
            "_score": 0.08952084,
            "_source": {
              "summary": "build scalable search applications using Elasticsearch without having to do complex low-level programming or understand advanced data science algorithms",
              "num_reviews": 18,
              "title": "Elasticsearch in Action",
              "publish_date": "2015-12-03"
            }
          },
          {
            "_index": "bookdb_index",
            "_type": "book",
            "_id": "2",
            "_score": 0.07602123,
            "_source": {
              "summary": "organize text using approaches such as full-text search, proper name recognition, clustering, tagging, information extraction, and summarization",
              "num_reviews": 12,
              "title": "Taming Text: How to Find, Organize, and Manipulate It",
              "publish_date": "2013-01-24"
            }
          }
        ]
      }
    

**备注 1**：要使用动态脚本，必须在你的 config/elasticsearch.yaml 里打开，更多参数，查看[Elasticsearch reference docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html)

**备注 2**：JSON 在编写时不能换行，所以需要用分号来分割