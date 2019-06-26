DeepER - Deep Entity Resolution
=========================
[![Travis](https://img.shields.io/badge/pypi-0.2-orange.svg?style=plastic)](https://pypi.python.org/pypi/deeperlib)
[![David](https://img.shields.io/badge/python-2.7-blue.svg?style=plastic)](https://www.python.org/)
	
A web data integration tool, A novel framework to overcome limitations, Easy for  configuration, Fully functional, Smooth interface.

which aims to find pairs of records that describe the same entity between a local database and a hidden database and has many applications in data enrichment and data cleaning. 


API Support
------------
DeepER is ready for the following API:

* [DBLP](http://dblp.uni-trier.de/faq/How+to+use+the+dblp+search+API.html)（DataBase systems and Logic Programming）
* [YELP](https://www.yelp.com/developers/documentation/v3/business_search)（Yelp Fusion API）
* [AMiner](http://doc.aminer.org/en/latest/s/index.html)（arnetminer）

### Custom

implement a subclass of deeper.api.simapi and pass it to deeper.core.smartcrawl 
and you would integrate a new api to collect more data.


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
