from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get("https://tuoitre.vn/the-gioi.html")

    soup = BeautifulSoup(response.content, "html.parser")

    #print(soup)

    titles = soup.findAll('h3', class_='box-title-text')
    links = [link.find('a').attrs["href"] for link in titles]
    news_data = []

    for link in links:
        news = requests.get("https://tuoitre.vn" + link)
        soup = BeautifulSoup(news.content, "html.parser")
        title = soup.find("h1", class_='detail-title').text
        abstract = soup.find("h2", class_='detail-sapo').text
        body = soup.find("div", class_='detail-content')
        image = body.find("img").get("src")

        news_data.append({
            'title': title,
            'abstract': abstract,
            'image': image,
            'url': "https://tuoitre.vn" + link
        })

    return render_template('index.html', news_data=news_data)

if __name__ == '__main__':
    app.run(debug=True)
