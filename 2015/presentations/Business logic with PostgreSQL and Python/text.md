# Business logic with PostgreSQL and Python

## Introduction

In my opinion PostgreSQL is the most advanced open source database. It has so many powerful features that is really difficult to put all of them in this one article.

Below I'm going to show you the least known features of PostgreSQL which is procedural languages and stored functions. By using stored procedures we are going to build business logic step by step.

## Business logic

By business logic we are going to call all of those blocks of code which are responsible for making calculations and taking decisions about data flow. In many cases most of developers decide to build business logic as part of ORM models. It is pretty convenient. Whenever data is being used from database ORM can take control and decide how data is going to be returned to upper objects. Some ORM frameworks like Django allow us to extend base model and start building our own logic in a very complex way.

Example piece of pseudo code in Django ORM


    from django.db import models

    class _MyBaseModel(models.Model):
      def save(self, *args, **kwargs):
        # we can have some magic here
        # code code code
        
        # call actual save, so "magic" will happen before saving data into DB
        super(_MyBaseModel, self).save(*args, **kwargs) 
        
    class History(_MyBaseModel):
      """ model which always calls custom save method before calling Django's save """
      shops = models.IntegerField('Number of shops', default = 0, null = True)
      customers = models.IntegerField('Number of customers', default = 0, null=True)
      customer_type = models.SmallIntegerField('Customer Type', choices = CustomerTypes.CHOICES)
      
      def save(self, *args, **kwargs):
          # also we can have another level of customization here
          super(History, self).save(*args, **kwargs)

With this simple example you can see how easy it is to customize save method in Django ORM. By having such a custom code you can put some business logic in there. For instance you are able to validate data prior to saving it in a database. The options are unlimited here.

Some developers prefer to have business logic as a bunch of classes with functionalities in them. That is also a good solution as long as you pay attention and always is only one source of truth.

## Source of truth

To explain to you what I call *source of truth* let me allow myself to use some example. Imagine web application that uses database as data storage and it accepts some page form being posted but in different views. Let's assume that mentioned form can have slight differences in those views. What you expect from your system based on given input (submitted page form) is to always validate and process data in exact same way. For example your system is going to check if there is any duplication in database, validate required data and data types. Obvious is that system based on given input always has to react in the same way and return designed result.

That is what I am going to use in this article as *source of truth*, in other words *Business Logic*. Each time input is given system will react in the same way. Each entry point of the system which uses the same context of data will react in the same way.


## Why not ORM?

Using ORM as a business logic container definitely has a lot of pros, although there is one serious problem with it. If you have a project which uses DB that is shared with other projects and those use different languages...then... you mostly are going to use API for such interactions with third-party software projects. What if you have to deal with legacy code where where having API is not an option? Where to store your single source of truth, iow. your business logic? How about using the database as one?

## Python

Compiling Python is not a difficult process. Let me show you in a few simples steps how to do it.

Download python source code

    wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz

Compile Python under your custom directory (*—prefix* flag). In below example I'm ging to compile Python under */opt/py* to make sure that Python which later on I will use with PostgreSQL is not conflicting with Python that is installed with operating system. Custom Python also has got one significant advantage. If operating system (ex. Linux) comes with Python that is main part of system tools (ex. yum) it is always good idea to isolate Python that you're about to use with your application from system's Python.

Please make sure to add *–enable-shared* flag during compilation. This option will tell Python to compile with shared libraries. Once Python libraries are compiled with shared option then any software can soft link them and use Python.

    ~/stuff/Python-2.7.10% ./configure —prefix=/opt/py –enable-shared

When compilation is finished, some operating systems when you try to run your compiled Python can return below error message.

    py ➤ bin/python2.7

    bin/python2.7: error while loading shared libraries: libpython2.7.so.1.0: cannot open shared object file: No such file or directory**

You have to add *lib path* of your newly compiled Python to the system lib path. For instance you can add below linbe to your .bashrc file. In my case I compiled Python under */opt/py* so that is why I added path as below.

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/py/lib
    
