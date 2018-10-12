# parser.py
# loads and parses marketcap.csv
import numpy as np


def loadMarketcapYears(path='data/'):
    """
    Loads the marketcap data stored in the marketcap-years.csv file.

    Input:
     path: string, path to folder containing the marketcap.csv file
           in other opearting systems the path may need to use a backslash

    Output:
     ticker: numpy array of strings, company ticker symbol (e.g.: AAPL)
     marketcap: numpy array of integers, market capitalization of
                company in dollars
     years: list of years
    """
    with open(f'{path}marketcap-years.csv', 'r') as csv:
        header = csv.readline().strip().split(',')
        assert len(header) >= 13, \
            "Expected at least 13 columns (ticker, 2007, 2008, ...)"
        data = csv.readlines()  # file is not big, about 4481 lines
    total = len(data)
    ticker = np.zeros(total, dtype='<U10')  # ticker < 10 chars
    marketcap = np.zeros((total, len(header) - 1), dtype='int')
    for i, line in zip(np.arange(total), data):
        split = line.replace('"', '').strip().split(',')
        ticker[i] = split[0]
        marketcap[i, :] = [float(val) if val != '' else 0 for val in split[1:]]
        # if marketcap not available store a 0
    return (ticker, marketcap, header[1:])


def loadMarketcapNames(path='data/'):
    """
    Loads the marketcap data stored in the marketcap.csv file.
    This marketcap file contains the most current market capitalization values
    and the stock tickers.

    Input:
     path: string, path to folder containing the marketcap.csv file

    Output:
     marketcap: numpy array of integers, market capitalization of
                company in dollars for most recent year (2018)
v     name: numpy array of strings, company name (e.g.: Apple Inc)
     ticker: numpy array of strings, company ticker symbol (e.g.: AAPL)
    """
    with open(f'{path}marketcap.csv', 'r') as csv:
        header = csv.readline().split(',')
        assert len(header) >= 3, \
            "Expected at least 3 columns (marketcap, name, ticker)"
        data = csv.readlines()  # file is not big, about 4481 lines
    total = len(data)
    marketcap = np.zeros(total, dtype='int')  # no need to keep cents
    name = np.zeros(total, dtype='<U500')  # name < 500 chars
    ticker = np.zeros(total, dtype='<U10')  # ticker < 10 chars
    for i, line in zip(np.arange(total), data):
        split = line.replace('"', '').strip().split(',')
        marketcap[i] = int(float(split[0]))
        name[i] = split[1]
        ticker[i] = split[2]
    return (marketcap, name, ticker)


def clearNames(name, also_remove=[], base_remove=[' Inc', ' Corp', ' Group']):
    """
    Removes words such as 'Inc', 'Corp' and 'Group' from stock names.

    Input:
     name: numpy array of strings, vector containing company names
     also_remove: list of strings, additional words to remove from names

    Output:
     clean_name: numpy array of strings, vector containing
                 cleaned company names
    """

    remove = [*base_remove, *also_remove]

    def removeFromWord(word):
        for r in remove:
            word = word.replace(r, '')
        return word.strip()

    return np.vectorize(removeFromWord)(name)


# Alert user of library being loaded
print(f'Loaded: stockslexicon/lib/parser.py')
