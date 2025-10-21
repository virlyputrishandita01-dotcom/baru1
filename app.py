from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
import os
import random, string
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import send_file, session
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "rahasia123"

SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"  # ganti dengan Secret Key dari Google

# ================ KONFIGURASI DATABASE =================
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   # isi jika ada
app.config['MYSQL_DB'] = 'portal_magang'

mysql = MySQL(app)

# ================ UPLOAD FOLDER =================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ================ DECORATOR ROLE-BASED =================
def login_required(role=None):
    """
    Gunakan @login_required(role='admin') atau @login_required(role='user')
    atau @login_required() (artinya hanya perlu login, role tidak dicek).
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            if 'loggedin' not in session:
                flash("❌ Anda harus login terlebih dahulu.", "danger")
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash("⚠️ Anda tidak memiliki akses ke halaman ini.", "warning")
                # arahkan ke dashboard sesuai role, jika ada
                if session.get('role') == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('dashboard'))
            return fn(*args, **kwargs)
        return decorated
    return wrapper

# ================ ROUTE: serve files (lihat di browser) =================
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Tampilkan file di browser (non-attachment)."""
    fname = os.path.basename(filename)
    full = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    if not os.path.isfile(full):
        flash("File tidak ditemukan.", "danger")
        return redirect(url_for('profile') if 'loggedin' in session and session.get('role') == 'user' else url_for('home'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], fname)

# ================ ROUTE: download attachment =================
@app.route('/download/<path:filename>')
@login_required()  # semua user harus login (admin atau user)
def download_surat(filename):
    """Download file sebagai attachment (pakai untuk surat_balasan)."""
    fname = os.path.basename(filename)
    full = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    if not os.path.isfile(full):
        flash("File tidak ditemukan.", "danger")
        # redirect sesuai role
        if 'role' in session and session.get('role') == 'admin':
            return redirect(url_for('admin'))
        return redirect(url_for('profile'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], fname, as_attachment=True)

# === FILTER UNTUK FORMAT TANGGAL ===
@app.template_filter('format_tanggal')
def format_tanggal(value):
    if not value:
        return ""
    try:
        # pastikan bisa parsing dari format ISO / DB (YYYY-MM-DD)
        tanggal_obj = datetime.strptime(str(value), "%Y-%m-%d")
        bulan_dict = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }
        bulan = bulan_dict[tanggal_obj.month]
        return f"{tanggal_obj.day} {bulan} {tanggal_obj.year}"
    except Exception:
        # kalau format di database beda, tampilkan apa adanya
        return str(value)

# ================ ROUTE UTAMA =================
@app.route('/')
def home():
    return render_template("index.html", title="Portal Magang")

@app.route('/contact')
def contact():
    return render_template("contact.html", title="Kontak Kami")

@app.route('/about')
def about():
    return render_template("about.html", title="Tentang Kami")


# ================ REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (nama,email,password,role) VALUES (%s,%s,%s,'user')",
                       (nama, email, password))
        mysql.connection.commit()
        cursor.close()
        flash("✅ Registrasi berhasil. Silakan login.", "success")
        return redirect(url_for('login'))

    return render_template("register.html", title="Register")


# ================ LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        recaptcha_response = request.form.get("g-recaptcha-response")
        
        # ✅ Verifikasi reCAPTCHA ke Google
        secret_key = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"  # ambil dari Google reCAPTCHA Admin Console
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {"secret": secret_key, "response": recaptcha_response}
        r = requests.post(verify_url, data=payload)
        result = r.json()

        if not result.get("success"):
            flash("❌ Verifikasi reCAPTCHA gagal. Silakan coba lagi.", "danger")
            return redirect(url_for('login'))
        
        # ✅ Cek user di database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['user_id'] = user['id']
            session['nama'] = user['nama']
            session['role'] = user['role']
            flash("✅ Login berhasil!", "success")
            if user['role'] == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Email atau password salah.", "danger")
            return redirect(url_for('login'))
        
    # GET: render login page. captcha image akan di-load dari /captcha
    return render_template("login.html", title="Login")

# ================ LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for('login'))