To simplify installation process of Python modules let's install **pip package manager**. 

    wget https://bootstrap.pypa.io/get-pip.py | /opt/py/bin/python
    
## PostgreSQL with Python support

Download source code.

    wget https://ftp.postgresql.org/pub/source/v9.4.4/postgresql-9.4.4.tar.bz2

Compile with Python support from */opt/py* directory. Same as during Python compilation I'm going to compile PostgreSQL under custom directory (*--prefix* flag) */opt/pgsql*.

    ./configure –prefix=/opt/pgsql —with-python PYTHON=/opt/py/bin/python
    
    make
    
    make install

Now you have to compile and install PostgreSQL plugins

    cd contrib
    
    make
    
    make install

## Create DB

Now it is time to start PostgreSQL. First you have to initialize name space. I used */opt/pg_data* directory for PostgreSQL storage.

    mkdir /opt/pg_data
    /opt/pgsql/bin/initdb /opt/pg_data

and start DB. Below command  will start PostgreSQL which is going to listen on all interfaces and port *5432* (default) and data directory (*-D* option) is going to be /opt/pg_data.

    /opt/pgsql/bin/postmaster -p 5432 -D /opt/pg_data/

Create new empty database *pie* with encoding  **UTF-8** (*-E* option). Option *-h* tells createdb command that PostgreSQL server listens on *localhost* and oport *5432* (option *-p*).

    /opt/pgsql/bin/createdb -h localhost -p5432  -E utf8 pie

Install Python support for database *pie*. Again we have to specify localhost (-h) and port (-p) that is being used by the server. Option *-d* allow you to create **plpythonu** language under *pie* database. Please notice that language that I created in below example is called **plpythonu*. Letter *u* stands for untrusted. Why untrusted? That is more about history of PostgresQL and Python support.

    /opt/pgsql/bin/createlang -h localhost -p5432 -d pie plpythonu
    
And that's it. Simple as that. Your new DB has full Python support and we can start organizing business logic in there.

## Word of the day

Before you are going to create your first plpython function you have to know how it works. Your compiled Python and its modules are fully accessible from plpython. This means that the entire Python standard library is fully accessible when writing your business logic. Also you can install any kind of module which you may use later from your functions.

I need to provide additional clarifications here, both terms 'procedural' and 'function' can be a little bit confusing for newcomers. Generally from PostgreSQL perspective you always create plpython function. You call plpython function which is stored in DB. What is "inside" of that function (Python objects or other functions) is up to you to decide. Procedural programming is not the only pattern that you can use inside of plpython. To illustrate two different bodies of function please check example from below.

    create or replace function my_first_function()
    returns int as
    $$
    
    class MyObjectA:
        def __init__(self):
            """some body of constructor"""
            
        def methodA(self, param_1, param_2):
            """body of the method"""
            
    class MyObjectB:
        def __init__(self):
            """some body of constructor"""
            
        def methodB(self, param_1, param_2):
            """body of the method"""
    
    b = methodB()
    a = MyObjectA()
    plpy.info("Some info message")
    return b.methodB(a.methodA(10, 15), "some string")
    
    
    $$
    LANGUAGE plpythonu VOLATILE;
    
Example of calling such a plpython function

    sql: SELECT * FROM my_first_function();
    
Same plpython function but with much simpler body

    create or replace function my_first_function()
    returns int as
    $$
    
    import random
    
    return random.randint(1,20)
    
    $$
    LANGUAGE plpythonu VOLATILE;
    
Example of calling such a plpython function

    sql: SELECT * FROM my_first_function();

You may notice that from PostgreSQL engine perspective calling *my_first_function* looks identical even if the actual body of function written in plpython is either flat function or complex object.

As for business logic with Python inside of database that I want show you I am not trying to convince you to start using procedural programming against object programming or the other way around. As I already said - it is up to you to decide what will fit best when writing plpython functions, although please read below Zen of Python. Again, again, and... again before you start writing actually any Python code.

> Beautiful is better than ugly.

