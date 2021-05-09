import sys


def update_readme(name):
    with open('README.md', 'w', encoding='utf-8') as fp:
        fp.write(f'issus name: {name}')


if __name__ == '__main__':
    update_readme(sys.argv[1])
