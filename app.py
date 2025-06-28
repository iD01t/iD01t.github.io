#!/usr/bin/env python3
"""
Desktop Assistant - Complete Solution
A full-featured desktop assistant with OpenAI integration, file operations, and export capabilities.
Created for cross-platform deployment and monetization.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import subprocess
import requests
import threading
from datetime import datetime
import webbrowser

# Import optional libraries with error handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI library not installed. GPT features will be disabled.")

try:
    from gtts import gTTS
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Audio libraries not available. Audio features will be disabled.")

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("FPDF library not available. PDF export will be disabled.")

try:
    from PIL import Image, ImageDraw, ImageFont
    IMAGE_AVAILABLE = True
except ImportError:
    IMAGE_AVAILABLE = False
    print("PIL library not available. Image generation will be disabled.")


class DesktopAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Assistant Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Load OpenAI configuration
        self.openai_client = None
        self.load_openai_config()
        
        # Setup GUI
        self.setup_gui()
        
        # Initialize pygame for audio
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.init()
            except:
                pass

    def load_openai_config(self):
        """Load OpenAI API key from configuration file."""
        try:
            if os.path.exists('openai_config.json'):
                with open('openai_config.json', 'r') as f:
                    config = json.load(f)
                    api_key = config.get('openai_api_key')
                    if api_key and OPENAI_AVAILABLE:
                        self.openai_client = openai.OpenAI(api_key=api_key)
                        print("OpenAI client initialized successfully")
            else:
                print("OpenAI config file not found. Create openai_config.json with your API key.")
        except Exception as e:
            print(f"Error loading OpenAI config: {e}")

    def setup_gui(self):
        """Create the main GUI interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Desktop Assistant Pro", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create buttons in rows
        self.create_buttons(button_frame)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Input:").pack(anchor=tk.W)
        self.input_text = tk.Text(input_frame, height=4, wrap=tk.WORD)
        self.input_text.pack(fill=tk.X, pady=(5, 0))
        
        # Output frame
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(output_frame, text="Output:").pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(output_frame, height=20, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def create_buttons(self, parent):
        """Create all feature buttons in organized rows."""
        buttons = [
            # Row 1: File Operations
            [
                ("Read File", self.read_file),
                ("Save Output", self.save_output),
                ("Execute Command", self.execute_command),
                ("Test API", self.test_api)
            ],
            # Row 2: AI & Processing
            [
                ("GPT Chat", self.gpt_chat),
                ("Auto eBook", self.auto_ebook),
                ("Format eBook", self.format_ebook),
                ("Clear Output", self.clear_output)
            ],
            # Row 3: Export Functions
            [
                ("Export PDF", self.export_pdf),
                ("Export HTML", self.export_html),
                ("Generate Audio", self.generate_audio),
                ("Create Cover", self.create_cover)
            ],
            # Row 4: Power Functions
            [
                ("Export All", self.export_all),
                ("Open Output Folder", self.open_output_folder),
                ("Show Help", self.show_help),
                ("Exit", self.root.quit)
            ]
        ]
        
        for row_buttons in buttons:
            row_frame = ttk.Frame(parent)
            row_frame.pack(fill=tk.X, pady=2)
            
            for text, command in row_buttons:
                btn = ttk.Button(row_frame, text=text, command=command, width=15)
                btn.pack(side=tk.LEFT, padx=2)

    def append_output(self, text):
        """Append text to output area."""
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.see(tk.END)
        self.root.update()

    def get_input(self):
        """Get text from input area."""
        return self.input_text.get("1.0", tk.END).strip()

    def get_output(self):
        """Get text from output area."""
        return self.output_text.get("1.0", tk.END).strip()

    def read_file(self):
        """Read and display file contents."""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.append_output(f"**File: {os.path.basename(file_path)}**")
                self.append_output("-" * 50)
                self.append_output(content)
                self.append_output("-" * 50)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def save_output(self):
        """Save output content to text file."""
        content = self.get_output()
        if not content:
            messagebox.showwarning("Warning", "No content to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.append_output(f"**Saved to: {file_path}**")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def execute_command(self):
        """Execute shell command and display results."""
        command = self.get_input()
        if not command:
            messagebox.showwarning("Warning", "Please enter a command.")
            return
        
        self.append_output(f"**Executing: {command}**")
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, 
                                  text=True, timeout=30)
            
            if result.stdout:
                self.append_output("STDOUT:")
                self.append_output(result.stdout)
            
            if result.stderr:
                self.append_output("STDERR:")
                self.append_output(result.stderr)
            
            self.append_output(f"**Return code: {result.returncode}**")
            
        except subprocess.TimeoutExpired:
            self.append_output("**Command timed out (30s limit)**")
        except Exception as e:
            self.append_output(f"**Error: {e}**")

    def test_api(self):
        """Test API endpoint with GET request."""
        url = self.get_input()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL.")
            return
        
        self.append_output(f"**Testing API: {url}**")
        
        try:
            response = requests.get(url, timeout=10)
            self.append_output(f"Status Code: {response.status_code}")
            self.append_output(f"Headers: {dict(response.headers)}")
            self.append_output("Response:")
            self.append_output(response.text[:1000])  # Limit output
            
        except Exception as e:
            self.append_output(f"**Error: {e}**")

    def gpt_chat(self):
        """Send message to GPT-4 and display response."""
        if not self.openai_client:
            messagebox.showerror("Error", "OpenAI client not available. Check your configuration.")
            return
        
        prompt = self.get_input()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt.")
            return
        
        self.append_output(f"**User:** {prompt}")
        self.append_output("**GPT-4:** Thinking...")
        
        def gpt_thread():
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500
                )
                
                # Clear the "Thinking..." message
                current_text = self.output_text.get("1.0", tk.END)
                lines = current_text.split('\n')
                if lines and "Thinking..." in lines[-2]:
                    # Remove the thinking line
                    self.output_text.delete("end-2l", "end-1l")
                
                # Add the actual response
                gpt_response = response.choices[0].message.content
                self.append_output(gpt_response)
                
            except Exception as e:
                self.append_output(f"**Error: {e}**")
        
        threading.Thread(target=gpt_thread, daemon=True).start()

    def auto_ebook(self):
        """Generate a complete eBook using GPT-4."""
        if not self.openai_client:
            messagebox.showerror("Error", "OpenAI client not available.")
            return
        
        topic = self.get_input()
        if not topic:
            messagebox.showwarning("Warning", "Please enter an eBook topic.")
            return
        
        self.append_output(f"**Generating eBook: {topic}**")
        self.append_output("This may take a moment...")
        
        def ebook_thread():
            try:
                prompt = f"""Create a comprehensive eBook about "{topic}". 
                
Structure it with:
1. Title page
2. Table of contents
3. Introduction
4. 5-7 main chapters with detailed content
5. Conclusion
6. About the author section

Make it professional, informative, and ready for publication. 
Target length: 10,000+ words.
Format with clear headings and sections."""

                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000
                )
                
                ebook_content = response.choices[0].message.content
                
                # Clear previous content and add the eBook
                self.output_text.delete("1.0", tk.END)
                self.append_output("**AUTO-GENERATED EBOOK**")
                self.append_output("=" * 50)
                self.append_output(ebook_content)
                
            except Exception as e:
                self.append_output(f"**Error generating eBook: {e}**")
        
        threading.Thread(target=ebook_thread, daemon=True).start()

    def format_ebook(self):
        """Format current output as an eBook structure."""
        content = self.get_output()
        if not content:
            messagebox.showwarning("Warning", "No content to format.")
            return
        
        # Create eBook structure
        formatted = f"""
# EBOOK FORMATTED OUTPUT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## TABLE OF CONTENTS
1. Introduction
2. Main Content
3. Conclusion

---

## INTRODUCTION

This document contains formatted content ready for eBook publication.

---

## MAIN CONTENT

{content}

---

## CONCLUSION

Thank you for reading this content. For more information, visit our website.

---

## ABOUT THE AUTHOR

This content was generated using Desktop Assistant Pro, a comprehensive automation tool for content creators and developers.

---

*End of eBook*
"""
        
        self.output_text.delete("1.0", tk.END)
        self.append_output(formatted)

    def export_pdf(self):
        """Export content to PDF file."""
        if not PDF_AVAILABLE:
            messagebox.showerror("Error", "PDF export not available. Install fpdf2: pip install fpdf2")
            return
        
        content = self.get_output()
        if not content:
            messagebox.showwarning("Warning", "No content to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                
                # Split content into lines and add to PDF
                lines = content.split('\n')
                for line in lines:
                    if len(line) > 80:
                        # Wrap long lines
                        words = line.split(' ')
                        current_line = ""
                        for word in words:
                            if len(current_line + word) < 80:
                                current_line += word + " "
                            else:
                                pdf.cell(0, 10, txt=current_line.strip(), ln=True)
                                current_line = word + " "
                        if current_line:
                            pdf.cell(0, 10, txt=current_line.strip(), ln=True)
                    else:
                        pdf.cell(0, 10, txt=line, ln=True)
                
                pdf.output(file_path)
                self.append_output(f"**PDF exported: {file_path}**")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export PDF: {e}")

    def export_html(self):
        """Export content to HTML file."""
        content = self.get_output()
        if not content:
            messagebox.showwarning("Warning", "No content to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html")]
        )
        
        if file_path:
            try:
                # Convert content to HTML
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Desktop Assistant Export</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Desktop Assistant Pro Export</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    <div class="content">
        <pre>{content}</pre>
    </div>
