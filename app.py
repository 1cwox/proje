from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'cok-gizli-bir-anahtar'  # Güvenlik için değiştirin
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PROFILE_FOLDER = 'static/profiles'
PROFILE_ALLOWED = {'kiz.jpg', 'erkek.jpg'}

# --- Örnek Veriler ---
couple = {
    'names': 'Ayşe & Mehmet',
    'date': '14 Şubat 2022',
    'spotify': 'https://open.spotify.com/playlist/62FG0UGeRurtxdRlHsG0jj?si=ba16ba8c2aaf4cae',
    'story': 'Ayşe ve Mehmet bir kitapçıda tesadüfen karşılaştılar. O günden beri birlikte hayatı keşfediyorlar.',
}

TIMELINE_FILE = 'timeline.json'

def load_timeline():
    if os.path.exists(TIMELINE_FILE):
        with open(TIMELINE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [
        {'date': '14.02.2022', 'title': 'İlk Tanışma', 'desc': 'Kitapçıda karşılaştık.'},
        {'date': '01.03.2022', 'title': 'İlk Buluşma', 'desc': 'Kafede uzun bir sohbet.'},
        {'date': '14.04.2022', 'title': 'İlk Seyahat', 'desc': 'İzmir gezisi.'},
        {'date': '14.02.2023', 'title': '1. Yıl', 'desc': 'Birlikte geçen ilk yıl.'},
    ]

def save_timeline(timeline):
    with open(TIMELINE_FILE, 'w', encoding='utf-8') as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

def get_gallery():
    files = []
    for fname in os.listdir(UPLOAD_FOLDER):
        if fname.lower().split('.')[-1] in ALLOWED_EXTENSIONS:
            files.append(f'uploads/{fname}')
    files.sort(reverse=True)
    return files

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

countdown = {
    'target_date': '2026-01-14T00:00:00',  # ISO format, JS için uygun
    'desc': 'Birlikte 3. yılımıza kalan süre'
}

# --- Admin Giriş Bilgisi ---
ADMIN_USER = 'admin'
ADMIN_PASS = '1234'

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user == ADMIN_USER and pw == ADMIN_PASS:
            session['role'] = 'admin'
            return redirect(url_for('love'))
        else:
            return render_template('admin_login.html', error='Hatalı kullanıcı adı veya şifre!')
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect(url_for('love'))

@app.route('/upload', methods=['POST'])
def upload():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Yetkisiz'}), 403
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya yok'}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Geçersiz dosya'}), 400
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    return jsonify({'success': True, 'filename': f'uploads/{filename}'})

@app.route('/delete_photo', methods=['POST'])
def delete_photo():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Yetkisiz'}), 403
    fname = request.json.get('filename')
    if not fname or not fname.startswith('uploads/'):
        return jsonify({'error': 'Geçersiz dosya'}), 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], fname.replace('uploads/', ''))
    if os.path.exists(path):
        os.remove(path)
        return jsonify({'success': True})
    return jsonify({'error': 'Dosya bulunamadı'}), 404

@app.route('/add_timeline', methods=['POST'])
def add_timeline():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Yetkisiz'}), 403
    data = request.get_json()
    date = data.get('date')
    title = data.get('title')
    desc = data.get('desc')
    if not date or not title or not desc:
        return jsonify({'error': 'Eksik veri'}), 400
    timeline = load_timeline()
    timeline.insert(0, {'date': date, 'title': title, 'desc': desc})
    save_timeline(timeline)
    return jsonify({'success': True})

@app.route('/update_profile_photo', methods=['POST'])
def update_profile_photo():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Yetkisiz'}), 403
    if 'file' not in request.files or 'which' not in request.form:
        return jsonify({'error': 'Eksik veri'}), 400
    which = request.form['which']
    if which not in PROFILE_ALLOWED:
        return jsonify({'error': 'Geçersiz dosya adı'}), 400
    file = request.files['file']
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png']:
        return jsonify({'error': 'Geçersiz dosya türü'}), 400
    save_path = os.path.join(PROFILE_FOLDER, which)
    file.save(save_path)
    return jsonify({'success': True, 'filename': f'profiles/{which}'})

@app.route('/')
def love():
    gallery = get_gallery()
    is_admin = session.get('role') == 'admin'
    timeline = load_timeline()
    return render_template(
        'love.html',
        couple=couple,
        timeline=timeline,
        gallery=gallery,
        countdown=countdown,
        is_admin=is_admin
    )

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROFILE_FOLDER, exist_ok=True)
    app.run(debug=True) 