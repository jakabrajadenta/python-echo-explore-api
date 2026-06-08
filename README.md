# Python Echo Explore API

Project belajar backend Python menggunakan **Django** dan **Django REST Framework (DRF)**.  
Mencakup CRUD User Management, Health Check endpoint, dan Echo endpoint untuk eksplorasi HTTP request-response.

---

## Tujuan Project

- Memahami konsep REST API dengan Django
- Belajar Django REST Framework (serializer, viewset, router)
- Eksplorasi struktur request HTTP melalui endpoint Echo
- Praktik koneksi Django ke PostgreSQL dengan skema kustom
- Memahami pola middleware untuk logging request

---

## Tech Stack

| Layer | Teknologi |
|---|---|
| Language | Python 3.11+ |
| Framework | Django 5.x |
| REST API | Django REST Framework 3.15+ |
| Database | PostgreSQL 14+ |
| DB Driver | psycopg2-binary |
| CORS | django-cors-headers |
| Config | python-dotenv |

---

## Fitur

| Fitur | Deskripsi |
|---|---|
| **CRUD Users** | Create, Read, Update, Delete data user |
| **Partial Update** | PATCH endpoint — update hanya field yang dikirim |
| **Filter & Pagination** | Query params `skip`, `limit`, `is_active` pada list user |
| **Health Check** | Cek status service dan koneksi database |
| **Echo Endpoint** | Memantulkan kembali seluruh detail request (method, headers, body, dsb) |
| **Request Logging** | Middleware mencatat setiap request: method, path, status, durasi |
| **CORS** | Konfigurasi Cross-Origin Resource Sharing |

---

## Struktur Folder

```
python-echo-explore-api/
├── apps/
│   ├── echo/               # Endpoint echo request-response
│   │   ├── views.py
│   │   └── urls.py
│   ├── health/             # Endpoint health check
│   │   ├── views.py
│   │   └── urls.py
│   └── users/              # CRUD User Management
│       ├── models.py       # Model Django (managed=False → pakai sql/ddl.sql)
│       ├── serializers.py  # DRF Serializer (validasi & transformasi data)
│       ├── views.py        # ViewSet (logic handler)
│       └── urls.py         # Router URL
├── config/
│   ├── settings.py         # Konfigurasi Django
│   ├── urls.py             # Root URL config
│   ├── middleware.py       # Request logging middleware
│   ├── wsgi.py             # Entry point WSGI (Gunicorn)
│   └── asgi.py             # Entry point ASGI (Uvicorn/Daphne)
├── sql/
│   ├── ddl.sql             # Buat tabel & trigger di PostgreSQL
│   └── dml.sql             # Data awal (seed)
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

### 1. Buat database PostgreSQL

```sql
CREATE DATABASE go_explore;
```

### 2. Jalankan DDL (buat tabel & trigger)

```bash
psql -U postgres -d go_explore -f sql/ddl.sql
```

### 3. Jalankan DML (isi data awal)

```bash
psql -U postgres -d go_explore -f sql/dml.sql
```

### 4. Jalankan migrasi Django

> Model `User` menggunakan `managed=False` — Django tidak menyentuh tabel.
> Migrasi ini hanya untuk kebutuhan internal Django (contenttypes, dll).

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
| `GET` | `/health` | Cek status service dan database |

**Contoh Response:**
```json
{
  "status": "ok",
  "service": "Python Echo Explore API",
  "version": "1.0.0",
  "timestamp": "2026-06-08T07:00:00+00:00",
  "dependencies": {
    "database": { "status": "ok" }
  }
}
```

---

### Echo

| Method | URL | Deskripsi |
|---|---|---|
| `GET` / `POST` / `PUT` / `PATCH` / `DELETE` | `/echo` | Pantulkan kembali detail request |

**Contoh Response:**
```json
{
  "timestamp": "2026-06-08T07:00:00+00:00",
  "method": "POST",
  "path": "/echo",
  "query_params": {},
  "headers": { "Content-Type": "application/json" },
  "body": { "pesan": "halo" },
  "client": { "host": "127.0.0.1" }
}
```

---

### Users (CRUD)

| Method | URL | Deskripsi |
|---|---|---|
| `GET` | `/api/v1/users/` | Daftar semua user |
| `POST` | `/api/v1/users/` | Tambah user baru |
| `GET` | `/api/v1/users/{id}/` | Detail user berdasarkan ID |
| `PUT` | `/api/v1/users/{id}/` | Update penuh (semua field wajib) |
| `PATCH` | `/api/v1/users/{id}/` | Update sebagian (hanya field yang dikirim) |
| `DELETE` | `/api/v1/users/{id}/` | Hapus user |

#### Query Params untuk List

| Param | Tipe | Default | Keterangan |
|---|---|---|---|
| `skip` | int | `0` | Lewati N record pertama (offset) |
| `limit` | int | `10` | Jumlah record maksimal (max: 100) |
| `is_active` | bool | - | Filter berdasarkan status aktif |

**Contoh:**
```
GET /api/v1/users/?limit=5&skip=0&is_active=true
```

#### Body untuk POST / PUT

```json
{
  "username": "budi_s",
  "email": "budi@example.com",
  "full_name": "Budi Santoso",
  "phone": "08123456789"
}
```

#### Body untuk PATCH (semua field opsional)

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

## Konsep yang Dipelajari

| Konsep | Letak di Kode |
|---|---|
| Django App (modular) | `apps/users/`, `apps/health/`, `apps/echo/` |
| Model dengan `managed=False` | `apps/users/models.py` |
| DRF Serializer | `apps/users/serializers.py` |
| DRF ViewSet | `apps/users/views.py` |
| DRF Router | `apps/users/urls.py` |
| Custom Middleware | `config/middleware.py` |
| Function-based View + `@api_view` | `apps/health/views.py`, `apps/echo/views.py` |
| Environment Config | `config/settings.py` + `.env` |

---

## Pengembangan Lebih Lanjut

- [ ] Tambah autentikasi JWT (djangorestframework-simplejwt)
- [ ] Tambah pagination bawaan DRF (`PageNumberPagination`)
- [ ] Tambah unit test dengan `pytest-django`
- [ ] Deploy dengan Gunicorn + Nginx
- [ ] Tambah Django Admin untuk pengelolaan data via UI
- [ ] Dockerize dengan `docker-compose`

---

## Lisensi

Project ini dibuat untuk keperluan belajar.
