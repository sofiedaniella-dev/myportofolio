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


### Tugas 3
1. 
- Mengapa kita menggunakan ModelForm?
Karena ModelForm otomatis membuat field dari model, memiliki validasi tipe data otomatis (`form.is_valid()`), lebih aman dari XSS/SQL Injection, dan mempermudah simpan data ke DB via `form.save()`.
- Mengapa CSRF Token Wajib?
`{% csrf_token %}` wajib untuk mencegah serangan *Cross-Site Request Forgery*. Token acak dipastikan cocok antara client dan server saat mengirim request POST/PUT/DELETE.

2. JSON lebih disukai dalam web modern karena:
* **Ukuran lebih kecil:** Tanpa tag pembuka/penutup seperti XML sehingga hemat bandwidth.
* **Parsing lebih cepat:** Langsung terbaca sebagai objek JavaScript native tanpa butuh DOM parser berat.
* **Lebih mudah dibaca:** Strukturnya ringkas dan standar untuk REST API modern.

3. Alur saat menggunakan fungsi view dalam bentuk JSON:
Request masuk > View mengambil data QuerySet dari DB > Serializer mengubah QuerySet jadi string JSON > View mengembalikan `HttpResponse` bernilai JSON.
Kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan karena Objek Python/QuerySet Django tidak bisa dikirim langsung melalui HTTP. Serialization mengubah objek kompleks tersebut menjadi teks JSON murni yang bisa dipahami browser/client.

