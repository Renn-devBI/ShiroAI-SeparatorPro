<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShiroAI SeparatorPro - AI Audio Separation Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            width: 300px;
            margin-bottom: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
        }
        
        h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #ff6b6b, #ffa86b, #ffda6b);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        h2 {
            font-size: 2rem;
            margin: 30px 0 15px;
            color: #6bcaff;
        }
        
        h3 {
            font-size: 1.5rem;
            margin: 20px 0 10px;
            color: #6bffc8;
        }
        
        p {
            margin-bottom: 15px;
            font-size: 1.1rem;
        }
        
        .badges {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }
        
        .badge {
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .python {
            background: #3776ab;
            color: white;
        }
        
        .pygame {
            background: #2ecc71;
            color: white;
        }
        
        .mutagen {
            background: #e74c3c;
            color: white;
        }
        
        .pillow {
            background: #3498db;
            color: white;
        }
        
        .mit {
            background: #f39c12;
            color: white;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .feature {
            background: rgba(255, 255, 255, 0.08);
            padding: 20px;
            border-radius: 15px;
            transition: transform 0.3s ease;
        }
        
        .feature:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        
        .installation {
            background: rgba(0, 0, 0, 0.2);
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
        }
        
        code {
            display: block;
            background: #1e1e2e;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            overflow-x: auto;
            font-family: 'Fira Code', monospace;
        }
        
        .ai-processing {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .ai-item {
            background: rgba(107, 202, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid #6bcaff;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .github-link {
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: #6e5494;
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: bold;
            transition: background 0.3s ease;
        }
        
        .github-link:hover {
            background: #56457a;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2.2rem;
            }
            
            h2 {
                font-size: 1.8rem;
            }
            
            .features {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <img src="https://top-gray-zo9uqyc2cs.edgeone.app/bg_f8f8f8-flat_750x_075_f-pad_750x1000_f8f8f8-removebg-preview.png" alt="ShiroAI SeparatorPro" class="logo">
            <h1>ShiroAI SeparatorPro</h1>
            <p>AI-Powered Audio Stem Separation Application</p>
            
            <div class="badges">
                <span class="badge python">Python 3.10+</span>
                <span class="badge pygame">PyGame</span>
                <span class="badge mutagen">Mutagen</span>
                <span class="badge pillow">Pillow</span>
                <span class="badge mit">MIT License</span>
            </div>
        </header>
        
        <section>
            <h2>✨ Features</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎶</div>
                    <h3>Multi-format Support</h3>
                    <p>MP3, WAV, FLAC, OGG - all major audio formats supported</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🤖</div>
                    <h3>AI Audio Separation</h3>
                    <p>Isolate vocals, drums, bass, and instruments with AI technology</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎨</div>
                    <h3>Modern GUI</h3>
                    <p>Intuitive and user-friendly interface with dark theme</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📊</div>
                    <h3>Real-time Visualization</h3>
                    <p>Audio waveform and processing metrics displayed in real-time</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🏷️</div>
                    <h3>Metadata Editor</h3>
                    <p>Edit ID3 tags and album art directly in the application</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">💾</div>
                    <h3>Export Options</h3>
                    <p>Save separated tracks in various formats and quality settings</p>
                </div>
            </div>
        </section>
        
        <section class="installation">
            <h2>🚀 Installation & Usage</h2>
            
            <h3>Prerequisites</h3>
            <code>Python 3.10 or newer</code>
            
            <h3>Clone & Setup</h3>
            <code>git clone https://github.com/Renn-devBI/ShiroAI-SeparatorPro.git<br>cd ShiroAI-SeparatorPro</code>
            
            <h3>Create Virtual Environment</h3>
            <code>python -m venv env310<br># On Windows:<br>env310\Scripts\activate<br># On macOS/Linux:<br>source env310/bin/activate</code>
            
            <h3>Install Dependencies</h3>
            <code>pip install pygame mutagen pillow</code>
            
            <h3>Run Application</h3>
            <code>python main.py</code>
        </section>
        
        <section>
            <h2>🎯 AI Processing Capabilities</h2>
            
            <h3>Stem Separation Types:</h3>
            <div class="ai-processing">
                <div class="ai-item">
                    <h4>Vocal Isolation</h4>
                    <p>Extract clean vocal tracks from any song</p>
                </div>
                <div class="ai-item">
                    <h4>Drum Separation</h4>
                    <p>Isolate percussion elements and beats</p>
                </div>
                <div class="ai-item">
                    <h4>Bass Extraction</h4>
                    <p>Separate low-frequency components</p>
                </div>
                <div class="ai-item">
                    <h4>Instrumental Isolation</h4>
                    <p>Remove vocals for karaoke versions</p>
                </div>
                <div class="ai-item">
                    <h4>Full Demixing</h4>
                    <p>Complete separation of all audio elements</p>
                </div>
            </div>
            
            <h3>AI Technologies Used:</h3>
            <ul>
                <li>Deep Neural Networks for audio source separation</li>
                <li>Spectrogram analysis and processing</li>
                <li>Machine learning models trained on thousands of tracks</li>
                <li>Real-time processing optimizations</li>
            </ul>
        </section>
        
        <section>
            <h2>🛠️ Project Structure</h2>
            <code>
ShiroAI-SeparatorPro/<br>
│<br>
├── main.py                 # Main application entry point<br>
├── audio_processor.py      # AI audio processing module<br>
├── gui.py                  # Graphical user interface<br>
├── utils.py                # Utility functions and helpers<br>
├── requirements.txt        # Project dependencies<br>
├── README.md               # Project documentation<br>
└── samples/                # Sample audio files for testing<br>
            </code>
        </section>
        
        <div class="footer">
            <h3>License</h3>
            <p>Distributed under the MIT License. See LICENSE for more information.</p>
            
            <h3>Author</h3>
            <p>Renn-devBI</p>
            
            <a href="https://github.com/Renn-devBI/ShiroAI-SeparatorPro" class="github-link">View on GitHub</a>
        </div>
    </div>
</body>
</html># ShiroAI-SeparatorPro
