from flask import Flask, render_template, request
from flask_cors import cross_origin
import requests
from bs4 import BeautifulSoup
import logging
from requests.exceptions import RequestException

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
@cross_origin()
def index(): 
    if request.method == 'POST':
        try:
            # query to search for images
            query = request.form['content'].replace(" ","")

            # fake user agent to avoid getting blocked by Google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            # fetch the search results page
            response = requests.get(f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M", headers=headers, timeout=10)

            # parse the HTML using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # find all img tags
            image_tags = soup.find_all("img")

            # Get image url of each image
            del image_tags[0]
            img_urls=[]
            for image_tag in image_tags:
                # get the image source URL
                image_url = image_tag['src']
                if image_url:
                    img_urls.append(image_url)
        
            return render_template('index.html', images=img_urls)
        
        except RequestException as req_err:
            logging.error("Request error: %s", req_err)
            return "An error occurred while trying to fetch the images."

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
