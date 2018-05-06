from flask import Flask, request, render_template, redirect, url_for, flash
import pytumblr

# Authenticate via API Key
client = pytumblr.TumblrRestClient('Bx7WX9YDTj9jn5ttururjm0a2OCIcOxc92u3fEHQho9NI6sKAE')
client.info()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_redir():
    return redirect(url_for('home', current=0))

@app.route('/from-<current>', methods=['GET','POST'])
def home(current):
    current = int(current)
    print ("Current value: {}".format(current))
    posts = client.tagged('landscape')
    photos = []
    for post in posts:
        if 'photos' not in post.keys(): continue
        for i in post['photos']:
            photos.append((i['original_size']['url']))
    #print ("Number of results: {} ".format(len(photos)))
    pic_pages = [[]]
    ind = 0
    #10 results per page
    for i in range(len(photos)):
        pic_pages[ind].append(photos[i])
        if i % 10 == 0 and i != 0:
            ind += 1
            pic_pages.append([])
    #current = 0
    print ('Number of pages {}'.format(len(pic_pages)))
    if request.method == 'GET':
        return render_template('index.html', current=current, pics=pic_pages[current], maxm=len(pic_pages) - 1)
    if request.method == 'POST':
        if request.form.get('submit') == 'Next Page':
            print ('Going to page {}'.format(current + 1))
            current += 1
            return render_template('index.html', current=current, pics=pic_pages[current if current < len(pic_pages) else current], \
                    maxm = len(pic_pages) - 1)
        elif request.form.get('submit') == 'Previous Page':
            print ('Going to page {}'.format(current - 1))
            current -= 1
            return render_template('index.html', current=current, pics=pic_pages[current if current > 0 else current], \
                    maxm = len(pic_pages) - 1)
