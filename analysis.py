def reweight(df):
    """
    Multiply columns by scalar to modify their influence on the distance
    """
    return df

def analyse(df):
    return 1


# firmNamesList, stockList, predictionList must have the same len
# stockList should have lists of stockValuesList (double market values of quarters)
# predictionList should have lists of predictionValuesList (double prediction values of quarters)
# So summing up also lists within lists should have the same len
def summarise(firmNamesList, stockList, predictionList):
    print(firmNamesList, stockList, predictionList)
