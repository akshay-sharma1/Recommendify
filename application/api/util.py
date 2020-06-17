# Builds relevant URLS
def build_url(*args):
    return '/'.join(args)


def build_recommendation_url(*args, **kwargs):
    url = build_url(*args)
    additional_url = '?'
    for key, value in kwargs.items():
        attribute = key + '=' + value
        attribute += '&'
        additional_url += attribute

    return url + additional_url


def create_authorization_header(access_token):
    return {'Authorization': 'Bearer {}'.format(access_token)}

def create_playlist_header(access_token):
    return {'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'}

