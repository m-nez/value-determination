import pandas


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

    # Calculation of Price to Earnings multiple
    df['P2E'] = df['Kurs'] * df['Ilość akcji'] / df['Zysk netto']

    # Calculation of P2E basis statics
    df['Max_P2E'] = df['P2E'][1:,].max()
    df['Min_P2E'] = df['P2E'][1:,].min()
    df['Median_P2E'] = df['P2E'][1:,].sort_values().median()
    df['Mean_P2E'] = df['P2E'][1:,].mean()

    # # If added Book Value per share multiple
    # df['BV'] = df['BV2S'] * df['Ilość akcji']
    # df['P2BV'] = df['Kurs'] * df['BV']
    #
    # # Calculation of P2E basis statics
    # df['Max_P2BV'] = df['P2BV'][1:,].max()
    # df['Min_P2BV'] = df['P2BV'][1:,].min()
    # df['Median_P2BV'] = df['P2BV'][1,:].sort_values().median()
    # df['Mean_P2BV'] = df['P2BV'][1:,].mean()

    return df


def exponential_smoothing(series, alpha):

    series_rev = list(reversed(series))
    result = [series_rev[0]] # first value is same as series
    for n in range(1,len(series_rev)):
        result.append(alpha*series_rev[n] + (1-alpha) * result[n-1])

    return list(reversed(result))


def esmooth_df(df, label, minrows, jtr = 0, alpha = 0.9):

    series = df[0][jtr][label]
    for itr in range(1, minrows):
        series = pandas.concat([series, df[itr][jtr][label]], axis = 1)

    series = series.apply(lambda x : exponential_smoothing(x, alpha))

    return series


# firmNamesList, stockList, predictionList must have the same len
# stockList should have lists of stockValuesList (double market values of quarters)
# predictionList should have lists of predictionValuesList (double prediction values of quarters)
# So summing up also lists within lists should have the same len
def summarise(firmNamesList, stockList, predictionList):
    print(firmNamesList, stockList, predictionList)
