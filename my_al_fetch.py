import requests
import json
import time
from collections import deque

url = "https://api.jikan.moe/v3/user/kil_14/animelist/completed"
response = requests.request('GET', url)
animeresponse = json.loads(response.text)

def fetch_particular_anime_details(mal_ids):
    url_dynamic = 'https://api.jikan.moe/v3/anime/'
    with open('animeSynopsis.js', 'w') as file:
        file.write('export const bestAnime = [')
    while mal_ids:
        mal_id = mal_ids[0]
        api_response = requests.request('GET', url_dynamic+str(mal_id))
        if(api_response.status_code == 429):
            print("#################### stopped waiting for rate limiter ################")
            time.sleep(10)
        else: 
            mal_ids.popleft()
            json_response = json.loads(api_response.text)
            dumpdata = {'title': json_response['title'], 'title_english': json_response['title_english'],'image_url': json_response['image_url'], 
                        'url': json_response['url'], 'trailer_url':json_response['trailer_url'], 'synopsis': json_response['synopsis']}
            with open('animeSynopsis.js', 'a') as file:
                file.write(json.dumps(dumpdata)+",")
            print(json_response['title'])
    with open('animeSynopsis.js', 'a') as file:
        file.write("]")
    file.close()

list_9_10 = deque()
for anime in animeresponse['anime']:
    if(anime['score'] == 9 or anime['score'] == '10'):
        list_9_10.append(anime['mal_id'])

# print(list_9_10)
print(f'Total anime with ratings >= 9: {len(list_9_10)}')
fetch_particular_anime_details(mal_ids=list_9_10)


# trailer_url -> we can use this
# title_english -> english title