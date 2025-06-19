# 🤖 Eva – Voice-Activated AI File Assistant

**Eva** is a smart voice assistant that activates when the person "Fayaz" is detected and responds to spoken commands to control files, folders, and system actions (like shutdown/restart). It combines **speech recognition**, **text-to-speech**, **file navigation**, and **sound feedback** into a powerful local assistant.

---

## 🎯 Features

- 🗣️ Voice-activated assistant
- 📂 Open files/folders by command (e.g., "open D directory", "open resume.pdf")
- 🔄 Go back in folder history
- ❌ Close currently opened files or folders
- 📴 Voice-confirmed shutdown and restart
- 🔉 Sound effects using `pygame`
- 🧠 Custom trigger word: `"eva"` (also supports misheard variants like "shiva", "fever")

---

## 🛠️ Technologies Used

- [`pyttsx3`](https://pypi.org/project/pyttsx3/) – Offline text-to-speech engine
- [`SpeechRecognition`](https://pypi.org/project/SpeechRecognition/) – For converting spoken language to text
- [`pygame`](https://pypi.org/project/pygame/) – For playing sound effects
- `pyautogui`, `os`, `subprocess`, `re` – File and system control
- Trigger logic based on detected user (i.e., `"fayaz"`)

---

## 🚀 How It Works

1. When **"fayaz"** is detected by facial recognition (or other means), Eva activates.
2. Plays a welcome sound and begins listening.
3. Responds to voice commands like:
   - `"open D directory"`
   - `"open resume.pdf"`
   - `"back"`
   - `"close"`
   - `"shutdown the system"` or `"restart the system"`
4. Offers spoken confirmations and sound feedback for actions.

---

## 📦 Requirements

Install dependencies using pip:

```bash
pip install pyttsx3 pygame SpeechRecognition pyautogui pyaudio
