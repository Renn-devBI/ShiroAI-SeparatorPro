# ShiroAI Separator Pro

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

```bash
## 📂 Struktur Project
ShiroAI-Separator-Pro/
│
├── vocaloffline.py # Program utama
├── shiroai_config.json # File konfigurasi (dibuat otomatis)
├── requirements.txt # Dependency list
└── README.md # Dokumentasi
```


---

## ⚙️ Persyaratan Sistem

- Python **3.8+**  
- **Pygame** → playback audio  
- **Mutagen** → metadata audio  
- **Pillow (PIL)** → handler image/icon  
- **CustomTkinter** → tampilan GUI modern (opsional, fallback ke Tkinter)  
- **Spleeter** → AI audio separation (vokal & instrumen)  

---

## 🚀 Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/username/ShiroAI-Separator-Pro.git
   cd ShiroAI-Separator-Pro
   ```

2. **Buat virtual environment (disarankan)**
 ```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt or pip install pygame mutagen pillow customtkinter spleeter
   python vocaloffline.py
   ```
   
🧠 Cara Kerja AI
Aplikasi ini menggunakan Deep Learning Spleeter (by Deezer) untuk memisahkan audio:
Input: File audio (.mp3, .wav, .flac, dll.)
Processing: Model 2-stems → memisahkan track jadi:
- 🎤 Vocals (suara penyanyi)
- 🎸 Instruments (musik/iringan)
- 
Progress bar & log real-time Output:
- File hasil pemisahan disimpan ke .wav
- Bisa pilih: hanya vokal, hanya instrumen, atau keduanya

## 🖼️ Preview Aplikasi
https://github.com/user-attachments/assets/6ab53196-76e1-4409-9baa-adb15dfd8791



- 🛠️ Fitur
- 🎧 Audio Preview (Vocals & Instruments)
- 🎚️ Kontrol volume + seek bar
- 🌙 Dark/Light Theme
- 💾 Simpan hasil pemisahan
- 📋 Log proses real-time
- 🚀 AI Vocal Separation dengan Spleeter

- 🗺️ Roadmap Pengembangan
 - _Support pemisahan 4/5 stems_
 - _Ekspor ke format lain (MP3, FLAC)_
 - _Playlist & batch processing_
 - _GUI interaktif dengan drag & drop_
 - _Visualisasi spektrum audio_
 
- **📜 Lisensi MIT.LICENSE**
**👨‍💻 Author ShiroAI Development Team**

[GitHub: @Renn-devBI]
