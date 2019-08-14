## Introduction
This article aims to provide necessary background for the presentation. Many concepts will be repeated in both media, but having read the article, the viewer will gain a better understanding of why the actions performed were needed and how they were performed.

## The Problem
Nordea Bank encountered some troubles, that would later be viewed as the biggest credit risk project in Europe... at least so would they say. The vast amount of data processed for the purposes of the aforementioned credit risk calculation proved to be inadequately handled, Nordea risked fines and reputation loss. This is why the MDP project was initialized.

### Big Data
By very definition the project stemmed from the fact that the bank did not understand handling of so called Big Data, which for the purposes of this topic should be defined as data which is mostly unstructured, varies in sources and formats and it is critically important to handle it securely and precisely.

### Quick Deadline
Approaching deadlines meant that there was no time for fancy tools and processes. The data needed to get ingested into Apache Hadoop data platform sooner rather than later. Many workarounds were designed, such as treating everything that is not easily definable as string. The data was later supposed to be repurposed/transformed, so this did not matter in the given moment.

### Failing Tools
We have hoped to reuse the ingest framework that was created in Nordea. However none of the patterns/generic methods fit. The data was coming in as fixed width files, CSVs, excels, while the framework recognized mostly mainframe format and data coming from databases. The team said they can be ready by the end of the year. This was a no-go - we needed the data inside the systems in matter of weeks, not months.

## The Solution
The solution was to sic loose an Expert IT Developer to do it. The Chosen One was me :-). I cracked my knuckles and began to work on ingesting the data.

### Python
Lo' and behold, Python 3 seemed up to the task. Armed with just Jupyter Notebook, Numpy and Pandas, this language, allowing easy prototyping and fast programming showed its potential in its entirety when parsing the various data sources given to us by the business.

### Apache Hadoop
Apache Hadoop is an ecosystem of tools allowing handling Big Data. It consists of many software solutions, ranging from schedulers, file systems to metadata bases and query engines.

### AWS, Dask
Much earlier there were some plans and POCs regarding usage of various tools improving the performance of the solution. At first we wanted to run it against our Hadoop Cluster - using Dask - but it turned out the cluster availability actually hindered the processes instead of empowering it. We have also checked possibilities of AWS, but then it turned out that cloud services for critical data is a no-go at Nordea Bank.

### Pandas
Turns out that Pandas itself is more then sufficient given a clear purpose and reusable target. It is a well-known library designed for handling data models and structures. They are kept in-memory as a unique object called the Dataframe, which is best described as a minimum viable table. Fortunately, most of the needed formats were already handled by the library, so the only thing needed was in many cases the optimization of input and corner-handling.

### Jupyter Notebook
What was very helpful is the usage of Jupyter Notebook, which will be featured extensively in the presentation. The fast prototyping allowed by Python is taken to another level with this persistence-keeping tool. Jupyter Notebook was designed and developed for use by data scientists. Its main draw is the formatting of code, which accepts normal code and keeps it in "cells". These cells are persistent, and the objects defined in one cell can be reused in another. This allows for decomposition of methods and functions without having to handle data storage, so that instead of storing the parsed data on hard drive (slow) it can be reused easily from memory (maximum fast!).

## Lessons Learnt
* you don't need complex systems to handle even terabytes of data
* Python is perfectly fast for most usages
    * When Python itself is too slow, Numpy/Cython is fast enough
* One developer with great freedom and well-defined requirement can do the work of a big team with chaotically managed backlog

## Sources
[Python](http://www.python.org/)
[Jupyter Notebook](https://jupyter.org/)
[Pandas](https://pandas.pydata.org/)
[Dask](https://dask.org/)
[Big Data](https://en.wikipedia.org/wiki/Big_data)
[Apache Hadoop](https://hadoop.apache.org/)
[Amazon Web Services](https://aws.amazon.com/)
