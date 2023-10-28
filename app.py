from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connect_string = 'mongodb+srv://test:sparta@cluster0.kix0qsf.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'
client = MongoClient(connect_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    file = request.files["file_give"]
    profile = request.files["profile_give"]

    if file and profile:  # Pastikan kedua file telah diunggah
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        # Proses file yang diunggah
        extension = file.filename.split('.')[-1]
        filename = f'static/post-{mytime}.{extension}'
        file.save(filename)

        extension = profile.filename.split('.')[-1]
        profilefilename = f'static/profile-{mytime}.{extension}'
        profile.save(profilefilename)

        time = today.strftime('%Y.%m.%d')

        doc = {
            'file': filename,
            'profile': profilefilename,
            'title': title_receive,
            'content': content_receive,
            'time': time
        }
        db.diary.insert_one(doc)

        return jsonify({'msg': 'Upload complete!'})
    else:
        return jsonify({'error': 'No file provided'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
