from flask import Flask, render_template, request, flash, redirect, url_for, json
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        event_description = request.form.get('event_description')
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Event created successfully!')
            return redirect(url_for('home'))

    event_name = request.args.get('event_name')
    event_description = request.args.get('event_description')
    image = request.args.get('image')

    return render_template('home.html', event_name=event_name, event_description=event_description, image=image)


@app.route('/host', methods=['GET'])
def host():
    return render_template('host.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return json.dumps({'filename': filename})


if __name__ == '__main__':
    app.run(debug=True)