# ================ ROUTE CAPTCHA =================
def generate_captcha_text(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/captcha")
def captcha():
    # buat teks captcha dan simpan di session (uppercase)
    text = generate_captcha_text(6)
    session['captcha_text'] = text

    # pengaturan gambar
    width, height = 200, 70
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # cari font yang tersedia
    font = None
    possible_fonts = [
        "C:/Windows/Fonts/arial.ttf",  # Windows
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"  # Linux alternatif
    ]
    for f in possible_fonts:
        try:
            font = ImageFont.truetype(f, 36)
            break
        except Exception:
            font = None
    if font is None:
        font = ImageFont.load_default()

    # garis noise
    for _ in range(6):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=(160,160,160), width=1)

    # letakkan teks (acak offset)
    text_x = 15
    for ch in text:
        y = random.randint(5, 20)
        draw.text(
            (text_x, y),
            ch,
            font=font,
            fill=(20+random.randint(0,80), 20+random.randint(0,80), 20+random.randint(0,80))
        )
        text_x += font.getsize(ch)[0] + random.randint(0, 2)

    # titik noise
    for _ in range(300):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        draw.point((x,y), fill=(random.randint(150,255), random.randint(150,255), random.randint(150,255)))

    # blur
    image = image.filter(ImageFilter.GaussianBlur(0.8))

    # simpan ke BytesIO
    buf = io.BytesIO()
    image.save(buf, 'PNG')
    buf.seek(0)

    # jangan cache supaya selalu random
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    return send_file(buf, mimetype='image/png'), 200, headers

# ================ DASHBOARD USER =================
@app.route('/dashboard')
@login_required(role='user')
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


# ================ FORMULIR PENDAFTARAN =================
@app.route('/formulir', methods=['GET', 'POST'])
@login_required(role='user')
def formulir():
    if request.method == 'POST':
        # Ambil data umum
        jenis_pendaftar = request.form.get('jenis_pendaftar')
        nama = request.form.get('nama')
        email = request.form.get('email')
        hp = request.form.get('no_telp')
        tgl_mulai = request.form.get('tgl_mulai')
        tgl_akhir = request.form.get('tgl_selesai')
        
        # Cek apakah mahasiswa atau siswa
        universitas = request.form.get('universitas') if jenis_pendaftar == 'mahasiswa' else None
        sekolah = request.form.get('sekolah') if jenis_pendaftar == 'siswa' else None
        
        # debug print
        print("Jenis:", jenis_pendaftar)
        print("Universitas:", universitas)
        print("Sekolah:", sekolah)
        
        # Ambil file upload
        surat = request.files.get('surat_izin')
        proposal = request.files.get('proposal')

        surat_filename = None
        proposal_filename = None

        # Simpan file surat izin magang
        if surat and surat.filename:
            surat_filename = secure_filename(surat.filename)
            surat.save(os.path.join(app.config['UPLOAD_FOLDER'], surat_filename))

        if proposal and proposal.filename:
            proposal_filename = secure_filename(proposal.filename)
            proposal.save(os.path.join(app.config['UPLOAD_FOLDER'], proposal_filename))

        # Simpan ke database
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO pendaftaran
         (user_id, jenis_pendaftar, nama, email, no_telp, tgl_mulai, tgl_selesai, universitas, sekolah, surat_izin, proposal)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (
            int(session['id']), jenis_pendaftar, nama, email, hp, tgl_mulai, tgl_akhir,
            universitas, sekolah, surat_filename, proposal_filename
        ))
        mysql.connection.commit()
        cursor.close()

        flash("✅ Pendaftaran berhasil dikirim!", "success")
        return redirect(url_for('profile'))

    return render_template("pendaftaran.html", title="Formulir Pendaftaran")

# ================ PROFILE PESERTA =================
@app.route('/profile')
@login_required(role='user')
def profile():
    user_id = session['user_id']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """SELECT p.*, u.nama, u.email 
             FROM pendaftaran p
             JOIN users u ON p.user_id = u.id
             WHERE p.user_id = %s"""
    cur.execute(sql, (user_id,))
    hasil = cur.fetchone()
    cur.close()

    if not hasil:
        flash("Data pendaftaran belum ditemukan. Silakan isi formulir dulu.", "info")
        return redirect(url_for('formulir'))

    # hasil sudah DictCursor, jadi bisa langsung pakai key
    data = {
        "jenis_pendaftar": hasil['jenis_pendaftar'],
        "sekolah": hasil['sekolah'],
        "nama": hasil['nama'],
        "email": hasil['email'],
        "universitas": hasil['universitas'],
        "no_telp": hasil['no_telp'],
        "tgl_mulai": hasil['tgl_mulai'],
        "tgl_selesai": hasil['tgl_selesai'],
        "surat_izin": hasil['surat_izin'],
        "proposal": hasil['proposal'],
        "status": hasil['status'],
        "surat_balasan": hasil['surat_balasan'],
        "alasan_penolakan": hasil.get('alasan_penolakan', None),
    }

    return render_template("profile.html", data=data)


