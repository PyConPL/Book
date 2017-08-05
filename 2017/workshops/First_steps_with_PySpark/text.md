
# Welcome to the 'First steps with PySpark'!

### What is Apache Spark?

> Apache Spark is a fast and general engine for large-scale data processing

> Run programs up to 100x faster than Hadoop MapReduce in memory, or 10x faster
on disk.

Project page: *https://spark.apache.org/*

### What is PySpark?

> PySpark is the Spark Python API, which exposes the Spark programming model to
Python.

Docs: https://spark.apache.org/docs/latest


### Spark ecosystem
- Spark SQL (for structured data)
- Spark Streaming (real time data)
- MLib (machine learning library)
- GraphX (graph processing)

### Main Spark concept

- DataFrames (stores your data)
- transformations (transform your data)
- actions (generate results)

### Spark context and SQL context

In order to use Spark and its DataFrame API we will need to use a SQLContext.
When running Spark, you start a new Spark application by creating a
SparkContext. You can then create a SQLContext from the SparkContext. When the
SparkContext is created, it asks the master for some cores to use to do work.
The master sets these cores aside just for you; they won't be used for other
applications.


    # Display the type of the Spark sqlContext
    type(sqlContext)


    # List sqlContext's attributes
    dir(sqlContext)


    # Use help to obtain more detailed information
    help(sqlContext)

Outside of pyspark or a notebook, SQLContext is created from the lower-level
SparkContext, which is usually used to create Resilient Distributed Datasets
(RDDs). An RDD is the way Spark actually represents data internally; DataFrames
are actually implemented in terms of RDDs.

While you can interact directly with RDDs, DataFrames are preferred. They're
generally faster, and they perform the same no matter what language (Python, R,
Scala or Java) you use with Spark.

In this course, we'll be using DataFrames, so we won't be interacting directly
with the Spark Context object very much. However, it's worth knowing that inside
pyspark or a notebook, you already have an existing SparkContext in the sc
variable. One simple thing we can do with sc is check the version of Spark we're
using:


### DataFrame

DataFrame is a 2-dimensional labeled data structure. Is consists of a series of
Row objects; each Row object has a set of named columns. You can think of a
DataFrame as modeling a table, though the data source being processed does not
have to be a table.
More formally, a DataFrame must have a schema, which means it must consist of
columns, each of which has a name and a type.

On DataFrames we perform transformations and actions. DataFrame is immutable, so
once it is created, it cannot be changed. As a result, each transformation
creates a new DataFrame. Finally, we can apply one or more actions to the
DataFrames.

Spark uses lazy evaluation, so transformations are not actually executed until
an action occurs.

#### Prepare testing data

We will use a third-party Python testing library called `fake-factory` to create
our dataset - a collection of randomly generated fake person records.


    from faker import Factory
    fake = Factory.create()
    fake.seed(4321)


    # Each entry consists of last_name, first_name, ssn, job, and age.
    from pyspark.sql import Row
    def fake_entry():
        name = fake.name().split()
        return Row(name[1], name[0], fake.ssn(), fake.job(), abs(2016 - fake.date_time().year) + 1)


    # Create a helper function to call a function repeatedly
    def repeat(times, func, *args, **kwargs):
        for _ in range(times):
            yield func(*args, **kwargs)


    data = list(repeat(10000, fake_entry))

Data is just a normal Python list, containing Spark SQL `Row` objects. Let's
look for details:


    data[0][0], data[0][1], data[0][2], data[0][3], data[0][4]


    # Check the size of the list
    len(data)

#### Create DataFrame

To create DataFrame we will use `createDataFrame` method:


    help(sqlContext.createDataFrame)


    data_df = sqlContext.createDataFrame(data, ('last_name', 'first_name', 'ssn', 'occupation', 'age'))


    print('type of data_df: {0}'.format(type(data_df)))


    data_df.printSchema()


    sqlContext.registerDataFrameAsTable(data_df, 'dataframe')


    # What methods can we call on this DataFrame?
    help(data_df)


    # How many partitions will the DataFrame be split into?
    data_df.rdd.getNumPartitions()


    new_df = data_df.distinct().select('*')
    new_df.explain(True)

#### Working on DataFrame


    # Transform data_df through a select transformation and rename the newly created '(age -1)' column to 'age'
    # Because select is a transformation and Spark uses lazy evaluation, no jobs, stages,
    # or tasks will be launched when we run this code.
    sub_df = data_df.select('last_name', 'first_name', 'ssn', 'occupation', (data_df.age - 1).alias('age'))


    # Query plan
    sub_df.explain(True)

