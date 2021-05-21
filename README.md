N-Gram Author Categorizer

There are two overarching elements to our project.  They are the creation of ready corpus components and the model development.  These will be split between Christopher and Arthur, respectively.  For the purposes of our work, we’ll be using this on English-language authors, although ideally the model should work with many languages.

For corpus creation, We will be using the NLTK package, specifically its corpus creation functionality, to acquire data from Project Gutenberg. (Christopher)
https://www.nltk.org/index.html 
https://www.gutenberg.org/
https://www.nltk.org/book/ 
We will be using ten authors, with the criteria being that they have at least 25 English language releases on Project Gutenberg.
William Shakespeare
https://www.gutenberg.org/ebooks/author/65
Mark Twain
https://www.gutenberg.org/ebooks/author/53
Arthur Conan Doyle
https://www.gutenberg.org/ebooks/author/69
Jane Austen
https://www.gutenberg.org/ebooks/author/68
Harriet Beecher Stower
https://www.gutenberg.org/ebooks/author/115
H.G. Wells
https://www.gutenberg.org/ebooks/author/30
Charles Dickens
https://www.gutenberg.org/ebooks/author/37
Jonathan Swift
https://www.gutenberg.org/ebooks/author/326
Edith Wharton
https://www.gutenberg.org/ebooks/author/104
Edgar Allen Poe
https://www.gutenberg.org/ebooks/author/481
10 works from each author will be collected to be used as corpus for the purposes of model building.  A few remaining works will be set aside for final testing.
The code loop for this bit will resemble the following:
Text sources ingested, header/footer/junk whitespace removed.
Pull authors’ names from texts - use to assign category.
Collate the text collections
Pass text collections and categories to next component.
For model development, we’ll produce a language model for each corpus using a Naive Bayes Classifier. (Arthur)
https://en.wikipedia.org/wiki/Naive_Bayes_classifier
https://www.youtube.com/watch?v=O2L2Uv9pdDA
https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
https://scikit-learn.org/stable/modules/naive_bayes.html
The code here will be two parts that do essentially the same thing, an initial classifier that generates output for the text corpora, then one that does the same for individual texts provided at use-time.
Ahead of time - Text histogram generated for each category (author)
Headwords created from unique tokens
Individual token counts produced for each headword generated
Implement smoothing (laplace/other?)
Probability produced - Word / Total Words
Results stored for later use
At use - Text histogram generated for new provided text (author unknown)
Headwords created from unique tokens
Individual token counts produced for each headword generated
Implement smoothing (laplace/other?)
Probability produced - Word / Total Words
Results compared with each category/author, cycling through each possible matching
Most often matched author is selected as category - for any ties, both are presented
Testing (Christopher) - 
In order to determine whether this works, we’ll then pull the author from each of the tested documents and compare them to the output of the above, to see if the Naive Bayes algorithm worked!  We can then look at possible resolutions for problems encountered.

Link to Github Repository - https://drive.google.com/file/d/1XsLLG-qCvtzJo-he7jZ6FU7W4Tjbo0vU/view?usp=sharing
(Note, at time of writing, it only contains the Readme, which includes the text of this M2 Assignment.)

Timeline

May 21 - Complete M2 Proposal
May 23 - Have general outline of each component prepared in code
    Corpus components using NLTK should be completed by this point.
May 30 - Have final “draft” of functional project completed
    The Bayes Classifier should be completed by this point.
June 6 - Have deliverable code project completed, collaborate on write-up
June 8 - Complete write-up final draft, final review of project materials
June 9 - Turn in deliverables
