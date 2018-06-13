def reweight(df):
    """
    Multiply columns by scalar to modify their influence on the distance

    df : pandas.DataFrame
    """
    return df

def analyse(df):
    """
    Return the predicted true share price

    df : pandas.DataFrame
        First row contains the values for the target company
        which share price is to be predicted.
        Other rows contain values for companies
        which are similar to the targe company.

        df["Kurs"][0] is the share price of the target company
    """
    return 1


# firmNamesList, stockList, predictionList must have the same len
# stockList should have lists of stockValuesList (double market values of quarters)
# predictionList should have lists of predictionValuesList (double prediction values of quarters)
# So summing up also lists within lists should have the same len
def summarise(firmNamesList, stockList, predictionList):
    print(firmNamesList, stockList, predictionList)
