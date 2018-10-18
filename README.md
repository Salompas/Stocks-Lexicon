# Table of Contents

1.  [Stocks Lexicon](#orgba5781f)
2.  [Installation](#orgd7d9b1b)
3.  [Examples](#org8c47d49)
4.  [Details](#org272ba67)


<a id="orgba5781f"></a>

# Stocks Lexicon

The main idea for this project is to provide a way to generalize a company's name/ticker to its size (market cap) and industry category.
This repository provides methods that map a stock's name/ticker to its market capitalization and its industry category.
The market capitalization of a company is categorized depending on how big the company is.
The market cap categories and industry categories are listed below:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Market Capitalization (in US$)</th>
<th scope="col" class="org-left">Category</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">Less than $50 million</td>
<td class="org-left">Nano</td>
</tr>


<tr>
<td class="org-left">Between $50 million and $300 million &nbsp;</td>
<td class="org-left">Micro</td>
</tr>


<tr>
<td class="org-left">Between $300 million and $2 billion</td>
<td class="org-left">Small</td>
</tr>


<tr>
<td class="org-left">Between $2 billion and $10 billion</td>
<td class="org-left">Mid</td>
</tr>


<tr>
<td class="org-left">Between $10 billion and $200 billion</td>
<td class="org-left">Large</td>
</tr>


<tr>
<td class="org-left">Grater than $200 billion</td>
<td class="org-left">Mega</td>
</tr>
</tbody>
</table>

<br/>

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Industry Categories</th>
<th scope="col" class="org-left">&#xa0;</th>
<th scope="col" class="org-left">&#xa0;</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">Automotive</td>
<td class="org-left">Consumer Durables &nbsp;</td>
<td class="org-left">Food & Beverage</td>
</tr>


<tr>
<td class="org-left">Material & Construction &nbsp;</td>
<td class="org-left">Insurance</td>
<td class="org-left">Banking</td>
</tr>


<tr>
<td class="org-left">Wholesale</td>
<td class="org-left">Metals & Mining</td>
<td class="org-left">Computer Software & Services</td>
</tr>


<tr>
<td class="org-left">Chemicals</td>
<td class="org-left">Leisure</td>
<td class="org-left">Transportation</td>
</tr>


<tr>
<td class="org-left">Telecommunications</td>
<td class="org-left">Media</td>
<td class="org-left">Electronics</td>
</tr>


<tr>
<td class="org-left">Health Services</td>
<td class="org-left">Utilities</td>
<td class="org-left">Tobacco</td>
</tr>


<tr>
<td class="org-left">Financial Services</td>
<td class="org-left">Diversified Services</td>
<td class="org-left">Internet</td>
</tr>


<tr>
<td class="org-left">Retail</td>
<td class="org-left">Specialty Retail</td>
<td class="org-left">Conglomerates</td>
</tr>


<tr>
<td class="org-left">Computer Hardware</td>
<td class="org-left">Aerospace/Defense</td>
<td class="org-left">Real Estate</td>
</tr>


<tr>
<td class="org-left">Drugs</td>
<td class="org-left">Energy</td>
<td class="org-left">Consumer NonDurables</td>
</tr>


<tr>
<td class="org-left">Manufacturing</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">Empty String (none available)</td>
</tr>
</tbody>
</table>


<a id="orgd7d9b1b"></a>

# Installation

First, clone the repository to your project folder:

    cd Project
    git clone https://github.com/Salompas/stockslexicon.git
    # creates a new folder named stockslexicon

The module defines a single class \`Stock\` that has methods to interact with the data. You can import the class directly:

    from stockslexicon.stocks import Stocks
    stocks = Stocks()                # instantiate the class

All methods of the class are documented and can be accessed via \`help(Stocks)\`.


<a id="org8c47d49"></a>

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

To recover the company's industry category:

    stocks.industry('AAPL')         # industry category for AAPL
    stocks.industryFromName('Apple')  # industry category for Apple

To generalize a company's name or ticker:

    stocks.generalizeTicker('GOOG', '2007')  # ('Large', 'Internet')
    stocks.generalizeName('Alphabet', 2018)  # ('Mega', 'Internet')


<a id="org272ba67"></a>

# Details

The market capitalization data covers (almost) all stocks listed in the United States from 2007 to 2018 (inclusive).

For a stock to be covered, it has to be available in 2018. If the company went bankrupt in 2017, then the company's stock will not show up in the data. If a stock that is available in 2018 (in October to be precise) and is not in the data, then it is most likely the result of a bug (please report it).

The market capitalization is computed at the end of each year, except in 2018 which computes the market capitalization in some date in October (this was when I first collected the data).

The market capitalization when not available for a company in some year is replaced by a zero (0).

There are two names available for each company, a common name (denoted by \`name\`) and its legal name (denoted by \`legal<sub>name</sub>\`). To obtain the common name we take each legal name and remove the words: Inc, Corp and Group.

The industry categories are not always available (for about 150 stocks). This happens for exchange traded funds (ETFs), over-the-counter contracts (OTCs) and some other stocks. When a category is not available an empty string is returned instead.
