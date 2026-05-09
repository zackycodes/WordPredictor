# 📝 Python Word Predictor

A lightweight, local word prediction engine built with Python. This tool uses a Markov Chain model to learn your typing patterns (or learn from classic literature) and suggest the next likely word in real-time.

## 🚀 Features
* __Local Training__: Feed the model .txt files (like novels or chat logs) to build a custom vocabulary.
* __Real-time Learning__: The script learns from your active typing while the program is running.
* __Persistent Memory__: Saves its "knowledge" to a .pkl file so it gets smarter every time you use it.
* __Global Hook__: Works in the background while you type in other applications.
* __Auto/Manual Modes__: Toggle between active prediction and quiet learning.

## 🎮 Controls
Key Action
* Space -> Completes a word and triggers a prediction for the next one.
* Tab -> Toggles between Auto (always predicting) and Manual mode.
* ` (Backtick) -> Safely saves your data and exits the program.
* Backspace ->Corrects the current word buffer.

## 🧠 How it Works
The engine uses a Bigram Model. It maps every word it sees to a Counter object containing all the words that have followed it in the past.
When you type a word, the script looks up that word in its dictionary and suggests the one with the highest frequency.

⚠️ Requirements
* __Python__: v3.6+
* __OS__: Windows or macOS (Linux requires root for keyboard library hooks).
* __Permissions__: Since this script listens to global keystrokes, some Antivirus software may flag it. It is recommended to run it in a controlled environment.
