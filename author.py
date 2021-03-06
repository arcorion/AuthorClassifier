# Author basically takes an author (or list of authors) name(s), searches for
# matches on Project Gutenberg, and then downloads the associated text
# documents.  Once those documents have been downloaded, it strips the headers
# and either saves or passes the text.
import re, gutenberg, os, argparse

def main():
    from gutenberg.query import get_metadata

    # Never implimented a parser before.  Looks like the most straightforward option for Python
    # is to use argparse - https://docs.python.org/3/howto/argparse.html
    # Implementing two options:
    # One: -n "Author name" - this takes the author's name and just passes it straight along.
    # Two: -f "filename.txt" - this takes a filename and loops through the names in the file.
    parser = argparse.ArgumentParser(description="Download the English texts" +
                                     " from an author on Project Gutenberg")
    parser.add_argument("-n", "--name", help = "input a string (in quotes)" + 
                        " of one author's name")
    parser.add_argument("-f", "--file", help = "input a filename with a " +
                        "list of author names separated by new lines\nif" +
                        " a file is input, the name flag is ignored")
    args = parser.parse_args()

    # Making sure there's a "texts" directory.  If not, creating one.
    # (Technically, it's doing the reverse of that, making a directory
    # and failing "gracefully" if that's not right.  I should fix this later...)
    try:
        os.mkdir("texts")
    except:
        print("The \"texts\" folder already exists, skipping...")
    # 
    # https://www.novixys.com/blog/python-check-file-can-read-write/#2_Check_if_File_can_be_Read
    if (args.file):
        if (os.access(args.file, os.R_OK)):
            author_file = open(args.file, 'r')
            author_list = author_file.readlines()
            # Funny timing - picked this line up from Python One-Liners
            # by Christian Mayer a couple of nights ago.
            author_list = [author.strip() for author in author_list]
            print(author_list)
        else:
            print("File " + args.file + " is not accessible.")
    elif (args.name):
        author_list = [args.name]
    else:
        author_list = []

    acquire_documents(author_list)
        
def acquire_documents(author_list):
    if (author_list):
        for input_name in author_list:
            # Requesting name of the author to be downloaded.
            name_in, formatted_name = query_name(input_name)
            # Searches for the author in the cache.  Any matched texts are passed as list to doc_list.
            doc_list = find_doc_list(formatted_name)
            # Writes the downloaded files
            if (len(doc_list) > 0):
                file_writer(name_in, doc_list)
            else:
                print("No texts found for the name " + name_in + ".")
    else:
        input_name = input("What author do you want to download?\nPlease use the form: FirstName MiddleName LastName: ")
        name_in, formatted_name = query_name(input_name)
        doc_list = find_doc_list(formatted_name)
        if (len(doc_list) > 0):
            file_writer(name_in, doc_list)
        else:
            print("No texts found for the name " + name_in + ".")

# Asking for author's name in "FirstName MiddleName MiddleName2 ... LastName" format.  I then split it
# and format the name to "LastName, FirstName MiddleName MiddleName2, etc", as that's what the query expects.
def query_name(name_in):
    split_name = name_in.split()
    formatted_name = split_name[(len(split_name) - 1)] + ","

    # Splitting up the name, formatting it to work with Gutenberg's search.
    for num in range(0, len(split_name) - 1):
        if num == (len(split_name) -1):
            pass
        else:
            formatted_name = formatted_name + " " + split_name[num]
    
    return name_in, formatted_name

def file_writer(name_in, doc_list):
    from gutenberg.acquire import load_etext
    from gutenberg.query import get_metadata
    # The directory is named after the author's name. There's no chance of
    # overlap on text number, since each document number is unique.
    dir_name = "texts/" + name_in
    try:
        os.mkdir(dir_name)
    except:
        print("The " + dir_name + " directory already exists, skipping...")

    # Goes through the elements of the frozenset doc_list and downloads them to text files.
    # Note, it checks to see if the text exists first, as some documents lack a text version.
    # An error is reported in such cases.
    with open(name_in + ".txt", "w") as concat_file:
        pass

    for number in doc_list:
        # Sometimes the download fails (usually because there's no text version of the document)
        # this tries to download the text, and if it fails, it produces an error and skips
        try:
            load_etext(number)
        except Exception as err:
            exception_type =  type(err).__name__
            print("File number " + str(number) + " not downloaded due to " + exception_type)
        else:
            title = next(iter(get_metadata('title', number)))
            print("Downloading Document Number " + str(number) + ": " + title +
                  " by " + name_in + ".")
            if (len(title) > 50):
                title = title[:50]

            document = download_doc(number)
            # Adapted from NLTK book - https://www.nltk.org/book/ch03.html

            # Reads the first line of the document to see if it is an audio reading 
            first_line = document.partition("\n")
            if (re.search(r"^this audio reading.*", first_line[0])):
                print("Document not downloaded - audio recording text")
                continue

            filepath = dir_name + "/" + str(number) + " " + title + ".txt"
            file = open(filepath, "w")

            file.write(document)

            # This is sloppy, but I wanted to make sure this was producing a concatenated
            # file. 
            with open(name_in + ".txt", "a") as concat_file:
                concat_file.write(download_doc(number))

            file.close()

# This function generates the document list to download based on the author's name.
# It specifically downloads just English, single author texts that aren't part of a collection,
# as the collections are typically duplicates of singular texts.  Note, it returns a set of
# documents, rather than a list, for improved performance.
def find_doc_list(name):
    # Reads a name in the format "LastName, FirstName", then returns a list of texts with that author's name.
    from gutenberg.query import get_etexts
    from gutenberg.query import get_metadata
    
    curated_docs = set() 

    # Narrows documents down to those written in English, have a single author, and aren't part of a collection.
    # Note, ruling out collections is done by excluding certain keywords, as shown in the re.search below.  It's possible
    # that they might produce false positives, but I suspect that'll be quite limited.
    # Sets are faster! https://towardsdatascience.com/python-lists-vs-sets-39bd6b5745e1
    text_set = set(get_etexts('author', name))

    for item in text_set:
        author_count = len(get_metadata('author', item))
        title = next(iter(get_metadata('title', item)))
        metalang = next(iter(get_metadata('language',item)))

        if (metalang == 'en') and (author_count == 1):
            if not (re.search(".*[Pp]roject [Gg]utenberg.*|.*[Ww]orks [Oo]f.*|.*[Cc]ollected.*", title)):
                curated_docs.add(item)       

    return curated_docs

def download_doc(docNum):
    # This function just downloads a text and returns the downloaded text.
    # While writing this, I ran into an issue where one of the Gutenberg
    # mirrors wasn't working.  I had to change the default mirror (though you
    # can also use an env variable) to make it work.  You can get a list of
    # mirrors here - https://www.gutenberg.org/MIRRORS.ALL.  I just used one of
    # the http mirrors.
    from gutenberg.acquire import load_etext
    from gutenberg.cleanup import strip_headers

    # Remove author's name from first lines

    document = strip_headers(load_etext(docNum)).strip()
    document = document.lower()

    # Save local copies of texts #.txt
    # Concatenate texts

    # Does this need to return the text?
    return document

if __name__ == "__main__":
    main()
