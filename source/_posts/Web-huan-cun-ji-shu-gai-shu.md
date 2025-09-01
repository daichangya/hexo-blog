---
title: Web缓存技术概述
id: 523
date: 2024-10-31 22:01:44
author: daichangya
excerpt: WWW是互联网上最受欢迎的应用之一，其快速增长导致网络拥塞和服务器超载，缓存技术被认为是减轻服务器负载、降低网络拥塞，减少客户访问延迟的有效途径之一。本文首先描述了Web缓存系统的基本要素及理想属性，然后介绍目前围绕Web缓存技术已经开展的研究，最后讨论Web缓存技术需要进一步研究的问题。
permalink: /archives/Web-huan-cun-ji-shu-gai-shu/
categories:
- 高性能系统设计
---

摘要WWW是互联网上最受欢迎的应用之一，其快速增长导致网络拥塞和服务器超载，缓存技术被认为是减轻服务器负载、降低网络拥塞，减少客户访问延迟的有效途径之一。本文首先描述了Web缓存系统的基本要素及理想属性，然后介绍目前围绕Web缓存技术已经开展的研究，最后讨论Web缓存技术需要进一步研究的问题。

**关键字**WWW缓存技术代理

1引言

WWW是互联网上最受欢迎的应用之一，其快速增长造成网络拥塞和服务器超载，导致客户访问延迟增大，WWW服务质量问题日益显现出来。缓存技术被认为是减轻服务器负载、降低网络拥塞、增强WWW可扩展性的有效途径之一，其基本思想是利用客户访问的时间局部性（Temporal Locality）原理，将客户访问过的内容在Cache中存放一个副本，当该内容下次被访问时，不必连接到驻留网站，而是由Cache中保留的副本提供。

Web内容可以缓存在客户端、代理服务器以及服务器端。研究表明，缓存技术可以显著地提高WWW性能\[1\]\[2\]，它可以带来以下好处：

（1）减少网络流量，从而减轻网络拥塞；

（2）降低客户访问延迟，其主要原因有：①缓存在代理服务器中的内容，客户可以直接从代理获取而不是从远程服务器获取，从而减小了传输延迟；②没有被缓存的内容由于网络拥塞及服务器负载的减轻而可以较快地被客户获取；

（3）由于客户的部分请求内容可以从代理处获取，从而减轻了远程服务器负载；

（4）如果由于远程服务器故障或网络故障造成远程服务器无法响应客户请求，客户可以从代理中获取缓存的内容副本，使得WWW服务的鲁棒性（Robustness）得到了加强。

Web缓存系统也会带来以下问题：

（1）客户通过代理获取的可能是过时的内容；

（2）如果发生缓存失效，客户的访问延迟由于额外的代理处理开销而增加。因此在设计Web缓存系统时，应力求做到Cache命中率最大化和失效代价最小化；

（3）代理可能成为瓶颈。因此应为一个代理设定一个服务客户数量上限及一个服务效率下限，使得一个代理系统的效率至少同客户直接和远程服务器相连的效率一样。

目前，围绕Web缓存系统及其最优化问题已经开展了广泛而深入的研究，这些研究工作主要是围绕代理的作用展开的。

2Web缓存系统的理想特性

一个理想的Web缓存系统应具有以下特性：

（1）快捷性：缓存系统应该能够有效地降低客户的访问延迟；

（2）鲁棒性：鲁棒性意味着可用性，客户希望Web服务随时可用；

（3）透明性：缓存系统对客户应是透明的，客户得到的结果仅仅是快速的响应和良好的可用性；

（4）可扩展性：Web缓存系统应能够随着网络规模和密度的不断增长而很好地进行扩展；

（5）高效性：Web缓存系统给网络带来的开销越小越好；

（6）适应性：缓存系统能够适应客户请求和网络环境的动态变化，这涉及到缓存管理、缓存路由、代理配置等，对于获得理想的缓存性能至关重要；

（7）稳定性：Web缓存系统采用的方案不应给网络带来不稳定；

（8）负载均衡：一个理想的缓存方案应能够将负载均匀地分发到整个网络，以避免某一个代理或服务器成为瓶颈或Hot spot点，而造成系统一部分甚至整个系统性能下降；

