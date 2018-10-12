# Table of Contents

1.  [Stocks Lexicon](#org61df977)
2.  [Usage](#org05f936b)
3.  [Examples](#org17b6cb9)
4.  [Details](#org945e571)


<a id="org61df977"></a>

# Stocks Lexicon

The idea of this repository is to provide a method to map stock names to market capitalization categories.
Given a stock name, either a ticker symbol or the name of the company, we should be able to recover the firm's market cap.


<a id="org05f936b"></a>

# Usage

First, clone the repository to your project folder:

    cd Project
    git clone https://github.com/Salompas/stockslexicon.git
    # creates a new folder named stockslexicon

The module defines a single class \`Stock\` that has methods to interact with the data. You can import the class directly:

    from stockslexicon.stocks import Stocks
    stocks = Stocks()                # instantiate the class

All methods of the class are documented and can be accessed via \`help(Stocks)\`.


<a id="org17b6cb9"></a>

# Examples

To recover the market size of a firm:

    stocks.size('AAPL')             # market size in 2018 (default)
    stocks.size('AAPL', '2007')       # market size in 2007

To recover the name of a stock given its ticker:

    stocks('AAPL', 'name')          # recovers name of stock with ticker AAPL
    stocks('AAPL', 'legal_name')    # legal name of stock with ticker AAPL

To recover the market capitalization in dollars:

    stocks('AAPL', '2007')          # market cap in dollars on 2007
    stocks('AAPL', '2018')          # market cap in dollars on 2018


<a id="org945e571"></a>

# Details

The market capitalization data covers (almost) all stocks listed in the United States from 2007 to 2018 (inclusive).

The market capitalization is computed at the end of each year, except in 2018 which computes the market capitalization in some date in October (this was when I first collected the data).

The market capitalization when not available for a company in some year is replaced by a zero (0).

There are two names available for each company, a common name (denoted by \`name\`) and its legal name (denoted by \`legal<sub>name</sub>\`). To obtain the common name we take each legal name and remove the words: Inc, Corp and Group.
