import re
import csv

# purpose of this program is to parse through the test of the pubmed '.txt' file to
# 1) create a csv file that includes author affiliation to be used in the first round of voting
# 2) to filter out articles that did not meet the following criteria
#       a) at least 50% US Based
#       b) at least 1 (one) US Based Academic author
#
# created February 28th, 2021 for the Big Ideas Lab
# by Kyle Ryan @kryan717 on Github

# used the following as reference when creating regex dictionary and parsing functions:https://www.vipinajayakumar.com/parsing-text-with-python/#string 

# this function identified if a given author had an affiliation in the USA
# returning a Boolean value
def is_USA(fau, info):
    for affiliation in info[fau]:
        # affiliation had a list of the affiliations of a given author (fau)
        if re.search('USA', affiliation, re.IGNORECASE):
            return True
    
    return False


# this function identified if a given author was based in academia
# returning a Boolean value
def is_college(fau, info):
    for affiliation in info[fau]:
        # affiliation had a list of the affiliations of a given author (fau)
        if re.search('college', affiliation, re.IGNORECASE)  or re.search('university', affiliation, re.IGNORECASE) or re.search('school', affiliation, re.IGNORECASE) or re.search('institute', affiliation, re.IGNORECASE) or re.search('society', affiliation, re.IGNORECASE):
            return True
    
    return False


# this dictionary created regex expressions that would be used to identify relevant parts of the 'txt' file
# fau gave full author name, others are self explanatory
dict = { 
    'pmid': re.compile(r'PMID- (?P<pmid>.*)\n'),
    'fau': re.compile(r'FAU - (?P<fau>.*)\n'),
    'affiliation': re.compile(r'AD  - (?P<affiliation>.*)'),
    'title': re.compile(r'TI  - (?P<title>.*)') 

}

# this function came largely from the above reference and used the dictionary to parse an inputted line
# returning the relevant key and the found information
def _parse(line):
    for key, rx in dict.items():
        found = rx.search(line)
        if found: 
            return key, found
        
    return None, None

# this function parsed through a given file and returns then a dictionary and a list    
# the dictionary, info, contained information that related the pmid to the author and affiliation
# the list contained all the titles found in the .txt that are reviews
def parse_search(filepath):
    # initializing necessary variables
    info = {}
    titles_w_review = list()
    pmid = ''
    fau = ''

    # this allows the relevant csv file to be read as an object and parsed
    with open(filepath, 'r') as file_object:
        line = file_object.readline()

        # goes through each line
        while line:
            # calls the line parsing function above
            key, found = _parse(line)

            ### for each of the following if statements, the relevant key determines the data placement in the dictionary
            
            if key == 'pmid':
                pmid = found.group('pmid')
                # the pmid sets up a new dictionary to hold information about its article
                info[pmid] = {}

            if key == 'title':
                title = found.group('title')
                # this adds the pmid of a title if it has review in it
                # there is an obvious error here: the search will not be comprehensive as lowercase isn't used and its inconsistent as regex isn't used
                # however, any titles missed will be screened in the voting, so the error is not of huge concern
                if(title.find('Review') != -1):
                    titles_w_review.append(pmid)

            if key == 'fau':
                fau = found.group('fau')
                # the nested dictionary at the place of the author name creates a list so all affiliations can be added
                info[pmid][fau] = list()

            if key == 'affiliation':
                affiliation = found.group('affiliation')
                line = file_object.readline() 
                # the following line statement leverages the knowledge of the .txt file to include affiliation information that may be multi-line
                while line[0] == ' ':
                    affiliation = affiliation + line 
                    line = file_object.readline() 
                # once the complete affiliation is compiled, it is added to the list
                info[pmid][fau].append(affiliation)
            else:
                # this ensures that if this is not an affiliation line, the parser continues smoothly to the next line
                line = file_object.readline()

    # returns aforementioned dictionary and list
    return info, titles_w_review


