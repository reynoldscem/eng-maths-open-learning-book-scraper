from collections import OrderedDict
from subprocess import call
import bs4
import os

URL = 'http://www3.ul.ie/~mlc/support/Loughborough%20website/'
BASE_DIR = './book/'

def get_identifier(link):
    return link.get('href').split('/')[0]

def main():
    with open('./book.html') as fd:
        data = fd.read()

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(data, 'html.parser')

    sections = soup.find('table').find('tr')

    chapter_names = map(lambda a: a.text, sections.find_all('b'))
    links = sections.find_all('a')
    chapter_identifiers = [get_identifier(link) for link in links]
    chapter_identifiers = list(dict.fromkeys(chapter_identifiers))
    identifier_to_name = dict(zip(chapter_identifiers, chapter_names))

    chapter_dict = {}
    for link in links:
        identifier = get_identifier(link)
        if identifier in chapter_dict:
            chapter_dict[identifier].append((link.get('href'), link.text))
        else:
            chapter_dict[identifier] = [(link.get('href'), link.text)]

    for index, (identifier, units) in enumerate(chapter_dict.items(), 1):
        index_string = '{0:02}'.format(index)
        dirname = '{} - {}'.format(index_string, identifier_to_name[identifier])
        chapter_dir = os.path.join(BASE_DIR, dirname)

        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)

        for unit in units:
            unit_href = unit[0]
            unit_code = unit_href.split('/')[1].split('.')[0]
            unit_name = unit[1]
            filename = '{} - {}.pdf'.format(unit_code, unit_name)

            file_url = URL + unit[0]
            output_path = os.path.join(chapter_dir, filename)
            call(['wget', '-O', output_path, file_url])

if __name__ == '__main__':
    main()
