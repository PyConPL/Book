# Business logic with PostgreSQL and Python

## Introduction

In my opinion PostgreSQL is the most advanced open source database. It has so many powerful features that is really difficult to put all of them in this one acticle.

Below I'm going to show you the least known features of PostgreSQL which is procedural languages and stored functions. By using stored procedures we are going to build business logic step by step.

## Business logic

This term we are going to call all of those blocks of code which are responsible for making calculations and taking decisions about data flow. In many cases most of developers decide to build business logic as part ORM models. It is pretty convenient. Whenever data is being used from database ORM can take control and decide how data is going to be returned to upper objects. Some ORM frameworks like Django allow us to extend base model and start building our own logic in a very complex way.

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

This simple example you can see how easly it is to customize save method in Django ORM. By having such a custom code you can put some business logic in there. For instance you are able to prevalidate data before saving or modify data before save takes an action. There are unlimited options.

Some developers prefer to have business logic as a bunch of classes and functionalities stored in them. That is also a good solution as long as you keep attention and always is only one source of truth (code/functionality repetitions).

## Why not ORM?

Using ORM as a business logic container definitely has a lot of pros, although there is one serious problem with it. If you have a project which uses DB that is shared with other projects and those use different languages...then... You are going to use API for such interactions with third-party software projects. How about if you have to deal with legacy code where there is not such option to have API? Where to have business logic with one source of truth. How about using DB as a main source of trust?

## Python

Compiling Python is not a difficult process. Let me show you in few simples steps how to do it.

Download python source code

    wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz

Compile it. Warning, Please pay attention about –enable-shared flag!

    ~/stuff/Python-2.7.10% ./configure —PREFIX=/opt/py –enable-shared

It is very important to remember to compile python with **–enable-shared** option. Without it during PostgreSQL compilation you're not going to be able to use compiled Python as procedural language extension.

Also on some systems if you try to run Python and you’re getting this kind of error

    py ➤ bin/python2.7

**bin/python2.7: error while loading shared libraries: libpython2.7.so.1.0: cannot open shared object file: No such file or directory**

Then you need to add lib path of your newly compiled python to the system lib path

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/py/lib
    
## PostgreSQL with Python support

Download source code.

    wget https://ftp.postgresql.org/pub/source/v9.4.4/postgresql-9.4.4.tar.bz2

Compile with Python support from */opt/py* directory

    ./configure –prefix=/opt/pgsql —with-python PYTHON=/opt/py/bin/python
    make
    make install

Now compile and install PostgreSQL plugins

    cd ~/stuff/postgresql-9.4.3/contrib
    make
    make install

## Create DB

Now it is time to start PostgreSQL. First you have to initialize name space.

    mkdir /opt/pg_data
    /opt/pgsql/bin/initdb /opt/pg_data

and start DB…

    /opt/pgsql/bin/postmaster -p 5432 -D /opt/pg_data/

Create new DB.

    /opt/pgsql/bin/createdb -h localhost  -E utf8 pie

Please remember about the correct encoding for DB! Now create new language for database pie

    /opt/pgsql/bin/createlang -h localhost  -d pie plpythonu
    
And that's it. Simple as that. Your new DB has full Python support and we can start orginizing business logic in there.

## First function

Before you are going to create your first plPython (PostgreSQL stored Python functions) you have to know how it works. Your newly compiled Python and its modules are fully accessible from plPython. This means that the entire Python standard library is fully accessible when writing your business logic. Also you can install any kind of module which you may use later from your functions.

Example plPython code

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


## Business logic basics

For bulding business logic I will use trigger functions on tables that I am going to create. Doesn't matter if tables are going to be controlled by any ORM or they are going to get access by using pure SQL. Each time data is being changed trigger is going to be used and corresponding function is going to be called. Of course when 

## Summary

