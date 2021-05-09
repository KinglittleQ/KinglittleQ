import sys
import numpy as np
from tabulate import tabulate
from pathlib import Path 


HYPER_LINK = '<a href="{}">{}</a>'
ISSUE_BODY =  "Just push 'Submit new issue'. You do not need to do anything else.".replace(' ', '+')
ISSUE_LINK = 'https://github.com/KinglittleQ/github-action-demo/issues/new?title=Put-{}&body=' + ISSUE_BODY
N = 15

EMPTY = 0
WHITE = 1
BLACK = 2

PLAYERS = {WHITE: 'white', BLACK: 'black'}
MARKERS = {EMPTY: '` `', WHITE: '`O`', BLACK: '`X`',
           WHITE + 64: '**`O`**', BLACK + 64: '**`X`**'}

def parse_issue_name(name):
    items = name.split('-')
    assert len(items) == 2
    row_id = int(items[0])
    col_id = int(items[1])

    return row_id, col_id


def parse_meta_data(row_id, col_id):
    data_dir = Path('.data')
    chessboard_file = data_dir / 'chessboard.txt'
    if chessboard_file.stat().st_size == 0:
        chessboard = np.zeros((N, N), dtype=np.int32)
    else:
        chessboard = np.loadtxt(chessboard_file, dtype=np.int32)

    n_whites = np.count_nonzero(chessboard == WHITE)
    n_blacks = np.count_nonzero(chessboard == BLACK)
    player = BLACK
    if n_whites < n_blacks:
        player = WHITE

    assert chessboard[row_id, col_id] == EMPTY
    chessboard[row_id, col_id] = player
    np.savetxt(chessboard_file, chessboard, fmt="%d")

    return player, chessboard


def next_player(player):
    assert player == WHITE or player == BLACK
    return (WHITE + BLACK) - player


def judge(chessboard):
    dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
    for i in range(N):
        for j in range(N):
            if chessboard[i][j] == EMPTY:
                continue
            player = chessboard[i][j]

            for d in dirs:
                x, y = i, j
                count = 0
                for k in range(5):
                    if x < 0 or x >= N or y < 0 or y >= N:
                        break

                    if chessboard[x, y] != player:
                        break
                    x += d[0]
                    y += d[1]
                    count += 1
                if count == 5:
                    x, y = i, j
                    for z in range(5):
                        chessboard[x, y] += 64
                        x += d[0]
                        y += d[1]
                    return player
    return EMPTY


def update_gobang(winner, player, chessboard):
    player = PLAYERS[player]

    headers = ['{}'.format(i) for i in range(N)]

    table = []
    for i in range(N):
        row = []
        for j in range(N):
            issue_link = ISSUE_LINK.format(f'{i}-{j}')
            marker = MARKERS[chessboard[i, j]]
            content = HYPER_LINK.format(issue_link, marker)
            row.append(content)
        table.append(row)

    table = str(tabulate(table, headers, tablefmt='github'))
    with open('gobang.md', 'w', encoding='utf-8') as fp:
        fp.write(f'`O` is white, `X` is black.\n')
        if winner == EMPTY:
            fp.write(f'You are {player} now\n\n')
        else:
            winner = PLAYERS[winner]
            link = ISSUE_LINK.format('restart')
            fp.write(f'Winner is {winner}! Click [here]({link}) to restart. \n\n')
        fp.write(table)


def update_readme():
    with open('description.md', 'r', encoding='utf-8') as fp:
        description = fp.read()
    with open('gobang.md', 'r', encoding='utf-8') as fp:
        gobang = fp.read()

    readme = description.replace('{gobang}', gobang)
    with open('README.md', 'w', encoding='utf-8') as fp:
        fp.write(readme)


def restart():
    data_dir = Path('.data')
    chessboard_file = data_dir / 'chessboard.txt'
    chessboard = np.zeros((N, N), dtype=np.int32)
    np.savetxt(chessboard_file, chessboard, fmt="%d")
    update_gobang(EMPTY, BLACK, chessboard)
    update_readme()


def start(issue_name):
    if issue_name == 'restart':
        restart()
        return

    row_id, col_id = parse_issue_name(issue_name)
    player, chessboard = parse_meta_data(row_id, col_id)

    winner = judge(chessboard)
    player = next_player(player)
    update_gobang(winner, player, chessboard)
    update_readme()


if __name__ == '__main__':
    start(sys.argv[1])
