
## Purpose

10-K filings  are rich sources of data about a firm's financial health, strategy, and risk factors. However, due to their length and complexity, investors may not fully process all the nuanced information they contain. The "Lazy Prices" paper, which this code closely aligns with, posits that changes in the language used in these filings can signal important shifts in a company's prospects. The authors demonstrate that these textual changes have predictive power for future stock returns, suggesting that the market underreacts to this information initially.

To empirically investigate this theory, this repo is designed to contain code that performs the following key tasks. 
- Data Acquisition and Loading: The first step is to gather all the 10-K filings to analyse. There's three ways to go about this:
        - One could fetch the documents from  50GB process begins with accessing and loading the Loughran-McDonald 10-K Document Dictionaries file. This massive 15.8GB text file contains pre-calculated word counts for each word in the LM dictionary for every 10-K filing in the dataset.
  10-Ks for 2022 for 498 of these firms using sec Edgar downloader. 