# 🔒 Encryption App

Aplikasi GUI Python sederhana dengan gaya GitHub untuk **enkripsi** dan **dekripsi** file menggunakan `Fernet` dari library `cryptography`.  
Dibuat dengan antarmuka berbasis **Tkinter** dan dilengkapi sidebar navigasi untuk pengalaman pengguna yang nyaman.

---

## ✨ Fitur

✅ Enkripsi file dengan password  
✅ Dekripsi file terenkripsi dengan password  
✅ Penyimpanan key per file di local (`keys.json`)  
✅ Daftar key yang tersimpan bisa dilihat di menu **Pengaturan**  
✅ Sidebar responsif yang bisa dibuka/tutup  
✅ Tampilan dark mode mirip GitHub

---

## 📦 Struktur Folder

- `encrypted_files/` → Folder tempat file terenkripsi disimpan  
- `decrypted_files/` → Folder tempat file hasil dekripsi disimpan  
- `keys/keys.json` → File JSON untuk menyimpan key yang dipakai per file

---

## ⚙️ Cara Pakai

1️ **Install dependensi:**
```bash
pip install cryptography
```
2 **Jalankan program** 
```
python encryption_app.py
```
3️ **Di aplikasi**

- Masukkan password (key) di kolom input

- Pilih menu Enkripsi File → pilih file yang ingin dienkripsi

- Pilih menu Dekripsi File → pilih file terenkripsi dari daftar

- Cek semua key yang tersimpan di menu Pengaturan

## Catatan Penting
>Password (key) yang kamu masukkan di-generate dengan SHA-256, sehingga hasil enkripsi sangat bergantung pada password yang dipakai.
Jika password salah saat dekripsi, file tidak akan bisa dibuka dan akan muncul error.
Simpan baik-baik file keys.json jika kamu ingin melihat key yang pernah dipakai.

##  Teknologi
>Python 3

>Tkinter (GUI)

>Cryptography (Fernet)

## Lisensi
Proyek ini dibuat untuk belajar dan pengembangan pribadi.
Feel free untuk fork, modifikasi, dan gunakan sesuai kebutuhan! 🚀

