This README functions as a write-up for our implementation of a Bayes [Author Classifier](https://github.com/arcorion/AuthorClassifier).

# Bayes Author Classifier

## Introduction

One of the key matters of import for this project was that it serve as a way for us to practice coding, as both members of this group have more of a background in linguistics than in programming.  The project itself has us using a collection of text files from the [Project Gutenberg](https://www.gutenberg.org/) ebook library.  This ended up being a more involved task than originally conceived, as the collection includes a wide variety of text types and formats.

The core loop of the "author.py" component requires that it:
* Generate a list of texts attributed to an author
* Reduce the list according to language (English), number of authors (solo only), type (removing text collections) and format (simple text files)
* Download the files from Project Gutenberg
* Strip away whitespace, header, and footer data
* Normalize the text (remove case and non-alphanumerics)
* Save the text files both individually and as a single text  

In addition to the core features, the module also allows for a user to pass the name of a file containing multiple lines of author names as download options, as well as a flag for accepting a string as an author name.

This saved text data is then used as the input for the second module, "make_model.py."  Within this module, the actual guts of the Naive Bayes Categorizer is implemented.  Within it, the output files from "author.py" are used to generate the model framework, and then each author's texts are integrated into a term matrix.  Columns are created, representing document classes (authors).  The texts in each author's directory are walked through, creating a list of all word-like tokens found.  If a new token is found, a one-filled row is created to represent add-1 smoothing.  The counts are incremented as each new token is found, and after all tokens for an author are found, the process is repeated with the next author.  After all authors have their vocabulary token counts finalized, the probabilities of each token are calculated per author.

Unfortunately, we did not manage to get to the test component of our project.  Implementation of such would require going through each document class (authors), summing the log of their previous probabilities, then summing the probability of the token matching a token in the document class in question with the log of the probability of the token in the test document.  Once this is done for each document class, the one with the highest sum total is chosen as the category label for the test document.

## Data

For this project, we used the previously mentioned Project Gutenberg library for our data.  We specifically selected a collection of authors with a minimum of 25 English language releases listed on Project Gutenberg.  These include William Shakespeare, Mark Twain, Arthur Conan Doyle, Jane Austen, Harriet Beecher Stowe, H.G. Wells, Charles Dickens, Jonathan Swift, Edith Wharton, and Edgar Allan Poe.  A few comments regarding bias in the data should be mentioned.  In particular, all of the selected authors are white, English speakers, and most are male.  They are also all from American or English backgrounds.  The selection stems largely from pre-existing bias, as several other authors were considered, but unfortunately lacked large enough corpuses to use.  It might be possible in future iterations of this project to work with a wider selection of authors, as well as to include non-English texts, as their's no inherent technical reason to exclude works in many differing languages.  The ultimate mechanism for choosing authors and language came down to personal familiarity with them from our perspective and availability of the texts via Project Gutenberg.

## Results

With the existing data we have available, the results are currently represented as a rather large set of CSVs, with some 295,908 tokens tracked for each document class.  The contextual probability of each token is represented along the rows, with the columns listed for each author in the order represented in the authors.csv, from left to right.  Edgar Allan Poe, Mark Twain, Edith Wharton, William Shakespeare, Jane Austen, Charles Dickens, H. G. (Herbert George) Wells, Arthur Conan Doyle, Jonathan Swift, and Harriet Beecher Stowe.  The token terms are represented in terms.csv, with their row matching the associated row in freqs.csv.

Since we don't have test information, there isn't a very straightforward way to describe the data, but we did want to comment on a particular aspect of the output.  Since the table is generated with the authors as the (invisible) column heads and the data was generated piecewise by author, after an author's texts are completed, any remaining tokens will be zero by default, with the result representing a probability calculated based on the add-1 smoothing.  As a result, skimming from top to bottom in the CSV shows very clearly where each text started and ended its contribution to the total number of tokens.

## References

### General References and Data Source

* Bender, E. M., & Friedman, B. (2018). Data Statements for Natural Language Processing: Toward Mitigating System Bias and Enabling Better Science. Transactions of the Association for Computational Linguistics, 6, 587–604. https://doi.org/10.1162/tacl_a_00041

* Brownlee, J. (2019, October 17). Naive Bayes Classifier From Scratch in Python. Machine Learning Mastery. https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

* Natural Language Toolkit — NLTK 3.6.2 documentation. (n.d.). Www.nltk.org. Retrieved June 10, 2021, from https://www.nltk.org/index.html

* Project Gutenberg. (2019). Project Gutenberg. https://www.gutenberg.org

* Speech and Language Processing. (2018). Stanford.edu. https://web.stanford.edu/~jurafsky/slp3/

* Starmer, J. (2020). Naive Bayes, Clearly Explained!!! [YouTube Video]. In YouTube. https://www.youtube.com/watch?v=O2L2Uv9pdDA

* Wikipedia Contributors. (2019, June 17). Naive Bayes classifier. Wikipedia; Wikimedia Foundation. https://en.wikipedia.org/wiki/Naive_Bayes_classifier

### For author.py module:

* Argparse Tutorial — Python 3.9.5 documentation. (n.d.). Docs.python.org. Retrieved June 10, 2021, from https://docs.python.org/3/howto/argparse.html

* Lekhonkhobe, Tshepang. (2018, February 10). Python How to Check if File can be Read or Written. Novixys Software Dev Blog. https://www.novixys.com/blog/python-check-file-can-read-write/

### For make_model.py module:

* file - How to get all of the immediate subdirectories in Python. (n.d.). Stack Overflow. Retrieved June 10, 2021, from https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python

* python - Split Strings into words with multiple word boundary delimiters. (n.d.). Stack Overflow. Retrieved June 10, 2021, from https://stackoverflow.com/questions/1059559/split-strings-into-words-with-multiple-word-boundary-delimiters

* Solved - UnicodeDecodeError: “charmap” codec can’t decode byte 0x9d. (n.d.). Www.youtube.com. Retrieved June 10, 2021, from https://www.youtube.com/watch?v=yC2y4tOdF0g