# ================ ADMIN =================
@app.route('/admin')
@login_required(role='admin')
def admin():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    search = request.args.get('search', '')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if search:
        like = f"%{search}%"
        sql = """SELECT p.*, u.nama, u.email
                 FROM pendaftaran p
                 JOIN users u ON p.user_id = u.id
                 WHERE u.nama LIKE %s OR u.email LIKE %s OR p.universitas LIKE %s OR p.status LIKE %s
                 ORDER BY p.id DESC
                 LIMIT %s OFFSET %s"""
        cursor.execute(sql, (like, like, like, like, per_page, offset))

        cursor_count = mysql.connection.cursor()
        cursor_count.execute("""SELECT COUNT(*)
                                FROM pendaftaran p
                                JOIN users u ON p.user_id = u.id
                                WHERE u.nama LIKE %s OR u.email LIKE %s OR p.universitas LIKE %s OR p.status LIKE %s""",
                             (like, like, like, like))
        total_pendaftar = cursor_count.fetchone()[0]
        cursor_count.close()
    else:
        sql = """SELECT p.*, u.nama, u.email
                 FROM pendaftaran p
                 JOIN users u ON p.user_id = u.id
                 ORDER BY p.id DESC
                 LIMIT %s OFFSET %s"""
        cursor.execute(sql, (per_page, offset))

        cursor_count = mysql.connection.cursor()
        cursor_count.execute("SELECT COUNT(*) FROM pendaftaran")
        total_pendaftar = cursor_count.fetchone()[0]
        cursor_count.close()

    data = cursor.fetchall()

    # FORMAT TANGGAL di sini
    for row in data:
        for field in ['tgl_mulai', 'tgl_selesai', 'created_at']:
            if field in row and row[field]:
                try:
                    date_obj = datetime.strptime(str(row[field]), "%Y-%m-%d")
                    row[field] = date_obj.strftime("%d %B %Y")
                except:
                    pass  # skip jika formatnya tidak sesuai

    # statistik (cursor terpisah)
    stat_cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    stat_cur.execute("SELECT COUNT(*) AS jumlah FROM pendaftaran WHERE status='sedang didisposisi'")
    disposisi = stat_cur.fetchone()['jumlah']
    stat_cur.execute("SELECT COUNT(*) AS jumlah FROM pendaftaran WHERE status='diterima'")
    diterima = stat_cur.fetchone()['jumlah']
    stat_cur.execute("SELECT COUNT(*) AS jumlah FROM pendaftaran WHERE status='ditolak'")
    ditolak = stat_cur.fetchone()['jumlah']
    stat_cur.close()
    cursor.close()

    total_pages = (total_pendaftar + per_page - 1) // per_page

    return render_template("admin.html",
                           data=data,
                           total_pendaftar=total_pendaftar,
                           disposisi=disposisi,
                           diterima=diterima,
                           ditolak=ditolak,
                           page=page,
                           total_pages=total_pages,
                           search=search,
                           title="Data Pendaftaran")

# ================ ADMIN DASHBOARD =================
@app.route('/admin/dashboard')
@login_required(role='admin')
def admin_dashboard():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # === Data Mahasiswa ===
    cur.execute("""
        SELECT 
            MONTH(tgl_mulai) AS bulan,
            COUNT(DISTINCT universitas) AS total_universitas,
            COUNT(user_id) AS total_mahasiswa
        FROM pendaftaran
        GROUP BY bulan
        ORDER BY bulan
    """)
    hasil = cur.fetchall()

    # === Data Sekolah / Siswa ===
    cur.execute("""
        SELECT 
            MONTH(tgl_mulai) AS bulan,
            COUNT(DISTINCT sekolah) AS total_sekolah,
            COUNT(user_id) AS total_siswa
        FROM siswa
        GROUP BY bulan
        ORDER BY bulan
    """)
    hasil_siswa = cur.fetchall()

    # === Hitung total keseluruhan ===
    cur.execute("SELECT COUNT(DISTINCT universitas) AS universitas FROM pendaftaran")
    total_universitas = cur.fetchone()['universitas']

    cur.execute("SELECT COUNT(*) AS mahasiswa FROM pendaftaran")
    total_mahasiswa = cur.fetchone()['mahasiswa']

    cur.execute("SELECT COUNT(DISTINCT sekolah) AS sekolah FROM siswa")
    total_sekolah = cur.fetchone()['sekolah']

    cur.execute("SELECT COUNT(*) AS siswa FROM siswa")
    total_siswa = cur.fetchone()['siswa']

    cur.close()

    # === Siapkan data untuk chart ===
    bulan_labels = []
    universitas_data = []
    mahasiswa_data = []
    sekolah_data = []
    siswa_data = []

    for i in range(1, 13):
        bulan_labels.append({
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }[i])
        # Mahasiswa
        m_row = next((r for r in hasil if r['bulan'] == i), {'total_mahasiswa': 0, 'total_universitas': 0})
        universitas_data.append(m_row['total_universitas'])
        mahasiswa_data.append(m_row['total_mahasiswa'])
        # Siswa
        s_row = next((r for r in hasil_siswa if r['bulan'] == i), {'total_siswa': 0, 'total_sekolah': 0})
        sekolah_data.append(s_row['total_sekolah'])
        siswa_data.append(s_row['total_siswa'])

    return render_template(
        "admin_dashboard.html",
        bulan_labels=bulan_labels,
        universitas_data=universitas_data,
        mahasiswa_data=mahasiswa_data,
        sekolah_data=sekolah_data,
        siswa_data=siswa_data,
        total_universitas=total_universitas,
        total_mahasiswa=total_mahasiswa,
        total_sekolah=total_sekolah,
        total_siswa=total_siswa
    )