（9）异构处理能力：随着网络规模和覆盖域的不断增大，网络将跨越一系列不同的硬件和软件体系结构。Web缓存系统应能够适应不同的网络体系结构；

（10）简单性：简单的方案容易实现且易被普遍接受，一个理想的Web缓存方案配置起来应简单易行。

围绕上述特性，一个Web缓存系统必须解决好以下问题：

（1）缓存体系结构：缓存代理在网络中如何组织和配置；

（2）代理合作：代理间如何合作，相互合作的代理可以提高命中率而改善缓存系统的性能；

（3）缓存路由：当一处缓存代理失效时，如何将请求向其它缓存代理转发；

（4）缓存替换算法：当缓存空间不够时，缓存内容如何替换；

（5）缓存一致性：即缓存内容的时效性问题，如何防止缓存的内容过时；

（6）内容预取：代理如何决定从服务器或其它代理处进行内容预取以减少客户的访问延迟；

（7）负载平衡：如何解决网络中的“Hot spot”现象；

（8）缓存内容：什么样的内容可以被缓存。

在设计Web缓存系统时，必须涉及上述问题。

3Web缓存方案概述

3.1Web缓存体系结构

一个Web缓存系统的性能取决于其客户群的大小，客户群越大，缓存的内容被再次请求的可能性就越高。相互合作的Cache组可能会提高命中率而提高缓存系统的性能，因此缓存系统的体系结构应确保代理间能够有效地进行合作。典型的缓存体系结构有以下几种：层次式、分布式和混合式。

