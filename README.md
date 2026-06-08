# User Management API — Django & DRF

Project belajar backend Python menggunakan **Django** dan **Django REST Framework (DRF)**.  
Membangun REST API untuk manajemen user dengan PostgreSQL sebagai database.

> **Catatan nama repo:** `python-echo-explore-api` — kata *echo* merujuk pada fitur endpoint `/echo` yang memantulkan kembali detail request, bukan nama framework. Framework yang digunakan adalah **Django**.

---

## Tujuan Project

- Memahami cara kerja REST API dengan Django dan Django REST Framework
- Belajar konsep Serializer, ViewSet, dan Router di DRF
- Praktik koneksi Django ke PostgreSQL dengan skema kustom (`user_management`)
- Memahami cara kerja middleware untuk logging setiap request
- Eksplorasi struktur HTTP request melalui endpoint `/echo`

---

## Tech Stack

| Layer | Teknologi |
|---|---|
| Language | Python 3.11+ |
| Framework | Django 5.x |
| REST API | Django REST Framework (DRF) 3.15+ |
| Database | PostgreSQL 14+ |
| DB Driver | psycopg2-binary |
| CORS | django-cors-headers |
| Config | python-dotenv |

---

## Fitur

| Fitur | Deskripsi |
|---|---|
| **CRUD Users** | Create, Read, Update (PUT & PATCH), Delete data user |
| **Filter & Pagination** | Query params `skip`, `limit`, `is_active` pada list user |
| **Health Check** | Cek status service dan koneksi database secara real-time |
| **Echo Endpoint** | Memantulkan kembali detail request yang masuk — berguna untuk debugging |
| **Request Logging** | Middleware mencatat setiap request: method, path, status code, dan durasi |
| **CORS** | Konfigurasi Cross-Origin Resource Sharing via django-cors-headers |

---

## Struktur Folder

```
python-echo-explore-api/
├── apps/
│   ├── echo/               # Endpoint /echo — pantulkan detail request
│   │   ├── views.py
│   │   └── urls.py
│   ├── health/             # Endpoint /health — status service & database
│   │   ├── views.py
│   │   └── urls.py
│   └── users/              # CRUD User Management
│       ├── models.py       # Django Model (managed=False → tabel dikelola via sql/ddl.sql)
│       ├── serializers.py  # DRF Serializer (validasi & transformasi data)
│       ├── views.py        # ViewSet (logic handler tiap endpoint)
│       └── urls.py         # DRF Router
├── config/
│   ├── settings.py         # Konfigurasi Django
│   ├── urls.py             # Root URL dispatcher
│   ├── middleware.py       # Custom request logging middleware
│   ├── wsgi.py             # Entry point untuk Gunicorn (production)
│   └── asgi.py             # Entry point untuk Uvicorn / Daphne (async)
├── sql/
│   ├── ddl.sql             # DDL: buat schema, tabel, index, trigger
│   └── dml.sql             # DML: data awal (seed)
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Prasyarat

- Python **3.11+**
- PostgreSQL **14+**
- pip

---

## Cara Install

### 1. Clone repository

```bash
git clone https://github.com/<username>/python-echo-explore-api.git
cd python-echo-explore-api
```

### 2. Buat virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi environment

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit file `.env` sesuai konfigurasi database lokal:

```env
DB_NAME=go_explore
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=ganti-dengan-secret-key-yang-aman
DEBUG=true
ALLOWED_HOSTS=*
```

---

## Setup Database

### 1. Buat database di PostgreSQL

```sql
CREATE DATABASE go_explore;
```

### 2. Jalankan DDL — buat schema, tabel, index, dan trigger

```bash
psql -U postgres -d go_explore -f sql/ddl.sql
```

### 3. Jalankan DML — isi data awal

```bash
psql -U postgres -d go_explore -f sql/dml.sql
```

### 4. Jalankan migrasi Django

> Model `User` menggunakan `managed = False`, artinya Django tidak akan membuat atau mengubah tabel lewat migrasi.  
> Perintah ini hanya dibutuhkan untuk kebutuhan internal Django (tabel `django_content_type`, dll).

```bash
python manage.py migrate
```

---

## Menjalankan Aplikasi

```bash
python manage.py runserver
```

Server berjalan di: `http://localhost:8000`

Untuk port kustom:

```bash
python manage.py runserver 0.0.0.0:9000
```

---

## Endpoint API

### Health Check

| Method | URL | Deskripsi |
|---|---|---|
| `GET` | `/health` | Cek status service dan koneksi database |

