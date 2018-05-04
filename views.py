from flask import Flask, request, render_template, redirect, url_for, flash
import pytumblr

# Authenticate via OAuth
"""client = pytumblr.TumblrRestClient(
  'Bx7WX9YDTj9jn5ttururjm0a2OCIcOxc92u3fEHQho9NI6sKAE',
  '00S9eupdPNaa1P4PBlyH8wTHN5qf6K3kLs5aXK7Uz9KlNt4cN5',
  'us7HkfHaGH64WHqmBZVjIm7YZExdyQrKuWCKYGu51HzNOyQcmh',
  '2JX4QQm7pOZeh9Pz6oflvEni98GhmGSX0ufe6t6PAVx7DXnz1j'
)"""

# Authenticate via API Key
client = pytumblr.TumblrRestClient('Bx7WX9YDTj9jn5ttururjm0a2OCIcOxc92u3fEHQho9NI6sKAE')

# Make the request
#client.tagged('cinemagraph')

# Make the request
client.info()
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        posts = client.tagged('vaporwave')
        photos = set()
        for post in posts:
            if 'photos' not in post.keys(): continue
            for i in post['photos']:
                photos.add((i['original_size']['url']))
        pics = list(photos)
        pic_cols = [pics[i::4] for i in range(4)]
        return render_template('index.html', pics=list(photos), col_len=len(list(photos))/4, pic_cols=pic_cols)
    #if request.method == 'POST':
