This README functions as a write-up for our implementation of the Bayes Author Categorizer.

# Bayes Author Categorizer

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

For this project, we used the previously mentioned Project Gutenberg library for our data.  We specifically selected a collection of authors with a minimum of 25 English language releases listed on Project Gutenberg.  These include William Shakespeare, Mark Twain, Arthur Conan Doyle, Jane Austen, Harriet Beecher Stowe, H.G. Wells, Charles Dickens, Jonathan Swift, Edith Wharton, and Edgar Allan Poe.  A few comments regarding bias in the data should be mentioned.  In particular, all of the selected authors are white, English speakers, and most are male.  They are also all from American or English backgrounds.  These biases likely stem partly from the 

## Results

## References
