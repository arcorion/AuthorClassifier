#The idea is to make a Naive Bayes model for text categorized by author.
#Each author will have a lexicon that maps the token to its frequency
# in texts by that author.
#These will be smoothed using some algorithm (probably Laplace Smoothing)

#The model will probably be a numpy table,
# with one axis for authors and another for tokens.

#This script will simply build the model from a corpus:
#It first gathers every unique token, then adds an UNK token, to a lexicon
#Then, for each author, it finds the Laplace-Smoothed probability
# that the word appears, given the author
#After sorting everything, the model is ready to go.

#The output consists of three matrices:
# Column labels: The list authors
# Row labels: The list of tokens in order of encounter
# Frequency table: The fequencies

#The procedure:
# Initialize frequency table as 1-by-1: first row is "UNK"
# For each work:
#  Separate the author and the text
#  If the author is not yet represented, add a column of zeroes for them and add their name to the list
#  Iterate through text. For each token:
#  If token is not represented, add a new row of zeroes for them and add it to the list
#  Add 1 to token count in the table, both under the "all" column and under the author's column
#   Better yet: just start each new row/col as being full of ones.
# Turn the totals into Laplace-Smoothed Frequencies
#  This is accomplished by adding 1 to each count before taking frequencies

import numpy,os,gutenberg,re
from gutenberg.query import get_metadata

def main():
    #Part 1: Initialize everything

    #Tries to make a "model" directory, fails gracefully if it already exists
    #Copied from Christopher's portion of the code
    try:
        os.mkdir("model")
    except:
        print("The \"model\" folder already exists, skipping...")

    #Make the initial 1-by-1 array
    counts = numpy.ones((1,1))
    #Initialize the vector of terms that labels the rows.
    terms = ['<UNK>']
    #Initialize the vector of authors that labels the columns.
    authors = []
    #Optional: add something that keeps track of how many works by a given author are being analyzed
    # and pass it as an argument of make_model

    ownDir, path = get_texts_dir()

    #Part 2: Make the table of counts, as well as the lists of terms and authors
    counts, terms, authors = make_model(counts, terms, authors, path)

    #Assorted debug lines
    #print('Authors:\n', authors)
    #print('Terms:\n', terms)
    #no_blowup()

    #Part 3: find the columnwise probabilities for each term
    countsPerAuthor = numpy.sum(counts, axis = 0)
    smoothFreqs = counts / countsPerAuthor

    #Epic 3-Part Finale: Save every item, each in its own CSV
    os.chdir(ownDir + '/model')
    #Finale Part 1: save the list of words
    numpy.savetxt("terms.csv", terms, delimiter =", ", fmt ='% s')
    #Finale Part 2: save the list of authors
    numpy.savetxt("authors.csv", authors, delimiter =", ", fmt ='% s')
    #Finale Part 3: save the frequencies
    numpy.savetxt("freqs.csv", smoothFreqs, delimiter =", ", fmt ='% s')

#Returns texts directory if it exists
#Raises an exception otherwise
def get_texts_dir():
    ownDir = os.getcwd()
    path = ownDir + '/texts/'
    if not os.path.isdir(path):
        raise Exception("Texts directory does not exist. Run author.py in this directory.")
    return ownDir, path