# ================ ADMIN ACTIONS =================

# 1. Update status umum (misalnya disposisi)
@app.route('/admin/update_status/<int:id>/<string:status>')
@login_required(role='admin')
def update_status(id, status):
    allowed = ["surat diproses", "sedang didisposisi", "ditolak"]
    if status not in allowed:
        flash("Status tidak valid.", "danger")
        return redirect(url_for('admin'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE pendaftaran SET status=%s WHERE id=%s", (status, id))
    mysql.connection.commit()
    cur.close()

    flash(f"✅ Status diubah menjadi: {status}", "success")
    return redirect(url_for('admin'))


# 2. Accept pendaftaran (khusus untuk upload surat balasan + set status diterima)
@app.route('/admin/accept/<int:id>', methods=['GET', 'POST'])
@login_required(role='admin')
def accept_pendaftaran(id):
    if request.method == 'POST':
        # Admin upload surat balasan -> otomatis diterima
        f = request.files.get('surat_balasan')
        if f and f.filename:
            fname = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))

            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE pendaftaran SET status=%s, surat_balasan=%s WHERE id=%s",
                ("diterima", fname, id)
            )
            mysql.connection.commit()
            cur.close()

            flash("✅ Pendaftaran diterima & surat balasan diupload.", "success")
        else:
            flash("⚠ Pilih file surat balasan terlebih dahulu.", "warning")
        return redirect(url_for('admin'))

    # Kalau GET → langsung set status jadi diterima tanpa upload
    cur = mysql.connection.cursor()
    cur.execute("UPDATE pendaftaran SET status=%s WHERE id=%s", ("diterima", id))
    mysql.connection.commit()
    cur.close()

    flash("✅ Status diubah menjadi: diterima", "success")
    return redirect(url_for('admin'))

    # Tolak pendaftaran
@app.route('/admin/reject/<int:id>')
@login_required(role='admin')
def reject_pendaftaran(id):
    if request.method == 'POST':
        alasan = request.form.get('alasan', 'Maaf untuk saat ini magang di Pengadilan Agama Sidoarjo sudah penuh.')

    cur = mysql.connection.cursor()
    cur.execute("UPDATE pendaftaran SET status=%s WHERE id=%s", ("ditolak", id))
    mysql.connection.commit()
    cur.close()

    flash("❌ Pendaftaran ditolak dengan alasan telah disimpan.", "danger")
    return redirect(url_for('admin'))

    # Kalau GET, tampilkan form konfirmasi
    return render_template('reject_form.html', id=id)

# ================ surat balasan =================
@app.route("/upload_balasan/<int:id>", methods=["POST"])
def upload_balasan(id):
    if "surat_balasan" not in request.files:
        flash("Tidak ada file yang diupload", "error")
        return redirect(url_for("admin"))

    file = request.files["surat_balasan"]
    if file.filename == "":
        flash("Nama file kosong", "error")
        return redirect(url_for("admin"))

    # Simpan file ke folder uploads
    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    # Simpan nama file ke database
    cur = mysql.connection.cursor()
    cur.execute("UPDATE pendaftaran SET surat_balasan=%s WHERE id=%s", (filename, id))
    mysql.connection.commit()
    cur.close()

    flash("Surat balasan berhasil diupload", "success")
    return redirect(url_for("admin"))

# ================ RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
