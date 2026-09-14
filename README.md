Nama : Sofie Daniella Ang
NPM : 2506619562
Kelas : PBP E

### Tugas 1
1. 
2.
3.

### Tugas 2
1. Alur MVT Django

urls.py Proyek & Aplikasi: Menerima request URL pengguna dan mengarahkannya ke fungsi view yang sesuai.

View: Mengambil data dari Model, mengolah logika, lalu mengirimkannya ke Template.

Model: Mengakses database untuk mengambil data.

Template: Merender data dinamis ke dalam struktur HTML untuk ditampilkan di browser.

2. Alasan Menggunakan Model (Bukan Hardcoded)

Kemudahan Pemeliharaan: Mengubah/menambah data cukup lewat database (seperti Django Admin), tanpa harus mengedit kode HTML.

Skalabilitas: Memudahkan pemisahan logika tampilan dan data, serta memungkinkan fitur dinamis seperti filter, pencarian, dan penanganan data dalam jumlah besar.

3. Perbedaan makemigrations vs migrate

makemigrations: Membuat cetak biru (script migration) berdasarkan perubahan pada models.py (belum mengubah database).

migrate: Mengeksekusi script migration tersebut untuk mengubah struktur tabel di database secara nyata.

Contoh: Menambahkan field baru di models.py (misal: organization = models.CharField(...)) wajib menjalankan makemigrations lalu migrate.