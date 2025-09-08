
---

```markdown
# 🎵 ShiroAI Separator Pro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-purple.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Spleeter](https://img.shields.io/badge/Spleeter-2stems-orange.svg)](https://github.com/deezer/spleeter)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<div align="center">
  <img src="https://top-gray-zo9uqyc2cs.edgeone.app/bg_f8f8f8-flat_750x_075_f-pad_750x1000_f8f8f8-removebg-preview.png" width="300"/>
  <p><em>AI-Powered Vocal & Instrument Separator</em></p>
</div>

---

## 📂 Struktur Project

```

ShiroAI-Separator-Pro/
│
├── vocaloffline.py        # Program utama
├── shiroai\_config.json    # File konfigurasi (dibuat otomatis)
├── requirements.txt       # Dependency list
└── README.md              # Dokumentasi

````

---

## ⚙️ Persyaratan Sistem

- Python **3.8+**
- **Pygame** untuk playback audio
- **Mutagen** untuk metadata audio
- **Pillow (PIL)** untuk image handler
- **CustomTkinter** (opsional, jika ingin UI modern)
- **Spleeter** (Deezer AI) untuk pemisahan audio (vokal & instrumen)

---

## 🚀 Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/username/ShiroAI-Separator-Pro.git
   cd ShiroAI-Separator-Pro
````

2. **Buat virtual environment (disarankan)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   atau manual:

   ```bash
   pip install pygame mutagen pillow customtkinter spleeter
   ```

4. **Jalankan aplikasi**

   ```bash
   python vocaloffline.py
   ```

---

## 🧠 Bagaimana AI Bekerja?

Di dalam program ini, digunakan **Deep Learning Model Spleeter** dari Deezer:

* **Input**: File audio (`.mp3`, `.wav`, `.flac`, dll.)
* **Processing**:

  * Memisahkan track menjadi **2 stems**:

    * 🎤 **Vocals (suara penyanyi)**
    * 🎸 **Accompaniment (instrumen musik)**
  * Progress bar + log real-time
* **Output**:

  * File audio terpisah disimpan dalam format `.wav`
  * Bisa dipilih: hanya vokal, hanya instrumen, atau keduanya

---

## 🖼️ Preview Aplikasi

<div align="center">
  <img src="https://iili.io/KJVonP2.png" alt="Preview Screenshot" width="700"/>
  <p><em>Modern UI dengan kontrol audio</em></p>
</div>

---

## 🛠️ Fitur

* 🎧 **Audio Preview** (vocals & instruments)
* 🎚️ Volume control + seek bar
* 🌙 **Light/Dark Theme**
* 💾 Simpan hasil pemisahan
* 📋 Log proses real-time
* 🚀 AI-Powered Separation (2-stems dengan Spleeter)

---

## 🗺️ Roadmap Pengembangan

* [ ] Support pemisahan **4/5 stems**
* [ ] Ekspor format audio lain (MP3, FLAC)
* [ ] Playlist & batch processing
* [ ] GUI lebih interaktif (drag & drop)
* [ ] Visualisasi spektrum audio

---

## 📜 Lisensi

Distribusi di bawah lisensi **MIT**.
Lihat file [LICENSE](LICENSE) untuk detail.

---

## 👨‍💻 Author

**ShiroAI Development Team**

* GitHub: [@yourusername](https://github.com/Renn-devBI)

---
