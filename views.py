from flask import Flask, request, render_template, redirect, url_for, flash
import pytumblr

# Authenticate via API Key
client = pytumblr.TumblrRestClient('Bx7WX9YDTj9jn5ttururjm0a2OCIcOxc92u3fEHQho9NI6sKAE')
client.info()
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        posts = client.tagged('landscape')
        photos = []
        for post in posts:
            if 'photos' not in post.keys(): continue
            for i in post['photos']:
                photos.append((i['original_size']['url']))
        #photos as set instead?
        pic_cols = [photos[i::4] for i in range(4)]
        return render_template('index.html', pics=photos, col_len=len(photos)/4, pic_cols=pic_cols)
