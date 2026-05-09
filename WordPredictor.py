import keyboard
import pickle
import time
import string
from pathlib import Path
from collections import defaultdict, Counter

class WordPredictor:
    def __init__(self, data_file="word_data.pkl", novel_file="novel.txt"):
        self.data_file = Path(data_file)
        self.novel_file = Path(novel_file)
        
        # Structure: { "word": Counter({"next_word": count}) }
        self.model = self._load_data()
        
        # State management
        self.running = True
        self.current_buffer = ""
        self.last_word = None
        self.auto_mode = False

    def _load_data(self):
        """Loads the prediction model from a pickle file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, "rb") as f:
                    return pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                pass
        return defaultdict(Counter)

    def save_data(self):
        """Saves the current model to disk."""
        with open(self.data_file, "wb") as f:
            pickle.dump(self.model, f)
        print(f"\n[System] Progress saved to {self.data_file}")

    def clean_word(self, word):
        """Lowercases and removes punctuation for better matching."""
        return word.lower().strip(string.punctuation)

    def train_from_file(self):
        """Pre-trains the model using a text file."""
        if not self.novel_file.exists():
            print(f"[Notice] {self.novel_file} not found. Starting fresh.")
            return

        print(f"[Training] Reading {self.novel_file}...")
        with open(self.novel_file, "r", encoding="utf-8") as f:
            for line in f:
                words = [self.clean_word(w) for w in line.split() if w]
                for i in range(len(words) - 1):
                    self.model[words[i]][words[i+1]] += 1
        print("[Training] Complete!")

    def predict_next(self, word):
        """Prints the most likely next word based on input."""
        word = self.clean_word(word)
        if word in self.model:
            prediction = self.model[word].most_common(1)[0][0]
            # \r clears the current line in some terminals for a cleaner look
            print(f"\n[Prediction: {prediction}]", end="\n> ", flush=True)

    def handle_keypress(self, event):
        """Processes keyboard events."""
        if event.event_type != 'down':
            return

        key = event.name

        # Exit command: `
        if key == '`':
            self.running = False
            return

        # Toggle Auto-mode: Tab
        if key == 'tab':
            self.auto_mode = not self.auto_mode
            print(f"\n[Mode] {'AUTO' if self.auto_mode else 'MANUAL'}")
            return

        if not self.auto_mode:
            if key == 'space':
                if self.current_buffer:
                    cleaned = self.clean_word(self.current_buffer)
                    
                    # Update model if we have a sequence
                    if self.last_word:
                        self.model[self.last_word][cleaned] += 1
                    
                    self.predict_next(cleaned)
                    self.last_word = cleaned
                    self.current_buffer = ""
            
            elif key == 'backspace':
                self.current_buffer = self.current_buffer[:-1]
            
            elif len(key) == 1:  # Capture standard characters
                self.current_buffer += key

    def start(self):
        """Main loop."""
        self.train_from_file()
        keyboard.on_press(self.handle_keypress)
        
        print("\n--- Predictor Active ---")
        print("Instructions:")
        print(" - Type normally in any window.")
        print(" - Press 'Tab' to toggle modes.")
        print(" - Press '`' (backtick) to Save and Exit.")
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.save_data()

if __name__ == "__main__":
    predictor = WordPredictor()
    predictor.start()
