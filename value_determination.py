import pandas
import numpy
import argparse
from scipy.spatial import KDTree
from sklearn.preprocessing import minmax_scale
from pyspark.sql import SparkSession
from pyspark import SparkContext
#import matplotlib.pyplot as plt
from analysis import analyse, reweight, summarise, esmooth_df


def task(quarter, k):
    """
    quarter : pandas.DataFrame
    k : int
    """
    quarter_normalized = pandas.DataFrame(
            minmax_scale(quarter.values.astype(numpy.float64)),
            columns=quarter.columns)
    quarter_normalized = reweight(quarter_normalized)
    points = quarter_normalized.values
    kdtree = KDTree(points)
    dist, ind = kdtree.query(points, k=k+1)
    dist = dist[:,1:]
    ind = ind[:,1:]

    results = []
    for main_i, indices in enumerate(ind):
        indices = numpy.append([main_i], indices)
        knearest = pandas.DataFrame(
                quarter.values[indices],
                columns=quarter.columns)

        results.append(analyse(knearest))

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="csv files with company data")
    parser.add_argument("-m", "--master", default="local")
    parser.add_argument("-k", default=5, help="k nearest companies to take for analysis")

    args = parser.parse_args()

    sc = SparkContext(
            master=args.master,
            appName="ValeDetermination")
    sc.setLogLevel("ERROR")
    spark = SparkSession(sc)

    csvs = {}
    for f in args.files:
        csvs[f] = pandas.read_csv(f)

    keys = list(csvs.keys())
    values = list(csvs.values())
    counts = [len(df) for df in values]
    argmin = numpy.argmin(counts)
    minrows = counts[argmin]

    quarters = []
    for i in range(1, minrows + 1):
        quarters.append(pandas.concat([df.iloc[-i, 1:] for df in values], axis=1).T)

    quartersRDD = sc.parallelize(quarters)
    results = quartersRDD.map(lambda x : task(x, int(args.k))).collect()

    # Exponential smoothing
    series = list()
    for itr in range(len(results[0])):
        series.append(esmooth_df(results, 'Median_P2E', minrows, itr, 0.9))

        # Exact valuation
        results[itr][0]['Median_P2E'] = series[itr].iloc[0,0]
        results[itr][0]['Kurs'] = results[itr][0]['Median_P2E'] * results[itr][0]['Zysk netto'] / results[itr][0]['Ilość akcji']

    summarise(results)

    spark.stop()
