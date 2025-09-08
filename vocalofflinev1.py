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
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import queue
import json

# Konfigurasi aplikasi
class Config:
    def __init__(self):
        self.app_name = "ShiroAIApps - Offline Vocal Separator"
        self.version = "1.0.0"
        self.supported_formats = ['.wav', '.mp3', '.flac', '.m4a', '.aac', '.ogg', '.wma']
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.config_file = "vocakapps_config.json"
        self.load_config()
    
    def load_config(self):
        """Load konfigurasi dari file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self.theme = config_data.get('theme', 'light')
                    self.last_output_dir = config_data.get('last_output_dir', str(Path.home() / "Downloads"))
            else:
                self.theme = 'light'
                self.last_output_dir = str(Path.home() / "Downloads")
        except:
            self.theme = 'light'
            self.last_output_dir = str(Path.home() / "Downloads")
    
    def save_config(self):
        """Simpan konfigurasi ke file"""
        try:
            config_data = {
                'theme': self.theme,
                'last_output_dir': self.last_output_dir
            }
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except:
            pass

class AudioSeparator:
    def __init__(self, progress_callback=None, log_callback=None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.is_processing = False
    
    def log(self, message):
        """Log pesan ke callback"""
        if self.log_callback:
            self.log_callback(message)
        print(message)
    
    def update_progress(self, value):
        """Update progress bar"""
        if self.progress_callback:
            self.progress_callback(value)
    
    def separate_audio(self, input_path, output_dir, output_format='both'):
        """Pisahkan audio menggunakan Spleeter"""
        try:
            self.is_processing = True
            self.log(f"Memulai pemisahan audio: {os.path.basename(input_path)}")
            self.update_progress(10)
            
            # Import Spleeter
            try:
                from spleeter.separator import Separator
                self.log("Spleeter berhasil dimuat")
            except ImportError:
                raise Exception("Spleeter tidak terinstall. Jalankan: pip install spleeter")
            
            self.update_progress(20)
            
            # Buat direktori sementara
            temp_dir = tempfile.mkdtemp(prefix='vocak_sep_')
            self.log(f"Direktori sementara: {temp_dir}")
            
            # Inisialisasi separator
            self.log("Menginisialisasi separator...")
            separator = Separator('spleeter:2stems')
            self.update_progress(30)
            
            # Proses pemisahan
            self.log("Memproses pemisahan audio...")
            separator.separate_to_file(input_path, temp_dir)
            self.update_progress(70)
            
            # Pindahkan file hasil
            input_basename = os.path.splitext(os.path.basename(input_path))[0]
            clean_name = re.sub(r'[^\w\-_\. ]', '_', input_basename)
            
            # Path file hasil spleeter
            spleeter_output_dir = os.path.join(temp_dir, input_basename)
            vocals_temp = os.path.join(spleeter_output_dir, "vocals.wav")
            accompaniment_temp = os.path.join(spleeter_output_dir, "accompaniment.wav")
            
            # Path file final
            vocals_final = os.path.join(output_dir, f"{clean_name}_vocals.wav")
            instruments_final = os.path.join(output_dir, f"{clean_name}_instruments.wav")
            
            results = []
            
            # Pindahkan file sesuai format yang diminta
            if output_format in ['vocals', 'both'] and os.path.exists(vocals_temp):
                shutil.move(vocals_temp, vocals_final)
                results.append(vocals_final)
                self.log(f"Vocals disimpan: {vocals_final}")
            
            if output_format in ['instruments', 'both'] and os.path.exists(accompaniment_temp):
                shutil.move(accompaniment_temp, instruments_final)
                results.append(instruments_final)
                self.log(f"Instruments disimpan: {instruments_final}")
            
            self.update_progress(90)
            
            # Bersihkan direktori sementara
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            self.update_progress(100)
            self.log("Pemisahan audio selesai!")
            
            # Bersihkan memori
            gc.collect()
            
            return results
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            # Bersihkan jika terjadi error
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise e
        
        finally:
            self.is_processing = False

class VocakApps:
    def __init__(self):
        self.config = Config()
        self.root = tk.Tk()
        self.setup_window()
        self.setup_theme()
        self.create_widgets()
        self.separator = None
        self.processing_thread = None
        
    def setup_window(self):
        """Setup window utama"""
        self.root.title(self.config.app_name)
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Icon (opsional)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center window di tengah layar"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
    def setup_theme(self):
        """Setup tema aplikasi"""
        self.style = ttk.Style()
        
        if self.config.theme == 'dark':
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def apply_dark_theme(self):
        """Apply tema dark"""
        self.root.configure(bg='#2b2b2b')
        
        self.style.theme_use('clam')
        
        # Konfigurasi warna dark theme
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TLabel', background='#2b2b2b', foreground='white')
        self.style.configure('TButton', background='#404040', foreground='white')
        self.style.configure('TEntry', fieldbackground='#404040', foreground='white')
        self.style.configure('TCombobox', fieldbackground='#404040', foreground='white')
        self.style.configure('TCheckbutton', background='#2b2b2b', foreground='white')
        self.style.configure('TProgressbar', background='#4CAF50')
        
        self.colors = {
            'bg': '#2b2b2b',
            'fg': 'white',
            'entry_bg': '#404040',
            'button_bg': '#404040',
            'accent': '#4CAF50',
            'text_bg': '#1e1e1e'
        }
    
    def apply_light_theme(self):
        """Apply tema light"""
        self.root.configure(bg='white')
        
        self.style.theme_use('clam')
        
        # Konfigurasi warna light theme
        self.style.configure('TFrame', background='white')
        self.style.configure('TLabel', background='white', foreground='black')
        self.style.configure('TButton', background='#f0f0f0', foreground='black')
        self.style.configure('TEntry', fieldbackground='white', foreground='black')
        self.style.configure('TCombobox', fieldbackground='white', foreground='black')
        self.style.configure('TCheckbutton', background='white', foreground='black')
        self.style.configure('TProgressbar', background='#2196F3')
        
        self.colors = {
            'bg': 'white',
            'fg': 'black',
            'entry_bg': 'white',
            'button_bg': '#f0f0f0',
            'accent': '#2196F3',
            'text_bg': 'white'
        }
    
    def toggle_theme(self):
        """Toggle antara light dan dark theme"""
        self.config.theme = 'light' if self.config.theme == 'dark' else 'dark'
        self.config.save_config()
        self.setup_theme()
        self.update_log_colors()
    
    def create_widgets(self):
        """Buat semua widget UI"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)  # Log area
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="ShiroAIApps", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, sticky="w")
        
        subtitle_label = ttk.Label(header_frame, text="Offline Vocal Separator", font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, sticky="w")
        
        # Theme toggle button
        theme_btn = ttk.Button(header_frame, text="🌓 Theme", command=self.toggle_theme, width=10)
        theme_btn.grid(row=0, column=1, sticky="e", padx=(0, 10))
        
        # Info button
        info_btn = ttk.Button(header_frame, text="ℹ️ Info", command=self.show_info, width=10)
        info_btn.grid(row=1, column=1, sticky="e", padx=(0, 10))
        
        header_frame.grid_columnconfigure(0, weight=1)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Audio", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        file_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="File:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, state="readonly")
        self.file_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        self.browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        self.browse_btn.grid(row=0, column=2)
        
        # Output settings
        output_frame = ttk.LabelFrame(main_frame, text="Pengaturan Output", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        output_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.output_entry.insert(0, self.config.last_output_dir)
        
        self.output_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output)
        self.output_btn.grid(row=0, column=2)
        
        ttk.Label(output_frame, text="Format:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        
        format_frame = ttk.Frame(output_frame)
        format_frame.grid(row=1, column=1, sticky="w", pady=(10, 0))
        
        self.format_var = tk.StringVar(value="both")
        ttk.Radiobutton(format_frame, text="Vocals Only", variable=self.format_var, value="vocals").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(format_frame, text="Instruments Only", variable=self.format_var, value="instruments").grid(row=0, column=1, sticky="w", padx=(20, 0))
        ttk.Radiobutton(format_frame, text="Both", variable=self.format_var, value="both").grid(row=0, column=2, sticky="w", padx=(20, 0))
        
        # Process button dan progress
        process_frame = ttk.Frame(main_frame)
        process_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        process_frame.grid_columnconfigure(0, weight=1)
        
        self.process_btn = ttk.Button(process_frame, text="🎵 Mulai Pemisahan", command=self.start_processing, style="Accent.TButton")
        self.process_btn.grid(row=0, column=0, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(process_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        
        self.status_var = tk.StringVar(value="Siap untuk memproses")
        self.status_label = ttk.Label(process_frame, textvariable=self.status_var)
        self.status_label.grid(row=2, column=0, pady=(5, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, 0))
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        self.log_text = ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        self.update_log_colors()
        
        # Setup message queue untuk thread communication
        self.message_queue = queue.Queue()
        self.root.after(100, self.process_queue)
        
        # Configure accent style
        self.style.configure("Accent.TButton", 
                           background=self.colors['accent'], 
                           foreground='white',
                           font=("Arial", 11, "bold"))
    
    def update_log_colors(self):
        """Update warna log area sesuai tema"""
        self.log_text.configure(
            bg=self.colors['text_bg'], 
            fg=self.colors['fg'],
            insertbackground=self.colors['fg']
        )
    
    def browse_file(self):
        """Browse file audio input"""
        filetypes = [
            ("Audio Files", " ".join([f"*{ext}" for ext in self.config.supported_formats])),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Pilih File Audio",
            filetypes=filetypes
        )
        
        if filename:
            # Validasi ukuran file
            file_size = os.path.getsize(filename)
            if file_size > self.config.max_file_size:
                messagebox.showerror("Error", f"File terlalu besar! Maksimal {self.config.max_file_size // (1024*1024)}MB")
                return
            
            self.file_var.set(filename)
            self.log_message(f"File dipilih: {os.path.basename(filename)}")
    
    def browse_output(self):
        """Browse direktori output"""
        directory = filedialog.askdirectory(
            title="Pilih Direktori Output",
            initialdir=self.output_var.get()
        )
        
        if directory:
            self.output_var.set(directory)
            self.config.last_output_dir = directory
            self.config.save_config()
            self.log_message(f"Output direktori: {directory}")
    
    def log_message(self, message):
        """Tambah pesan ke log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, log_entry)
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)
    
    def update_progress(self, value):
        """Update progress bar dari thread"""
        self.message_queue.put(('progress', value))
    
    def update_status(self, status):
        """Update status label dari thread"""
        self.message_queue.put(('status', status))
    
    def log_from_thread(self, message):
        """Log message dari thread"""
        self.message_queue.put(('log', message))
    
    def process_queue(self):
        """Proses pesan dari queue"""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                
                if msg_type == 'progress':
                    self.progress_var.set(data)
                elif msg_type == 'status':
                    self.status_var.set(data)
                elif msg_type == 'log':
                    self.log_message(data)
                elif msg_type == 'finished':
                    self.processing_finished(data)
                elif msg_type == 'error':
                    self.processing_error(data)
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.process_queue)
    
    def start_processing(self):
        """Mulai proses pemisahan audio"""
        # Validasi input
        if not self.file_var.get():
            messagebox.showerror("Error", "Pilih file audio terlebih dahulu!")
            return
        
        if not self.output_var.get():
            messagebox.showerror("Error", "Pilih direktori output terlebih dahulu!")
            return
        
        if not os.path.exists(self.file_var.get()):
            messagebox.showerror("Error", "File audio tidak ditemukan!")
            return
        
        if not os.path.exists(self.output_var.get()):
            messagebox.showerror("Error", "Direktori output tidak ditemukan!")
            return
        
        # Disable tombol dan mulai processing
        self.process_btn.configure(state='disabled', text="⏳ Memproses...")
        self.progress_var.set(0)
        self.status_var.set("Memulai pemisahan audio...")
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_audio_thread)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def process_audio_thread(self):
        """Thread untuk memproses audio"""
        try:
            # Buat separator
            separator = AudioSeparator(
                progress_callback=self.update_progress,
                log_callback=self.log_from_thread
            )
            
            # Proses pemisahan
            results = separator.separate_audio(
                self.file_var.get(),
                self.output_var.get(),
                self.format_var.get()
            )
            
            self.message_queue.put(('finished', results))
            
        except Exception as e:
            self.message_queue.put(('error', str(e)))
    
    def processing_finished(self, results):
        """Callback ketika processing selesai"""
        self.process_btn.configure(state='normal', text="🎵 Mulai Pemisahan")
        self.status_var.set(f"Selesai! {len(results)} file berhasil dibuat")
        
        # Show success message
        result_msg = "Pemisahan audio berhasil!\n\nFile yang dibuat:\n"
        for result in results:
            result_msg += f"• {os.path.basename(result)}\n"
        
        messagebox.showinfo("Sukses", result_msg)
        
        # Ask if want to open output folder
        if messagebox.askyesno("Buka Folder", "Buka folder output?"):
            self.open_output_folder()
    
    def processing_error(self, error_msg):
        """Callback ketika terjadi error"""
        self.process_btn.configure(state='normal', text="🎵 Mulai Pemisahan")
        self.status_var.set("Error saat memproses")
        self.progress_var.set(0)
        
        messagebox.showerror("Error", f"Terjadi kesalahan:\n{error_msg}")
    
    def open_output_folder(self):
        """Buka folder output"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(self.output_var.get())
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{self.output_var.get()}"')
            else:
                os.system(f'xdg-open "{self.output_var.get()}"')
        except:
            pass
    
    def show_info(self):
        """Tampilkan info aplikasi"""
        info_text = f"""
{self.config.app_name}
Version: {self.config.version}

Aplikasi untuk memisahkan vocal dan instrumental dari file audio.

Supported Formats:
{', '.join(self.config.supported_formats)}

Requirements:
• Spleeter library
• TensorFlow
• FFmpeg

Cara Install:
pip install spleeter

Developed with ❤️
        """.strip()
        
        messagebox.showinfo("Info", info_text)
    
    def run(self):
        """Jalankan aplikasi"""
        self.log_message("VocakApps siap digunakan!")
        self.log_message("Pilih file audio dan mulai pemisahan vocal.")
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
    
    def on_closing(self):
        """Handle penutupan aplikasi"""
        if self.processing_thread and self.processing_thread.is_alive():
            if messagebox.askyesno("Konfirmasi", "Masih ada proses yang berjalan. Tutup aplikasi?"):
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Fungsi utama"""
    try:
        # Cek apakah spleeter terinstall
        try:
            import spleeter
        except ImportError:
            print("Error: Spleeter tidak terinstall!")
            print("Jalankan command berikut untuk install:")
            print("pip install spleeter")
            input("Tekan Enter untuk keluar...")
            return
        
        # Jalankan aplikasi
        app = VocakApps()
        app.run()
        
    except KeyboardInterrupt:
        print("\nAplikasi dihentikan oleh user")
    except Exception as e:
        print(f"Error: {e}")
        input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main()