# this function creates a csv from the inputted rows and with the given name, it returns nothing
def make_csv(rows, name):
      with open(name, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(rows)   

# this is the main function which goes through the list, filters out articles based on above criteria 
# then, makes a csv for use in next round of lit review
if __name__ == '__main__':
    # initiatilizes relevant variables
    # pmid_USAled will nclude the pmid's of articles that meet the 50% USA led criteria
    pmid_USAled = list()
    # pmid_USAled includes the pmid's of articles that meet the 50% USA led criteria
    pmid_non_USAled_or_no_US_academic = list()
    # pmid_auth_aff is a dictionary with the pmid values as keys and holding a list of author followed by affiliation for each author
    pmid_auth_aff = {}


    # local filepath of .txt file
    filepath = 'pubmed.txt'


    # this parses the full file and sets relevant information to the variables that will be used
    info, titles_w_review = parse_search(filepath)
 


    # this for loop goes through each pmid and decides if the criteria are met, adding to relevant lists accordingly
    for pmid in info.keys():
        # initializing
        # this is the total number of authors for given pmid
        count = 0
        # this is the total number of US authors for given pmid
        usa_count = 0
        # this is a boolean to see if a given pmid has a US based academic author
        one_college_USA = False
        # creates list in the dictionary
        pmid_auth_aff[pmid] = list()

        # goes through each author in nested dictionary
        for author in info[pmid]:

            # this add the author and all affiliations to a new list
            pmid_auth_aff[pmid].append(author)
            pmid_auth_aff[pmid].append(info[pmid][author])


            # this checks first if an author is US based
            if is_USA(author, info[pmid]):
                # if yes, adds to US count
                usa_count = usa_count+1
                # then checks if the author is an academic
                if is_college(author, info[pmid]):
                    # if yes, boolean turns to True
                    one_college_USA = True
                # count still added to overall # of authors
                count = count + 1
            else:
                # if not US, count still added
                count = count + 1
        
        # checks if the # of US authors is greater than half and ensures one is US based
        if usa_count * 2 >= count and one_college_USA: 
            # if yes, pmid added to USAled
            pmid_USAled.append(pmid)
        else:
            # if no, pmid added to non USAled
            pmid_non_USAled_or_no_US_academic.append(pmid)


    # lines will be the final list of rows made into a new csv
    lines = list()

    # the pubmed.csv file allows us to use the information we've gathered to quickly create a new csv w/ only files that are USA led w/ at least 1 US academic
    with open('pubmed.csv', 'r') as readFile:
        reader = csv.reader(readFile)

        for line in reader:
            # this replaces the authors box with the authors and their affiliation to the pubmed.csv
            # this removes the lines that are not US led or don't have 
            if line[0] not in pmid_non_USAled_or_no_US_academic and line[0] not in titles_w_review:
                # this adds the edited line to the final list of rows
                lines.append(line)  

    # this creates the new csv to be used in the next round and is filtered for the authors which are USA led and have at least one academic
    make_csv(lines, 'pubmed_filtered_full.csv')



    # this creates a cleaner csv file with only: pmid, authors and their affiliations seperated but without additional information from the .csv file
    # the purpose of this file was more about checking for accuracy that any continued functional use
    lines_cleaned = list()
    current_row = 0
    # goes through each pmid
       for pmid in pmid_USAled:
        # if statement maintains same pmid's accepted as above
        if pmid not in pmid_non_USAled_or_no_US_academic and pmid not in titles_w_review:
            # adds pmid by itself in a list
            lines_cleaned.append([pmid])
            # goes through each author
            for author in info[pmid]:
                # adds the author
                lines_cleaned[current_row].append(author) 
                # adds the list of the authors affiliations
                for affiliation in info[pmid][author]:
                    lines_cleaned[current_row].append(affiliation)
            # keeps track of row
            current_row = current_row + 1

    # makes the csv
    make_csv(lines_cleaned, 'pubmed_filtered_limited.csv')