> Explicit is better than implicit.

> Simple is better than complex.

> Flat is better than nested.

> Readability counts.

> If the implementation is hard to explain, it’s a bad idea

What I am trying to point out here is that you should be careful when creating plpython functions, they should not be too complex. Simplicity can bring you a lot of benefits, especially when debugging the code to nail a bug.

# Hello world

Let me show you how to write the classical hello world function

    create or replace function logic.hello_world()
    returns void as
    $$
    """
    Code code code code
    """
    plpy.info("hello world")
    $$
    LANGUAGE plpythonu VOLATILE;
    

As you can see from above example you are able to print out some log messages. They go to stdout of PostgreSQL directly which means in production stout is redirected to a log file. Depending on PostgreSQL log level you can hide some unwanted messages from plPy function same as some context like which function calls which. Example of a verbose log level.

    pie=# select * from logic.view_and_set_discounted_sales(20, 23) ;
    INFO:  [view_and_set_discounted_sales] Updating item id: 36 with new discounted price: 0.529331946972
    CONTEXT:  PL/Python function "view_and_set_discounted_sales"
    INFO:  [view_and_set_discounted_sales] Updating item id: 40 with new discounted price: 5.03912459204
    CONTEXT:  PL/Python function "view_and_set_discounted_sales"
    INFO:  [view_and_set_discounted_sales] Updating item id: 45 with new discounted price: 3.37963644177
    CONTEXT:  PL/Python function "view_and_set_discounted_sales"

PostgreSQL with above log level (notice) will not only show you your *info* messages but also **context** in which it's been logged. That is something that is very helpful with debugging production cases. Once function is being called from context statement you can see what kind of triggers or sub-functions were called. Example message

    INFO:  [view_and_set_discounted_sales] Updating item id: 45 with new discounted price: 3.37963644177
    CONTEXT:  PL/Python function "view_and_set_discounted_sales"
    
Let's stop here for a minute and analyze that example.

*INFO* - log level of the message
*[view_and_set_discounted_sales] Updating item id: 45 with new discounted price: 3.37963644177* - Custom message that function prints out
*CONTEXT:  PL/Python function "view_and_set_discounted_sales"* - context in which above message has been logged.

To be able to control **log level** that PostgreSQL is going to catch or ignore please use one of below options in /opt/pgsql/postgresql.conf settings file. 

**client_min_messages** - Controls which message levels are sent to the client (ex. postgreSQL shell)

**log_min_messages** - Controls which message levels are written to the server log



Available values of log level in order of decreasing detail:

1. debug5
2. debug4
3. debug3
4. debug2
5. debug1
6. log
7. notice
8. warning
9. error


## Database schema

First comes first. Below you can see structure of tables and relations for database *pie* which I will use in future examples.

    CREATE TABLE client
    (
      id bigserial NOT NULL,
      row_change_time timestamp without time zone NOT NULL,
      c_name varchar,
      c_surname varchar,
      dob date,
      e_mail varchar,
      CONSTRAINT client_pkey PRIMARY KEY (id),
      CONSTRAINT client_email_key UNIQUE (e_mail)
    );
    
    
    CREATE TABLE item
    (
        id bigserial NOT NULL,
        item_name text,
        item_price Decimal(10,2),
        item_serial_nr varchar(32),
        active boolean,
      CONSTRAINT item_pkey PRIMARY KEY (id),
      CONSTRAINT item_name_id_key UNIQUE (item_name, item_serial_nr)
    );
    
    CREATE TABLE bill
    (
      id bigserial NOT NULL,
      bill_created timestamp without time zone NOT NULL,
      shop_code varchar(32) NOT NULL,
      field_hash varchar(32) NOT NULL,
      client_id bigint NOT NULL,
      bill_sent boolean default false,
      bill_number varchar,
      CONSTRAINT bill_pkey PRIMARY KEY (id),
      CONSTRAINT billcode_hash_key UNIQUE (shop_code, field_hash)
      
    );
    
    ALTER TABLE bill
      ADD FOREIGN KEY (client_id) REFERENCES client (id) ON DELETE CASCADE ON UPDATE CASCADE;
    
    
    
    CREATE TABLE bill_item
    (
        id bigserial NOT NULL,
        item_name text,
        item_qty int,
        item_price float,
        item_discount_value float default 0,
        item_id bigint,
        bill_id bigint,
      CONSTRAINT bill_item_pkey PRIMARY KEY (id),
      CONSTRAINT bill_name_id_key UNIQUE (bill_id, item_id)
    );
    
    ALTER TABLE bill_item
      ADD FOREIGN KEY (item_id) REFERENCES item (id) ON DELETE CASCADE ON UPDATE CASCADE;
    ALTER TABLE bill_item
      ADD FOREIGN KEY (bill_id) REFERENCES bill(id) ON DELETE CASCADE ON UPDATE CASCADE;
    
    
    CREATE SCHEMA logic;
    
    CREATE SEQUENCE public.bill_number_seq;

