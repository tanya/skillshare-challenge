from flask import Flask, request, render_template, redirect, url_for, flash
import pytumblr
from werkzeug import import_string, cached_property

# Authenticate via API Key
client = pytumblr.TumblrRestClient('Bx7WX9YDTj9jn5ttururjm0a2OCIcOxc92u3fEHQho9NI6sKAE')
client.info()
#app = Flask(__name__)
pic_pages = [[]]

"""
class LazyView(object):
    def __init__(self, import_name):
        self.__name__ = import_name
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)
"""

#@app.route('/', methods=['GET', 'POST'])
def index(keyword=''):
    """
        - Gets images tagged with keyword (default: 'landscape') from Tumblr
        - Divides API response into 10 responses per page
        - Loads first page
    """

    global pic_pages

    def get_imgs(keyword):
        if keyword == '': keyword = 'landscape'
        pic_pages = [[]]
        posts = client.tagged(keyword)
        photos, ind = [], 0
        for post in posts:
            if 'photos' not in post.keys(): continue
            for i in post['photos']:
                photos.append((i['original_size']['url']))

        #10 results per page
        for i in range(len(photos)):
            pic_pages[ind].append(photos[i])
            if i % 10 == 0 and i != 0:
                ind += 1
                pic_pages.append([])
        print (len(pic_pages))
        return pic_pages

    if request.method == 'POST':
        keyword = request.form.get('query')
        pic_pages = get_imgs(keyword)
        return redirect(url_for('home', current=0))

    pic_pages = get_imgs('landscape')
    return redirect(url_for('home', current=0))

#@app.route('/page=<current>', methods=['GET','POST'])
def home(current):
    """
        - Handles subsequent requests
    """
    current = int(current)
    maxm = len(pic_pages) - 1
    #current is modified in frontend, for post
    return render_template('index.html', current=current, pics=pic_pages[current], maxm=maxm)

