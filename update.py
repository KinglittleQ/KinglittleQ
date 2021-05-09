import sys
from tabulate import tabulate


def update_readme(name):
    table = [['one','two','three'],['four','five','six'],['seven','eight','nine']]
    table = str(tabulate(table, tablefmt='html'))
    with open('README.md', 'w', encoding='utf-8') as fp:
        fp.write(f'issus name: {name}\n\n')
        fp.write(table)


if __name__ == '__main__':
    update_readme(sys.argv[1])
