import os
import random

import requests
from dotenv import load_dotenv

from tools import save_photo, get_file_name, is_vk_error


def get_uploaded_vk_img_attributes(vk_access_token, vk_api_version, vk_group_id):
    payloads = {
        'access_token': vk_access_token,
        'v': vk_api_version,
        'group_id': vk_group_id,
    }
    upload_vk_attributes = get_vk_api_response(payloads, 'photos.getWallUploadServer')

    album_id, upload_url, user_id = upload_vk_attributes.json()['response'].values()

    comic_img_name = os.listdir('images')[0]

    vk_hash, photo, server = upload_vk_img(comic_img_name, upload_url)

    payloads = {
        'user_id': user_id,
        'group_id': vk_group_id,
        'photo': photo,
        'server': server,
        'hash': vk_hash,
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    uploaded_picture = post_vk_api_response(payloads, 'photos.saveWallPhoto')

    return comic_img_name, uploaded_picture, user_id


def post_vk_api_response(payloads, vk_api_method):
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    response = requests.post(vk_api_url, params=payloads)

    return response


def upload_vk_img(comic_img, upload_url):
    with open(f'images/{comic_img}', 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, files=files)

    response.raise_for_status()

    server, photo, vk_hash = response.json().values()

    return vk_hash, photo, server


def get_comic():
    current_comic_url = 'https://xkcd.com/info.0.json'
    response = requests.get(current_comic_url)
    response.raise_for_status()
    comics_number = response.json()['num']
    random_comic_number = random.randint(1, comics_number)

    url = f'https://xkcd.com/{random_comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    comic_title = comic['alt']
    img_name = get_file_name(comic['img'])

    return comic_title, img_name, comic['img']


def get_vk_api_response(payloads, vk_api_method):
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    response = requests.get(vk_api_url, params=payloads)

    response.raise_for_status()
    return response


def main():
    load_dotenv()

    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    vk_api_version = '5.131.'
    pictures_directory = 'images'

    comic_title, img_name, img_url = get_comic()

    save_photo(pictures_directory, img_name[1], img_url)

    comic_img_name, uploaded_picture, user_id = get_uploaded_vk_img_attributes(
        vk_access_token, vk_api_version, vk_group_id
    )
    try:
        is_vk_error(uploaded_picture)
    except requests.HTTPError as exp:
        print(exp)
    finally:
        comic_img_name = os.listdir('images')[0]
        os.remove(f'images/{comic_img_name}')

    vk_photo = uploaded_picture.json()['response'][0]

    payloads = {
        'user_id': user_id,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': f"photo{vk_photo['owner_id']}_{vk_photo['id']}",
        'message': comic_title,
        'access_token': vk_access_token,
        'v': vk_api_version
    }

    post_vk_wall_comic = post_vk_api_response(payloads, 'wall.post')

    try:
        is_vk_error(post_vk_wall_comic)
    except requests.HTTPError as exp:
        print(exp)


if __name__ == '__main__':
    main()
