# value-determination
Determine the value of companies using comparative analysis
# Setting up a standalone Spark cluster
Download [Apache Spark 2.3.0](https://spark.apache.org/downloads.html).
Extract on each host. Go to the extracted directrory.
On a host designated to be master:
```
./sbin/start-master.sh
```
On hosts designated to be slaves
(Master must be a URL of the form spark://hostname:port):
```
./sbin/start-slave.sh <master>
```
A slave process can also run on the same host as master.
# Dependencies
```
pip install pyspark
```
# Usage
```
./bin/spark-submit value_determination.py [-m MASTER] files [files ...]
```
