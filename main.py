import tkinter as tk
from tkinter import ttk
from translate import Translator
from langdetect import detect
from gtts import gTTS
import os
from playsound import playsound

def on_click(event, text_widget, default_text):
    if text_widget.get("1.0", tk.END).strip() == default_text:
        text_widget.delete("1.0", tk.END)
        text_widget.config(fg="black")

def on_focus_out(event, text_widget, default_text):
    if not text_widget.get("1.0", tk.END).strip():
        text_widget.insert(tk.END, default_text)
        text_widget.config(fg="gray")

def translate_text():
    source_text = text_box_source.get("1.0", tk.END).strip()
    if not source_text:
        return

    source_language = detect(source_text)
    target_language = language_combobox.get()

    translator = Translator(from_lang=source_language, to_lang=target_language)
    translation = translator.translate(source_text)

    text_box_target.delete("1.0", tk.END)
    text_box_target.insert(tk.END, translation)

def voice_text():
    text = text_box_target.get("1.0", tk.END).strip()
    if not text:
        return

    target_language = language_combobox.get()

    # Generate the speech
    tts = gTTS(text=text, lang=target_language)
    tts.save("temp_audio.mp3")

    # Play the speech
    playsound("temp_audio.mp3")

    # Optionally, remove the temporary file
    os.remove("temp_audio.mp3")

root = tk.Tk()
root.title("Simple Translator")
root.geometry("900x600")
root.resizable(False, False)

# Main Frame
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Title Label
title_label = tk.Label(main_frame, text="Text Translator", font=("Arial", 18, "bold"), bg="#f0f0f0")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Source Text Box
text_box_source = tk.Text(main_frame, height=15, width=35, font=("Arial", 14), fg="gray", bg="#ffffff", bd=2, relief=tk.SUNKEN)
text_box_source.grid(row=1, column=0, padx=10, pady=10)
default_text_source = "Enter text here..."
text_box_source.insert(tk.END, default_text_source)
text_box_source.bind("<FocusIn>", lambda event: on_click(event, text_box_source, default_text_source))
text_box_source.bind("<FocusOut>", lambda event: on_focus_out(event, text_box_source, default_text_source))

# Target Text Box
text_box_target = tk.Text(main_frame, height=15, width=35, font=("Arial", 14), fg="gray", bg="#ffffff", bd=2, relief=tk.SUNKEN)
text_box_target.grid(row=1, column=2, padx=10, pady=10)
default_text_target = "Translated text will appear here..."
text_box_target.insert(tk.END, default_text_target)
text_box_target.bind("<FocusIn>", lambda event: on_click(event, text_box_target, default_text_target))
text_box_target.bind("<FocusOut>", lambda event: on_focus_out(event, text_box_target, default_text_target))

# Language Selection Combobox
languages = ["af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "fi", "fr", "gu", "he",
"hi", "hr", "hu", "id", "it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl",
"pt", "ro", "ru", "sk", "sl", "so", "sq", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi", "zh-cn", "zh-tw"]
language_combobox = ttk.Combobox(main_frame, values=languages, font=("Arial", 14))
language_combobox.grid(row=2, column=0, padx=10, pady=10)
language_combobox.set("en")

# Translate Button
translate_button = tk.Button(main_frame, text="Translate", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", relief=tk.RAISED, command=translate_text)
translate_button.grid(row=2, column=2, padx=10, pady=20)

# Listen Button
voice_button = tk.Button(main_frame, text="Listen", font=("Arial", 14, "bold"), bg="#2196F3", fg="white", relief=tk.RAISED, command=voice_text)
voice_button.grid(row=3, column=2, padx=10, pady=10)

# Run the application
root.mainloop()
