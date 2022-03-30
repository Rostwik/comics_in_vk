import os
import pathlib
import urllib

import requests


def get_file_name(url_string):
    url_attributes = urllib.parse.urlsplit(url_string, scheme='', allow_fragments=True)
    url_path = urllib.parse.unquote(url_attributes.path, encoding='utf-8', errors='replace')
    file_name = os.path.split(url_path)[1]
    return file_name


def save_photo(directory_name, image_name, image_url, payloads=None, ext=''):
    pathlib.Path(directory_name).mkdir(exist_ok=True)
    response = requests.get(image_url, params=payloads)
    response.raise_for_status()
    path_to_save = f'{directory_name}/{image_name}{ext}'
    with open(path_to_save, 'wb') as file:
        file.write(response.content)


def is_vk_error(response):
    vk_response = response.json()

    error = vk_response.get('error')
    if error:

        raise requests.HTTPError(
            f"Код ошибки: {error['error_code']} \n"
            f"Описание ошибки:  {error['error_msg']}"
        )
