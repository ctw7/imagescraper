from bottle import route, run, Bottle, request
from bs4 import BeautifulSoup as bs4
import requests

app = Bottle()

# receive url from user
@app.route('/imgscraper')
def get_url():
    return '''
        <form action="/getimages" method='POST'>
            <input name="inputurl" type="url" />
            <input value="Scrape Images" type="submit" />
        </form>
    '''

# return images to user
@app.route('/getimages', method=['GET', 'POST'])
def get_images():
    # get the users input url
    url = request.forms.get('inputurl')

    # gets html from the url, parses it, and finds all img srcs
    def collect_image_srcs():
        image_sources = []

        # image_source filters
        file_type = ['png', 'jpg']
        src_type = ['src', 'data-src']

        # parse inputurl for all html img tags
        html_page = requests.get(url)
        soup = bs4(html_page.content, 'html.parser')
        images = soup.findAll('img')

        # for each image
        for i in images:
            # with a desired file type
            for f in file_type:
                # from the given source
                for s in src_type:
                    # if it meets all of the above, add it to list
                    if s in i.attrs and f in str(i[s]):
                        image_sources.append(i[s])
                    else:
                        continue

        # print(image_sources)
        return image_sources
    
    # TODO create func to return images to client as an html img gallery

    collect_image_srcs()

run(app, host='localhost', port=8080, debug=True)