</body>
</html>"""
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                self.append_output(f"**HTML exported: {file_path}**")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export HTML: {e}")

    def generate_audio(self):
        """Convert output to speech MP3 file."""
        if not AUDIO_AVAILABLE:
            messagebox.showerror("Error", "Audio not available. Install: pip install gtts pygame")
            return
        
        content = self.get_output()
        if not content:
            messagebox.showwarning("Warning", "No content to convert.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")]
        )
        
        if file_path:
            try:
                # Limit content length for TTS
                if len(content) > 5000:
                    content = content[:5000] + "... Content truncated for audio generation."
                
                self.append_output("**Generating audio...**")
                
                tts = gTTS(text=content, lang='en')
                tts.save(file_path)
                
                self.append_output(f"**Audio generated: {file_path}**")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate audio: {e}")

    def create_cover(self):
        """Create a cover image for eBook."""
        if not IMAGE_AVAILABLE:
            messagebox.showerror("Error", "Image generation not available. Install: pip install Pillow")
            return
        
        title = self.get_input()
        if not title:
            title = "Desktop Assistant Pro Export"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        
        if file_path:
            try:
                # Create a simple cover image
                width, height = 800, 1200
                img = Image.new('RGB', (width, height), color='#2c3e50')
                draw = ImageDraw.Draw(img)
                
                # Try to use a better font, fall back to default
                try:
                    title_font = ImageFont.truetype("arial.ttf", 60)
                    subtitle_font = ImageFont.truetype("arial.ttf", 30)
                except:
                    title_font = ImageFont.load_default()
                    subtitle_font = ImageFont.load_default()
                
                # Add title
                bbox = draw.textbbox((0, 0), title, font=title_font)
                title_width = bbox[2] - bbox[0]
                title_x = (width - title_width) // 2
                draw.text((title_x, 300), title, fill='white', font=title_font)
                
                # Add subtitle
                subtitle = "Generated by Desktop Assistant Pro"
                bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
                subtitle_width = bbox[2] - bbox[0]
                subtitle_x = (width - subtitle_width) // 2
                draw.text((subtitle_x, 800), subtitle, fill='#ecf0f1', font=subtitle_font)
                
                # Add border
                draw.rectangle([50, 50, width-50, height-50], outline='#3498db', width=5)
                
                img.save(file_path)
                self.append_output(f"**Cover image created: {file_path}**")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create cover: {e}