#Makes the model, operating in multiple parts
def make_model(counts, terms, authors, path):

    #Part 1: Get list of subfolders of /texts
    # Taken from https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
    listAuthorFolders = [f.path for f in os.scandir(path) if f.is_dir()]

    #Part 2: Iterate through each folder and build the model
    currentColumn = 0
    for authorFolder in listAuthorFolders:
        #Part 2.1: Get the name of the author, and add a column if necessary
        author = get_author(authorFolder)
        #Debug line: print the author folder directory
        #print(authorFolder)
        #Debug line: print author's name
        print('Reading texts by: ', author)
        authors.append(author)
        
        #Add a column of ones if currentColumn > 0
        if currentColumn > 0:
            newCol = numpy.ones((counts.shape[0], 1))
            #Debug line: print the new column
            #print("newCol: ", newCol)
            counts = numpy.concatenate((counts, newCol), 1)

        #Part 2.2: analyze the texts
        for title in os.listdir(authorFolder):
            #Part 2.2.1: Get the text in readable file form
            textPath = authorFolder + '/' + title
            #Debug line: print the name of the text
            print('Now reading: ', title)
            #Debug line: make sure the formatting is right
            #print(textPath)

            #Part 2.2.2: get the text as a read-only file
            #This video really saved me on this part:
            # https://www.youtube.com/watch?v=yC2y4tOdF0g
            file = open(textPath, 'r', encoding = 'utf-8')
            
            #Debug line: print the name and the first 192 bytes of each file:
            #print(title + ' successfully read')
            #print(file.read(192))
            #At this point, a more sophisticated program would remove all control characters,
            # namely U+0000 - U+001F and U+0080 to U+009F

            #Part 2.2.3: tokenize!
            #A token is limited to alphanumeric characters, apostrophes, and hyphens.
            #Idea to use regex package:
            # https://stackoverflow.com/questions/1059559/split-strings-into-words-with-multiple-word-boundary-delimiters
            allTokens = re.findall(r"[\w'-]+", file.read())

            #Part 2.2.4: analysis!
            # Iterate over all tokens
            for token in allTokens:
                #Part 2.2.4.1: check if the token is in the term list,
                # adding a row of ones to the count matrix
                # and the token to the list of terms if not
                if not token in terms:
                    newRow = numpy.ones((1, counts.shape[1]))
                    counts = numpy.concatenate((counts, newRow), 0)
                    terms.append(token)

                #Part 2.2.4.2: update the term matrix
                currentTermCount = counts[terms.index(token), currentColumn]
                newTermCount = currentTermCount + 1
                counts[terms.index(token), currentColumn] = newTermCount
                
            
            #Part 2.2.5: close the file
            file.close()

        #Debug lines: print the matrix of frequencies and its shape
        #print(counts)
        #print(counts.shape)

        #Part 2.3: increment currentColumn by 1
        currentColumn = currentColumn + 1
            
    #Finale: return the counts, terms, and author vectors
    return counts, terms, authors

#Deduces the common author of all the texts in a folder, returning their name as a string.
#If every text has multiple authors, it raises an exception.
#Will also crash if the metadata cache has not been downloaded yet.
#Made upon realizing that some works have multiple authors.
def get_author(authorFolder):
    #Part 1: set up currset variable, which will contain author info.
    # On the first iteration only, it will be an int.
    currset = 0

    #Part 2: iterate through all works and deduce a common author
    for title in os.listdir(authorFolder):
        #Part 2.1: Get the number of the text as provided by Project Gutenberg
        number = int(title.split()[0])
        
        #Part 2.2: Use that number to get the author from the metadata cache
        authors = get_metadata('author', number)

        #Part 2.3: update currset
        #Part 2.3a: on the first run, just replace it with the newly-obtained frozen set
        if type(currset) is int:
            currset = authors
        #Part 2.3b: on subsequent runs, replace currset with the intersection of it and the new set
        else:
            currset = currset.intersection(authors)
        #debug line: print the current set
        #print(currset)

    #Final step: get the author, or throw an error if there is somehow not exactly one
    authorList = []
    for author in currset:
        authorList.append(author)
    if len(authorList) != 1:
        message = "No common author, or too many common authors in " + authorFolder + "."
        raise Exception(message)

    author = authorList[0]
    #Debug line: print author name
    #print(author)
    return process_name(author)
        

#Simple method to change the format of the author's name
# from "Last, First" to "First Last"
def process_name(author):
    names = author.split(", ")
    return names[1] + " " + names[0]

#This simple debugging function indicates that nothing has blown up yet
def no_blowup():
    print("alright, nothing has blown up yet")

if __name__ == "__main__":
    main()
