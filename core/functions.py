from igdb.wrapper import IGDBWrapper
import json, random
import os
# from igdb.exceptions import IGDBWrapperException

from requests import post, get
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path_p = os.path.join(base_dir, 'p')
file_path_f = os.path.join(base_dir, 'f')

CLIENT_ID       = 'bxk20sz4bgqjz52yq8gr5eik6erggk'
CLIENT_SECRET   = 'usqinjg9vui01n1fuvpbu75wamjlq7'
TOKEN_URL       = 'https://id.twitch.tv/oauth2/token'

def getToken():
    data = {
       "client_id": CLIENT_ID,
       "client_secret": CLIENT_SECRET,
       "grant_type": "client_credentials"
   }
    
    token = ''
    file = open(file_path_p, 'r')
    token = f'{file.read()}'
    file.close()

    if token == '':
        file = open(file_path_p, 'w')
        response = post(TOKEN_URL, data=data)
        print('dam')

        try:
            file.write(response.json()["access_token"])
            token = response.json()["access_token"]
        except:
            file.write('')
        file.close()

    return token

def getWrapper():
    return IGDBWrapper(CLIENT_ID, getToken())

def query():
    file = open(file_path_f, 'r')
    stuff = file.read()
    file.close()
    wrapper = getWrapper()
    if stuff != '':
        games = json.loads(stuff)
        game = random.choice(games)
        try:
            game = getGameDetails(game, wrapper)
        except Exception as e:
            game = gameException(e)

    else:
        query = f"""
        fields name, version_title, cover.image_id, summary, storyline, videos, tags, game_modes, age_ratings, artworks, screenshots, url, themes;
        where platforms = (6,14,3)
        & rating > 80
        & rating_count > 400
        & game_modes != null;
        sort popularity desc;
        limit 500;
        """
        try:
            response = wrapper.api_request(endpoint="games", query=query)

            games = json.loads(response.decode('utf-8'))
            game = random.choice(games)

            game = getGameDetails(game, wrapper)
        
            with open(file_path_f, 'w') as file:
                json.dump(games, file)

        except Exception as e:
            game = gameException(e)

    return game


def mode_names(game, wrapper):
    modes = []
    if "game_modes" in game:
        gm_query = f'fields name; where id = ({",".join(map(str, game["game_modes"]))});'
        response = wrapper.api_request(endpoint="game_modes", query=gm_query)

        modes = json.loads(response.decode('utf-8'))

        names = []
        for mode in modes:
            if mode["name"] != '':
                names.append(mode["name"])
    else:
        return []
    return names

def theme_names(game, wrapper):
    modes = []
    if "themes" in game:
        gt_query = f'fields name; where id = ({",".join(map(str, game["themes"]))});'
        response = wrapper.api_request(endpoint="themes", query=gt_query)

        themes = json.loads(response.decode('utf-8'))

        names = []
        for theme in themes:
            if theme["name"] != '':
                names.append(theme["name"])
    else:
        return []
    return names

def genre_names(game, wrapper):
    modes = []
    if "genres" in game:
        gt_query = f'fields name; where id = ({",".join(map(str, game["genres"]))});'
        response = wrapper.api_request(endpoint="genres", query=gt_query)

        themes = json.loads(response.decode('utf-8'))

        names = []
        for theme in themes:
            if theme["name"] != '':
                names.append(theme["name"])
    else:
        return []
    return names


def screenshots_urls(game, wrapper):
    shots = []
    if "screenshots" in game:
        sc_query = f'fields url; where id = ({",".join(map(str, game["screenshots"]))});'
        response = wrapper.api_request(endpoint="screenshots", query=sc_query)

        shots = json.loads(response.decode('utf-8'))

        urls = []
        for shot in shots:
            if shot["url"] != '':
                urls.append(shot["url"])
    else:
        return []

    return urls

def getCover(game):
    if "cover" in game and "image_id" in game["cover"]:
        cover = f'https://images.igdb.com/igdb/image/upload/t_cover_big/{game["cover"]["image_id"]}.jpg'
    else:
        cover = ''

    return cover

def getVideo(game, wrapper):
    url = ''
    if "videos" in game:
        video = random.choice(game["videos"])
        vd_query = f'fields video_id; where id = {video};'
        response = wrapper.api_request(endpoint="game_videos", query=vd_query)

        vd = json.loads(response.decode('utf-8'))

        try:
            url = 'https://www.youtube.com/embed/' + (vd["video_id"] if "video_id" in vd else [x["video_id"] for x in vd][0])
        except:
            url = ''

    return url

def getArtworks(game, wrapper):
    artworks = []
    if "artworks" in game:
        sc_query = f'fields url; where id = ({",".join(map(str, game["artworks"]))});'
        response = wrapper.api_request(endpoint="artworks", query=sc_query)

        artworks = json.loads(response.decode('utf-8'))

        urls = []
        for shot in artworks:
            if shot["url"] != '':
                urls.append(shot["url"])
    else:
        return []

    return urls


def getGameDetails(game, wrapper):
    game["mode_names"]          = mode_names(game, wrapper)
    game["theme_names"]         = theme_names(game, wrapper)
    game["genre_names"]         = genre_names(game, wrapper)
    game["screenshots_urls"]    = screenshots_urls(game, wrapper)
    game["image_url"]           = getCover(game)
    game["video_url"]           = getVideo(game, wrapper)
    game["artwork_urls"]        = getArtworks(game, wrapper)

    return game

def gameException(e):
    print(f'e: {e}')
    game = {}
    game["image_url"] = ''
    game["name"] = 'Oops...'
    game["summary"] = 'Oh no! An oopsie-doopsie ocuwwed >.< The little monkeys on our headquarters r working VEWY HAWD to solve the pwoblem UwU ***try reloading the page.***'
    return game