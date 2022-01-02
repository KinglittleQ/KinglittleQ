from time import sleep
from urllib.request import Request, urlopen
import json
import traceback

GITHUB_REPOS_API = 'https://api.github.com/users/{username}/repos?per_page=100&page={page}'
PRINT_LINE = '{repo_name: <40}:{star_cnt: >6}'


def count_stargazers(username):
    print('Count stargazers of {}\'s GitHub repositries...\n\n'.format(username))
    repos_list = get_repos_list(username)

    total = 0
    for repo in repos_list:
        if repo['stargazers_count'] > 0:
            print(PRINT_LINE.format(
                repo_name=repo['name'], star_cnt=repo['stargazers_count']))
            total += repo['stargazers_count']

    print('\n' + PRINT_LINE.format(repo_name='TOTAL', star_cnt=total))
    return total


def get_repos_list(username):
    repos_list = []

    try:
        page = 1
        repos_list_tmp = []
        while len(repos_list_tmp) > 0 or page == 1:
            api = GITHUB_REPOS_API.format(username=username, page=page)
            request = Request(api)
            with urlopen(request) as res:
                repos_list_tmp = json.load(res)

            if len(repos_list_tmp) == 0:
                break

            repos_list += repos_list_tmp
            page += 1
            if page > 10:
                print('Abnormal number of attempts.')
                break

            sleep(1)
    except:
        print(traceback.format_exc())

    return repos_list


def update_readme():
    with open('description.md', 'r', encoding='utf-8') as fp:
        description = fp.read()
    with open('gobang.md', 'r', encoding='utf-8') as fp:
        gobang = fp.read()

    # count number of stars
    nstars = count_stargazers('KinglittleQ')
    description = description.replace('{github_stars}', str(nstars))

    readme = description.replace('{gobang}', gobang)
    with open('README.md', 'w', encoding='utf-8') as fp:
        fp.write(readme)
