from app import app
from flask import render_template, redirect, url_for, request
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
import json
from app.models.product import Product
from app.utils import get_item

plt.switch_backend('Agg')


    
@app.route('/')

def index():
    return render_template('index.html.jinja')


@app.route('/extract', methods=['POST', 'GET'])
def extract():
    
    if request.method == 'POST':

        product_id = request.form.get("product_id")
        product = Product(product_id)
        product.extract_product()

        
        return redirect(url_for('product', product_id = product_id))
    else:
        return render_template('extract.html.jinja')

@app.route('/products')
def products():
    products = [filename.split('.')[0] for filename in os.listdir('app/opinions')]
    return render_template('products.html.jinja', products = products)

@app.route('/about')
def about():
    return render_template('about.html.jinja')

@app.route('/product/<product_id>')
def product(product_id):
    opinions = pd.read_json(f"app/opinions/{product_id}.json")
    opinions['stars'] = opinions['stars'].map(lambda x: float(x.split("/")[0].replace(",", ".")))
    stats = {
        "opinions_count": len(opinions.index),
        "pros_count": opinions['pros'].map(bool).sum(),
        "cons_count": opinions['cons'].map(bool).sum(),
        "average_score": opinions['stars'].mean().round(2)
    }
    if not os.path.exists("app/plots"):
        os.makedirs("app/plots")
    recommendation = opinions.recommendation.value_counts(dropna = False).sort_index().reindex(["Nie polecam", "Polecam", None])
    recommendation.plot.pie(
        label="", 
        autopct="%1.1f%%", 
        colors=["crimson", "forestgreen", "lightskyblue"],
        labels=["Nie polecam", "Polecam", "Nie mam zdania"]
    )
    plt.title("Rekomendacja")
    plt.savefig(f"app/static/plots/{product_id}_recommendations.png")
    plt.close()

    stars = opinions['stars'].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
    stars.plot.bar(color = 'pink')
    plt.title("Oceny produktu")
    plt.xlabel("Liczba gwiazdek")
    plt.ylabel("Liczba opinii")
    plt.grid(True, axis='y')
    plt.xticks(rotation=0)
    plt.savefig(f"app/static/plots/{product_id}_stars.png")
    plt.close()
    return render_template("product.html.jinja", stats=stats, product_id=product_id, opinions=opinions)