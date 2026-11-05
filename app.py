from flask import Flask, render_template, request, flash, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

app.secret_key = 'kunci-rahasia-kantin-p06'

menu_list = [
    {
        'id': 1,
        'nama': 'Nasi Goreng Spesial',
        'harga': 'Rp 15.000',
        'kategori': 'Makanan',
        'deskripsi': 'Nasi goreng dengan bumbu rempah pilihan, telur mata sapi, dan kerupuk renyah.'
    },
    {
        'id': 2,
        'nama': 'Mie Ayam Bakso',
        'harga': 'Rp 13.000',
        'kategori': 'Makanan',
        'deskripsi': 'Mie kenyal gurih disajikan dengan suwiran ayam manis dan 2 butir bakso sapi.'
    },
    {
        'id': 3,
        'nama': 'Es Teh Manis Jumbo',
        'harga': 'Rp 5.000',
        'kategori': 'Minuman',
        'deskripsi': 'Teh melati segar disajikan dingin manis penyejuk dahaga saat istirahat kuliah.'
    }
]


@app.route('/')
def home():
    return render_template('index.html', menu_list=menu_list)


@app.route('/menu/<int:id>')
def detail_menu(id):
    menu = next((item for item in menu_list if item['id'] == id), None)
    return render_template('detail.html', menu=menu, id=id)


@app.route('/halo/<nama>')
def sapa_user(nama):
    return f"<h1>Halo, {escape(nama)}!</h1><p>Selamat datang di Kantin Kampus.</p>"


# ====================================================================
# FORM MASUKAN (KONTAK)
# ====================================================================
@app.route('/kontak', methods=['GET', 'POST'])
def kontak():
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        pesan = request.form.get('pesan', '').strip()

        errors = []
        if not nama:
            errors.append('Nama lengkap wajib diisi!')
        if not pesan:
            errors.append('Pesan masukan wajib diisi!')

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('kontak.html')

        flash(f'Terima kasih, {nama}! Masukan Anda telah berhasil dikirim.', 'success')
        return redirect(url_for('kontak'))

    return render_template('kontak.html')


# ====================================================================
# LOGIN ADMIN
# ====================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username', '').strip()
        p = request.form.get('password', '').strip()
        if u == 'admin' and p == '12345':
            flash('Login berhasil! Selamat datang, Admin Kantin.', 'success')
            return redirect(url_for('home'))
        flash('Username atau password salah! Coba lagi.', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')


# ====================================================================
# REGISTRASI MEMBER (P06: sanitasi + validasi sisi server)
# ====================================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 1. Tangkap & sanitasi input
        nama = request.form.get('nama', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm', '').strip()

        # 2. Wadah error collector
        errors = []

        if not nama:
            errors.append('Nama lengkap wajib diisi!')
        elif len(nama) < 3:
            errors.append('Nama minimal 3 huruf!')

        if not email:
            errors.append('Email wajib diisi!')
        elif '@' not in email or '.' not in email:
            errors.append('Format email tidak valid!')

        if not password:
            errors.append('Password wajib diisi!')
        elif len(password) < 6:
            errors.append('Password minimal 6 karakter!')

        if password != confirm:
            errors.append('Konfirmasi kata sandi tidak cocok!')

        # 3. Keputusan validasi
        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('register.html')

        flash(f'Selamat datang, {nama}! Pendaftaran berhasil.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