### Actions

> Action operations cause Spark to perform the (lazy) transformation operations
that are required to compute the values returned by the action.

#### collect()

> Return all the elements of the dataset as an array at the driver program. This
is usually useful after a filter or other operation that returns a sufficiently
small subset of the data.

> Be careful while expecting a big amount of results. The data returned to the
driver must fit into the driver's available memory. If not, the driver will
crash.


    # Use collect to view result
    results = sub_df.collect()
    print(results)

#### show()

> Another (usually better) way to visualize the data. If you don't tell `show()`
how many rows to display, it displays 20 rows.


    sub_df.show()

If you'd prefer that show() not truncate the data, you can tell it not to:


    sub_df.show(n=30, truncate=False)

In Databricks, there's an even nicer way to look at the values in a DataFrame:
The display() helper function.



    display(sub_df)

#### count()

> Returns the number of elements in the dataset.


    # Counting records
    print(data_df.count())
    print(sub_df.count())

#### first() and take()

> One useful thing to do when we have a new dataset is to look at the first few
entries to obtain a rough idea of what information is available. In Spark, we
can do that using actions like `first()`, `take()`, and `show()`. Note that for
the `first()` and `take()` actions, the elements that are returned depend on how
the DataFrame is partitioned.

> Instead of using the `collect()` action, we can use the take(n) action to
return the first n elements of the DataFrame. The `first()` action returns the
first element of a DataFrame, and is equivalent to `take(1)[0]`.


    print("first: {0}\n".format(sub_df.first()))
    print("Four of them: {0}\n".format(sub_df.take(4)))


    display(sub_df.take(4))

### Transformations

#### Filtering

> The `filter()` method is a transformation operation that creates a new
DataFrame from the input DataFrame, keeping only values that match the filter
expression.

> An alias to `filter()` is `where()`


    filtered_df = sub_df.filter(sub_df.age < 10)
    filtered_df.show(truncate=False)
    filtered_df.count()

#### User defined functions (UDF)

> To pass function over our DataFrame we can define user defined function (UDF).
UDF is a special wrapper around a function, allowing the function to be used in
a DataFrame query.

> Also `lambda` functions and `map`, `reduce` operations are often useful.


    from pyspark.sql.types import BooleanType
    less_ten = udf(lambda s: s < 10, BooleanType())
    lambda_df = sub_df.filter(less_ten(sub_df.age))
    lambda_df.show()
    lambda_df.count()


    # Let's collect the even values less than 10
    even = udf(lambda s: s % 2 == 0, BooleanType())
    even_df = lambda_df.filter(even(lambda_df.age))
    even_df.show()
    even_df.count()

#### orderBy()

> orderBy() allows you to sort a DataFrame by one or more columns, producing a
new DataFrame.

> orderBy() takes one or more columns, either as names (strings) or as Column
objects. To get a Column object, we use one of two notations on the DataFrame:
>    Pandas-style notation: filtered`_`df.age
>    Subscript notation: filtered`_`df['age']



    # Get the five oldest people in the list. To do that, sort by age in descending order.
    display(dataDF.orderBy(dataDF.age.desc()).take(5))


    display(dataDF.orderBy('age').take(5))

#### distinct() and dropDuplicates()
> distinct() filters out duplicate rows, and it considers all columns.

> dropDuplicates() is like distinct(), except that it allows us to specify the
columns to compare.


    print(data_df.count())
    print(data_df.distinct().count())


    print data_df.dropDuplicates(['first_name', 'last_name']).count()

#### drop()

> drop() is like the opposite of select(): Instead of selecting specific columns
from a DataFrame, it drops a specified column from a DataFrame.

Here's a simple use case: Suppose you're reading from a 1,000-column CSV file,
and you have to get rid of five of the columns. Instead of selecting 995 of the
columns, it's easier just to drop the five you don't want.



    data_df.drop('occupation').drop('age').show()

#### groupBy()

> groupBy() allows you to perform aggregations on a DataFrame.

> Unlike other DataFrame transformations, `groupBy()` does not return a
DataFrame. Instead, it returns a special GroupedData object that contains
various aggregation functions.

