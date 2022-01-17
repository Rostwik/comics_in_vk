import requests

from tools import save_photo, get_file_name

if __name__ == '__main__':
    pictures_directory = 'images'
    comics = 353
    url = f'https://xkcd.com/{comics}/info.0.json'

    response = requests.get(url).json()
    img_name = get_file_name(response['img'])

    print(response['img'], img_name)
    save_photo(pictures_directory, img_name[1], response['img'])
