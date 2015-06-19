import json
import os
from flask import Flask, redirect, url_for, render_template, request, session
from flask.ext.session import Session

from werkzeug import secure_filename
import indicoio

# hi
"What's up! Thanks for reaching out Dillon, made my day"

app = Flask(__name__)
# session allows you to share variables between pages
# by saving it to
sess = Session()

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['name'] = request.form.get('name', default='anon')
        path = os.path.dirname(os.path.abspath(__file__)) + "/static/img/pictures/" + session['name']

        selfie = request.files['file']
        if selfie and allowed_file(selfie.filename):
            filename = secure_filename(selfie.filename)
            if not os.path.exists(path):
                os.makedirs(path)
            selfie.save(os.path.join(path, filename))
    else:
        return render_template("upload.html")
    return render_template("index.html")


@app.route('/crunch', methods=['POST'])
def send_to_indico():

    path = os.path.dirname(os.path.abspath(__file__)) + "/static/img/pictures/" + session['name']

    selfie_list = []
    for f in os.listdir(path):
        new_path = os.path.join(path, f)
        if os.path.isfile(new_path) and f[f.index('.')+1:] in ALLOWED_EXTENSIONS:
            selfie_list.append(new_path)
    print selfie_list

    emotion_scores = indicoio.batch_fer(selfie_list, api_key="0f73d0a7c698469192cbd74886b48615")

    emotions = []
    emotion_values = []
    [emotions.extend(snapshot.keys()+['break']) for snapshot in emotion_scores]
    [emotion_values.extend(snapshot.values()+[0]) for snapshot in emotion_scores]

    print 'emotions', emotions, '\n', 'emotion_values', emotion_values
    return json.dumps({'scores': emotion_values, 'labels': emotions})


if __name__ == '__main__':
    app.config["UPLOAD_FOLDER"] = "/static/img/pictures/"
    app.config["SESSION_TYPE"] = "filesystem"

    app.secret_key = "woah it's a secret!"
    sess.init_app(app)

    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), processes=2)