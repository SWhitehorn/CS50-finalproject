from flask import Flask, render_template, redirect, request
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from random_words import RandomWords

app = Flask(__name__)
newsapi = NewsApiClient(api_key='4dfc7780dc9e4e09805c5ef6e302157e')

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    
    else:
        word = request.form.get("word")
        return news(word)


@app.route('/news')
def news(filter = ''):

    if filter == '':
        return random_word()

    else:
        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
        data = newsapi.get_everything(qintitle=filter, language='en', page_size=20, from_param=yesterday)
        articles = data['articles']
        articles = articles[:10]

        word = filter.capitalize()
        
        if data['totalResults'] == 0:
            return render_template('noresults.html', word=word)

        else:
            return render_template('results.html', articles=articles, word=word)


def random_word():
    
    rw = RandomWords()
    word = rw.random_word() 
    return news(word)

if __name__ == "__main__":
    app.run(debug=True)