**Contoh Response — service normal:**
```json
{
  "status": "ok",
  "service": "User Management API",
  "version": "1.0.0",
  "timestamp": "2026-06-08T07:00:00+00:00",
  "dependencies": {
    "database": { "status": "ok" }
  }
}
```

**Contoh Response — database tidak dapat dijangkau:**
```json
{
  "status": "degraded",
  "service": "User Management API",
  "version": "1.0.0",
  "timestamp": "2026-06-08T07:00:00+00:00",
  "dependencies": {
    "database": {
      "status": "error",
      "error": "could not connect to server: Connection refused"
    }
  }
}
```

---

### Echo

Endpoint ini **memantulkan kembali** semua detail request yang masuk — berguna untuk memahami struktur HTTP request, memeriksa header yang dikirim client, atau men-debug body yang diterima server.

| Method | URL | Deskripsi |
|---|---|---|
| `GET` / `POST` / `PUT` / `PATCH` / `DELETE` | `/echo` | Pantulkan kembali detail request |

**Contoh Response:**
```json
{
  "timestamp": "2026-06-08T07:00:00+00:00",
  "method": "POST",
  "path": "/echo",
  "full_url": "http://localhost:8000/echo",
  "query_params": {},
  "headers": {
    "Content-Type": "application/json",
    "User-Agent": "curl/8.0"
  },
  "body": { "pesan": "halo dari client" },
  "client": {
    "host": "127.0.0.1",
    "user_agent": "curl/8.0"
  }
}
```

---

### Users — CRUD

| Method | URL | Deskripsi |
|---|---|---|
| `GET` | `/api/v1/users/` | Daftar semua user |
| `POST` | `/api/v1/users/` | Tambah user baru |
| `GET` | `/api/v1/users/{id}/` | Detail user berdasarkan ID |
| `PUT` | `/api/v1/users/{id}/` | Ganti semua field user (semua field wajib dikirim) |
| `PATCH` | `/api/v1/users/{id}/` | Update sebagian field (hanya field yang ingin diubah) |
| `DELETE` | `/api/v1/users/{id}/` | Hapus user secara permanen |

#### Query Params — List Users

| Param | Tipe | Default | Keterangan |
|---|---|---|---|
| `skip` | `int` | `0` | Lewati N record pertama (offset) |
| `limit` | `int` | `10` | Jumlah record yang dikembalikan (maks: 100) |
| `is_active` | `true` / `false` | — | Filter berdasarkan status aktif |

**Contoh request dengan filter:**
```
GET /api/v1/users/?limit=5&skip=0&is_active=true
```

#### Body — POST / PUT

```json
{
  "username": "budi_s",
  "email": "budi@example.com",
  "full_name": "Budi Santoso",
  "phone": "08123456789"
}
```

#### Body — PATCH (semua field opsional)

```json
{
  "is_active": false
}
```

#### Contoh Response User

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Administrator",
  "phone": "081200000001",
  "is_active": true,
  "created_at": "2026-06-08T07:00:00+07:00",
  "updated_at": "2026-06-08T07:00:00+07:00"
}
```

---

## Konsep Django yang Dipelajari

| Konsep | Letak di Kode |
|---|---|
| Modular Django Apps | `apps/users/`, `apps/health/`, `apps/echo/` |
| Model `managed=False` | `apps/users/models.py` — tabel dikelola via SQL, bukan migrasi |
| DRF Serializer | `apps/users/serializers.py` — validasi input & format output |
| DRF ViewSet | `apps/users/views.py` — handler CRUD dalam satu class |
| DRF Router | `apps/users/urls.py` — generate URL otomatis dari ViewSet |
| Function-based View + `@api_view` | `apps/health/views.py`, `apps/echo/views.py` |
| Custom Middleware | `config/middleware.py` — logging setiap request |
| Django Settings via `.env` | `config/settings.py` + `python-dotenv` |

---

## Pengembangan Lebih Lanjut

- [ ] Autentikasi JWT dengan `djangorestframework-simplejwt`
- [ ] Pagination bawaan DRF (`PageNumberPagination`)
- [ ] Unit test dengan `pytest-django`
- [ ] Dokumentasi API otomatis dengan `drf-spectacular` (OpenAPI / Swagger)
- [ ] Django Admin panel untuk pengelolaan data via UI browser
- [ ] Containerize dengan Docker dan `docker-compose`
- [ ] Deploy production dengan Gunicorn + Nginx

---

## Lisensi

Project ini dibuat untuk keperluan belajar.
