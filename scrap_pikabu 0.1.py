# from bs4 import BeautifulSoup
# import requests
# import json
#
#
# def scrap_pars(urls):
#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.928 Yowser/2.5 Safari/537.36"
#     }
#     response = requests.get(urls, headers=headers)
#
#     src = response.text
#
#     with open("index.html", "w") as file:
#         file.write(src)
#     tag_list = {}
#     soup = BeautifulSoup(src, "lxml")
#     all_article = soup.find_all("article")
#
#     for item in all_article:
#         try:
#             _image = item.find(class_="story-image__image").get("data-src")
#         except AttributeError:
#             _image = "Нет изображения"
#         try:
#             tag = item.find("div", class_="story__tags tags story__tags_skeleton").text
#         except AttributeError:
#             tag = "Нет тега"
#         tag_list[tag.strip()] = _image
#
#     with open("post_info.json", "w") as file:
#         json.dump(tag_list, file, indent=4, ensure_ascii=False)
#
# def main():
#     scrap_pars("https://pikabu.ru/best")
#
# if __name__ == "__main__":
#     main()