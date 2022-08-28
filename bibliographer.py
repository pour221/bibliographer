from parser import Article

print("Ok, let's start to do bibliography in easy way!")

user_pattern_exists = False
user_pattern = []
while True:
    doi = input('DOI: ')
    if doi in ['end', 'close', 'exit', 'done']:
        print('I hope i could help you!')
        break
    article = Article(doi)
    while not user_pattern_exists:
        print("Let's make your pattern")
        print('You need to choose sequence of elements. You can choose the following elements: ')
        for number, part_of_pattern in enumerate(article.publication_info.keys()):
            print(f'{number + 1}. {part_of_pattern.capitalize()}')
        authors_sequence_needed = input('Do you need a sequence of authors? ')
        if authors_sequence_needed in ['yes', 'yeah', 'sure', 'y']:
            print(
                'You can use "1_author", "2_author" etc. to select an author by position or choose "authors" to '
                'select all of their')
        elif authors_sequence_needed in ['no', 'not', 'n']:
            pass
        else:
            continue
        user_pattern = article.set_pattern()
        print(user_pattern)
        user_pattern_exists = True
        break
    print(article.make_bibliography(user_pattern))



# article.user_pattern = ['1_author', '.', ' ', 'title', '.', ' ', '//', ' ', 'authors', '.', ' ', '/', ' ', 'journal_title', ',', ' ', 'year', ',', ' ', 'volume', '(', 'issue', ')', ',', ' ', 'pages', '.']
# ['1_author', '.', ' ', 'title', '.', ' ', '//', ' ', 'authors', '.', ' ', '/', ' ', 'journal_title', ',', ' ', 'year', ',', ' ', 'volume', '(', 'issue', ')', ',', ' ', 'pages', '.']