## Main pattern

For building business logic in database I will use two main things:

* triggers with trigger functions on tables
* plpython functions to access data from database

## Triggers

Triggers are going to help me with making my data to be consistent. Doesn't matter if tables are going to be controlled by ORM or they are going to get accessed by using pure SQL. Each time data is being changed trigger will be used with corresponding function. Of course based on which conditions PostgreSQL engine will call triggered function is up to you to define.

Trigger function can be call before or after

* update
* insert 
* delete

How to define trigger on a table foo you can see below. Trigger function *my_trigger_function* will be called *after insert* of each record.

    CREATE TRIGGER my_trigger
        AFTER INSERT ON table_foo
            FOR EACH ROW EXECUTE PROCEDURE my_trigger_function();
            
To show you how trigger can be applied on tables let's try to look closer on below example. Let's create table *foo* and *foo_backup*. Structure of these tables is following:

    CREATE TABLE foo
    (
      id bigserial NOT NULL,
      row_change_time timestamp without time zone NOT NULL,
      e_mail varchar,
      CONSTRAINT foo_pkey PRIMARY KEY (id),
      CONSTRAINT foo_email_key UNIQUE (e_mail)
    );

To be able to protect data in table *foo* from being deleted let's apply a trigger in that table.

    CREATE TRIGGER my_trigger_before_delete
        BEFORE DELETE ON foo
            FOR EACH ROW EXECUTE PROCEDURE protect_data();

