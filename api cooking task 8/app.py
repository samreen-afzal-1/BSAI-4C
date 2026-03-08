from flask import Flask, render_template, request, redirect
import requests
import json
import os

app = Flask(__name__)

SEARCH_API = "https://www.themealdb.com/api/json/v1/1/search.php?s="
INGREDIENT_API = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
CATEGORY_API = "https://www.themealdb.com/api/json/v1/1/filter.php?c="
CATEGORIES_LIST = "https://www.themealdb.com/api/json/v1/1/categories.php"
RANDOM_API = "https://www.themealdb.com/api/json/v1/1/random.php"

FAV_FILE="favorites.json"

if not os.path.exists(FAV_FILE):
    with open(FAV_FILE,"w") as f:
        json.dump([],f)

def load_fav():
    with open(FAV_FILE) as f:
        return json.load(f)

def save_fav(data):
    with open(FAV_FILE,"w") as f:
        json.dump(data,f,indent=4)


@app.route('/', methods=['GET','POST'])
def home():

    recipes=[]
    
    # Load categories
    categories_data=requests.get(CATEGORIES_LIST).json()
    categories=categories_data['categories']

    # Random chef suggestion
    suggestion=requests.get(RANDOM_API).json()['meals']

    if request.method=="POST":

        query=request.form.get('query')
        search_type=request.form.get('search_type')
        category=request.form.get('category')

        if category!="all":
            url=CATEGORY_API+category

        elif search_type=="ingredient":
            url=INGREDIENT_API+query

        else:
            url=SEARCH_API+query

        data=requests.get(url).json()

        if data['meals']:
            recipes=data['meals']

    return render_template(
        "index.html",
        recipes=recipes,
        suggestion=suggestion,
        categories=categories
    )


@app.route('/favorite',methods=['POST'])
def favorite():

    recipe=request.form.to_dict()

    fav=load_fav()
    fav.append(recipe)
    save_fav(fav)

    return redirect('/favorites')


@app.route('/favorites')
def favorites():

    recipes=load_fav()

    return render_template("favorites.html",recipes=recipes)


if __name__ == "__main__":
    app.run(debug=True)