# CV Lens AI

AI toolkit berbasis Python untuk menganalisis CV terhadap deskripsi pekerjaan, menghitung skor kesesuaian bergaya ATS, dan menemukan skill gap secara transparan. Dibangun dengan FastAPI dan logika NLP yang ditulis dengan standard library Python, sehingga tidak membutuhkan API key berbayar dan data CV tidak perlu dikirim ke layanan pihak ketiga.

Project ini lahir dari pengalaman membangun SkillMap, platform AI untuk analisis CV dan rekomendasi karier. CV Lens AI adalah versi yang lebih ringan, fokus, dan dapat dipakai ulang sebagai layanan review CV, API untuk komunitas belajar, atau fondasi produk SaaS.

## Fitur Utama

- Skor ATS 0 sampai 100 dari gabungan kemiripan teks TF-IDF dan rasio skill yang cocok
- Deteksi skill otomatis berdasarkan taksonomi yang dapat diubah, mencakup programming, data dan AI, backend, frontend, dan soft skills
- Daftar matched skills dan missing skills yang jelas, bukan skor kotak hitam
- Rekomendasi perbaikan yang konkret dan dapat langsung ditindaklanjuti
- Ekstraksi kata kunci dari CV atau deskripsi pekerjaan
- Ringkasan ekstraktif untuk dokumen panjang
- Tersedia sebagai REST API dan command line interface

## Cara Kerja Skor

Skor akhir dihitung dengan rumus yang terbuka agar hasilnya dapat dijelaskan kepada pengguna maupun rekruter. Lima puluh persen berasal dari cosine similarity TF-IDF antara teks CV dan teks lowongan, dan lima puluh persen sisanya berasal dari proporsi skill pada lowongan yang juga ditemukan di CV. Implementasi TF-IDF ditulis manual dengan modul math dan collections untuk menunjukkan pemahaman konsep, bukan sekadar memanggil library.

## Menjalankan Project

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Buka dokumentasi interaktif di http://127.0.0.1:8000/docs setelah server berjalan.

## Memakai CLI

```bash
python cli.py analyze --cv examples/sample_cv.txt --job examples/sample_job.txt
python cli.py keywords --file examples/sample_cv.txt --top 10
python cli.py summarize --file examples/sample_job.txt
```

Contoh output analisis:

```json
{
  "ats_score": 54.87,
  "verdict": "Cukup selaras, masih bisa ditingkatkan",
  "text_similarity": 0.3751,
  "skill_match_ratio": 0.7222,
  "matched_skills": ["fastapi", "pandas", "python", "sql", "tensorflow"],
  "missing_skills": ["docker", "linux", "nlp", "pytorch", "scikit-learn"],
  "recommendations": ["Pelajari atau tampilkan skill yang belum ada di CV ini: docker, linux, nlp, pytorch, scikit-learn."]
}
```

Output di atas adalah hasil nyata dari file contoh pada folder examples, dan akan berbeda tergantung isi CV dan lowongan yang dipakai.

## Endpoint API

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| GET | / | Info aplikasi |
| GET | /health | Cek status server |
| POST | /analyze | Analisis CV terhadap deskripsi pekerjaan |
| POST | /keywords | Ekstraksi kata kunci |
| POST | /summarize | Ringkasan ekstraktif |

## Struktur Project

```
app/
  main.py            Aplikasi FastAPI
  schemas.py         Skema request dan response
  services/
    preprocessing.py Pembersihan teks dan tokenisasi
    skills.py        Taksonomi dan deteksi skill
    analyzer.py      TF-IDF, cosine similarity, dan scoring
    keywords.py      Ekstraksi kata kunci
    summarizer.py    Ringkasan ekstraktif
cli.py               Antarmuka command line
examples/            Contoh CV dan deskripsi pekerjaan
tests/               Unit test untuk logika inti
```

## Menjalankan Test

```bash
pytest -q
```

## Roadmap

- Upload dan ekstraksi teks dari file PDF
- Ekspor laporan analisis ke PDF
- Dukungan taksonomi skill per industri
- Dashboard web sederhana untuk pengguna non teknis

## Potensi Penggunaan

Toolkit ini dapat ditawarkan sebagai jasa review CV untuk mahasiswa dan pencari kerja, diintegrasikan ke komunitas atau platform belajar sebagai API, atau dikembangkan menjadi SaaS analisis CV dengan model berlangganan.

## Author

**Ade Bintang**

Mahasiswa Informatika Universitas Gunadarma dengan fokus pada AI Engineering dan Data Science. Pengalaman pada Python, machine learning, deep learning, dan pengembangan API dengan FastAPI melalui Coding Camp 2026 powered by DBS Foundation dan Asah 2026 led by Dicoding.

GitHub: [@kerb0y](https://github.com/kerb0y)

## License

MIT License. Lihat file LICENSE untuk detailnya.
