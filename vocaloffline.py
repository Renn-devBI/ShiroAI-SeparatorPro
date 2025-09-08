# Jangan merubah kode yang ada di sini karna akan merubah isi module juga yang sudah ada!
# Jika ingin merubah di sarankan install module dari awal agar tidak terjadi nya error di env

import os
import sys
import re
import threading
import tempfile
import shutil
import time
import gc
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import queue
import json
import pygame
from mutagen import File as MutagenFile
from PIL import Image, ImageTk
import io
import subprocess

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    import tkinter.ttk as ttk

class Config:
    def __init__(self):
        self.app_name = "ShiroAI Separator Pro"
        self.version = "2.2.0"
        self.supported_formats = ['.wav', '.mp3', '.flac', '.m4a', '.aac', '.ogg', '.wma']
        self.max_file_size = 100 * 1024 * 1024
        self.config_file = "shiroai_config.json"
        self.temp_dir = tempfile.mkdtemp(prefix='shiroai_')
        self.load_config()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self.theme = config_data.get('theme', 'dark')
                    self.last_input_dir = config_data.get('last_input_dir', str(Path.home()))
                    self.last_output_dir = config_data.get('last_output_dir', str(Path.home() / "Downloads"))
                    self.volume = config_data.get('volume', 0.7)
            else:
                self.theme = 'dark'
                self.last_input_dir = str(Path.home())
                self.last_output_dir = str(Path.home() / "Downloads")
                self.volume = 0.7
        except:
            self.theme = 'dark'
            self.last_input_dir = str(Path.home())
            self.last_output_dir = str(Path.home() / "Downloads")
            self.volume = 0.7
    
    def save_config(self):
        try:
            config_data = {
                'theme': self.theme,
                'last_input_dir': self.last_input_dir,
                'last_output_dir': self.last_output_dir,
                'volume': self.volume
            }
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except:
            pass

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        self.is_playing = False
        self.is_paused = False
        self.current_file = None
        self.position = 0
        self.duration = 0
        self.vocals_path = None
        self.instruments_path = None
        
    def load_audio(self, file_path):
        try:
            self.current_file = file_path
            self.get_duration()
            return True
        except Exception as e:
            print(f"Error loading audio: {e}")
            return False
    
    def get_duration(self):
        try:
            if self.current_file:
                audio_file = MutagenFile(self.current_file)
                if audio_file and audio_file.info:
                    self.duration = audio_file.info.length
                else:
                    self.duration = 0
        except:
            self.duration = 0
    
    def play(self):
        try:
            if self.current_file and os.path.exists(self.current_file):
                if self.is_paused:
                    pygame.mixer.music.unpause()
                    self.is_paused = False
                else:
                    pygame.mixer.music.load(self.current_file)
                    pygame.mixer.music.play(start=self.position)
                self.is_playing = True
                return True
        except Exception as e:
            print(f"Error playing audio: {e}")
        return False
    
    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.position = 0
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
    
    def get_pos(self):
        if self.is_playing:
            return pygame.mixer.music.get_pos() / 1000.0
        return self.position
    
    def seek(self, position):
        self.position = position
        if self.is_playing:
            self.stop()
            self.play()
    
    def is_playing_audio(self):
        return pygame.mixer.music.get_busy()

