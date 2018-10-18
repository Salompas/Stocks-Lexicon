# stockslexicon.py
import os
import numpy as np
from .lib import parser

# obtain path to data folder
_DATA_FOLDER = f'{__file__[:-9]}/data/'

# Check if original data is in place
assert 'marketcap.csv' in os.listdir(_DATA_FOLDER), \
    "Expected marketcap.csv in data/ folder"


class Stocks:
    def __init__(self):
        """
        Populates the contents with market cap values per year and industry
        categories for all companies with data available in the
        file marketcap-years.csv.
        """

        # Load all ticker symbols and names available in 2018
        name = parser.loadCompanyNames(_DATA_FOLDER)

        # Load map between ticker and industry category in 2018
        industry = parser.loadIndustryCategories(_DATA_FOLDER)

        # Load market cap data for the 2007-2018 period
        (ticker, marketcap, year) = parser.loadMarketcapYears(_DATA_FOLDER)

        # Create dictionary to map ticker to contents:
        # - Market cap per year
        # - Company legal name
        # - Company name optimized for search
        # - Company industry category
        self.contents = dict.fromkeys(ticker)
        for i in np.arange(len(ticker)):
            legalName = name[ticker[i]]
            clearName = str(parser.clearNames(legalName))
            try:
                industryCategory = industry[ticker[i]]
            except KeyError:
                industryCategory = ''  # not available
            self.contents[ticker[i]] = dict(
                zip(year, marketcap[i, :]),
                legal_name=legalName,
                name=clearName,
                industry=industryCategory
            )

        # Store number of stocks, years and range of the data
        self.total_tickers = len(ticker)
        self.total_years = len(year)
        self.year_start = int(year[0])
        self.year_end = int(year[-1])
        self.range_years = range(self.year_start, self.year_end + 1)

    def __repr__(self):
        return '\n'.join((f'Stocks',
                          f'Total Tickers: {self.total_tickers}',
                          f'Data Range: {str(self.range_years)}'))

    def __call__(self, ticker, field=''):
        """
        Calling the class with a ticker symbol returns the
        information about the company.
        If an additional field is supplied, like a year, then the specific
        information stored in that field is returned.

        Examples:
         self('AAPL') returns a dictionary containing Apple's marketcap
                      values over the years, the company's name and its
                      legal name
         self('AAPL', 'name') returns the company's name
         self('AAPL', '2007') returns the company's marketcap in 2007
        """
        if field == '':
            for key in self.contents[ticker]:
                print(f'{key}: {self.contents[ticker][key]}')
        else:
            return self.contents[ticker][field]

    def __build_name_ticker_dict__(self):
        """
        Constructs a map between company names to company tickers.
        """
        self.nameToTicker = {v['name']: k for k, v in self.contents.items()}

    def __build_list_of_names__(self):
        """
        Constructs a list of all company names available.
        """
        self.allNames = np.array(
            [self(k, 'name') for k in self.contents.keys()], dtype='<U500')

    @staticmethod
    def categorizeMarketcap(marketcap):
        """
        Categorizes the market capitalization into the following categories:
        - Nano:                 market cap < 50 million
        - Micro: 50  million <= market cap < 300 million
        - Small: 300 million <= market cap < 2   billion
        - Mid:   2   billion <= market cap < 10  billion
        - Large: 10  billion <= market cap < 200 billion
        - Mega:  200 billion <= market cap

        Input:
         marketcap: numpy array of ints, contains market
                    capitalizations in dollars

        Output:
         categories: numpy array of strings, contains market capitalization
                     separated by categories
        """
        boundary = np.array([50, 300, 2000, 10000, 200000])*1000000
        categories = np.array(['Nano', 'Micro', 'Small',
                               'Mid', 'Large', 'Mega'])

        def categorize(value):
            i = len(categories) - 1
            for bound in boundary:
                if value < bound:
                    i -= 1
            return categories[i]

        return np.vectorize(categorize)(marketcap)

    def size(self, ticker, year='2018'):
        """
        Returns the categorized market capitalization of a company at a
        given year (2018 is default year).
        See the method categorizeMarketcap for the categories.

        Input:
         ticker: string, ticker symbol of company (e.g.: 'AAPL')
         year: string, year for the company size

        Output:
         size: string, categorized market cap of the company on a given year
               see self.categorizeMarketcap help for categories
        """
        return str(self.categorizeMarketcap(self(ticker, str(year))))

    def tickerFromName(self, name):
        """
        Returns the company ticker given its cleared name.

        Input:
         name: string, company cleared name (e.g.: 'Apple')

        Output:
         ticker: string, company ticker symbol (e.g.: 'APPL')
        """
        try:
            return self.nameToTicker[name]
        except AttributeError:
            self.__build_name_ticker_dict__()
            return self.tickerFromName(name)

    def sizeFromName(self, name, year='2018'):
        """
        Returns the categorized market capitailization of a company at
        a given year. Takes name of the company instead of ticker symbol.

        Input:
         ticker: string, ticker symbol of company (e.g.: 'AAPL')
         year: string, year for the company size

        Output:
         size: string, categorized market cap of the company on a given year
               see self.categorizeMarketcap help for categories
        """
        return self.size(self.tickerFromName(name), year)

    def listAllNames(self):
        """
        Returns a list containing all company names.

        Output:
         allNames: numpy array of strings, contains the name of all companies
        """
        try:
            return self.allNames
        except AttributeError:
            self.__build_list_of_names__()
            return self.allNames

    def industry(self, ticker):
        """
        Returns the company's industry category.

        The possible categories are:
        - Automotive
        - Consumer Durables
        - Food & Beverage
        - Material & Construction
        - Insurance
        - Banking
        - Wholesale
        - Metals & Mining
        - Computer Software & Services
        - Chemicals
        - Leisure
        - Transportation
        - Telecommunications
        - Media
        - Electronics
        - Health Services
        - Utilities
        - Tobacco
        - Financial Services
        - Diversified Services
        - Internet
        - Retail
        - Specialty Retail
        - Conglomerates
        - Computer Hardware
        - Aerospace/Defense
        - Real Estate
        - Drugs
        - Energy
        - Consumer NonDurables
        - Manufacturing
        - Empty String (''): no category is available (ETFs for example)

        Input:
         ticker: string, company ticker symbol

        Output:
         industry: string, industry category
        """
        return self.contents[ticker]['industry']

    def industryFromName(self, name):
        """
        Returns a company's industry category from its name as
        opposed to from its ticker symbol.

        See Stocks.industry for industry categories.
        """
        return self.industry(self.tickerFromName(name))

    def generalizeTicker(self, ticker, year='2018'):
        """
        Returns a generalized representation of a company from its
        ticker symbol.
        The representation generalizes the company to:
        - Company size: market cap category
                        (see Stocks.categorizeMarketcap for categories)
        - Company industry: industry category
                        (see Stocks.industry for categories)

        Input:
         ticker: string, ticker symbol of a company (e.g.: 'AAPL')
         year: string or int, year of the market cap

        Output:
         res: tuple, first element is the company size and the
              second is the company industry
        """
        return (self.size(ticker, str(year)), self.industry(ticker))

    def generalizeName(self, name, year='2018'):
        """
        Returns a generalized representation of a company from its
        name.
        The representation generalizes the company to:
        - Company size: market cap category
                        (see Stocks.categorizeMarketcap for categories)
        - Company industry: industry category
                        (see Stocks.industry for categories)

        Input:
         ticker: string, company name (e.g.: 'Apple')
         year: string or int, year of the market cap

        Output:
         res: tuple, first element is the company size and the
              second is the company industry
        """
        return (self.sizeFromName(name, year), self.industryFromName(name))
