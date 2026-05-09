# Product Requirements Document (PRD)
# 🌦️ SEAWeather — Informatics Dashboard Cuaca Asia Tenggara

**Versi:** 1.1.0 *(Revised)*
**Tanggal:** April 2026
**Status:** Revised Draft
**Tech Stack:** Shiny Python + Weatherstack API (Free Plan)
**Author:** Alfa Pradana

> **📝 Changelog v1.0 → v1.1:**
> Setelah verifikasi response JSON aktual dari endpoint `GET /current`, ditemukan bahwa **Free Plan Weatherstack ternyata mengembalikan data `astro` (astronomi) dan `air_quality` (kualitas udara)** secara langsung — data ini sebelumnya diasumsikan tidak tersedia. PRD ini direvisi untuk memanfaatkan temuan tersebut secara penuh, termasuk penambahan dua panel fitur baru: **Panel Langit & Astronomi** dan **Panel Kualitas Udara (AQI)**.
>
> **Perubahan utama:** Tabel data API (§5.2), fitur baru §5.6 & §5.7, peringatan baru §5.8, layout UI (§8.2), Data Model cache (§9.1), scope update (§10), dan revisi timeline (§11).

---

## 📋 Daftar Isi

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Target User & Use Case](#3-target-user--use-case)
4. [API Constraints & Strategy](#4-api-constraints--strategy)
5. [Fitur & Functional Requirements](#5-fitur--functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Arsitektur Aplikasi](#7-arsitektur-aplikasi)
8. [UI/UX Specification](#8-uiux-specification)
9. [Data Model](#9-data-model)
10. [Batasan & Out of Scope](#10-batasan--out-of-scope)
11. [Milestones & Timeline](#11-milestones--timeline)
12. [Risiko & Mitigasi](#12-risiko--mitigasi)

---

## 1. Executive Summary

**SEAWeather** adalah dashboard informatif berbasis Shiny Python yang menampilkan data cuaca real-time untuk kota-kota di wilayah Asia Tenggara, ditenagai oleh Weatherstack API Free Plan. Produk ini dirancang untuk dua segmen utama: pelancong yang ingin memantau kondisi cuaca sebelum bepergian, dan masyarakat di wilayah dengan kondisi cuaca tidak menentu.

Verifikasi aktual terhadap response API menunjukkan bahwa **Free Plan memberikan data yang jauh lebih kaya dari dokumentasi resmi**, mencakup tiga kelompok data utama:

| Kelompok Data | Field | Status |
|---------------|-------|--------|
| ☁️ **Cuaca Standar** | Suhu, kelembaban, angin, tekanan, visibilitas, UV, awan | ✅ Tersedia |
| 🌙 **Astronomi** | Sunrise, sunset, moonrise, moonset, moon phase, moon illumination | ✅ **Tersedia (baru dikonfirmasi)** |
| 🫁 **Kualitas Udara** | CO, NO₂, O₃, SO₂, PM2.5, PM10, EPA Index, DEFRA Index | ✅ **Tersedia (baru dikonfirmasi)** |

Temuan ini secara signifikan memperluas nilai dashboard tanpa menambah konsumsi API call.

---

## 2. Problem Statement

### 2.1 Masalah yang Diidentifikasi

| # | Masalah | Dampak |
|---|---------|--------|
| 1 | Pelancong sulit menemukan cuaca real-time untuk kota-kota ASEAN dalam satu platform | Pengambilan keputusan perjalanan yang kurang optimal |
| 2 | Tidak ada dashboard yang menggabungkan cuaca, kualitas udara, dan pola musiman | Masyarakat tidak siap menghadapi perubahan cuaca & polusi |
| 3 | Tidak ada informasi astronomi (sunrise/sunset) yang mudah diakses saat traveling | Pelancong tidak bisa merencanakan aktivitas outdoor optimal |
| 4 | Kualitas udara di kota-kota ASEAN sering buruk namun tidak mudah dipantau | Risiko kesehatan bagi penduduk & wisatawan (PM2.5 Jakarta: 81.45) |
| 5 | Tidak ada fitur "sticky" yang membuat user kembali | Rendahnya user retention |

### 2.2 Proposisi Nilai

> "Satu dashboard, semua yang perlu Anda tahu tentang langit Asia Tenggara — cuaca real-time, kualitas udara, pola musim, dan info astronomi dalam tampilan yang memukau."

---

## 3. Target User & Use Case

### 3.1 Persona Utama

#### 🎒 Persona A: Si Pelancong
- **Profil:** Usia 22–40 tahun, sering bepergian antar negara ASEAN, tech-savvy
- **Pain Point:** Harus membuka banyak tab untuk cuaca, kualitas udara, dan info sunrise destinasi
- **Goal:** Satu tempat untuk semua info sebelum packing & saat di perjalanan
- **Use Case Utama:**
  - Cek cuaca + AQI kota tujuan sebelum berangkat
  - Lihat jam sunrise/sunset untuk merencanakan aktivitas outdoor & foto
  - Pantau apakah sedang musim hujan di destinasi

#### 🏠 Persona B: Warga Wilayah Cuaca Tidak Menentu
- **Profil:** Usia 18–55 tahun, tinggal di daerah tropis/kepulauan
- **Pain Point:** Kualitas udara memburuk tanpa peringatan, cuaca berubah drastis
- **Goal:** Monitor harian kondisi cuaca & udara lokal
- **Use Case Utama:**
  - Cek AQI tiap pagi sebelum aktivitas outdoor
  - Pantau panel musim untuk antisipasi musim hujan/kemarau
  - Lihat fase bulan untuk keperluan nelayan/pertanian

#### 🔬 Persona C (Baru): Peneliti / Mahasiswa Epidemiologi & Kesehatan Lingkungan
- **Profil:** Peneliti yang memerlukan data lingkungan untuk studi korelasi kesehatan
- **Pain Point:** Data AQI dan cuaca tersebar di platform berbeda, tidak visual
- **Goal:** Pantau tren PM2.5 dan kondisi cuaca secara bersamaan
- **Use Case Utama:**
  - Monitor indikator kualitas udara (PM2.5, PM10) di kota studi
  - Lihat kondisi cuaca yang berkorelasi dengan kualitas udara

### 3.2 Tabel User Journey

| Tahap | Pelancong | Warga Lokal | Peneliti |
|-------|-----------|-------------|---------|
| **Onboarding** | Pilih kota tujuan | Pilih kota domisili | Pilih kota penelitian |
| **Aksi Utama** | Cek cuaca + AQI | Cek AQI pagi hari | Monitor AQI + cuaca |
| **Aksi Sekunder** | Lihat sunrise/sunset | Pantau tren musim | Komparasi antar kota |
| **Retention Hook** | Info astronomi + musim | Panel AQI harian | Panel komparasi data |

---

## 4. API Constraints & Strategy

### 4.1 Batasan Weatherstack Free Plan

| Parameter | Detail |
|-----------|--------|
| **Kuota** | 100 request/bulan |
| **Endpoint Aktif** | `/current` (confirmed via actual test) |
| **Data per Request** | Cuaca standar + **Astronomi** + **Kualitas Udara** (3-in-1!) |
| **Endpoint TIDAK Tersedia** | `/historical`, `/forecast` (paid only) |
| **Protocol** | HTTP only (HTTPS = paid) |
| **Bulk Query** | ❌ Tidak tersedia |

> **⚠️ Catatan Kritis:** Meskipun free plan secara teknis mengembalikan `astro` dan `air_quality`, Weatherstack **tidak mendokumentasikan** ini secara eksplisit di free tier. Ada kemungkinan ini berubah. Strategi mitigasinya adalah menambahkan **null-safety check** untuk kedua field tersebut di kode — jika field hilang, UI gracefully degraded.

### 4.2 Analisis Value per API Call

Satu API call ke `/current` kini menghasilkan:

```
1 Request = Cuaca (12 field) + Astronomi (6 field) + Kualitas Udara (8 field)
         = 26 data points per kota
```

Ini mengubah kalkulasi efisiensi dari "100 request cuaca saja" menjadi **"100 request × 26 data point = 2.600 data points/bulan"** — sangat efisien.

### 4.3 Strategi Manajemen Kuota (Diperbarui)

**S1 — Smart Caching dengan TTL Adaptif**

| Kondisi | Cache TTL |
|---------|-----------|
| Default (cuaca stabil) | 2 jam |
| Cuaca sedang hujan/badai (precip > 0) | 45 menit (lebih sering update) |
| Kualitas udara AQI sangat buruk (EPA ≥ 4) | 1 jam |
| Malam hari (is_day = "no") | 3 jam (cuaca lebih stabil) |

**S2 — On-Demand Fetching Only**
- Tidak ada auto-refresh — hanya fetch saat user pilih kota baru atau tekan tombol Refresh
- Tombol Refresh dilengkapi **cooldown timer** yang ditampilkan secara visual

**S3 — Seasonal & Climate Data = 100% Static**
- Fitur Pantau Musim menggunakan CSV klimatologi lokal → **nol API call**

**S4 — API Usage Meter**
- Counter real-time: "Request tersisa: XX/100"
- Peringatan: kuning (≤ 20), merah (≤ 10)
- Estimasi: "Cukup untuk ~X hari lagi"

**S5 — Graceful Degradation**
- Jika `astro` atau `air_quality` tidak ada dalam response → sembunyikan panel terkait dengan pesan "Data tidak tersedia"
- Jika quota habis → tampilkan cache terakhir + badge "⚠️ Data mungkin tidak terkini"

### 4.4 Estimasi Konsumsi API per Bulan

| Aktivitas | Call/Kejadian | Estimasi Kejadian/Bulan | Total |
|-----------|---------------|------------------------|-------|
| Pilih kota baru (cache miss) | 1 | ~60 | 60 |
| Refresh manual | 1 | ~15 | 15 |
| Cold start (cache expired) | 1 | ~10 | 10 |
| **Total Estimasi** | | | **~85 calls** |
| **Buffer Tersisa** | | | **15 calls** |

---

## 5. Fitur & Functional Requirements

### 5.1 Onboarding — City Selector (Wajib)

**Deskripsi:** Splash screen pemilihan kota saat pertama kali membuka aplikasi.

| ID | Requirement |
|----|-------------|
| FR-01 | Tampilkan modal/splash screen saat aplikasi pertama kali dibuka |
| FR-02 | Daftar kota diorganisir per negara (11 negara ASEAN) |
| FR-03 | Search bar dengan autocomplete (fuzzy search) |
| FR-04 | Minimal 5 kota per negara ASEAN |
| FR-05 | Pilihan kota tersimpan di session state |
| FR-06 | User dapat ubah kota kapan saja via dropdown navbar |

**Daftar Kota Minimum per Negara:**

| Negara | Kota |
|--------|------|
| 🇮🇩 Indonesia | Jakarta, Surabaya, Medan, Bali, Makassar, Yogyakarta, Bandung |
| 🇲🇾 Malaysia | Kuala Lumpur, Penang, Kota Kinabalu, Johor Bahru, Kuching |
| 🇸🇬 Singapura | Singapore |
| 🇹🇭 Thailand | Bangkok, Chiang Mai, Phuket, Pattaya, Hat Yai |
| 🇻🇳 Vietnam | Hanoi, Ho Chi Minh City, Da Nang, Hue |
| 🇵🇭 Filipina | Manila, Cebu, Davao, Quezon City |
| 🇲🇲 Myanmar | Yangon, Mandalay, Naypyidaw |
| 🇰🇭 Kamboja | Phnom Penh, Siem Reap |
| 🇱🇦 Laos | Vientiane, Luang Prabang |
| 🇧🇳 Brunei | Bandar Seri Begawan |
| 🇹🇱 Timor-Leste | Dili |

---

### 5.2 Panel Real-Time Weather (Fitur Wajib Utama)

**Deskripsi:** Panel utama cuaca terkini dari endpoint `GET /current`.

**Data Fields dari API (Confirmed):**

#### Grup A — Cuaca Standar (`current.*`)

| Field API | Label UI | Unit | Contoh Nilai |
|-----------|----------|------|--------------|
| `current.temperature` | Suhu | °C | 29 |
| `current.feelslike` | Terasa Seperti | °C | 31 |
| `current.weather_descriptions[]` | Kondisi | Teks | "Light Rain, Rain" |
| `current.weather_icons[]` | Ikon | URL gambar | *(URL CDN)* |
| `current.humidity` | Kelembaban | % | 84 |
| `current.wind_speed` | Kec. Angin | km/h | 15 |
| `current.wind_degree` | Derajat Angin | ° | 10 |
| `current.wind_dir` | Arah Angin | Mata angin | "N" |
| `current.pressure` | Tekanan Udara | mb | 1007 |
| `current.precip` | Presipitasi | mm | 0 |
| `current.cloudcover` | Tutupan Awan | % | 75 |
| `current.uv_index` | Indeks UV | 0–11+ | 7 |
| `current.visibility` | Visibilitas | km | 5 |
| `current.is_day` | Siang/Malam | yes/no | "yes" |
| `current.observation_time` | Waktu Observasi | HH:MM AM/PM | "07:37 AM" |

#### Grup B — Astronomi (`current.astro.*`) ✨ *Baru Dikonfirmasi*

| Field API | Label UI | Contoh Nilai |
|-----------|----------|--------------|
| `current.astro.sunrise` | Matahari Terbit 🌅 | "05:53 AM" |
| `current.astro.sunset` | Matahari Terbenam 🌇 | "05:47 PM" |
| `current.astro.moonrise` | Bulan Terbit 🌕 | "04:41 PM" |
| `current.astro.moonset` | Bulan Terbenam | "04:30 AM" |
| `current.astro.moon_phase` | Fase Bulan | "Waxing Gibbous" |
| `current.astro.moon_illumination` | Iluminasi Bulan | 97 (%) |

#### Grup C — Kualitas Udara (`current.air_quality.*`) ✨ *Baru Dikonfirmasi*

| Field API | Label UI | Satuan | Contoh Nilai |
|-----------|----------|--------|--------------|
| `current.air_quality.co` | Karbon Monoksida (CO) | µg/m³ | 3427.85 |
| `current.air_quality.no2` | Nitrogen Dioksida (NO₂) | µg/m³ | 60.75 |
| `current.air_quality.o3` | Ozon (O₃) | µg/m³ | 20 |
| `current.air_quality.so2` | Sulfur Dioksida (SO₂) | µg/m³ | 49.15 |
| `current.air_quality.pm2_5` | Partikel Halus (PM2.5) | µg/m³ | 81.45 |
| `current.air_quality.pm10` | Partikel Kasar (PM10) | µg/m³ | 81.65 |
| `current.air_quality.us-epa-index` | US EPA AQI Index | 1–6 | 4 |
| `current.air_quality.gb-defra-index` | UK DEFRA Index | 1–10 | 4 |

**Functional Requirements:**

| ID | Requirement |
|----|-------------|
| FR-07 | Fetch data dari `http://api.weatherstack.com/current` |
| FR-08 | Render semua field Grup A dalam kartu cuaca utama |
| FR-09 | Tampilkan timestamp "Diperbarui: [localtime dari API]" |
| FR-10 | Badge kondisi cuaca dengan warna (hijau=cerah, biru=hujan, abu=berawan) |
| FR-11 | Tombol "🔄 Refresh" dengan cooldown visual countdown |
| FR-12 | Tampilkan `location.name`, `location.country`, `location.region` sebagai header |
| FR-13 | Tampilkan API usage meter |
| FR-14 | Null-safety: jika `astro`/`air_quality` tidak ada dalam response → sembunyikan panel terkait |

---

### 5.3 Panel Pantau Musim (Retention Feature — Wajib)

**Deskripsi:** Panel interaktif pola musiman berbasis data statis klimatologi. **Tidak mengonsumsi API call.**

#### 5.3.1 Kalender Musim

| ID | Requirement |
|----|-------------|
| FR-15 | Kalender 12 bulan dengan kode warna: 🟦 Hujan, 🟩 Kemarau, 🟨 Transisi |
| FR-16 | Highlight bulan aktif saat ini |
| FR-17 | Tooltip hover pada bulan: rata-rata suhu & curah hujan historis |

#### 5.3.2 Grafik Iklim Bulanan

| ID | Requirement |
|----|-------------|
| FR-18 | Dual-axis chart: line (suhu rata-rata) + bar (curah hujan rata-rata) per bulan |
| FR-19 | Garis vertikal penanda bulan aktif |
| FR-20 | Perbandingan suhu real-time vs rata-rata historis bulan ini (delta °C) |

#### 5.3.3 Kartu Status Musim

| ID | Requirement |
|----|-------------|
| FR-21 | Kartu: "Saat ini: Musim [X]" dengan ikon animasi |
| FR-22 | Estimasi akhir musim: "Berlangsung hingga ~[Bulan]" |
| FR-23 | Tips kontekstual berdasarkan musim (bawa payung, tabir surya, dll.) |

#### 5.3.4 Komparasi Antar Kota

| ID | Requirement |
|----|-------------|
| FR-24 | Dropdown tambah kota pembanding (maks. 2 kota) |
| FR-25 | Side-by-side grafik suhu & curah hujan musiman |

---

### 5.4 Panel Langit & Astronomi ✨ *Fitur Baru v1.1*

**Deskripsi:** Panel dedicated untuk data astronomi yang tersedia dari API. Sangat berguna bagi pelancong (golden hour photography, aktivitas outdoor) dan komunitas lokal (nelayan, petani).

| ID | Requirement |
|----|-------------|
| FR-26 | Visualisasi arc/timeline harian: posisi matahari dari sunrise ke sunset |
| FR-27 | Tampilkan jam sunrise dan sunset secara prominent |
| FR-28 | Tampilkan jam moonrise dan moonset |
| FR-29 | Visual fase bulan dengan ikon animasi (🌑🌒🌓🌔🌕🌖🌗🌘) |
| FR-30 | Persentase iluminasi bulan sebagai gauge chart |
| FR-31 | Hitung & tampilkan "Durasi Siang Hari" = sunset − sunrise |
| FR-32 | Hitung & tampilkan "Golden Hour" = ±30 menit dari sunrise & sunset |
| FR-33 | Badge: "☀️ Siang" atau "🌙 Malam" berdasarkan `is_day` |

**Interpretasi Fase Bulan (Label Bahasa Indonesia):**

| Nilai API | Label ID | Ikon |
|-----------|----------|------|
| New Moon | Bulan Baru | 🌑 |
| Waxing Crescent | Bulan Sabit Awal | 🌒 |
| First Quarter | Kuartal Pertama | 🌓 |
| Waxing Gibbous | Bulan Cembung Awal | 🌔 |
| Full Moon | Bulan Purnama | 🌕 |
| Waning Gibbous | Bulan Cembung Akhir | 🌖 |
| Last Quarter | Kuartal Terakhir | 🌗 |
| Waning Crescent | Bulan Sabit Akhir | 🌘 |

---

### 5.5 Panel Kualitas Udara (AQI) ✨ *Fitur Baru v1.1*

**Deskripsi:** Panel dedicated untuk data kualitas udara berdasarkan field `air_quality` dari API. Relevan khususnya untuk kota-kota ASEAN yang memiliki masalah polusi udara (Jakarta PM2.5: 81.45 µg/m³ — kategori **Tidak Sehat**).

#### 5.5.1 AQI Summary Card

| ID | Requirement |
|----|-------------|
| FR-34 | Tampilkan US EPA AQI Index (1–6) sebagai kartu besar dengan warna kategori |
| FR-35 | Label kategori EPA dalam Bahasa Indonesia (lihat tabel di bawah) |
| FR-36 | Tampilkan UK DEFRA Index sebagai referensi sekunder |

**Tabel Kategori US EPA AQI Index:**

| EPA Index | Kategori | Warna | Rekomendasi |
|-----------|----------|-------|-------------|
| 1 | Baik | 🟢 Hijau | Aman untuk semua aktivitas |
| 2 | Sedang | 🟡 Kuning | Sensitif: batasi aktivitas luar |
| 3 | Tidak Sehat (Sensitif) | 🟠 Oranye | Kelompok sensitif hindari luar ruangan |
| 4 | Tidak Sehat | 🔴 Merah | Semua orang batasi aktivitas luar |
| 5 | Sangat Tidak Sehat | 🟣 Ungu | Hindari semua aktivitas outdoor |
| 6 | Berbahaya | 🟤 Maroon | Darurat kesehatan — tetap dalam ruangan |

#### 5.5.2 Pollutant Breakdown

| ID | Requirement |
|----|-------------|
| FR-37 | Tampilkan bar chart atau gauge untuk masing-masing polutan: PM2.5, PM10, CO, NO₂, O₃, SO₂ |
| FR-38 | Garis referensi WHO/standar batas aman pada chart setiap polutan |
| FR-39 | Badge "⚠️ Di Atas Batas WHO" jika polutan melebihi ambang batas |
| FR-40 | Highlight PM2.5 sebagai indikator primer (polutan paling relevan kesehatan) |

**Ambang Batas WHO (24-jam) sebagai referensi:**

| Polutan | WHO Guideline (µg/m³) |
|---------|----------------------|
| PM2.5 | 15 µg/m³ |
| PM10 | 45 µg/m³ |
| NO₂ | 25 µg/m³ |
| O₃ | 100 µg/m³ |
| SO₂ | 40 µg/m³ |

#### 5.5.3 Health Advisory

| ID | Requirement |
|----|-------------|
| FR-41 | Saran kesehatan otomatis berdasarkan EPA Index: "Gunakan masker saat beraktivitas di luar" |
| FR-42 | Rekomendasi berbeda untuk kelompok sensitif (anak-anak, lansia, penderita asma) |

---

### 5.6 Sistem Peringatan Cuaca & Udara (Diperluas)

**Deskripsi:** Deteksi otomatis kondisi berbahaya dari data real-time.

| ID | Trigger Kondisi | Threshold | Tipe Banner |
|----|----------------|-----------|-------------|
| FR-43 | UV Index tinggi | UV ≥ 8 | 🟡 Kuning — "Lindungi kulit Anda" |
| FR-44 | UV Index ekstrem | UV ≥ 11 | 🔴 Merah — "UV Ekstrem — Hindari paparan langsung" |
| FR-45 | Angin kencang | Wind ≥ 60 km/h | 🔴 Merah — "Waspadai angin kencang" |
| FR-46 | Kelembaban ekstrem | Humidity ≥ 90% | 🟡 Kuning — "Lembap Ekstrem" |
| FR-47 | Visibilitas rendah | Visibility ≤ 2 km | 🟡 Kuning — "Jarak pandang terbatas" |
| FR-48 | AQI berbahaya | EPA Index ≥ 4 | 🔴 Merah — "Kualitas udara buruk — gunakan masker" |
| FR-49 | PM2.5 di atas WHO | PM2.5 > 15 | 🟡 Kuning — "PM2.5 melebihi standar WHO" |
| FR-50 | Bulan Purnama | moon_phase = Full Moon | ℹ️ Biru — "Malam ini Bulan Purnama 🌕" |

---

### 5.7 Peta Mini Regional

| ID | Requirement |
|----|-------------|
| FR-51 | Peta Asia Tenggara menggunakan `folium` atau `plotly` |
| FR-52 | Titik kota aktif di-highlight berbeda |
| FR-53 | Klik titik kota → update kota aktif (tanpa API call jika ada di cache) |
| FR-54 | Tidak mengonsumsi API call |

---

### 5.8 Favorit & History

| ID | Requirement |
|----|-------------|
| FR-55 | Simpan hingga 5 kota favorit (session state) |
| FR-56 | Quick-access chip untuk kota favorit di atas dashboard |
| FR-57 | History 3 kota terakhir yang dicek |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement |
|----|-------------|
| NFR-01 | Load awal dari cache ≤ 2 detik |
| NFR-02 | Fetch API ke tampilan ≤ 5 detik |
| NFR-03 | Tidak crash saat API limit tercapai (graceful degradation) |
| NFR-04 | Null-safety untuk semua field `astro` dan `air_quality` |

### 6.2 Usability

| ID | Requirement |
|----|-------------|
| NFR-05 | Responsive untuk layar 1280px+ (desktop-first, mobile-friendly) |
| NFR-06 | Dark mode / Light mode toggle |
| NFR-07 | Bilingual: Bahasa Indonesia & English |
| NFR-08 | Navigasi utama ≤ 2 klik dari manapun |
| NFR-09 | AQI color coding konsisten dengan standar US EPA di seluruh UI |

### 6.3 Reliability

| ID | Requirement |
|----|-------------|
| NFR-10 | Saat API unavailable → tampilkan cache terakhir |
| NFR-11 | Error handling dengan pesan user-friendly (bukan error stack trace) |
| NFR-12 | Validasi input kota sebelum API call |
| NFR-13 | Jika field `astro`/`air_quality` hilang dari response → UI degraded gracefully |

### 6.4 Security

| ID | Requirement |
|----|-------------|
| NFR-14 | API key di file `.env`, tidak di-hardcode |
| NFR-15 | Koneksi HTTP (sesuai batasan free plan) dengan catatan risiko |
| NFR-16 | `.env` masuk ke `.gitignore` |

---

## 7. Arsitektur Aplikasi

### 7.1 Stack Teknologi

```
┌─────────────────────────────────────────────────┐
│               SEAWeather v1.1                   │
│                                                 │
│  UI Layer                                       │
│  ┌───────────────────────────────────────────┐ │
│  │ Shiny Python (>= 0.6)                     │ │
│  │ Plotly (chart AQI, iklim, astronomi)      │ │
│  │ Folium (peta regional)                    │ │
│  │ Custom CSS (glassmorphism dark theme)     │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  Service Layer                                  │
│  ┌───────────────────────────────────────────┐ │
│  │ weather_service.py   → fetch + parse API  │ │
│  │ cache_manager.py     → TTL adaptif        │ │
│  │ aqi_engine.py        → kalkulasi + label  │ │
│  │ astro_engine.py      → golden hour, durasi│ │
│  │ alert_engine.py      → deteksi threshold  │ │
│  │ seasonal_data.py     → load CSV statis    │ │
│  │ api_counter.py       → tracking usage     │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  Data Layer                                     │
│  ┌───────────────────────────────────────────┐ │
│  │ Weatherstack API /current (HTTP)          │ │
│  │   └─ weather + astro + air_quality        │ │
│  │ cities_sea.json          (static)         │ │
│  │ seasonal_climate.csv     (static)         │ │
│  │ who_pollutant_limits.json (static)        │ │
│  │ cache.json               (session)        │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### 7.2 Struktur Direktori Proyek

```
seaweather/
│
├── app.py                        # Entry point Shiny Python
├── .env                          # API_KEY (tidak di-commit)
├── .gitignore                    # Includes .env, cache.json
├── requirements.txt
│
├── components/
│   ├── city_selector.py          # Onboarding modal
│   ├── weather_card.py           # Kartu cuaca standar
│   ├── astro_panel.py            # Panel Langit & Astronomi ✨
│   ├── aqi_panel.py              # Panel Kualitas Udara ✨
│   ├── season_panel.py           # Panel Pantau Musim
│   ├── map_widget.py             # Peta mini regional
│   ├── alert_banner.py           # Banner peringatan
│   └── api_meter.py              # Usage counter widget
│
├── services/
│   ├── weather_service.py        # Weatherstack API wrapper
│   ├── cache_manager.py          # Caching + adaptive TTL
│   ├── aqi_engine.py             # AQI parsing + WHO comparison ✨
│   ├── astro_engine.py           # Golden hour, durasi siang ✨
│   ├── alert_engine.py           # Multi-threshold alert detection
│   └── seasonal_data.py          # Load & query CSV klimatologi
│
├── data/
│   ├── cities_sea.json            # Master list kota ASEAN
│   ├── seasonal_climate.csv      # Data iklim historis statis
│   └── who_pollutant_limits.json  # Referensi batas WHO ✨
│
├── assets/
│   ├── styles.css                # Dark theme + glassmorphism
│   ├── moon_phases/              # Ikon fase bulan SVG
│   └── weather_icons/            # Ikon cuaca custom
│
└── utils/
    ├── api_counter.py            # Persistensi counter API
    └── helpers.py                # Format, konversi, parsing
```

### 7.3 Alur Data (Data Flow) — Diperbarui

```
User Pilih Kota
      │
      ▼
Cache Manager
┌─────────────────────────────────────┐
│ Apakah cache valid (TTL belum exp)? │
└─────────────────────────────────────┘
      │
  ┌───┴─────┐
 VALID    EXPIRED/MISS
  │            │
  ▼            ▼
Gunakan    Cek API Counter
Cache      (tersisa request?)
  │            │
  │        ┌───┴───┐
  │       ADA    HABIS
  │        │       │
  │        ▼       ▼
  │     Fetch     Tampilkan
  │     /current  Cache + badge
  │        │      "⚠️ Data lama"
  │        ▼
  │     Parse Response:
  │     ├── current.* → weather_card
  │     ├── current.astro.* → astro_panel
  │     └── current.air_quality.* → aqi_panel
  │        │
  │        ▼
  │     Simpan ke Cache (adaptive TTL)
  │     Increment API Counter
  │        │
  └────────┤
           ▼
     Render Dashboard:
     ├── WeatherCard
     ├── AstroPanel
     ├── AQIPanel
     ├── AlertBanner (jika threshold terpenuhi)
     ├── SeasonPanel (dari static CSV)
     └── MapWidget
```

---

## 8. UI/UX Specification

### 8.1 Design Language

| Aspek | Spesifikasi |
|-------|-------------|
| **Tema Default** | Dark mode, glassmorphism card |
| **Background** | `#0a0e1a` (deep navy) + bintang subtle untuk efek langit malam |
| **Accent Primary** | `#00d4ff` (cyan electric) |
| **AQI Baik** | `#00ff87` (hijau neon) |
| **AQI Buruk** | `#ff4444` (merah) |
| **AQI Berbahaya** | `#7b2d8b` (ungu) |
| **Astronomi** | `#ffd700` (emas) untuk matahari, `#c0c0c0` (perak) untuk bulan |
| **Font UI** | Inter |
| **Font Data** | Roboto Mono |
| **Ikon Cuaca** | CDN `weather_icons[]` dari API + custom override SVG |
| **Motion** | Fade-in cards, shimmer loading, animated moon phase indicator |

### 8.2 Layout Utama Dashboard — v1.1

```
┌────────────────────────────────────────────────────────────────────────┐
│  🌦️ SEAWeather v1.1   [📍 Jakarta, Indonesia ▼]    [🌙 Dark] [EN/ID]  │ ← Navbar
│  ⚡ Jakarta  ⚡ Bangkok  ⚡ Kuala Lumpur  [+ Tambah Favorit]           │ ← Favorites
│  ⚠️ Kualitas Udara TIDAK SEHAT (EPA 4) — Gunakan masker saat ke luar  │ ← Alert Banner
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ROW 1 — Cuaca & Lokasi                                                │
│  ┌──────────────────────────────┐  ┌─────────────────────────────┐    │
│  │  ☁️ CUACA REAL-TIME          │  │  🌅 LANGIT & ASTRONOMI      │    │
│  │  📍 Jakarta, Jakarta Raya    │  │                             │    │
│  │                              │  │  [====☀️============]       │    │
│  │  🌧️  29°C  (Terasa 31°C)    │  │   05:53           17:47     │    │
│  │  Light Rain, Rain            │  │   Sunrise         Sunset    │    │
│  │                              │  │   Durasi Siang: 11j 54m    │    │
│  │  💧 84%  💨 15km/h ↑N       │  │   Golden Hour: 05:23–05:53 │    │
│  │  👁 5km  ☁️ 75%  🌡 1007mb  │  │                             │    │
│  │  ☀️ UV: 7 (Tinggi)          │  │  🌔 Waxing Gibbous 97% 🌕  │    │
│  │  ⏱ Diperbarui: 14:37 WIB   │  │   Moonrise: 16:41           │    │
│  │                              │  │   Moonset: 04:30            │    │
│  │  [🔄 Refresh (45 mnt)]      │  │                             │    │
│  └──────────────────────────────┘  └─────────────────────────────┘    │
│                                                                        │
│  ROW 2 — Kualitas Udara                                                │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │  🫁 KUALITAS UDARA                                              │   │
│  │                                                                 │   │
│  │  US EPA: 🔴 4 — TIDAK SEHAT    UK DEFRA: 4                     │   │
│  │                                                                 │   │
│  │  PM2.5: ████████████░░  81.5 µg/m³  ⚠️ > WHO (15 µg/m³)      │   │
│  │  PM10:  ████████████░░  81.7 µg/m³  ⚠️ > WHO (45 µg/m³)      │   │
│  │  CO:    ████░░░░░░░░░░  3427 µg/m³                             │   │
│  │  NO₂:  ███░░░░░░░░░░░   60.8 µg/m³  ⚠️ > WHO (25 µg/m³)      │   │
│  │  O₃:   ██░░░░░░░░░░░░   20.0 µg/m³                             │   │
│  │  SO₂:  ███░░░░░░░░░░░   49.2 µg/m³  ⚠️ > WHO (40 µg/m³)      │   │
│  │                                                                 │   │
│  │  💡 Saran: Kenakan masker N95 saat beraktivitas di luar ruangan│   │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ROW 3 — Musim & Peta                                                  │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐     │
│  │  🍃 PANTAU MUSIM             │  │  🗺️ PETA REGIONAL           │     │
│  │  Jakarta — 🌧️ Musim Hujan  │  │                             │     │
│  │  Est. berlanjut s/d Maret   │  │  [Mini Map ASEAN — Folium]  │     │
│  │                              │  │                             │     │
│  │  Jan Feb Mar ... Nov Des    │  └─────────────────────────────┘     │
│  │  🟦 🟦 🟨 ... 🟦 🟦        │                                       │
│  │                              │  ┌─────────────────────────────┐    │
│  │  [Grafik Suhu & Hujan]      │  │  [API Calls: ██████░ 85/100]│    │
│  │                              │  │  Tersisa: 15 request        │    │
│  │  [+ Bandingkan Kota]        │  └─────────────────────────────┘    │
│  └─────────────────────────────┘                                      │
└────────────────────────────────────────────────────────────────────────┘
```

### 8.3 Onboarding Modal

```
┌──────────────────────────────────────────┐
│  🌏 Selamat Datang di SEAWeather         │
│  Cuaca · Udara · Langit Asia Tenggara    │
│                                          │
│  Mulai dengan memilih kota Anda:         │
│  [🔍 Cari kota atau negara...         ]  │
│                                          │
│  🇮🇩 Indonesia                          │
│    ● Jakarta   ● Bali   ● Surabaya       │
│    ● Yogyakarta  ● Medan  ● Bandung      │
│                                          │
│  🇲🇾 Malaysia · 🇸🇬 Singapura ...       │
│                                          │
│  📡 Data cuaca + udara + langit dalam    │
│  satu tampilan.                          │
│                                          │
│         [ Lihat Dashboard → ]            │
└──────────────────────────────────────────┘
```

---

## 9. Data Model

### 9.1 Struktur Cache — Diperbarui (cache.json)

```json
{
  "Jakarta": {
    "fetched_at": "2026-04-30T14:37:00+07:00",
    "expires_at": "2026-04-30T15:22:00+07:00",
    "ttl_minutes": 45,
    "ttl_reason": "precip=0 & AQI=4",
    "api_calls_used": 85,
    "data": {
      "request": {
        "type": "City",
        "query": "Jakarta, Indonesia",
        "language": "en",
        "unit": "m"
      },
      "location": {
        "name": "Jakarta",
        "country": "Indonesia",
        "region": "Jakarta Raya",
        "lat": "-6.215",
        "lon": "106.845",
        "timezone_id": "Asia/Jakarta",
        "localtime": "2026-04-30 14:37",
        "utc_offset": "7.0"
      },
      "current": {
        "observation_time": "07:37 AM",
        "temperature": 29,
        "feelslike": 31,
        "weather_descriptions": ["Light Rain, Rain"],
        "weather_icons": ["https://cdn.worldweatheronline.com/..."],
        "wind_speed": 15,
        "wind_degree": 10,
        "wind_dir": "N",
        "pressure": 1007,
        "precip": 0,
        "humidity": 84,
        "cloudcover": 75,
        "uv_index": 7,
        "visibility": 5,
        "is_day": "yes",
        "astro": {
          "sunrise": "05:53 AM",
          "sunset": "05:47 PM",
          "moonrise": "04:41 PM",
          "moonset": "04:30 AM",
          "moon_phase": "Waxing Gibbous",
          "moon_illumination": 97
        },
        "air_quality": {
          "co": "3427.85",
          "no2": "60.75",
          "o3": "20",
          "so2": "49.15",
          "pm2_5": "81.45",
          "pm10": "81.65",
          "us-epa-index": "4",
          "gb-defra-index": "4"
        }
      }
    }
  }
}
```

### 9.2 Data Statis: who_pollutant_limits.json (Baru)

```json
{
  "who_2021_guidelines": {
    "pm2_5": { "24h": 15, "annual": 5, "unit": "µg/m³" },
    "pm10":  { "24h": 45, "annual": 15, "unit": "µg/m³" },
    "no2":   { "24h": 25, "annual": 10, "unit": "µg/m³" },
    "o3":    { "8h": 100, "unit": "µg/m³" },
    "so2":   { "24h": 40, "unit": "µg/m³" },
    "co":    { "24h": 4000, "unit": "µg/m³" }
  }
}
```

### 9.3 seasonal_climate.csv

```csv
city,country,month,avg_temp_c,avg_rainfall_mm,season_type,season_label_id
Jakarta,Indonesia,1,26.5,300,rainy,Musim Hujan
Jakarta,Indonesia,2,26.8,270,rainy,Musim Hujan
Jakarta,Indonesia,3,27.0,210,transition,Transisi
...
```

---

## 10. Batasan & Out of Scope

### 10.1 Dalam Scope — v1.1 ✅

- ✅ Real-time weather (suhu, angin, kelembaban, UV, visibilitas)
- ✅ **Data Astronomi** (sunrise, sunset, moonrise, moonset, fase bulan) — *Baru dikonfirmasi*
- ✅ **Kualitas Udara** (PM2.5, PM10, CO, NO₂, O₃, SO₂, EPA Index) — *Baru dikonfirmasi*
- ✅ Smart caching dengan TTL adaptif
- ✅ Panel Pantau Musim (data statis, nol API call)
- ✅ Sistem peringatan multi-threshold (cuaca + AQI)
- ✅ Peta mini regional
- ✅ Onboarding city selector modal
- ✅ API usage meter
- ✅ Kota favorit (session-based)
- ✅ Dark/Light mode

### 10.2 Out of Scope — Butuh Paid Plan ❌

- ❌ Weather forecast 7/14 hari (`/forecast` endpoint)
- ❌ Historical weather per hari dari API (`/historical` endpoint)
- ❌ Hourly weather breakdown
- ❌ HTTPS API calls
- ❌ Bulk/multi-city request dalam satu call
- ❌ Push notification
- ❌ Persistent multi-user session (database)
- ❌ Deployment produksi cloud (v1.1 = prototype lokal)

---

## 11. Milestones & Timeline — Direvisi

| Fase | Milestone | Deliverable | Durasi |
|------|-----------|-------------|--------|
| **Fase 1** | Setup & Foundation | Struktur proyek, `.env`, API wrapper, caching adaptive | 1 minggu |
| **Fase 2** | Core Weather UI | City selector, weather card, onboarding modal | 1 minggu |
| **Fase 3** | AQI & Astronomi Panel | AQI breakdown + WHO reference, astro timeline | 1 minggu |
| **Fase 4** | Pantau Musim | Dataset statis, dual-axis chart, kalender musim | 1 minggu |
| **Fase 5** | Polish & Extras | Peta mini, alert system, favorites, dark mode | 1 minggu |
| **Fase 6** | Testing & QA | API mock, null-safety test, edge cases | 3 hari |
| **Total** | | | **~5.5 minggu** |

---

## 12. Risiko & Mitigasi — Diperbarui

| # | Risiko | Prob. | Dampak | Mitigasi |
|---|--------|-------|--------|----------|
| R1 | Kuota 100 req/bulan habis sebelum bulan berakhir | Sedang | Tinggi | Adaptive TTL cache + on-demand fetch only |
| R2 | Field `astro` / `air_quality` dihapus dari free plan tanpa notifikasi | Sedang | Tinggi | Null-safety di semua akses field; graceful degradation panel |
| R3 | API Weatherstack down/tidak tersedia | Rendah | Sedang | Fallback ke cache + pesan informatif |
| R4 | Nilai AQI dari API berbeda dengan ground truth lokal | Sedang | Sedang | Tampilkan disclaimer sumber data |
| R5 | Performance lambat dengan banyak Plotly chart | Sedang | Sedang | Lazy loading panel; render hanya saat visible |
| R6 | API key exposed | Rendah | Tinggi | Wajib `.env` + `.gitignore` |
| R7 | Data seasonal statis tidak akurat | Rendah | Rendah | Cantumkan sumber & tahun data referensi |
| R8 | HTTP (bukan HTTPS) rentan MITM | Sedang | Sedang | Tampilkan warning di UI; dokumentasikan untuk upgrade ke paid |

---

## Appendix A — Confirmed API Response Structure

Response aktual dari `GET http://api.weatherstack.com/current?access_key=KEY&query=Jakarta`:

```json
{
  "request":  { "type", "query", "language", "unit" },
  "location": { "name", "country", "region", "lat", "lon",
                "timezone_id", "localtime", "localtime_epoch", "utc_offset" },
  "current": {
    "observation_time", "temperature", "weather_code",
    "weather_icons[]", "weather_descriptions[]",
    "wind_speed", "wind_degree", "wind_dir",
    "pressure", "precip", "humidity", "cloudcover",
    "feelslike", "uv_index", "visibility", "is_day",
    "astro": {
      "sunrise", "sunset", "moonrise", "moonset",
      "moon_phase", "moon_illumination"
    },
    "air_quality": {
      "co", "no2", "o3", "so2", "pm2_5", "pm10",
      "us-epa-index", "gb-defra-index"
    }
  }
}
```

> **Total: 26 data points per 1 API request** (vs. asumsi awal 15 data point)

---

## Appendix B — Dependencies Python

```txt
# requirements.txt
shiny>=0.6.0
requests>=2.31.0
plotly>=5.18.0
pandas>=2.1.0
folium>=0.15.0
python-dotenv>=1.0.0
pytz>=2024.1
```

---

## Appendix C — Kalkulasi Golden Hour

```python
# services/astro_engine.py
from datetime import datetime, timedelta

def calculate_golden_hours(sunrise_str: str, sunset_str: str) -> dict:
    """
    Golden Hour = ~30 menit setelah sunrise & ~30 menit sebelum sunset
    Blue Hour = ~20 menit sebelum sunrise & ~20 menit setelah sunset
    """
    fmt = "%I:%M %p"
    sunrise = datetime.strptime(sunrise_str, fmt)
    sunset = datetime.strptime(sunset_str, fmt)

    return {
        "morning_blue_start":  sunrise - timedelta(minutes=20),
        "morning_golden_start": sunrise,
        "morning_golden_end":   sunrise + timedelta(minutes=30),
        "evening_golden_start": sunset - timedelta(minutes=30),
        "evening_golden_end":   sunset,
        "evening_blue_end":     sunset + timedelta(minutes=20),
        "daylight_duration":    str(sunset - sunrise)
    }
```

---

*Dokumen ini akan direvisi ke v2.0 jika ada upgrade ke paid plan (menambahkan forecast & historical API).*

---
**© 2026 SEAWeather Project | PRD v1.1 — Revised based on actual API verification**
