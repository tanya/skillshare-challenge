import views
from werkzeug import import_string, cached_property
from flask import Flask
from lazyview import LazyView

app = Flask(__name__)
app.add_url_rule('/', methods=['GET','POST'],
                 view_func=LazyView('views.index'))
app.add_url_rule('/page=<current>', methods=['GET','POST'],
                 view_func=LazyView('views.home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
