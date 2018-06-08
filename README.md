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

pip install dash==0.21.1
pip install dash-renderer==0.13.0
pip install dash-html-components==0.11.0
pip install dash-core-components==0.23.0
pip install plotly --upgrade
```
# Usage
```
$SPARK_HOME/bin/spark-submit --py-files analysis.py value_determination.py files/*.csv
```
