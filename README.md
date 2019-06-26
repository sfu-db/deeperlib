Deeper, a data enrichment system through progressive deep deb crawling.
=========================
[![Travis](https://img.shields.io/badge/pypi-0.2-orange.svg?style=plastic)](https://pypi.python.org/pypi/deeperlib)
[![David](https://img.shields.io/badge/python-2.7-blue.svg?style=plastic)](https://www.python.org/)
	
Deeper is a system for data enrichment with web data. Given a local data table, it is able to efficiently find the matching records in a deep website through keyword search interface API, so that the returned data can be used to enrich the local data.


APIs Supportted
------------
The current version implemented API for the following websites as examples:

* [DBLP](http://dblp.uni-trier.de/faq/How+to+use+the+dblp+search+API.html)（DataBase systems and Logic Programming）
* [YELP](https://www.yelp.com/developers/documentation/v3/business_search)（Yelp Fusion API）
* [AMiner](http://doc.aminer.org/en/latest/s/index.html)（arnetminer）

### Custom

You can also implement other APIs based on your needs by implementing a subclass of deeper.api.simapi and pass it to deeper.core.smartcrawl.


Documentation
------------
Fantastic documentation is available at [https://sfu-db.github.io/deeperlib/](https://sfu-db.github.io/deeperlib/) 


Requirements
------------

* pqdict>=1.0.0
* requests>=2.18.4
* simplejson>=3.11.1
* rauth>=0.7.3

Requests officially supports Python 2.7.13, and runs great on PyPy.


Installation and Update
-----------------------

```
pip install deeperlib
```

```
pip install --upgrade deeperlib
```

Publication
-----------
[1]. P. Wang et al. Progressive Deep Web Crawling Through Keyword Queries For Data Enrichment. SIGMOD 2019.  
[2]. P. Wang et al. Deeper: A Data Enrichment System Powered by Deep Web. SIGMOD 2018 (demo).
