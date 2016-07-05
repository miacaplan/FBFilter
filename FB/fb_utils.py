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

if __name__ == '__main__':
    print(search_groups('סתם מנסה', 1, 'EAALmkmmgVssBAE0F3F9laFTXr8KUSPB2m9E3ttt3Xs17z1xb9t1EsvAijVoypSSqJrbkyJPlyAzQnuQgwfKX308TozyqRoaZCwtzEyA5mjKeDKGcTyrL5andZAZB9hOTefnDBBif2vtuatTjr8AgQ5eZCUdIPyAZD'))