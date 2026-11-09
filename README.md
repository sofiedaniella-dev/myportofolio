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

**Tugas 3 AI Use Disclosure**
Dalam pengerjaan tugas ini, saya memanfaatkan Generative AI (Gemini) sebagai assistant.
Tools yang digunakan:
1. Memberikan potongan kode Django yang sedang dikembangkan secara spesifik beserta pesan error atau perilaku yang tidak sesuai.
2. Meminta AI memberikan opsi perbaikan paling efisien dan langsung melakukan refactor sesuai dengan kebutuhan  tugas
3. Meminta penjelasan singkat mengenai konsep teoritis (seperti CSRF, JSON vs XML, dan Serialization) untuk mengembangkan pemahaman.


## AI Disclosure Tugas 4
Dalam pengerjaan Tugas 4, saya memanfaatkan Generative
AI (Gemini) sebagai assistant.
Tools yang digunakan:
1. Pengecekan dan Debugging kode Django beserta pesan error untuk membantu pengecekan dan meminta penjelasan error message yang muncul.
2. Membantu dalam refactoring kode agar lebih efisien.
3. Meminta skenario pengujian (checklist) untuk menguji 4 peran pengguna (guest, user, editor, superuser).


## Tugas 5
1. Debouncing adalah teknik untuk menunda eksekusi suatu fungsi hingga suatu jeda waktu berlalu tanpa event baru.
Debouncing penting diterapkan pada fitur pencarian AJAX agar dapat mencegah overload pada server, menghemat konsumsi bandwith internet, mencegah masalah respons yang tidak sesuai urutan, dan meningkatkan pengalaman pengguna (User Experience).

2. Penggunaan await pada fetch() berfungsi untuk menghentikan sementara (pause) eksekusi fungsi async sampai Promise yang dikembalikan oleh fetch() selesai diproses.
Jika kita tidak menggunakan await:
- variabel akan langsung menyimpan objek Promise yang statusnya masih pending (bukan data respon/hasil dari server)
- aplikasi akan menghasilkan error saat mencoba membaca/mengolah data tsb, karena data dari server belum benar-benar diterima.

3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!
XSS (Cross-Site Scripting) adalah jenis kerentanan keamanan web di mana penyerang berhasil menyisipkan skrip berbahaya ke dalam konten halaman web yang dipercayai oleh pengguna lain.
Data via AJAX/JavaScript lebih rentan dibanding Template Django karena Django Template engine memiliki auto-escaping secara default, Django memperlakukan karakter HTML menjadi bentuk entitas aman.

## AI Disclosure Tugas 5
Dalam pengerjaan Tugas 5, saya memanfaatkan Generative
AI (Gemini) sebagai alat bantu untuk memahami konsep dan debuggin kode, khususnya dalam penerapan AJAX dan fetch API yang awalnya terdapat error. Seluruh kode tetap saya implementasikan, uji, dan sesuaikan dengan struktur project yang telah saya kerjakan sebelumnya.


