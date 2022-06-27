from flask import Flask, jsonify, request, render_template
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/amazon', methods=["POST"])
def amazon():
    request_data = request.get_json()
    mytext=request_data['sendinfo']
    url='https://www.amazon.com/s?k={0}'.format(mytext)
    headers={"FUser":"XSaint","user-agent":"XSaint"}
    
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        urls=soup.find('div', attrs={"class":"s-main-slot s-result-list s-search-results sg-row"}).find_all('a',attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        urls_2=["https://www.amazon.com"+ i.get('href') for i in urls[0:10]]
        aux = []
        for k in urls[0:10]:
            rating = k.find('span', class_='a-size-medium a-color-base a-text-normal')
            rating2 = k.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            if rating:    
                aux.append(rating.text)
            elif rating2:
                aux.append(rating2.text)
            else:
                aux.append('None')
        return jsonify({"links": urls_2, "texto": aux})
    return jsonify({"answer":"failed"})


if __name__=="__main__":
    app.run(debug=True, port=5000)
    #app.run(debug=True, port=5000,host="0.0.0.0")