## Описание

Программа сохраняет изображение комикса и комментарий автора. Комментарий автора появляется, если навести курсор на изображение [Пример комикса](https://xkcd.com/353/). Для этого используется [API](https://xkcd.com/json.html). Далее картинка и комментарий автора размещаются в группе во Вконтакте [VK](https://vk.com/) с использованием [API](https://dev.vk.com/reference)

## Требования к окружению

Для работы программы необходим установленный Python, pip.


## Как установить

Для корректной работы необходимо установить библиотеки.
Используйте pip для установки зависимостей:

```
pip install -r requirements.txt
```

## Как запустить программу

Необходимо создать файл .env в корне папки программы, и заполнить следующие параметры для подключения к бд:

- VK_ACCESS_TOKEN - access_token VK, используется для обращение к методам API VK

Далее из консоли запустить программу:

```
python main.py
```

Чтобы получить access_token, необходимо зарегистрировать приложение [Для разработчиков](https://dev.vk.com/) и далее пройти процедуру [Implicit Flow](https://dev.vk.com/api/access-token/implicit-flow-user). Обратите внимание на следующие нюансы:

- Убрать параметр redirect_uri у запроса на ключ
- Параметр scope указать через запятую, вот так: scope=photos,groups
- Если в адресной строке появился code= вместо access_token=, проверьте правильность параметра response_type

## Цель проекта

Автоматизировать работу администратора группы в Telegram.