class AudioSeparator:
    def __init__(self, progress_callback=None, log_callback=None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.is_processing = False
        self.temp_vocals_path = None
        self.temp_instruments_path = None
    
    def log(self, message):
        if self.log_callback:
            self.log_callback(message)
        print(message)
    
    def update_progress(self, value):
        if self.progress_callback:
            self.progress_callback(value)
    
    def separate_audio(self, input_path, config):
        try:
            self.is_processing = True
            self.log(f"🎵 Memulai pemisahan audio: {os.path.basename(input_path)}")
            self.update_progress(10)
            
            try:
                if getattr(sys, 'frozen', False):
                    spleeter_path = os.path.join(os.path.dirname(sys.executable), 'spleeter')
                    if os.path.exists(spleeter_path):
                        sys.path.insert(0, spleeter_path)
                
                from spleeter.separator import Separator
                self.log("✅ Spleeter berhasil dimuat")
            except ImportError:
                raise Exception("❌ Spleeter tidak ditemukan. Pastikan file spleeter tersedia.")
            
            self.update_progress(20)
            
            temp_dir = config.temp_dir
            os.makedirs(temp_dir, exist_ok=True)
            
            self.log("🔧 Menginisialisasi separator...")
            separator = Separator('spleeter:2stems')
            self.update_progress(30)
            
            self.log("⚡ Memproses pemisahan audio...")
            separator.separate_to_file(input_path, temp_dir)
            self.update_progress(70)
            
            input_basename = os.path.splitext(os.path.basename(input_path))[0]
            spleeter_output_dir = os.path.join(temp_dir, input_basename)
            
            self.temp_vocals_path = os.path.join(spleeter_output_dir, "vocals.wav")
            self.temp_instruments_path = os.path.join(spleeter_output_dir, "accompaniment.wav")
            
            self.update_progress(90)
            self.log("✨ Pemisahan audio selesai! Siap untuk preview")
            self.update_progress(100)
            
            gc.collect()
            
            return self.temp_vocals_path, self.temp_instruments_path
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            raise e
        
        finally:
            self.is_processing = False
    
    def save_results(self, output_dir, original_filename, output_format='both'):
        try:
            if not (self.temp_vocals_path and self.temp_instruments_path):
                raise Exception("Tidak ada hasil untuk disimpan")
            
            clean_name = re.sub(r'[^\w\-_\. ]', '_', os.path.splitext(original_filename)[0])
            results = []
            
            if output_format in ['vocals', 'both'] and os.path.exists(self.temp_vocals_path):
                vocals_final = os.path.join(output_dir, f"{clean_name}_vocals.wav")
                shutil.copy2(self.temp_vocals_path, vocals_final)
                results.append(vocals_final)
                self.log(f"💾 Vocals disimpan: {os.path.basename(vocals_final)}")
            
            if output_format in ['instruments', 'both'] and os.path.exists(self.temp_instruments_path):
                instruments_final = os.path.join(output_dir, f"{clean_name}_instruments.wav")
                shutil.copy2(self.temp_instruments_path, instruments_final)
                results.append(instruments_final)
                self.log(f"💾 Instruments disimpan: {os.path.basename(instruments_final)}")
            
            return results
            
        except Exception as e:
            self.log(f"❌ Error saving: {str(e)}")
            raise e

class ModernShiroAI:
    def __init__(self):
        self.config = Config()
        self.setup_root()
        self.setup_theme()
        self.create_widgets()
        self.separator = None
        self.processing_thread = None
        self.audio_player = AudioPlayer()
        self.current_preview_type = None
        self.setup_message_queue()
        
    def setup_root(self):
        if CTK_AVAILABLE:
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()
            
        self.root.title(self.config.app_name)
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        
        try:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(os.path.dirname(sys.executable), 'yukichibi.ico')
            else:
                icon_path = 'yukichibi.ico'
                
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"1000x750+{x}+{y}")
    
    def setup_theme(self):
        if CTK_AVAILABLE:
            ctk.set_appearance_mode(self.config.theme)
            ctk.set_default_color_theme("blue")
        
    def create_widgets(self):
        if CTK_AVAILABLE:
            main_frame = ctk.CTkFrame(self.root)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            main_frame = tk.Frame(self.root, bg='#212121')
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_header(main_frame)
        self.create_input_section(main_frame)
        self.create_preview_section(main_frame)
        self.create_output_section(main_frame)
        self.create_process_section(main_frame)
        self.create_log_section(main_frame)
    
    def create_header(self, parent):
        if CTK_AVAILABLE:
            header_frame = ctk.CTkFrame(parent, height=70)
            header_frame.pack(fill="x", pady=(0, 10))
            header_frame.pack_propagate(False)
            
            title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            title_frame.pack(fill="both", expand=True, padx=15, pady=10)
            
            title_label = ctk.CTkLabel(title_frame, 
                                     text="🎵 ShiroAI Separator Pro", 
                                     font=ctk.CTkFont(size=24, weight="bold"))
            title_label.pack(side="left")
            
            subtitle_label = ctk.CTkLabel(title_frame, 
                                        text="AI-Powered Vocal Separator", 
                                        font=ctk.CTkFont(size=12))
            subtitle_label.pack(side="left", padx=(15, 0), pady=(5, 0))
            
            control_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            control_frame.pack(side="right", padx=15, pady=10)
            
            info_btn = ctk.CTkButton(control_frame, 
                                   text="ℹ️ Info", 
                                   command=self.show_about,
                                   width=80)
            info_btn.pack(side="right", padx=(5, 0))
            
            theme_btn = ctk.CTkButton(control_frame, 
                                    text="🌙 Theme", 
                                    command=self.toggle_theme,
                                    width=80)
            theme_btn.pack(side="right")
        
    def create_input_section(self, parent):
        if CTK_AVAILABLE:
            input_frame = ctk.CTkFrame(parent)
            input_frame.pack(fill="x", pady=(0, 10))
            
            title_label = ctk.CTkLabel(input_frame, 
                                     text="📁 Audio Input", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
            title_label.pack(anchor="w", padx=15, pady=(10, 5))
            
            file_frame = ctk.CTkFrame(input_frame)
            file_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            self.file_var = tk.StringVar()
            self.file_entry = ctk.CTkEntry(file_frame, 
                                         textvariable=self.file_var,
                                         placeholder_text="Pilih file audio...",
                                         height=35)
            self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)
            
            self.browse_btn = ctk.CTkButton(file_frame, 
                                          text="📂 Browse", 
                                          command=self.browse_file,
                                          width=100,
                                          height=35)
            self.browse_btn.pack(side="right")
    
    def create_preview_section(self, parent):
        if CTK_AVAILABLE:
            preview_frame = ctk.CTkFrame(parent)
            preview_frame.pack(fill="x", pady=(0, 10))
            
            title_label = ctk.CTkLabel(preview_frame, 
                                     text="🎧 Audio Preview", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
            title_label.pack(anchor="w", padx=15, pady=(10, 5))
            
            controls_container = ctk.CTkFrame(preview_frame)
            controls_container.pack(fill="x", padx=15, pady=(0, 10))
            
            type_frame = ctk.CTkFrame(controls_container)
            type_frame.pack(fill="x", pady=(0, 10))
            
            type_label = ctk.CTkLabel(type_frame, text="Audio Type:", font=ctk.CTkFont(size=12, weight="bold"))
            type_label.pack(side="left", padx=(0, 15))
            
            self.preview_type_var = tk.StringVar(value="vocals")
            vocals_radio = ctk.CTkRadioButton(type_frame, 
                                            text="🎤 Vocals", 
                                            variable=self.preview_type_var, 
                                            value="vocals",
                                            command=self.switch_preview_audio)
            vocals_radio.pack(side="left", padx=(0, 15))
            
            instruments_radio = ctk.CTkRadioButton(type_frame, 
                                                 text="🎸 Instruments", 
                                                 variable=self.preview_type_var, 
                                                 value="instruments",
                                                 command=self.switch_preview_audio)
            instruments_radio.pack(side="left")
            
            player_frame = ctk.CTkFrame(controls_container)
            player_frame.pack(fill="x", pady=(0, 10))
            
            btn_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
            btn_frame.pack(pady=5)
            
            self.prev_btn = ctk.CTkButton(btn_frame, 
                                        text="⏮️ 10s", 
                                        command=lambda: self.seek_audio(-10),
                                        width=80,
                                        state="disabled")
            self.prev_btn.pack(side="left", padx=(0, 5))
            
            self.play_btn = ctk.CTkButton(btn_frame, 
                                        text="▶️ Play", 
                                        command=self.toggle_play,
                                        width=80,
                                        state="disabled")
            self.play_btn.pack(side="left", padx=(0, 5))
            
            self.stop_btn = ctk.CTkButton(btn_frame, 
                                        text="⏹️ Stop", 
                                        command=self.stop_audio,
                                        width=80,
                                        state="disabled")
            self.stop_btn.pack(side="left", padx=(0, 5))
            
            self.next_btn = ctk.CTkButton(btn_frame, 
                                        text="⏭️ 10s", 
                                        command=lambda: self.seek_audio(10),
                                        width=80,
                                        state="disabled")
            self.next_btn.pack(side="left", padx=(0, 15))
            
            volume_label = ctk.CTkLabel(btn_frame, text="🔊 Volume:", font=ctk.CTkFont(size=12))
            volume_label.pack(side="left", padx=(0, 10))
            
            self.volume_slider = ctk.CTkSlider(btn_frame, 
                                             from_=0, to=1, 
                                             number_of_steps=100,
                                             command=self.change_volume,
                                             width=120)
            self.volume_slider.pack(side="left")
            self.volume_slider.set(self.config.volume)
            
            progress_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
            progress_frame.pack(fill="x", pady=(0, 5))
            
            self.audio_progress = ctk.CTkProgressBar(progress_frame)
            self.audio_progress.pack(fill="x", pady=(0, 5))
            self.audio_progress.set(0)
            
            self.time_label = ctk.CTkLabel(progress_frame, text="00:00 / 00:00", font=ctk.CTkFont(size=10))
            self.time_label.pack()
    
    def create_output_section(self, parent):
        if CTK_AVAILABLE:
            output_frame = ctk.CTkFrame(parent)
            output_frame.pack(fill="x", pady=(0, 10))
            
            title_label = ctk.CTkLabel(output_frame, 
                                     text="💾 Output Settings", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
            title_label.pack(anchor="w", padx=15, pady=(10, 5))
            
            dir_frame = ctk.CTkFrame(output_frame)
            dir_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            dir_label = ctk.CTkLabel(dir_frame, text="📁 Output Directory:", font=ctk.CTkFont(size=12, weight="bold"))
            dir_label.pack(anchor="w", padx=(0, 10), pady=(5, 5))
            
            dir_select_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
            dir_select_frame.pack(fill="x", pady=(0, 5))
            
            self.output_var = tk.StringVar(value=self.config.last_output_dir)
            self.output_entry = ctk.CTkEntry(dir_select_frame, 
                                           textvariable=self.output_var,
                                           height=35)
            self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            self.output_btn = ctk.CTkButton(dir_select_frame, 
                                          text="📂 Browse", 
                                          command=self.browse_output,
                                          width=100,
                                          height=35)
            self.output_btn.pack(side="right")
            
            format_frame = ctk.CTkFrame(output_frame)
            format_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            format_label = ctk.CTkLabel(format_frame, text="🎵 Save Format:", font=ctk.CTkFont(size=12, weight="bold"))
            format_label.pack(anchor="w", pady=(0, 5))
            
            format_options = ctk.CTkFrame(format_frame, fg_color="transparent")
            format_options.pack(fill="x", pady=(0, 5))
            
            self.format_var = tk.StringVar(value="both")
            
            vocals_cb = ctk.CTkRadioButton(format_options, 
                                         text="🎤 Vocals Only", 
                                         variable=self.format_var, 
                                         value="vocals")
            vocals_cb.pack(side="left", padx=(0, 15))
            
            instruments_cb = ctk.CTkRadioButton(format_options, 
                                              text="🎸 Instruments Only", 
                                              variable=self.format_var, 
                                              value="instruments")
            instruments_cb.pack(side="left", padx=(0, 15))
            
            both_cb = ctk.CTkRadioButton(format_options, 
                                       text="🎵 Both Files", 
                                       variable=self.format_var, 
                                       value="both")
            both_cb.pack(side="left")
    
    def create_process_section(self, parent):
        if CTK_AVAILABLE:
            process_frame = ctk.CTkFrame(parent)
            process_frame.pack(fill="x", pady=(0, 10))
            
            btn_container = ctk.CTkFrame(process_frame)
            btn_container.pack(fill="x", padx=15, pady=10)
            
            self.process_btn = ctk.CTkButton(btn_container, 
                                           text="🚀 Generate AI Separation", 
                                           command=self.start_processing,
                                           height=40,
                                           font=ctk.CTkFont(size=14, weight="bold"),
                                           fg_color=("#1f538d", "#14375e"),
                                           hover_color=("#14375e", "#1f538d"))
            self.process_btn.pack(side="left", padx=(0, 10))
            
            self.save_btn = ctk.CTkButton(btn_container, 
                                        text="💾 Save Results", 
                                        command=self.save_results,
                                        height=40,
                                        font=ctk.CTkFont(size=14),
                                        state="disabled")
            self.save_btn.pack(side="left", padx=(0, 10))
            
            self.reset_btn = ctk.CTkButton(btn_container, 
                                         text="🔄 Reset", 
                                         command=self.reset_app,
                                         height=40,
                                         font=ctk.CTkFont(size=14))
            self.reset_btn.pack(side="right")
            
            progress_container = ctk.CTkFrame(process_frame)
            progress_container.pack(fill="x", padx=15, pady=(0, 10))
            
            self.progress_var = tk.DoubleVar()
            self.progress_bar = ctk.CTkProgressBar(progress_container, variable=self.progress_var)
            self.progress_bar.pack(fill="x", pady=(0, 5))
            
            self.status_var = tk.StringVar(value="Ready to process audio - Select file and click Generate")
            self.status_label = ctk.CTkLabel(progress_container, textvariable=self.status_var)
            self.status_label.pack(pady=(0, 5))
    
    def create_log_section(self, parent):
        if CTK_AVAILABLE:
            log_frame = ctk.CTkFrame(parent)
            log_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            title_label = ctk.CTkLabel(log_frame, 
                                     text="📋 Process Log", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
            title_label.pack(anchor="w", padx=15, pady=(10, 5))
            
            self.log_text = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(size=11))
            self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        else:
            log_frame = tk.Frame(parent, bg='#2b2b2b')
            log_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            title_label = tk.Label(log_frame, 
                                 text="📋 Process Log", 
                                 font=("Arial", 12, "bold"),
                                 fg="white", bg='#2b2b2b')
            title_label.pack(anchor="w", padx=15, pady=(10, 5))
            
            self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                    font=("Consolas", 10), 
                                                    bg='#1e1e1e', 
                                                    fg='white',
                                                    insertbackground='white')
            self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))
    
    def setup_message_queue(self):
        self.message_queue = queue.Queue()
        self.root.after(100, self.process_queue)
        
        self.update_audio_position()
    
    def browse_file(self):
        filetypes = [
            ("Audio Files", " ".join([f"*{ext}" for ext in self.config.supported_formats])),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            initialdir=self.config.last_input_dir,
            filetypes=filetypes
        )
        
        if filename:
            file_size = os.path.getsize(filename)
            if file_size > self.config.max_file_size:
                messagebox.showerror("Error", f"File too large! Maximum {self.config.max_file_size // (1024*1024)}MB")
                return
            
            self.file_var.set(filename)
            self.config.last_input_dir = os.path.dirname(filename)
            self.config.save_config()
            self.log_message(f"📁 File selected: {os.path.basename(filename)}")
    
    def browse_output(self):
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_var.get()
        )
        
        if directory:
            self.output_var.set(directory)
            self.config.last_output_dir = directory
            self.config.save_config()
            self.log_message(f"📂 Output directory: {directory}")
    
    def toggle_theme(self):
        if CTK_AVAILABLE:
            self.config.theme = 'light' if self.config.theme == 'dark' else 'dark'
            self.config.save_config()
            ctk.set_appearance_mode(self.config.theme)
            self.log_message(f"🎨 Theme switched to {self.config.theme}")
    
    def show_about(self):
        about_text = f"""🎵 {self.config.app_name} v{self.config.version}

🤖 AI Technology:
• Deep Learning-based audio separation
• 2-stems separation (vocals & accompaniment)

👨‍💻 Developer:
• ShiroAI Development Team
• Built with Python & CustomTkinter

🔧 Features:
• Real-time audio preview
• Modern responsive UI
• Dark/Light theme support
• Multiple output formats
• Advanced audio controls

📦 This is a standalone application
Created with ❤️ for music enthusiasts
"""
        
        if CTK_AVAILABLE:
            dialog = ctk.CTkToplevel()
            dialog.title("About ShiroAI Separator Pro")
            dialog.geometry("500x500")
            dialog.resizable(False, False)
            
            dialog.transient(self.root)
            dialog.grab_set()
            
            text_widget = ctk.CTkTextbox(dialog, font=ctk.CTkFont(size=12))
            text_widget.pack(fill="both", expand=True, padx=20, pady=20)
            text_widget.insert("1.0", about_text)
            text_widget.configure(state="disabled")
            
            close_btn = ctk.CTkButton(dialog, text="Close", command=dialog.destroy)
            close_btn.pack(pady=(0, 20))
        else:
            messagebox.showinfo("About", about_text)
    
    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        if CTK_AVAILABLE:
            self.log_text.insert("end", log_entry)
            self.log_text.see("end")
        else:
            self.log_text.insert("end", log_entry)
            self.log_text.see("end")
    
    def reset_app(self):
        self.audio_player.stop()
        
        self.file_var.set("")
        self.progress_var.set(0)
        self.status_var.set("Ready to process audio - Select file and click Generate")
        self.audio_progress.set(0)
        self.time_label.configure(text="00:00 / 00:00")
        
        if CTK_AVAILABLE:
            self.process_btn.configure(state="normal", text="🚀 Generate AI Separation")
            self.play_btn.configure(state="disabled", text="▶️ Play")
            self.stop_btn.configure(state="disabled")
            self.save_btn.configure(state="disabled")
            self.prev_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")
        
        self.separator = None
        self.current_preview_type = None
        
        if CTK_AVAILABLE:
            self.log_text.delete("1.0", "end")
        else:
            self.log_text.delete("1.0", "end")
        
        self.log_message("🔄 Application reset successfully!")
        self.log_message("📋 Select an audio file to start vocal separation")
    
    def start_processing(self):
        if not self.file_var.get():
            messagebox.showerror("Error", "Please select an audio file!")
            return
        
        if not os.path.exists(self.file_var.get()):
            messagebox.showerror("Error", "Audio file not found!")
            return
        
        self.audio_player.stop()
        self.play_btn.configure(state="disabled")
        self.stop_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.prev_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        
        if CTK_AVAILABLE:
            self.process_btn.configure(state="disabled", text="⏳ Processing...")
        
        self.progress_var.set(0)
        self.status_var.set("Starting AI separation process...")
        
        self.processing_thread = threading.Thread(target=self.process_audio_thread)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def process_audio_thread(self):
        try:
            separator = AudioSeparator(
                progress_callback=self.update_progress,
                log_callback=self.log_from_thread
            )
            
            vocals_path, instruments_path = separator.separate_audio(
                self.file_var.get(),
                self.config
            )
            
            self.separator = separator
            self.audio_player.vocals_path = vocals_path
            self.audio_player.instruments_path = instruments_path
            self.message_queue.put(('finished', (vocals_path, instruments_path)))
            
        except Exception as e:
            self.message_queue.put(('error', str(e)))
    
    def switch_preview_audio(self):
        if not (hasattr(self, 'separator') and self.separator):
            return
            
        self.audio_player.stop()
        
        preview_type = self.preview_type_var.get()
        audio_path = None
        
        if preview_type == "vocals" and self.audio_player.vocals_path:
            audio_path = self.audio_player.vocals_path
            self.current_preview_type = "vocals"
            self.log_message("🎤 Switched to vocals preview")
        elif preview_type == "instruments" and self.audio_player.instruments_path:
            audio_path = self.audio_player.instruments_path
            self.current_preview_type = "instruments"
            self.log_message("🎸 Switched to instruments preview")
        
        if audio_path and self.audio_player.load_audio(audio_path):
            if CTK_AVAILABLE:
                self.play_btn.configure(state="normal")
                self.stop_btn.configure(state="normal")
                self.prev_btn.configure(state="normal")
                self.next_btn.configure(state="normal")
            
            if self.audio_player.play():
                if CTK_AVAILABLE:
                    self.play_btn.configure(text="⏸️ Pause")
                self.log_message(f"▶️ Playing {self.current_preview_type}")
    
    def toggle_play(self):
        if not self.current_preview_type:
            return
            
        if self.audio_player.is_playing:
            self.audio_player.pause()
            if CTK_AVAILABLE:
                self.play_btn.configure(text="▶️ Play")
            self.log_message("⏸️ Audio paused")
        else:
            if self.audio_player.play():
                if CTK_AVAILABLE:
                    self.play_btn.configure(text="⏸️ Pause")
                self.log_message(f"▶️ Playing {self.current_preview_type}")
    
    def stop_audio(self):
        self.audio_player.stop()
        if CTK_AVAILABLE:
            self.play_btn.configure(text="▶️ Play")
        self.audio_progress.set(0)
        self.time_label.configure(text="00:00 / 00:00")
        self.log_message("⏹️ Audio stopped")
    
    def seek_audio(self, seconds):
        if not self.audio_player.current_file:
            return
            
        new_position = max(0, min(self.audio_player.get_pos() + seconds, self.audio_player.duration))
        self.audio_player.seek(new_position)
        
        direction = "forward" if seconds > 0 else "backward"
        self.log_message(f"⏩ Seeked {abs(seconds)}s {direction}")
    
    def change_volume(self, value):
        self.audio_player.set_volume(value)
        self.config.volume = value
        self.config.save_config()
    
    def update_audio_position(self):
        if self.audio_player.is_playing_audio() and self.audio_player.duration > 0:
            current_time = self.audio_player.get_pos()
            if current_time >= 0:
                progress = current_time / self.audio_player.duration
                self.audio_progress.set(progress)
                
                current_str = self.format_time(current_time)
                duration_str = self.format_time(self.audio_player.duration)
                if CTK_AVAILABLE:
                    self.time_label.configure(text=f"{current_str} / {duration_str}")
        
        elif not self.audio_player.is_playing_audio() and self.audio_player.is_playing:
            self.audio_player.is_playing = False
            if CTK_AVAILABLE:
                self.play_btn.configure(text="▶️ Play")
            self.audio_progress.set(0)
        
        self.root.after(100, self.update_audio_position)
    
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def save_results(self):
        if not (hasattr(self, 'separator') and self.separator):
            messagebox.showerror("Error", "No processed audio to save!")
            return
        
        if not self.output_var.get():
            messagebox.showerror("Error", "Please select output directory!")
            return
        
        if not os.path.exists(self.output_var.get()):
            messagebox.showerror("Error", "Output directory not found!")
            return
        
        try:
            original_filename = os.path.basename(self.file_var.get())
            results = self.separator.save_results(
                self.output_var.get(),
                original_filename,
                self.format_var.get()
            )
            
            result_msg = "✅ Audio separation saved successfully!\n\nFiles created:\n"
            for result in results:
                result_msg += f"• {os.path.basename(result)}\n"
            
            if CTK_AVAILABLE:
                dialog = ctk.CTkToplevel()
                dialog.title("Save Successful")
                dialog.geometry("400x300")
                dialog.resizable(False, False)
                dialog.transient(self.root)
                dialog.grab_set()
                
                label = ctk.CTkLabel(dialog, text=result_msg, font=ctk.CTkFont(size=12), justify="left")
                label.pack(padx=20, pady=20)
                
                btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
                btn_frame.pack(fill="x", padx=20, pady=(0, 20))
                
                open_btn = ctk.CTkButton(btn_frame, text="📂 Open Folder", 
                                       command=lambda: self.open_folder(self.output_var.get()))
                open_btn.pack(side="left", padx=(0, 10))
                
                close_btn = ctk.CTkButton(btn_frame, text="Close", command=dialog.destroy)
                close_btn.pack(side="right")
            else:
                messagebox.showinfo("Save Successful", result_msg)
                self.open_folder(self.output_var.get())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")
    
    def open_folder(self, path):
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except:
            pass
    
    def update_progress(self, value):
        self.message_queue.put(('progress', value))
    
    def log_from_thread(self, message):
        self.message_queue.put(('log', message))
    
    def process_queue(self):
        try:
            while True:
                try:
                    msg_type, data = self.message_queue.get_nowait()
                    
                    if msg_type == 'progress':
                        self.progress_var.set(data / 100)
                        self.status_var.set(f"Processing... {int(data)}%")
                        
                    elif msg_type == 'log':
                        self.log_message(data)
                        
                    elif msg_type == 'finished':
                        vocals_path, instruments_path = data
                        self.status_var.set("✅ Separation completed! Ready to preview and save")
                        if CTK_AVAILABLE:
                            self.process_btn.configure(state="normal", text="✅ Separation Complete")
                            self.save_btn.configure(state="normal")
                            self.play_btn.configure(state="normal")
                            self.stop_btn.configure(state="normal")
                            self.prev_btn.configure(state="normal")
                            self.next_btn.configure(state="normal")
                        
                        self.log_message("✨ Audio separation completed successfully!")
                        self.log_message("🎧 Use the preview controls to listen to the results")
                        self.log_message("💾 Click 'Save Results' to export the separated audio")
                        
                        self.current_preview_type = "vocals"
                        self.preview_type_var.set("vocals")
                        self.audio_player.load_audio(vocals_path)
                        
                    elif msg_type == 'error':
                        self.status_var.set(f"❌ Error: {data}")
                        if CTK_AVAILABLE:
                            self.process_btn.configure(state="normal", text="🚀 Generate AI Separation")
                        self.log_message(f"❌ Processing failed: {data}")
                        messagebox.showerror("Processing Error", f"Audio separation failed:\n{data}")
                        
                except queue.Empty:
                    break
                    
        finally:
            self.root.after(100, self.process_queue)
    
    def run(self):
        self.log_message(f"🎵 Welcome to {self.config.app_name} v{self.config.version}")
        self.log_message("📋 Select an audio file to start vocal separation")
        self.log_message("🎧 Use the preview controls to listen to the results")
        self.log_message("💾 Save your separated audio files when ready")
        
        try:
            self.root.mainloop()
        finally:
            self.cleanup()
    
    def cleanup(self):
        self.audio_player.stop()
        self.config.save_config()
        
        try:
            if hasattr(self, 'separator') and self.separator:
                if hasattr(self.separator, 'temp_vocals_path') and self.separator.temp_vocals_path:
                    try:
                        os.remove(self.separator.temp_vocals_path)
                    except:
                        pass
                if hasattr(self.separator, 'temp_instruments_path') and self.separator.temp_instruments_path:
                    try:
                        os.remove(self.separator.temp_instruments_path)
                    except:
                        pass
        except:
            pass

if __name__ == "__main__":
    try:
        app = ModernShiroAI()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")