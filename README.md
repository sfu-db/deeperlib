DeepER - Deep Entity Resolution
=========================

A web data integration tool, A novel framework to overcome limitations, Easy for  configuration, Fully functional, Smooth interface.

which aims to find pairs of records that describe the same entity between a local database and a hidden database and has many applications in data enrichment and data cleaning. 


API Support
------------
DeepER is ready for the following API:

* [DBLP](http://dblp.uni-trier.de/faq/How+to+use+the+dblp+search+API.html)（DataBase systems and Logic Programming）
* [YELP](https://www.yelp.com/developers/documentation/v3/business_search)（Yelp Search API）
* [AMiner](http://doc.aminer.org/en/latest/s/index.html)（arnetminer）

### Custom

implement a subclass of deeper.api.simapi and pass it to deeper.core.smartcrawl 
and you would integrate a new api to collect more data.


Documentation
------------
Fantastic documentation is available at [https://sfu-db.github.io/deeper/](https://sfu-db.github.io/deeper/) 


Requirements
------------

* pqdict==1.0.0
* requests==2.18.4
* simplejson==3.11.1
* matplotlib==2.0.2
* numpy==1.13.1
* rauth==0.7.3

Requests officially supports Python 2.7.13(64-bit), and runs great on PyPy.


Installation and Update
-----------------------
pip install -r requirements.txt

easy_install deeper-0.1-py2.7.egg

Changelog
----------
v0.1a

* 2017/09/14 deeper's birthday



Discussing
----------
<table> 
	<tr> 
		<th>Author</th> 
		<th>email</th>
	</tr> 
	<tr> 
		<th>yongjun he</th> 
		<th>141250047@smail.nju.edu.cn</th> 
	</tr>  
</table>