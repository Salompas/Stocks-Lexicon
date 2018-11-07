# stockslexicon.py
import os
import numpy as np
from .lib import parser
from fuzzywuzzy import process

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

        # generate helper dictionaries
        self.__build_list_of_names__()  # list of all company names
        self.__build_name_ticker_dict__()  # maps company name to ticker

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
        # Update company names that are better known by other names
        # For example: Alphabet with ticker GOOG is better known as Google
        self.nameToTicker['Google'] = 'GOOG'

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
        except KeyError:
            raise KeyError

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
        return '_'.join(self.contents[ticker]['industry'].split(' '))

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

    def generalizeNameFuzzy(self, name, year='2018'):
        """
        Returns a generalized representation of a company from its
        name. Uses fuzzy search to match company name.
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
        try:
            res = process.extractOne(name, self.allNames)
        except AttributeError:
            self.__build_list_of_names__()
            return self.generalizeNameFuzzy(name, year)
        else:
            if res[1] >= 95:    # scores go from 0 to 100, 95 is the chosen threshold
                return (self.sizeFromName(res[0], year),
                        self.industryFromName(res[0]))
            else:
                raise ValueError

    def findNameInString(self, string):
        """
        Finds name of a company in a string and returns the range of indices
        to get that name.

        Input:
         string: string, contains sequence of words separated by whitespace

        Output:
         result: slice or None, if not None then contains a slice that matches
                 the company name in the original string. That is, if you call
                 string[result] you will get the company name that was found.
        """
        for name in self.allNames:
            if name in string:
                starts_at = string.index(name)
                ends_at = starts_at + len(name)
                return slice(starts_at, ends_at)
        return None

    def generalizeCompany(self, ticker_or_name, year='2018'):
        """
        Generalizes a company name or ticker to its market cap category.

        Intput:
         ticker_or_name: string, contains either a company name or a ticker

        Output:
         result: string or None, if ticker_or_name contains the name or ticker
                 of some company, then returns its market cap and industry categories
        """
        res = None
        try:
            res = '_'.join(self.generalizeTicker(ticker_or_name, year)).upper()
        except KeyError:
            try:
                res = '_'.join(self.generalizeName(ticker_or_name, year)).upper()
            except KeyError:
                pass
        return res

    # def generalizeTickersInString(self, string, year='2018'):
    #     """
    #     Takes a string without company names and generalizes each of its words.
    #     If the word is a ticker symbol,
    #     excluding tickers with a single letter, then it is generalized to the
    #     company market cap and industry categories.
    #     If the word is not a ticker symbol, then it is not modified.
    #     """
    #     parsed = ''
    #     for word in string.split(' '):
    #         # skip single letters
    #         if len(word) != 1:
    #             try:
    #                 parsed += self.generalizeCompany(word, year)
    #             except TypeError:
    #                 parsed += word
    #             finally:
    #                 parsed += ' '
    #     return parsed.strip()


    # def generalizeString(self, string, year='2018'):
    #     """
    #     Parses a string applying the following generalization:
    #     - Stocks-Lexicon: generalize company names to market cap (6 categories)
    #                  (there are about ___ companies which are mapped
    #                   to ___ market cap categories) and industry category

    #     Input:
    #      string: string, a string which may contain the name/ticker of companies
    #      year: string, contains year from which to recover the market cap category

    #     Output:
    #      result: string, contains original string but with company names and tickers
    #              substituted by their respective market cap and industry categories
    #     """
    #     # find company names
    #     indices = self.findNameInString(string)
    #     # if there are no company names, then generalize tickers
    #     if indices == None:
    #         return self.generalizeTickersInString(string, year)
    #     else:                       # there is a company name in the string
    #         company = self.generalizeCompany(string[indices], year)
    #         # get substrings around the company name
    #         before = string[:indices.start]
    #         after = string[indices.stop:]
    #         if len(before) == 0 and len(after) == 0:
    #             return f'{company}'
    #         elif len(before) == 0 and len(after) != 0:
    #             after_parsed = self.generalizeString(after, year)
    #             return f'{company} {after_parsed}'
    #         elif len(before) != 0 and len(after) == 0:
    #             before_parsed = self.generalizeString(before, year)
    #             return f'{before_parsed} {company}'
    #         elif len(before) != 0 and len(after) != 0:
    #             before_parsed = self.generalizeString(before, year)
    #             after_parsed = self.generalizeString(after, year)
    #             return f'{before_parsed} {company} {after_parsed}'
