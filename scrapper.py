from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

rating_map = {
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5
}

data_books = []


for page in range(1, 51) :
    url = base_url.format(page)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books :
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = rating_map.get(book.find("p", class_="star-rating")["class"][1])
        avability = book.find("p", class_="instock availability").text.strip()

        data_books.append({
            "title" : title,
            "price" : price,
            "rating" : rating,
            "avability" : avability
        })

df = pd.DataFrame(data_books)
df.to_csv("data/books.csv", index=False)

print("Scraping completed. Data saved to data/books.csv")