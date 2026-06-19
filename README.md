# Kriptografi_Makalah_RDH

# 🔐 Reversible Data Hiding (RDH) - Bidirectional Histogram Shifting

Repositori ini berisi implementasi program antarmuka baris perintah (CLI) berbasis Python untuk melakukan steganografi pada citra medis digital menggunakan metode **Reversible Data Hiding (RDH)**. 

Algoritma yang digunakan adalah **Bidirectional Histogram Shifting** yang telah dimodifikasi untuk mengatasi masalah ketidakstabilan matriks piksel pada gambar radiologi (seperti X-Ray dan MRI) yang didominasi oleh latar belakang gelap/hitam absolut.

Proyek ini dikembangkan sebagai bagian dari eksperimen makalah tugas mata kuliah **II4021 Kriptografi**, Program Studi Sistem dan Teknologi Informasi, Institut Teknologi Bandung (ITB).

---

## ✨ Fitur Utama
1. **Penyisipan Data (*Embedding*)**: Menyisipkan teks Rekam Medis Elektronik (RME) rahasia ke dalam citra diagnostik dengan tingkat distorsi visual yang sangat rendah (PSNR rata-rata > 48 dB).
2. **Ekstraksi & Pemulihan (*Extraction & Recovery*)**: Mengekstrak data RME secara presisi 100% sekaligus merestorasi matriks piksel gambar penampung kembali ke wujud aslinya tanpa ada degradasi permanen (*lossless*).
3. **Pergeseran Dua Arah (*Bidirectional Shifting*)**: Mampu beradaptasi dan beroperasi dengan lancar meskipun nilai intensitas *Peak Point* lebih besar daripada *Zero Point* ($P > Z$).
4. **Generator Histogram**: Fitur bawaan untuk mengekstraksi dan menyimpan grafik analisis distribusi intensitas warna (*grayscale*) citra beserta penanda titik puncaknya.

---

## 🛠️ Prasyarat (Dependencies)
Pastikan Python 3.x sudah terpasang di sistem Anda. Anda memerlukan beberapa pustaka eksternal untuk menjalankan program ini. Instal pustaka yang dibutuhkan menggunakan `pip`:

```bash
pip install numpy Pillow matplotlib
```

---

# 🧑‍💻Cara Menjalankan
1. **Clone Repositori ke Lokal**
```bash
git clone [https://github.com/Nawafarai05/Kriptografi-Makalah-RD.git](https://github.com/Nawafarai05/Kriptografi-Makalah-RD.git)
cd Kriptografi-Makalah-RD
```
2. **Jalankan program utama**
```bash
python rdh.py
```
3. **Setelah dijalankan, Anda akan disambut dengan menu pilihan seperti di bawah ini.** Pilih saja sesuai kebutuhan dan ikuti arahan input yang dibutuhkan
``` bash
==================================================
 PROGRAM REVERSIBLE DATA HIDING (HISTOGRAM SHIFTING)
==================================================
1. Embed Pesan (Sisipkan data ke gambar)
2. Extract Pesan (Ambil data & pulihkan gambar)
3. Buat Grafik Histogram
4. Keluar
==================================================
```

Panduan Menu:

**Menu 1 (Embed Pesan)**: Anda akan diminta memasukkan nama file gambar asli (misal: chest_xray.png), teks pesan rahasia yang ingin disisipkan, dan nama keluaran citra stego (misal: stego_chest.png). Program akan otomatis mencetak nilai Peak Point, Zero Point, dan kalkulasi PSNR (dB).

**Menu 2 (Extract Pesan)**: Anda akan diminta memasukkan nama citra stego, nilai Peak dan Zero (yang didapatkan dari langkah Embed), serta nama untuk gambar pemulihan. Program akan mencetak pesan rahasia ke layar terminal dan menyimpan gambar yang telah dipulihkan.

**Menu 3 (Buat Grafik Histogram)**: Digunakan untuk melakukan inspeksi awal sebaran matriks sebelum steganografi dilakukan. Output berupa berkas gambar .png berisi grafik sebar.

---

# 🗃️Sturktur 
📦Kriptografi-Makalah-RD
 ┣ 📜 rdh.py                  # Skrip utama program RDH
 ┣ 📜 README.md               # Dokumentasi proyek ini
 ┣ 📜 chest_xray.png          # (Sampel) Citra Sinar-X Dada asli
 ┣ 📜 leg_xray.png            # (Sampel) Citra Sinar-X Kaki asli
 ┗ 📜 brain_xray.png          # (Sampel) Citra MRI Otak asli

---

# 👨‍💻 Penulis
Nawaf Amjad Rizqi A. Ismail (18223073)

Program Studi Sistem dan Teknologi Informasi, ITB
