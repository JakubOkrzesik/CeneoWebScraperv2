from numpy import extract
from app import app
from flask import render_template, redirect
import os
from numpy import average
import pandas as pd
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
import json

def get_item(ancestor, selector, attribute=None, return_list = None):
    try:
        if return_list:
            return [item.get_text().strip() for item in ancestor.select(selector)]
        if attribute:
            return ancestor.select_one(selector)[attribute]
        else:
            return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None
    
selectors = {
    'author' : ['span.user-post__author-name'],
    'recomendation': ['span.user-post__author-recomendation > em'],
    'star_amount' : ['span.user-post__score-count'],
    'useful' : ['button.vote-yes'],
    'useless' : ['button.vote-no'],
    'publish_date' : ['span.user-post__published > time:nth-child(2)', 'datetime'],
    'purchase_date' : ['span.user-post__published > time:nth-child(2)', 'datetime'],
    'pros' : ['div.review-feature__title--positives ~ div.review-feature__item', None, True],
    'cons' : ['div.review-feature__title--negatives ~ div.review-feature__item', None, True]
}






@app.route('/')
@app.route('/index')
@app.route('/index/<name>')
def index(name="Hello World"):
    return render_template("index.html.jinja", text=name)

@app.route('/extract/<product_id>')
def extract(product_id):
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"

    urls = []

    all_opinions = []

    while(url):
        response = requests.get(url)

        page = BeautifulSoup(response.text, 'html.parser')

        opinions = page.select('div.js_product-review')

        for opinion in opinions:
    
            single_opinion = {
                key:get_item(opinion, *value)
                    for key, value in selectors.items()
            }
            single_opinion["opinion_id"] = opinion["data-entry-id"]

            all_opinions.append(single_opinion)
        
        try:
            url = "https://www.ceneo.pl" + page.select_one('a.pagination__next')['href']
        except TypeError:
            url = None
        
        urls.append(url)


    with open(f'opinions/{product_id}.json', 'w', encoding='UTF-8') as f:
        json.dump(all_opinions, f, indent=4, ensure_ascii=False)


@app.route('/products')
def products():
    products = [filename.split('.')[0] for filename in os.listdir('opinions')]
    return render_template

@app.route('/about')
def about():
    pass

@app.route('/product/<product_id>')
def product(product_id):
    opinions = pd.read_json(f'opinions/{product_id}.json')
    print(opinions)

    opinions.stars = opinions.star_amount.map(lambda x: float(x.split('/')[0].replace(',', '.')))
    stats = {
        'opinions_count' : len(opinions.index),
        'pros_count' : opinions.pros.map(bool).sum(),
        'cons_count' : opinions.cons.map(bool).sum(),
        'average_count' : opinions.stars.mean().round(2)

    }
    
    recommendation = opinions.recomendation.value_counts(dropna = False).sort_index().reindex(['Nie polecam', 'Polecam', None])
    recommendation.plot.pie(
        label="", 
        autopct='%1.1f%%',
        colors=['crimson', 'lightskyblue', 'forestgreen'],
        labels=['Nie polecam', 'Polecam', 'Nie mam zdania']
        )

    plt.title('Rekomendacja')
    plt.savefig(f'app/static/plots/{product_id}_recommendations.png')
    plt.close()

    stars = opinions.stars.value_counts().sort_index().reindex(list())
    stars.plot.bar()
    plt.title('Oceny produktu')
    plt.xlabel('Liczba gwiazdek')
    plt.ylabel('Liczba opinii')
    plt.grid(True)
    plt.xticks(rotation=0)
    plt.show()
    plt.savefig(f"app/static/plots/{product_id}_stars.png")
    return render_template('products.html.jinja')