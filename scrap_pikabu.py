from bs4 import BeautifulSoup
import requests
import json


def scrap_pars(urls):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.928 Yowser/2.5 Safari/537.36"
    }
    tag_list = []
    page = 1
    count = 1

    while True:
        params = {
            "page": page
        }

        response = requests.get(urls, headers=headers, params=params)
        src = response.text

        soup = BeautifulSoup(src, "html.parser")
        all_article = soup.find_all("article")

        if not all_article:
            break

        for item in all_article:
            try:
                _image = item.find(class_="story-image__image").get("data-src")
            except AttributeError:
                _image = "Нет изображения"
            try:
                tag = item.find("div", class_="story__tags tags story__tags_skeleton").text
            except AttributeError:
                tag = "Нет тега"

            tag_list.append({
                "номер поста": count,
                "изображение": _image,
                "Тег": tag.strip()
            })

        page += 1
        count += 1

    with open("post_info.json", "w") as file:
        json.dump(tag_list, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    scrap_pars("https://pikabu.ru/best")