import wikipediaapi

wiki = wikipediaapi.Wikipedia('Shaurya CS 571 Project', 'en')


def create_word_dict(word_bank):
    word_page_dict = {}
    for word in word_bank:
        # if count >= 10:
        #     return word_page_dict
        word = word.lower()
        #fileName = word + ".txt"
        #destination = open(fileName, "w", encoding="utf-8")
        word_page = wiki.page(word)
        if word_page.exists():
            summary = word_page.summary
            wordCorpus = summary + "\n\n"
            if len(summary) < 500:
                links = word_page.links
                for link_word in links.keys():
                    new_page = links[link_word]
                    wordCorpus += new_page.summary + "\n\n"
            #destination.write(wordCorpus)
            word_page_dict[word] = wordCorpus
            #destination.close()
    return word_page_dict
