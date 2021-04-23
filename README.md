## About

This file was written to aid in a literature review on the funding in digitial clinical health measures. 

The purpose of this program is to parse through the test of the pubmed '.txt' file to
1) create a new csv file that includes author affiliation to be used in the first round of voting
2) edit a pubmed '.csv' file to filter out articles that did not meet the following criteria
      1) at least 50% US Based
      2) at least 1 (one) US Based Academic author 
      3) does not have the word 'Review' in the title of articles
Any articles without these characteristics are removed.

It is currently in a pretty early stage and is not hugely friendly to use, but can be done as follows. 

## How to Use

1. Clone the repo to a local folder which houses your pubmed .txt search file  
2. On line 172, change the `filepath = 'pubmed.txt'` to whatever the filepath of your .txt file is
3. On line 227, change the `with open('pubmed.csv', 'r') as readFile:` to whatever the filepath of your .txt file is
4. If you want on lines 238 and 263, you can change the names of the files created and put in the current directory. 
5. In the terminal run in the directory that houses the repo and the relevant pubmed files run: `python3 pubmed_author_filtering.py`

## Next Steps

There are number of changes that will be made in the coming weeks to make it more friendly for users and more efficient. Please feel free to submit
pull requests and reach out to kryan717@gmail.com with any thoughts/questions/concerns. Thanks!
