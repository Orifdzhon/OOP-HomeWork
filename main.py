import requests
import json

text = input("Введите текст для картинки: ")
yadisk_token = "ваш_токен_яндекс_диска_здесь"

group_name = "GB-Python"

url = f"https://cataas.com/cat/says/{text}?width=400&height=400"
response = requests.get(url)

if response.status_code == 200:
    headers = {
        "Authorization": f"OAuth {yadisk_token}"
    }

    create_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
    params_folder = {"path": group_name}

    requests.put(create_folder_url, headers=headers, params=params_folder)

    safe_filename = "".join(c for c in text if c.isalnum() or c in (' ', '-', '_')).strip()
    if not safe_filename:
        safe_filename = "cat_image"

    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    params_upload = {
        "path": f"{group_name}/{safe_filename}.jpg",
        "overwrite": "true"
    }

    upload_response = requests.get(upload_url, headers=headers, params=params_upload)

    if upload_response.status_code == 200:
        href = upload_response.json()["href"]

        put_response = requests.put(href, data=response.content)

        if put_response.status_code == 201:
            info_url = "https://cloud-api.yandex.net/v1/disk/resources"
            info_params = {"path": f"{group_name}/{safe_filename}.jpg", "fields": "size"}

            info_response = requests.get(info_url, headers=headers, params=info_params)

            file_info = {
                "filename": f"{safe_filename}.jpg",
                "size": info_response.json()["size"],
                "path": f"{group_name}/{safe_filename}.jpg",
                "text": text
            }

            json_file = open("files_info.json", "w")
            json.dump([file_info], json_file)
            json_file.close()

            print(f"Картинка загружена в папку '{group_name}' на Яндекс.Диске")
            print(f"Создан файл files_info.json с информацией")
        else:
            print("Ошибка загрузки файла")
    else:
        print("Ошибка получения ссылки для загрузки")
else:

    print("Ошибка получения картинки")
