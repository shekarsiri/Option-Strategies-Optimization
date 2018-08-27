# Option-Strategies-Optimization

This software is intended to be used for optimization of strategies involving the financial derivative asset known as option.
For a quick intro to options please refer to: https://www.optionsplaybook.com/option-strategies/

This Option Strategy Optimizer is currently compatible with the data format distributed by the free delayed quotes from CBOE.
Go to http://www.cboe.com/delayedquote/quote-table-download

How to use:
1. Download a table with the options data from the link above
2. Go to the folder where you saved the OSO software files and paste the downloaded table with the name “quotedata”. 
Make sure the format extension is .dat
3. Open quotedata.dat in notepad++ and replace all spaces with commas (windows: ctrl+h replace all) and save it
4. Run ExecutableModule.py and check if the table was successfully loaded
