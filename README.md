# value-determination
Determine the value of companies using comparative analysis
# Setting up a standalone Spark cluster
Download [Apache Spark 2.3.0](https://spark.apache.org/downloads.html).
Extract on each host. Go to the extracted directrory.
Set SPARK\_HOME:
```
export SPARK_HOME=$PWD
```
On a host designated to be master:
```
$SPARK_HOME/sbin/start-master.sh
```
On hosts designated to be slaves
(Master must be a URL of the form spark://hostname:port):
```
$SPARK_HOME/sbin/start-slave.sh <master>
```
A slave process can also run on the same host as master.
# Dependencies
```
pip install pyspark numpy pandas sklearn scipy
```
# Usage
```
$SPARK_HOME/bin/spark-submit --py-files analysis.py value_determination.py files/*.csv
```