![](http://www1.lob.cn/upload/050719021586401.jpg)

图1 Web缓存系统体系结构图

**3.1.1层次式缓存体系结构**

Harvest项目\[3\]首先提出了层次式Web缓存体系结构。在层次式缓存体系结构中，Cache在网络呈多级配置，如图1（a）所示。为简单起见，假定有四级：底层Cache、局域层Cache、区域层Cache、广域层Cache。底层是客户/浏览器Cache，当客户端Cache不能满足客户的请求时，该请求被转发到局域层Cache，如果仍然得不到满足，则该请求被转发到区域层Cache直至广域层Cache。如果该请求在各级Cache中都得不到满足，则请求最终被转发到服务器。然后服务器对该请求的响应自顶向下地发送给客户，在沿途的每一个中间层Cache中留下一个副本。请求相同内容的其它请求则自下而上地进行转发，直到在某一级Cache中得到满足。

层次式缓存体系结构带宽效率高，点击率较高的Web内容可以快速高效地分布到网络中。但该体系结构也存在一些不足\[4\]：

（1）建立层次式缓存体系结构，缓存服务器必须配置在网络中关键的访问点上，缓存服务器间需相互合作；

（2）每一级Cache都会带来额外的延迟；

（3）高层Cache可能会成为瓶颈并带来较长的排队延迟；

（4）同一个内容的多个副本被保存在不同的Cache中，整个系统Cache空间利用率不高。

**3.1.2分布式缓存体系结构**

针对层次式缓存结构的上述缺陷，一些研究者提出了分布式缓存体系结构，在这种结构中，只有低层Cache,如图1（b）所示。文献\[5\]中的分布式Web缓存结构中，没有超出局域层的中间Cache层，Cache之间相互协作以处理失效。为了确定将客户请求转发给哪一个局域层Cache来获取失效的内容，每一个局域层Cache保留一份其它局域层Cache中缓存内容的目录信息，以便发生失效时将客户请求准确地转发到相应的局域层Cache。缓存阵列路由协议CARP\[6\]（Cache Array Routing protocol）是一种分布式缓存方案，它将URL空间分割成不同的部分，将每一部分指定给一组松散耦合的Cache组，每个Cache只能缓存具有指定给它的URL的Web内容，从而可以根据客户请求内容的URL来确定将请求转发给哪一个Cache。

在分布式缓存结构中，大多数的网络流量都发生在网络底层，不容易产生网络拥塞，Cache空间利用率高，且可以更好地实现负载共享，容错性更好。然而，一个大规模的分布式缓存系统的配置可能会遇到几个问题：连接次数较多、带宽要求高、管理困难\[4\]。

**3.1.3混合式缓存体系结构**

混合式体系结构如图1（c）所示，同级Cache采用分布式缓存结构，相互合作。Harvest集团设计的互联网缓存协议ICP（the Internet Cache Protocol）支持从RTT最小的父Cache或邻居Cache中获取相应的内容。

**3.1.4缓存体系结构的优化**

研究表明\[4\]层次式缓存体系结构和分布式缓存结构相比，层次式缓存体系结构具有较短的连接时间，因此将较小的文档缓存在中间层Cache中可以减少访问延迟；分布缓存结构具有较短的传输时间和较高的带宽利用率。理想的方案就是将二者结合起来，充分发挥各自的长处，同时减少连接时间和传输时间。

3.2缓存路由

出于对Web缓存系统扩展性的考虑，大多数缓存系统将大量的Cache分散在互联网上，这样带来的最大问题是如何快速地定位缓存有所需内容的Cache，这就是缓存路由问题。该问题有点类似于网络路由，但却不能用同样的方式解决。传统的网络路由可依地址聚类（层次式的地址表示使得地址聚类成为可能）而进行，但是在WWW中，具有相同URL前缀或服务器地址前缀的文档未必发送给相同的客户，难以对路由地址进行聚类，这样缓存路由表将大得难以管理。此外，缓存内容不断更新，过时的缓存路由信息将导致缓存失效。为降低Cache失效的代价，理想的缓存路由算法应该将客户的请求路由到下一个代理，该代理具有较高的命中可能性且位于或接近于客户到服务器的网络路径上。

**3.2.1缓存路由表法**

Malpani等人\[7\]将一组Cache组合起来，当客户的请求被转发到指定的Cache时，如果该Cache缓存有请求的内容，则将其发送给客户，否则通过IP组播将请求转发给同组的其它Cache，由缓存有相应内容的Cache对客户的请求进行响应，如果所有Cache中都没有缓存请求的内容，则该请求被转发到源服务器。Harvest\[3\]缓存系统将Cache组织成层次式结构并使用Cache解析协议ICP（Internet Cache Protocol），当发生Cache失效时，低层Cache在将客户请求转发到上一层Cache前，首先查询兄弟节点Cache是否缓存有相应的内容，以避免顶层Cache超载。自适应Web缓存系统\[8\]为每一个服务器建立Cache树，树中的Cache被组织成相互重叠的多点传送组，一个请求通过这些传送组来获取相应的缓存内容。该方法对每一个服务器构造不同的Cache树，因此没有根结点的超载问题，自配置性和鲁棒性都比较好。但是对点击率较低的内容请求可能会经过较多的Cache，产生较大的Cache通信开销，作者建议通过限制请求经过的Cache数来解决该问题。

**3.2.2哈希函数法**

Cache阵列路由协议CARP\[6\]使用一个基于阵列成员列表和URL的哈希函数来确定一个Web对象确切的缓存地址或一个Web对象应缓存在什么地方。在Summary Cache\[9\]中，每个代理保存一个同组中其它代理所缓存内容的URL摘要信息，该代理在转发客户请求时检查这些摘要信息以确定将请求转发给哪一个代理。为减小开销，这些摘要信息定期进行更新。试验表明该系统可以显著地减少Cache间的信息数量、带宽消耗以及协议带来的CPU开销，而保持和ICP几乎一样的缓存命中率。

3.3Cache替换算法

Cache替换算法是影响代理缓存系统性能的一个重要因素，一个好的Cache替换算法可以产生较高的命中率。目前已经提出的算法可以划分为以下三类：

（1）传统替换算法及其直接演化，其代表算法有：①LRU（Least Recently Used）算法：将最近最少使用的内容替换出Cache；②LFU（Lease Frequently Used）算法：将访问次数最少的内容替换出Cache；③Pitkow/Recker\[10\]提出了一种替换算法：如果Cache中所有内容都是同一天被缓存的，则将最大的文档替换出Cache，否则按LRU算法进行替换。

（2）基于缓存内容关键特征的替换算法，其代表算法有：①Size\[10\]替换算法：将最大的内容替换出Cache；②LRU—MIN\[11\]替换算法：该算法力图使被替换的文档个数最少。设待缓存文档的大小为S，对Cache中缓存的大小至少是S的文档，根据LRU算法进行替换；如果没有大小至少为S的对象，则从大小至少为S/2的文档中按照LRU算法进行替换；③LRU—Threshold\[11\]替换算法：和LRU算法一致，只是大小超过一定阈值的文档不能被缓存；④Lowest Lacency First\[12\]替换算法：将访问延迟最小的文档替换出Cache。

（3）基于代价的替换算法，该类算法使用一个代价函数对Cache中的对象进行评估，最后根据代价值的大小决定替换对象。其代表算法有：①Hybrid\[12\]算法：算法对Cache中的每一个对象赋予一个效用函数，将效用最小的对象替换出Cache；②Lowest Relative Value\[13\]算法：将效用值最低的对象替换出Cache；③Least Normalized Cost Replacement（LCNR）\[14\]算法：该算法使用一个关于文档访问频次、传输时间和大小的推理函数来确定替换文档；④Bolot等人\[15\]提出了一种基于文档传输时间代价、大小、和上次访问时间的权重推理函数来确定文档替换；⑤Size—Adjust LRU（SLRU）\[16\]算法：对缓存的对象按代价与大小的比率进行排序，并选取比率最小的对象进行替换。

总之，为了使Cache命中率最大化，围绕Cache替换算法已经开展了大量的工作，但是替换算法的性能很大程度上取决于WWW访问的特性，还没有哪一种替换算法能够对所有Web访问模式都优于其它算法。

**3.4缓存一致性**

Web缓存系统可以减小访问延迟，但带来了一个副作用：缓存的副本提供给客户的可能是过时的内容，因此必须有一套缓存一致性机制来确保缓存的内容能够及时进行更新及有效性确认，以便为客户提供最新的内容。

目前主要有两种缓存一致性类型：强缓存一致性和弱缓存一致性。

**3.4.1强缓存一致性**

（1）客户端确认：对于每一次访问，代理都认为缓存的内容已经过时并随请求发送一个“IF—Modified—Since—date”报头到服务器。如果在指定的时间后该内容发生了变化，则服务器将更新后的内容发送给代理并最终发送给客户；如果请求内容未修改，则发回 “304”响应，表示文档未修改，缓存内容继续有效。

（2）服务器确认：当服务器检测到一个内容发生变化时，服务器向所有最近请求过该内容并有可能缓存该内容的客户发送作废信息\[17\]。该方法要求服务器必须保存一个访问该内容的客户链表以便发送作废信息，当客户数量很大时，该方法将变得不适用，同时，该链表本身也可能过时，造成服务器向许多已经不再缓存该内容的客户发送作废信息。

**3.4.2弱缓存一致性**

（1）自适应TTL\[18\]（Time To Live）机制：通过观察一个文档的生存期来调整其生存时间，从而解决缓存一致性问题。如果一个文档在一个相当长的时间内都未修改过，它往往不会再发生变化。这样，一个文档的生存期属性被赋予一个该文档目前“年龄”（等于目前时间减去上一次修改的时间）的百分比。自适应TTL法可以将一个文档过时的可能性控制在＜5%的范围内。大多数的代理服务器都使用该机制，但是这种基于文档生存期的缓存一致性机制并不能确保缓存内容的有效性。

（2）捎带作废机制

Krishnamurthy等人提出使用捎带作废机制来提高缓存一致性的效率。他们提出了三种机制：①捎带确认PCV\[19\]（Piggyback Cache Validation）机制：利用代理发送给服务器的请求来提高缓存一致性。例如，当一个代理向服务器发出请求时，它捎带一系列缓存的但可能过时的来自该服务器的内容进行有效性确认；②捎带作废PSI\[20\]（Piggyback Service Invalidation）机制：其基本思想是当服务器对代理进行响应时，把一系列上次代理访问后变化的内容告诉代理服务器并由代理将这些内容作废，从而延长其它缓存内容在Cache中的缓存时间；③PSI和PCV混合机制\[21\]：该机制根据代理上次请求作废的时间距当前时间间隔的大小来确定采用何种机制，以实现最佳的总体性能。如果这个时间间隔较小，则使用PSI机制，否则使用PCV机制来对缓存内容进行确认。其基本原理是时间间隔越小，与PSI一起发送的作废数量就小，但随着时间的增长，发送作废的开销将大于请求确认的开销。

**3.5内容预取**

Web缓存技术可以提高Web性能，但研究表明\[22\]，不管采用何种缓存方案，最大缓存命中率通常不大于40～50%。为进一步提高缓存命中率，引入了预取技术。预取技术本质上是一种主动缓存技术，其基本思想是在处理客户的当前请求时，利用客户访问内容或模式的先验知识，对客户接下来的请求内容进行预测，并利用客户请求的间隙将预测内容缓存在Cache中，从而更好地隐藏延迟，提高服务质量。

早期研究集中在浏览器/客户与Web服务器之间进行内容预取，当代理被引入后，人们的研究兴趣转到了代理与服务器之间的预取技术研究。研究表明预取技术可以有效地降低客户访问延迟，但预取技术仍饱受争议，原因有二：

（1）内容预取是一种实时性要求较高的任务，它主要利用客户请求的间隔进行，而这个间隔一般情况下小于一分钟\[23\]，如果在这段时间内不能完成预取任务，预取将变得毫无意义。因此对预取算法的效率有较高的要求。

（2）内容预取是通过加重服务器负载及增加网络流量为代价来降低客户端响应时间的，因此对预取的准确度有较高的要求。同时，一个预取模型在确定预取文档的数量时，必须考虑客户的访问特性、服务器负载及网络流量状况，如果抛开这些因素来进行预取可能会造成事与愿违的效果。

总之，一个良好的预取模型，效率、准确度要高，付出代价小。围绕预取的高效性和准确性还需做进一步的研究。

**3.5负载平衡**

当众多客户同时从一台服务器获取数据或服务时就会发生Hot Spot现象，导致服务器性能下降甚至失效。目前处理该问题的方法大多数是使用某些复制策略将被请求的内容分贮在互联网上，从而将负载分散到多个服务器（代理）上\[24\]，避免单个服务器成为为瓶颈。

3.6缓存内容

一个代理可能发挥多种作用，除进行数据缓存外还可以进行连接缓存和计算缓存。连接缓存指在客户与代理、代理与服务器间使用持久连接，来减少建立TCP连接开销及服务器发送时的慢起动开销，从而减小客户访问延迟时间\[25\]。计算缓存可以看作是Web服务器可以将它们的部分服务迁移到代理，以减轻服务器瓶颈，其应用之一就是动态数据缓存，通过代理来缓存动态数据并将一部分计算迁移到代理，由代理来产生和维护缓存的动态数据，从而提高客户获取动态数据的性能。

4需要进一步研究的问题

围绕Web缓存技术已经开展了大量的研究并取得了丰硕成果，但仍有一些问题需做进一步的研究。这些问题包括：

（1）客户访问模式研究：通过研究客户的访问模式，从而更好地进行缓存管理和内容预取，提高缓存命中率；

（2）动态数据缓存：目前Web缓存命中率不高的一个重要原因是相当一部分内容（私有数据、授权数据、动态数据等）不能被缓存。如何使得更多的数据可以缓存以及如何减小客户访问非缓存页面的访问延迟已经成为提高Web性能的关键问题；

（3）Web流量特征：缓存系统的效率在于Web访问流的时间局部性以及良好的Cache管理策略，理解Web客户产生的负载特性对于更好地设计和提供Web服务具有重要意义；

（4）代理配置：要获得良好的Web性能，代理的配置至关重要，代理配置策略的理想标准是：自组织、高效路由、负载均衡、行为稳定等，围绕此问题还需做进一步的研究。

总之，提高Web性能的前沿研究在于开发扩展性、鲁棒性、适应性、稳定性好、高效且能够较好地配置在当前及今后网络中的缓存方案。

**参考文献**

\[1\]R. Caceres, F. Douglis, A. Feldmann, G. Glass, and M. Rabinovich, Web proxy caching: the devil is in the details, ACM Performance Evaluation Review, 26(3): pp. 11-15, December 1998.

\[2\]B. M. Duska, D. Marwood, and M. J. Feelay, The measured access characteristics of World Wide Web client proxy caches, Proceedings of USENIX Symposium on Internet Technologies and Systems(http://cs.ubc.ca/spider/feeley/wwwap/wwwap.html).

\[3\]A. Chankhunthod, P. B. Danzig, C. Neerdaels, M. F. Schwartz, and K. J. Worrel, A hierarchical Internet object cache, Usenix’96, January 1996.

\[4\]P. Rodriguez, C. Spanner, and E. W. Biersack, Web caching architectures: hierarchical and distributed caching, Proceedings of WCW’99.

\[5\]R. Tewari, M. Dahlin, H. Vin, and J. Kay, Beyond hierarchies: design considerations for distributed caching on the Internet, Technical Report TR98-04, Department of Computer Science, University of Texas at Austin, February 1998.

\[6\]V. Valloppillil and K. W. Ross, Cache array routing protocol v1.0, Internet Draft_draft- vinod-carp-v1-03.txt

\[7\]R. Malpani, J. Lorch, and D. Berger, Making World Wide Web caching servers cooperate, Proceedings of the 4th International WWW Conference, Boston, MA, Dec. 1995

\[8\]E. Cohen, B. Krishnamurthy, and J. Rexford, Evaluating server-assisted cache replacement in the Web, Proceedings of the European Symposium on Algorithms-98, 1998.

\[9\]L. Fan, P. Cao, J. Almeida, and A. Z. Broder, Summary cache: a scalable wide-area Web cache sharing protocol, Proceedings of Sigcomm’98.

\[10\]S. Williams, M. Abrams, C. R. Standridge, G. Abdulla, and E. A. Fox, Removal policies in network caches for World-Wide Web documents, Proceedings of Sigcomm’96.

\[11\]M. Abrams, C. R. Standridge, G. Abdulla, S. Williams, and E. A. Fox, Caching proxies: limitations and potentials, Proceedings of the 4th International WWW Conference, Boston, MA, Dec. 1995.

\[12\]R. P. Wooster and M. Abrams, Proxy caching that estimates page load delays, Proceedings of the 6th International WWW Conference, April 1997 (http://www.cs.vt.edu/ chitra/docs/www6r/).

\[13\]P. Lorenzetti, L. Rizzo, and L. Vicisano, Replacement policies for a proxy cache .

\[14\]P. Scheuermann, J. Shim, and R. Vingralek, A case for delay-conscious caching of Web documents, Proceedings of the 6th International WWW Conference, Santa Clara, Apr. 1997.

\[15\]J. C. Bolot and P. Hoschka, Performance engineering of the World-Wide Web: Application to dimensioning and cache design, Proceedings of the 5th International WWW Conference, Paris, France, May 1996.

\[16\]C. Aggarwal, J. L. Wolf, and P. S. Yu, Caching on theWorld Wide Web, IEEE Transactions on Knowledge and data Engineering, Vol. 11, No. 1, January/February 1999.

\[17\]P. Cao and C. Liu, Maintaining strong cache consistency in theWorld WideWeb, Proceedings of the 17th IEEE International Conference on Distributed Computing Systems, May 1997.

\[18\]V. Cate, Alex - a global file system, Proceedings of the 1992 USENIX File System Workshop, pp. 1-12, May 1992.

\[19\]B. Krishnamurthy and C. E.Wills, Study of piggyback cache validation for proxy caches in the World Wide Web, Proceedings of the 1997 USENIX Symposium on Internet Technology and Systems, pp. 1-12, December 1997.

\[20\]B. Krishnamurthy and C. E. Wills, Piggyback server invalidation for proxy cache coherency, Proceedings of the WWW-7 Conference, pp. 185-194, 1998.

\[21\]B. Krishnamurthy and C. E. Wills, Proxy cache coherency and replacement - towards a more complete picture, ICDC99, June 1999.

\[22\]F. Douglis, A. Feldmann, B. Krishnamurthy, and J. Mogul, Rate of change and other metrics: a live study of the World-Wide Web, Proceedings of the 1997 Usenix Symposium on Internet Technologies and Systems (USITS-97), Dec. 1997.

\[23\]B. Krishnamurthy and J. Rexford. Web Protocols and Practice : HTTP 1.1, Networking Protocols, Caching, and Tra_c Measurement. Addison-Wesley, 2001.

\[24\]P. Barford, A. Bestavros, A. Bradley, and M. E. Crovella, Changes in Web client access patterns: characteristics and caching implications, World Wide Web (special issue on Characterization and Performance Evaluation), 1999.

\[25\]A. Feldmann, R. Caceres, F. Douglis, G. Glass, and M. Rabinovich, Performance of Web proxy caching in heterogeneous bandwidth environments, Proceedings of Infocom’99.