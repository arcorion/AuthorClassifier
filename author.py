# Author basically takes an author (or list of authors) name(s), searches for matches on Project Gutenberg, and then downloads the associated text documents.  Once those documents have been downloaded, it strips the headers and either saves or passes the text.
import sys,re,gutenberg,os

def main():
    from gutenberg.acquire import load_etext
    from gutenberg.query import get_metadata

    # Making sure there's a "texts" directory.  If not, creating one.
    # (Technically, it's doing the reverse of that, making a directory
    # and failing "gracefully" if that's not right.  I should fix this later...)
    try:
        os.mkdir("texts")
    except:
        print("The \"texts\" folder already exists, skipping...")


    # Asking for author's name in "FirstName LastName" format.  I then split it
    # and format the name to "LastName, FirstName", as that's what the query expects.
    name_in = input("What author do you want to download? Please use the form: FirstName LastName: ")
    name = name_in.split()

    # Searches for the author in the cache.  Any matches texts are passed as frozenset to doc_list.
    doc_list = find_doc_list(name[1] + ", " + name[0])
    
    # The directory is named after the author's last name - will want to change this later, but
    # this should work for the moment.  There's no chance of overlap on text number, since each
    # document number is unique.
    dir_name = "texts/" + name[1]
    try:
        os.mkdir(dir_name)
    except:
        print("The " + dir_name + " directory already exists, skipping...")

    # Goes through the elements of the frozenset doc_list and downloads them to text files.
    # Note, it checks to see if the text exists first, as some documents lack a text version.
    # An error is reported in such cases.
    # (Note to self, this could probably be put inside the download_doc function with a tiny
    # bit of reworking.  Why don't you do that?)
    #
    # It seems to stall on document number 3999 for Mark Twain until I hit CTRL-C.  Why is that?
    # Possible answer - it's just long.  When I check the text file, it seems to be mid-stream.
    #
    # Also, how to remove non-English docs? Duplicate texts?
    for number in doc_list:
        try:
            load_etext(number)
        except:
            print("File number " + str(number) + " not downloaded, an error occurred.")
        else:
            title = next(iter(get_metadata('title', number)))
            filepath = dir_name + "/" + str(number) + " " + title + ".txt"
            file = open(filepath, "w")
            file.write(download_doc(number))
            file.close()

def find_doc_list(name):
    # Reads a name in the format "LastName, FirstName", then returns the frozenset of texts with that author's name.
    from gutenberg.query import get_etexts
    from gutenberg.query import get_metadata

    # Works out single-author texts
    text_list = get_etexts('author', name)

    return text_list

def download_doc(docNum):
    # This function just downloads a text and returns the downloaded text.
    # While writing this, I ran into an issue where one of the Gutenberg mirrors wasn't working.  I had to change the default mirror (though you can also use an env variable) to make it work.  You can get a list of mirrors here - https://www.gutenberg.org/MIRRORS.ALL.  I just used one of the http mirrors.
    from gutenberg.acquire import load_etext
    from gutenberg.cleanup import strip_headers
    from gutenberg.query import get_metadata

    # Remove author's name from first lines


    file_text = strip_headers(load_etext(docNum)).strip()
    title = next(iter(get_metadata('title', docNum)))
    author = next(iter(get_metadata('author',docNum)))

    print("Downloading Document Number " + str(docNum) + ": " + title + " by " + author + ".")

    # Save local copies of texts #.txt
    # Concatenate texts

    return file_text

if __name__ == "__main__":
    main()
