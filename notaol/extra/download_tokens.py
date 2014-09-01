'''Download tokens lists from the Internet Archive.'''
import os.path
import string
import requests


TEMPLATE = ('https://web.archive.org/web/20020205183644id_/'
            'http://www.aol-files.com/fdo91/tokens/{}')

FILES = tuple(
    ['1998.txt', 'list_tokens.html', 'token_!.html', 'token_0-9.html'] +
    ['token_{}.html'.format(char) for char in string.ascii_lowercase]
)


def main():
    for filename in FILES:
        if not os.path.exists(filename):
            print('Fetch', filename)

            url = TEMPLATE.format(filename)

            response = requests.get(url)

            with open(filename, 'wb') as out_file:
                out_file.write(response.text.encode('utf-8'))


if __name__ == '__main__':
    main()