> The most commonly used aggregation function is `count()`, but there are others
(like `sum()`, `max()`, and `avg()`.

> These aggregation functions typically create a new column and return a new
DataFrame.



    data_df.groupBy('occupation').count().show(truncate=False)


    data_df.groupBy().avg('age').show(truncate=False)


    # We can also use groupBy() to do another useful aggregations:
    print("Maximum age: {0}".format(data_df.groupBy().max('age').first()[0]))
    print("Minimum age: {0}".format(data_df.groupBy().min('age').first()[0]))

#### sample()

> Returns a new DataFrame with a random sample of elements from the dataset. It
takes in a `withReplacement` argument, which specifies whether it is okay to
randomly pick the same item multiple times from the parent DataFrame (so when
`withReplacement=True`, you can get the same item back multiple times). It takes
in a `fraction` parameter, which specifies the fraction elements in the dataset
you want to return. (So a fraction value of 0.20 returns 20% of the elements in
the DataFrame.) It also takes an optional `seed` parameter that allows you to
specify a seed value for the random number generator, so that reproducible
results can be obtained.


    sampled_df = data_df.sample(withReplacement=False, fraction=0.10)
    print sampled_df.count()
    sampled_df.show()


    print(data_df.sample(withReplacement=False, fraction=0.05).count())

### Caching DataFrames

For efficiency Spark keeps your DataFrames in memory, so it can quickly access
the data. However, memory is limited - if you try to keep too many partitions in
memory, Spark will automatically delete partitions from memory to make space for
new ones. If you later refer to one of the deleted partitions, Spark will
automatically recreate it for you, but that takes time.

So, if you plan to use a DataFrame more than once, then you should tell Spark to
cache it. You can use the `cache()` operation to keep the DataFrame in memory.
However, you must still trigger an action on the DataFrame, such as `collect()`
or `count()` before the caching will occur.


    # Cache the DataFrame
    filtered_df.cache()
    # Trigger an action
    print(filtered_df.count())
    # Check if it is cached
    print(filtered_df.is_cached)

 For efficiency, once you are finished using cached DataFrame, you can
optionally tell Spark to stop caching it in memory by using the DataFrame's
`unpersist()` method to inform Spark that you no longer need the cached data.


    # If we are done with the DataFrame we can unpersist it so that its memory can be reclaimed
    filtered_df.unpersist()
    # Check if it is cached
    print(filtered_df.is_cached)

### Debugging

Internally, Spark executes using a Java Virtual Machine (JVM). pySpark runs
Python code in a JVM using Py4J. Py4J enables Python programs running in a
Python interpreter to dynamically access Java objects in a Java Virtual Machine.
Methods are called as if the Java objects resided in the Python interpreter and
Java collections can be accessed through standard Python collection methods.
Py4J also enables Java programs to call back Python objects.
This implies that coding errors often result in a complicated, confusing stack
trace that can be difficult to understand.

Spark's use of lazy evaluation can make debugging more difficult because code is
not always executed immediately.


    def broken_ten(value):
        """
        Incorrect implementation of the ten function
        (the `if` statement checks an undefined variable `val` instead of `value`).
        :param value: a number.
        :return bool: whether `value` is less than 10.
    
        The function references `val`, which is not available in the local or global
        namespace, so a `NameError` is raised.
        """
        return True if (val < 10) else False
    
    bt_udf = udf(broken_ten)
    broken_df = sub_df.filter(bt_udf(sub_df.age) == True)


    # Now we'll see the error
    # Click on the `+` button to expand the error and scroll through the message.
    broken_df.count()

#### Coding style

To make your coding style more readable, enclose the statement in parentheses
and put each method, transformation, or action on a separate line.


    # Final version
    from pyspark.sql.functions import *
    (data_df
     .filter(data_df.age > 20)
     .select(concat(data_df.first_name, lit(' '), dataDF.last_name), dataDF.occupation)
     .show(truncate=False)
     )

### EXERCISE

Create DataFrame containing basic info (last`_`name, first`_`name, ssn, job, age)
about 20000 people.


    # Solution here

Remove column 'ssn'


    # Solution here

Display the number of different jobs


    # Solution here

What is the job of the oldest person?


    # Solution here

Display 10 most frequent first names with numbers of occurrences


    # Solution here

What is the most frequent job for people under 20?


    # Solution here

Display all rare jobs (jobs that occurs only once in our dataset)


    # Solution here

### I/O

We can create DataFrame reading data from file.
> text file: `sqlContext.read.text(file)`

> csv file: `sqlContext.read.csv(file)`

> json file: `sqlContext.read.json(file)`


    filename = "pantadeusz.txt"
    text_df = sqlContext.read.text(filename, encoding="utf-8")
    text_df.show(15, truncate=False)

### EXERCISE

Print 10 most common words in `Pan Tadeusz`.

Note:
- we need first properly transform input data (remove punctuations, trailing and
leading spaces, change to lowercase)


    # Solution here