I will make a copy of data when field *row_change_time* is greater then 15 minutes. 

    create or replace function protect_data()
    returns trigger as
    $$
    from datetime import datetime
    
    v = datetime.now() - datetime.strptime(TD['old']['row_change_time'][:19], '%Y-%m-%d %H:%M:%S')
    
    if v.seconds/60.0 > 15:
        # backup data before losing it
        plpy.info('Backing up data...')
        sql = """INSERT INTO foo_backup (row_change_time, e_mail) 
                    VALUES ('{0}', '{1}')".format(TD['old']['row_change_time'],
                                                TD['old']['e_mail'])
    	plpy.execute(sql)
    
    
    $$
    LANGUAGE plpythonu VOLATILE;
    

## plpython functions 

As it was already mentioned another PostgreSQL feature which is going to be used to build business logic in DB are *plpython functions*. These functions will be used by all the applications that will access database. Each time I will try to modify or read some data in database *pie* I will call a function instead of a table directly.

Example of such approach can be plpython function which takes 2 arguments and returns set of records which are considered by PostgreSQL as a table. Such a table works as view which of course can be used in regular SQL queries. Below I pasted a function which for given bill number will apply given discount. Just to remind you table structures were shown in chaper "schema*.

    create or replace function logic.view_and_set_discounted_sales(
    in_bill_number bigint,
    in_discount_percentage float,
    out out_id bigint,
    out out_bill_number varchar,
    out out_item_name text,
    out out_item_price Decimal(10,2),
    out out_item_serial_nr varchar,
    out out_bill_sent boolean
    )
    returns setof record as
    $$
    
    from decimal import Decimal

    sql = """SELECT bill.id, bill_number, bill_item.item_name, bill_item.item_qty, bill_item.item_price, item_discount_value, bill_id, bill_sent, item_id,
    item_serial_nr
    FROM
    bill LEFT JOIN bill_item on (bill.id =bill_id)
    LEFT JOIN item on (item_id=item.id)
    WHERE 
    bill.id=%d""" % (in_bill_number)
    result = []
    plpy.debug(sql);
    for x in plpy.execute(sql):
        item_price = plpy.execute("SELECT item_price FROM bill_item WHERE item_id=%d AND bill_id=%d" % (x['item_id'], x['bill_id']))[0]['item_price']    
        discounted_price = float(item_price)*((100.0-in_discount_percentage)/100.0)
        result.append([x['id'], x['bill_number'], x['item_name'], discounted_price, x['item_serial_nr'], x['bill_sent']])

    return result
    $$
    LANGUAGE plpythonu VOLATILE;
    
Executing above function on a bill table is going to return below results. Of course I pre-filled tables with data to be easy to simulate working function.

    pie=# select * from logic.view_and_set_discounted_sales(20, 33);
    
    out_id | out_bill_number |     out_item_name     | out_item_price |        out_item_serial_nr        | out_bill_sent
    --------+-----------------+-----------------------+----------------+----------------------------------+---------------
     20 | 20              | My awesome product 6  | 0.687444086976 | 109a95fce2b40f146d15c743c5cd0278 | t
     20 | 20              | My awesome product 10 |    6.544317652 | 3fda3c7814fc94a0dba9fc2bb190adab | t
     20 | 20              | My awesome product 15 |  4.38913823607 | 2ad4a8800fd241d5cf6519404a385aa1 | t
    (3 rows)

and different value for *in_discount_percentage* parameter

    pie=# select * from logic.view_and_set_discounted_sales(20, 23) ;
    
     out_id | out_bill_number |     out_item_name     | out_item_price |        out_item_serial_nr        | out_bill_sent
    --------+-----------------+-----------------------+----------------+----------------------------------+---------------
     20 | 20              | My awesome product 6  | 0.529331946972 | 109a95fce2b40f146d15c743c5cd0278 | t
     20 | 20              | My awesome product 10 |  5.03912459204 | 3fda3c7814fc94a0dba9fc2bb190adab | t
     20 | 20              | My awesome product 15 |  3.37963644177 | 2ad4a8800fd241d5cf6519404a385aa1 | t
    (3 rows)

As you can see in above example it is possible to create function which allows you to return dynamic table where returned data depends on input values. Also as I said previously PostgreSQL understands result of such a query as a table so you can do as for instance

    pie=# select * from logic.view_and_set_discounted_sales(20, 23) WHERE out_item_serial_nr='109a95fce2b40f146d15c743c5cd0278';
    
     out_id | out_bill_number |    out_item_name     | out_item_price |        out_item_serial_nr        | out_bill_sent
    --------+-----------------+----------------------+----------------+----------------------------------+---------------
         20 | 20              | My awesome product 6 | 0.407585599168 | 109a95fce2b40f146d15c743c5cd0278 | t
    (1 row)

## Simple cache

Let's put all the mentioned triggers and plpython functions together into one working business logic. Let's create simple caching system.

Let's start with triggers. Each time table *bill* is going to get updates I will revalidate only that chunk of data that has changed and save the result to Redis cache. Trigger definition is going to be like this.

    CREATE TRIGGER t_bill_i
        AFTER INSERT OR UPDATE ON bill
        FOR EACH ROW EXECUTE PROCEDURE logic.tgr_bill_i();

As I mentioned before you have an access to all Python modules and standard libraries, so let's install Redis module.

    /opt/py/bin/pip install redis

Body of trigger function *logic.tgr_bill_i* you can see below.

    create or replace function logic.tgr_bill_i()
    returns trigger as
    $$
    import redis
    from cPickle import dumps
    in_server = '127.0.0.1'
    in_port = 6379
    
    POOL = redis.ConnectionPool(host=in_server, port = in_port if in_port is not None else 6379, db = 1)
    r = redis.Redis(connection_pool = POOL)
    
    if TD['new']['bill_created']:
        bill_key = 'bill_active:%s' % TD['new']['field_hash']
        r.set(bill_key, dumps({
            'bill_created' : TD['new']['bill_created'],
            'shop_code' : TD['new']['shop_code'],
            'field_hash' : TD['new']['field_hash'],
            'id' : TD['new']['id'],
            'client_id' : TD['new']['client_id']
            }))
        plpy.info('[tgr_bill_i] Saving bill hash: {0}'.format(bill_key))
    $$
    LANGUAGE plpythonu VOLATILE;


Once data is being saved to Redis we can access such data by using below plpython function.

    create or replace function logic.get_active_bills()
    returns text as
    $$
    
    import redis
    from cPickle import loads
    from cjson import encode
    
    in_server = '127.0.0.1'
    in_port = 6379
    
    POOL = redis.ConnectionPool(host=in_server, port = in_port if in_port is not None else 6379, db = 1)
    r = redis.Redis(connection_pool = POOL)
    
    status = {'msg' : '', 'status' : False } # let False means error, True - all OK
    bills = r.keys('bill_active:*')
    all_bills = []
    for k in bills if bills else []:
        out = r.get(k)
        if out is None:
            continue
        data = loads(out)
        all_bills.append(data)
    
    return encode({'status' : status, 'data' : all_bills})
    $$
    LANGUAGE plpythonu VOLATILE;
            
As you may see above example is going to return JSON object. For instance such a data can be returned directly to a browser without post processing (if you're writing web application). 

To demonstarte you how to call above function from Python please use below example.

    import psycopg2
    import psycopg2.extras
    
    def read_bills():
        conn = psycopg2.connect(my_connection_string)
        cur = conn.cursor('foo', cursor_factory=psycopg2.extras.DictCursor)
    
        sql = "SELECT * FROM logic.get_active_bills()"
        cur.execute(sql)
        res = cPickle.loads(conn.fetchall()[0]['get_active_bills'])
        
        return res # JSON structure
        
    if __name__ == '__main__':
        print 'This is my JSON result from cache', read_bills()

Most important part of above example is to notice that I'm **calling function** instead of making SQL query which gets **data from table** directly. BY doing so I am making sure that I actually use my business logic. By getting data directly from a table like 

    sql = "SELECT * FROM bill"

I'd bypass business logic and I could get not that kind of data which I should get. That is actually the **essence of business logic** on database side. Calling functions and views instead of reading data directly from tables and having bunch of triggers around tables are the key to have business logic with PostgreSQL and Python.

## Summary

Caching here was just an example. It also returns JSON structure instead of set of records. The options how to transform data and what kind of data state to return and in which format are countless. The key part as already mentioned is to start using functions whenever you want to access data. Of course you do not have to be to extreme and *always* use only functions to be able to access tables. You have to find the right balance where it is better to allow changing data by using functions and where data can be changed directly in the table and triggers will do the *magic*.

## Advantages

1. Logic on DB side makes many things simpler and much cleaner to control.
2. By having triggers you do not have to worry if data is going to be changed from your application, ORM, raw SQL or any third-party modules.
3. Simple to debug and replicate bugs.
4. Multiprocessing (controlled by database).
5. Direct access to data (all is running on DB side).
6. Clear separation from business logic and the actual code of application (dry code).

## Disadvantages

1. Very complex unittest.
2. Nested and long loops can cause significant memory foot prints.
3. Exclusive locks can cause altering triggers on tables (not trigger functions!) to hang during update unitl lock is removed.
4. Schema migrations always have to go in hand with functions changes.


## References

http://python.org

http://www.postgresql.org/docs/

https://kmonsoor.wordpress.com/2015/08/10/seven-deadly-sins-in-python-code/

