import facebook

from FB import connect
import requests

# search?q= סתם כי&type=group
def search_groups(q, user_token):
    res = []
    graph = facebook.GraphAPI(access_token=user_token, version='2.5')
    o = graph.get_object('search',
        q=q,
        type='group',
        fields='icon,picture,name',
        limit=100)
    page = o
    while True:
        for group in page['data']:
            res.append(group)
        try:
            page = requests.get(page['paging']['next']).json()
        except KeyError:
            break
    return res

def is_group_admin(group_id, user_id, user_token):
    graph = facebook.GraphAPI(access_token=user_token, version='2.5')
    o = graph.get_object('{}/admined_groups'.format(user_id),
        limit=100)
    page = o
    while True:
        if any(group_id == group['id'] for group in page['data']):
            return True
        try:
            page = requests.get(page['paging']['next']).json()
        except KeyError:
            break
    return False

if __name__ == '__main__':
    print(is_group_admin('953251484750615', '141041462982709', 'EAALmkmmgVssBAINIecwCNhGP84aB6QbPGmwiBPYfiixIlwcjm3lEvVFgufj6ytQQaA7mICD4C305Q7t8qjfMpwZClZAfN4ZBXrhzvjJ5coaQyd2KI6u9PKj1tdtejomL239ltEDMagJGwe0Xq4uG0gg1qnVZC7TrbSvRSwMX4gZDZD'))