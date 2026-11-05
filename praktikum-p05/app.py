from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = 'oka'

# Data menu kantin kampus sederhana untuk praktikum
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
        'deskripsi': 'Teh melati segar disajikan dingin manis penyejuk dahaga saat kuliah terik.'
    }
]

@app.route('/')
def home():
    return render_template('index.html', menu_list=menu_list)

# Tambahkan di PALING BAWAH app.py:

# 1. Rute Dinamis Detail Menu (Converter Integer: <int:id>)
@app.route('/menu/<int:id>')
def detail_menu(id):
    menu = next((item for item in menu_list if item['id'] == id), None)
    return render_template('detail.html', menu=menu, id=id)

# 2. Rute Dinamis Salam Pelanggan (Variable Rule String: <nama>)
@app.route('/halo/<nama>')
def sapa_user(nama):
    return f"<h1>Halo, {nama}!</h1><p>Selamat datang di Kantin Kampus.</p>"

@app.route('/kontak', methods=['GET', 'POST'])
def kontak():
    if request.method == 'POST':
        nama = request.form.get('nama')
        pesan = request.form.get('pesan')
        flash(f'Terima kasih, {nama}! Masukan Anda telah berhasil dikirim.', 'success')
        return redirect(url_for('kontak'))
    return render_template('kontak.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u == 'admin' and p == '12345':
            flash('Login berhasil! Selamat datang, Admin Kantin.', 'success')
            return redirect(url_for('home'))
        flash('Username atau password salah! Coba lagi.', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
