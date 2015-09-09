# Business logic with PostgreSQL and Python

## Introduction

In my opinion PostgreSQL is the most advanced open source database. It has so many powerful features that is really difficult to put all of them here in this one acticle.

Here below I'm going to show you the least known feature of PostgreSQL which is procedural languages and stored functions. By using those stored procedures we are going to build business logic step by step.

## Business logic

By this term we are going to call all of those blocks of code which are responsible for making calculations and taking decisions about data flow. In many cases most of developers decide to build business logic as a part ORM models. It is pretty convenient. Whenever data is being used from database ORM can take control and decide how data is going to be returned to upper objects. Some ORM frameworks like Django allow us to extend base model and start building our own logic in a very complex way.

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

By this simple example you can see how easly it is to customize save method in Django ORM. By having such a custom code you can put some business logic in there. For instance you are able to prevalidate data before saving or modify data before save takes an action. There are unlimited options.

Some developers prefer to have business logic as a bunch of classes and functionalities stored in them. That is also a good solution as long as you keep attention and always in your code there is only one source of truth (code/functionality repetitions).

## Why not ORM?

Using ORM as a business logic container definitely has a lot of pros, although there is one serious problem with it. If you have a project which uses DB that is shared with other projects and those use different languages...then... You are going to use API for such a interactions with third-party software projects. How about if you have to deal with legacy code where there is not such an option to have API? Where to have business logic with one source of truth. How about using DB as a main source of trust?
