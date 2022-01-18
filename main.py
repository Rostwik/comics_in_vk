import os

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

    pictures_directory = 'images'
    comics = 353
    url = f'https://xkcd.com/{comics}/info.0.json'

    response = requests.get(url).json()
    print(response['alt'])

    img_name = get_file_name(response['img'])

    save_photo(pictures_directory, img_name[1], response['img'])

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
    album_id, upload_url, user_id = requests.get(vk_api_url, params=payloads).json()['response'].values()
    print(album_id, '\n', upload_url, '\n', user_id)

