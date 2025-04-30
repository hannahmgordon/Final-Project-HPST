
## Purpose

The readme should contain a link to the website built off this analysis

The code used to scrape and download data (and if you click-and-download anything, a link to the source) can be separate files, and the code used to load, clean, merge, and explore the data.
The code used to do the analysis

Your presentation file needs to be in this repo. If you use google slides, you should include them as a PDF in this folder / put a link to the slides in the readme.

Visit our website, which showcases: 

10-K filings  are rich sources of data about a firm's financial health, strategy, and risk factors. However, due to their length and complexity, investors may not fully process all the nuanced information they contain. The "Lazy Prices" paper, which this code closely aligns with, posits that changes in the language used in these filings can signal important shifts in a company's prospects. The authors demonstrate that these textual changes have predictive power for future stock returns, suggesting that the market underreacts to this information initially.

To empirically investigate this theory, this repo is designed to contain code that performs textual analysis tasks on the 10-K files from 1993 to 2024 for the S&P 500 firms.

- Data Acquisition and Loading: The first step is to gather all the 10-K filings to analyse. There's three ways to go about this:

    - One could fetch the documents using the SEC EDGAR downloader.  This method provides the most direct access to the original data but requires significant amount of time to process, clean and prepare the text for analysis.
    - One can also download a giant 50 GB folder of all 10-X files in a zipped format. The raw text files are cleaned by removing non-textual data, structural markup, and irrelevant headers/footers to isolate the textual content for analysis.
    - Alternatively, one can also use the Loughran-McDonald 10-K Document Dictionaries file. This 15.8GB (unzipped) text file contains pre-calculated word counts for each word in the LM dictionary for every 10-K filing in the dataset. This was the quickest option, and we decided to use it. 


- Now that the data is prepared, for the actual textual analysis, we determined it would be best to utilise the cosine similarity to measure the changes in the texts. 