import os
import random

import requests

from tools import save_photo, get_file_name
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    # vk_api_method = 'groups.get'
    vk_api_method = 'photos.getWallUploadServer'
    vk_api_version = '5.131.'
    vk_user_id = 840163
    vk_group_id = 210209209
    vk_application_id = 8054782

    pictures_directory = 'images'

    current_comic_url = 'https://xkcd.com/info.0.json'
    response = requests.get(current_comic_url)
    response.raise_for_status()
    comics_number = response.json()['num']
    random_comic = random.randint(1, comics_number)

    url = f'https://xkcd.com/{random_comic}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()
    comics_title = comics['alt']
    img_name = get_file_name(comics['img'])

    save_photo(pictures_directory, img_name[1], comics['img'])

    # payloads = {
    #     'access_token': vk_access_token,
    #     'v': vk_api_version,
    #     'user_id': vk_user_id,
    #
    # }
    payloads = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'group_id': vk_group_id,

    }
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    response = requests.get(vk_api_url, params=payloads)
    response.raise_for_status()
    album_id, upload_url, user_id = response.json()['response'].values()

    files = os.listdir('images')
    comic_img = files[0]

    with open(f'images/{comic_img}', 'rb') as file:
        files = {
            'photo': file
        }

        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        server, photo, hash = response.json().values()

    vk_api_method = 'photos.saveWallPhoto'

    payloads = {
        'user_id': user_id,
        'group_id': vk_group_id,
        'photo': photo,
        'server': server,
        'hash': hash,
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    response = requests.post(vk_api_url, params=payloads)
    response.raise_for_status()
    uploaded_picture = response.json()['response'][0]

    vk_api_method = 'wall.post'
    payloads = {
        'user_id': user_id,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': f"photo{uploaded_picture['owner_id']}_{uploaded_picture['id']}",
        'message': comics_title,
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    response = requests.post(vk_api_url, params=payloads)
    response.raise_for_status()

    os.remove(f'images/{comic_img}')