### Tugas 6
# 1. Konsep RESTful API, serta Perbedaan PUT dan PATCH
* **REST (Representational State Transfer)** adalah arsitektur standar dalam pembuatan layanan web yang memanfaatkan protokol HTTP secara konsisten untuk mengelola sumber daya. REST menekankan pada statelessness, interface yang seragam (*uniform interface*), serta penggunaan metode/verb HTTP secara tepat (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
* **Mengapa JSON saja belum cukup?** Mengembalikan format JSON saja hanya berarti API tersebut menggunakan format pertukaran data JSON (*JSON-over-HTTP*). Sebuah API baru dapat disebut **RESTful** apabila menerapkan prinsip-prinsip arsitektur REST secara utuh, seperti:
  1. **Resource-Based URLs:** Menggunakan URI yang merepresentasikan objek/entitas (misal: `/api/v1/projects/`).
  2. **Standard HTTP Verbs & Status Codes:** Memakai metode HTTP sesuai peruntukannya serta me-return HTTP Status Code yang tepat (`200`, `201`, `400`, `403`, `404`, `204`).
  3. **Stateless:** Setiap permintaan dari klien harus membawa semua informasi yang dibutuhkan server tanpa bergantung pada *state* dari permintaan sebelumnya.
  4. **HATEOAS / Uniform Interface:** Menyediakan struktur respons yang konsisten dan panduan navigasi status data.
* **Perbedaan `PUT` dan `PATCH`:**
  * **`PUT` (Full Replacement):** Digunakan untuk mengganti seluruh isi sumber daya yang ada dengan data baru yang dikirimkan. Semua field wajib disertakan dalam *payload*; field yang tidak dikirimkan akan dianggap kosong/direset ke nilai default.
    * *Contoh Penggunaan:* Mengganti seluruh profil pengguna di mana klien mengirimkan ulang seluruh data formulir profil lengkap.
  * **`PATCH` (Partial Update):** Digunakan untuk memperbarui hanya sebagian field pada sumber daya tanpa mengubah field lain yang tidak disebutkan dalam *payload*.
    * *Contoh Penggunaan:* Mengubah status star (`is_starred`) atau mengganti judul proyek saja tanpa perlu mengirimkan ulang deskripsi, URL, dan tech stack-nya.
# 2. Peran Serializer pada Django REST Framework (DRF)
* **Peran Serializer:** Serializer pada DRF bertindak sebagai jembatan dua arah antara tipe data kompleks di Django (seperti objek *Model QuerySet*) dan format data terstruktur yang mudah diproses via jaringan (seperti *JSON/XML*). Serializer menangani proses **Serialisasi** (Model → JSON) dan **Deserialisasi** (JSON → Model) sekaligus melakukan **validasi data input**.
* **Keuntungan dibandingkan `JsonResponse` Manual (Tutorial 05):**
  1. **Validasi Data Otomatis & Terpusat:** Serializer menyediakan metode validasi bawaan (`is_valid()`, `validate_<field>`) untuk sanitasi HTML (`strip_tags`), tipe data, dan konstrain unik tanpa perlu menulis kondisional `if-else` manual.
  2. **Pengurangan Boilerplate Code:** Menggunakan `ModelSerializer` secara otomatis memetakan field model ke dalam serializer secara aman tanpa perlu merakit `dict` manual baris demi baris.
  3. **Penanganan Field Relational & Calculated:** Memudahkan pembuatan field kalkulasi read-only (`SerializerMethodField`) seperti menghitung jumlah star (`star_count`) dan mengecek status login pengguna (`is_starred`).
  4. **Integrasi Browsable API:** DRF dapat secara otomatis meng-generate antarmuka GUI web (*Browsable API*) dan dokumentasi skema berkat struktur serializer.
# 3. Perbedaan Autentikasi vs Otorisasi & Pentingnya Permission Class di Server
* **Perbedaan Utama:**
  * **Autentikasi (Authentication):** Proses verifikasi *siapa* pengguna tersebut (memastikan identitas pengguna, misal: mengecek login username & password).
  * **Otorisasi (Authorization):** Proses penentuan *hak apa saja* yang boleh dilakukan oleh pengguna yang telah terautentikasi (memastikan izin akses, misal: apakah pengguna berunsur grup `Editor` boleh mengedit data).
* **Mengapa Harus Ditiadakan/Diperiksa di Server (Permission Class)?**
  * Menyembunyikan tombol di template HTML/JavaScript frontend **bukanlah fitur keamanan**, melainkan hanya peningkatan kenyamanan tampilan pengguna (*UX*).
  * Pengguna yang paham teknologi (*attacker* / pengguna biasa) dapat dengan mudah memotong (*bypass*) tampilan frontend dengan mengirimkan HTTP Request langsung ke API endpoint menggunakan tools seperti `cURL`, Postman, atau Console Browser.
  * Oleh karena itu, pemeriksaan hak akses wajib ditegakkan di sisi server melalui **Permission Class** (`IsPortfolioOwnerOrEditorOrReadOnly`) agar server secara tegas menolak permintaan tidak sah dengan status `403 Forbidden`.
# 4. Perlindungan CSRF pada SessionAuthentication dan Keterbatasan `force_authenticate`
* **Mengapa Tetap Membutuhkan Token CSRF?**
  * `SessionAuthentication` memanfaatkan cookie sesi (`sessionid`) browser untuk mengenali identitas pengguna yang sedang login.
  * Cookie disertakan secara otomatis oleh browser pada setiap HTTP Request yang mengarah ke domain aplikasi, termasuk permintaan lintas situs (*Cross-Site Request Forgery* / CSRF).
  * Jika permintaan yang mengubah data (`POST`, `PUT`, `PATCH`, `DELETE`) tidak dilindungi dengan header `X-CSRFToken`, penyerang bisa membuat situs jebakan yang memaksa browser korban mengirimkan permintaan perubahan data tanpa sepengetahuan korban.
* **Mengapa Test `force_authenticate` Belum Cukup?**
  * `force_authenticate(user=...)` pada `APITestCase` bekerja dengan cara membypass mekanisme autentikasi dan pemeriksaannya secara langsung pada objek `request.user` di level DRF untuk mempermudah pengujian logika logika permissions/view.
  * Perintah tersebut **tidak mensimulasikan alur autentikasi session HTTP nyata** dan **secara sengaja melewati jalur pemeriksaan middleware CSRF**.
  * Untuk membuktikan perlindungan CSRF berjalan dengan benar, pengujian harus menggunakan `APIClient(enforce_csrf_checks=True)` dengan metode `.login()`, lalu memverifikasi bahwa permintaan mutasi data tanpa header `X-CSRFToken` mengembalikan status `403 Forbidden`.

## AI Disclosure Tugas 6
Saya menggunakan Gemini sebagai alat bantu untuk memahami konsep teknis yang diminta tugas.

**AI Tool*
Gemini

**AI Chat Log*
https://share.gemini.google/jdTuPQypwpYz

