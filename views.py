from flask import Flask, request, render_template, redirect, url_for, flash
import pytumblr

# Authenticate via API Key
client = pytumblr.TumblrRestClient('Bx7WX9YDTj9jn5ttururjm0a2OCIcOxc92u3fEHQho9NI6sKAE')
client.info()
app = Flask(__name__)
pic_pages = [[]]

@app.route('/', methods=['GET', 'POST'])
def index(keyword=''):
    """
        - Gets images tagged with keyword (default: 'landscape') from Tumblr
        - Divides API response into 10 responses per page
        - Loads first page
    """
    if keyword == '': keyword = 'landscape'
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
    return redirect(url_for('home', current=0))

@app.route('/page=<current>', methods=['GET','POST'])
def home(current):
    """
        - Handles subsequent requests
    """
    current = int(current)
    maxm = len(pic_pages) - 1

    if request.method == 'GET':
        return render_template('index.html', current=current, pics=pic_pages[current], maxm=maxm)

    if request.method == 'POST':
        #current is modified in frontend
        return render_template('index.html', current=current, pics=pic_pages[current], maxm=maxm)
