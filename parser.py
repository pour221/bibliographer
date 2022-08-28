import re
import crossref_commons.retrieval


class Publication:
    """
    The basic class. Get all information about publication and make dict which include type of publication, year,
    authors, publication title, journal title, short journal title, volume, pages and years.
    """
    publication_info = None
    user_pattern = None
    
    def __init__(self, doi: str) -> None:
        self.__doi = doi
        self.meta = crossref_commons.retrieval.get_publication_as_json(self.__doi)
        self.get_publication_info()

    @property
    def doi(self) -> str:
        return self.__doi

    @doi.setter
    def doi(self, doi: str) -> None:
        self.__doi = doi

    def get_publication_info(self) -> None:
        """
        Take meta information from doi and make a dict
        """
        self.publication_info = {
            'type': self.meta.get('type'),
            'doi': self.meta.get('URL'),
            'authors': {},
            'title': ''.join(self.meta.get('title')),
            'journal_title': self.meta.get('container-title'),
            'journal_title_short': self.meta.get('short-container-title'),
            'volume': self.meta.get('volume'),
            'issue': self.meta.get('issue'),
            'pages': self.meta.get('page'),
            'year': self.meta.get('created').get('date-parts')[0][0],
            'publisher': self.meta.get('publisher'),
        }
        for position, author in enumerate(self.meta['author']):
            self.publication_info['authors'][f'{position + 1}_author'] = {'name': author.get('given'),
                                                                          'surname': author.get('family')}


class Article(Publication):
    """

    """

    # user_pattern = None

    def __init__(self, doi: str) -> None:
        super().__init__(doi)

    @staticmethod
    def set_pattern() -> list:
        """
        Make a list with keyword or symbols that will be a pattern (use like a key in dict)
        """
        elem_number = 1
        user_pattern: list[str] = []
        while True:
            pattern_elem = input(f'Choose the {elem_number} elem: ').lower()
            if pattern_elem == 'end':
                break
            user_pattern.append(pattern_elem)
            elem_number += 1
            # self.user_pattern = user_pattern
        return user_pattern

    # def set_authors_pattern(self, elem_number):
    #     elem_number = elem_number

    def get_all_authors(self) -> str:
        """
        Return all authors names in str format (ready to use in pattern when authors sequence doesn't matter)
        """
        authors_list = []
        list_of_dict_authors = list(self.publication_info.get('authors').values())
        for dict_elem in list_of_dict_authors:
            if dict_elem['name'] is None:
                if dict_elem['surname'] is not None:
                    authors_list.append(f'{dict_elem["surname"]}')
                else:
                    continue
            elif dict_elem['surname'] is None:
                if dict_elem['name'] is not None:
                    authors_list.append(f'{dict_elem["name"]}')
                else:
                    continue
            else:
                authors_list.append(f'{dict_elem["name"]} {dict_elem["surname"]}')
        return ', '.join(authors_list)

    def get_enumerate_authors(self) -> dict:
        """
        Return a dict with enumerate authors names which can use in pattern when author sequence matters
        """
        dict_authors = self.publication_info.get('authors')
        new_dict_authors = {}
        for key, value in dict_authors.items():
            if value['name'] is not None and value['surname'] is not None:
                new_dict_authors[key] = f'{value["name"]}, {value["surname"]}'
            else:
                if value['name'] is None:
                    if value['surname'] is not None:
                        new_dict_authors[key] = f'{value["surname"]}'
                    else:
                        continue
                elif value['surname'] is None:
                    if value['name'] is not None:
                        new_dict_authors[key] = f'{value["name"]}'
                    else:
                        continue
                else:
                    continue
        return new_dict_authors

    def clear_title(self) -> None:
        """
        Remove unnecessary characters from article title
        """
        regex_patterns = {
            '1': r' ?<([^<>]+)> ?',
            '2': '\n',
            '3': r'(?<= ) {2,}| {2,}(?=[.,])'
        }
        title = self.publication_info.get('title')
        for i in regex_patterns.values():
            title = re.sub(i, '', title)
        # regex_pattern_1 = r' ?<([^<>]+)> ?'
        # regex_pattern_2 = '\n'
        # regex_pattern_3 = r' {2,}'
        # title = self.publication_info.get('title')
        # title = re.sub(regex_pattern_1, '', title)
        # title = re.sub(regex_pattern_2, '', title)
        # title = re.sub(regex_pattern_3, '', title)
        self.publication_info['title'] = title


    def make_bibliography(self, pattern) -> str:
        """
        make bibliographic reference using user pattern
        """
        link = []
        for elem in pattern:
            if (elem[0].isdigit() and len(elem) > 1) or elem[0].isalpha():
                if elem[0].isalpha():
                    if elem == 'authors':
                        link.append(self.get_all_authors())
                    elif elem == 'title':
                        self.clear_title()
                        link.append(self.publication_info.get(elem))
                    else:
                        if type(self.publication_info.get(elem)) == list:
                            link.append(str(self.publication_info.get(elem)[0]))
                        else:
                            link.append(str(self.publication_info.get(elem)))
                elif elem[0].isdigit():
                    link.append(str(self.get_enumerate_authors().get(elem)))
                else:
                    print('something went wrong')
                    # raise SystemExit
            elif not elem[0].isdigit() and not elem[0].isalpha():
                link.append(str(elem))
            else:
                print('something went wrong')
        return ''.join(link)

class BookEtc(Publication):
    pass


if __name__ == '__main__':
    while True:
        doi = input('DOI: ')
        if doi == 'end':
            break
        abstarct = Article(doi)
        user_pattern = ['1_author', '.', ' ', 'title', '.', ' ', '//', ' ', 'authors', '.', '/', ' ', 'journal_title', ',', ' ', 'year', ',', ' ', 'volume', '(', 'issue', ')', ',', ' ', 'pages']
        # abstarct.clear_title()
        a = abstarct.make_bibliography(user_pattern)
        print(a)


