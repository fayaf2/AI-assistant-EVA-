# Check if Fayaz is detected
if name == "fayaz":
    # Speak the message with the name of the detected person
    engine_face.say(f'I see {name}!')
    engine_face.runAndWait()

    # Activate the second code snippet
    print("Fayaz detected. Activating the second code snippet...")
    
    # Constants
    SOUND_FOLDER = "D:\\SJF" # Folder containing sound files
    SOUND_TUTURU = os.path.join(SOUND_FOLDER, "iphone.mp3")
    SOUND_TIMEOUT = os.path.join(SOUND_FOLDER, "timeout_sound.mp3")
    SOUND_SUCCESS = os.path.join(SOUND_FOLDER, "twitter.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Initialize pyttsx3
    engine = pyttsx3.init()

    # Set properties for child female voice with adjusted pitch and speed
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.setProperty('rate', 200)
    engine.setProperty('pitch', 200)

    current_path = None
    opened_file = None

    def recognize_speech(recognizer, audio):
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}. Please try again.")
            return None

    def play_sound(sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def close_file_explorer(file_to_close=None):
        try:
            if file_to_close:
                if os.path.isfile(file_to_close):
                    pyautogui.hotkey('alt', 'f4')
                    print(f"Closed file: {file_to_close}")
                    if os.path.dirname(file_to_close) != current_path:
                        close_file_explorer(file_to_close=os.path.dirname(file_to_close))
                elif os.path.isdir(file_to_close):
                    pyautogui.hotkey('alt', 'f4')
                    print(f"Closed folder: {file_to_close}")
                else:
                    print(f"Unsupported item type: {file_to_close}")
            else:
                print("No file specified to close")
        except Exception as e:
            print(f"Error closing file explorer: {e}")

    def open_drive(drive_letter, file_name=None):
        global current_path, opened_file
        try:
            close_file_explorer(file_to_close=opened_file)

            path = f"{drive_letter.upper()}:\\"
            if file_name:
                path = os.path.join(current_path, file_name)

            if os.path.exists(path):
                os.startfile(path)
                feedback = os.path.basename(path) if os.path.isdir(path) or os.path.isfile(path) else drive_letter.upper()
                print(f"Opened {feedback}")
                engine.say(f"Opened {feedback}")
                engine.runAndWait()

                current_path = path if os.path.isdir(path) else os.path.dirname(path)
                opened_file = path
                return current_path
            else:
                print(f"Path not found: {path}")
                return None
        except Exception as e:
            print(f"Error opening path: {e}")
            return None

    def go_back():
        global current_path, opened_file
        if current_path:
            if os.path.isfile(opened_file):
                close_file_explorer(file_to_close=opened_file)
                current_path = os.path.dirname(opened_file)
                print(f"Updated current path: {current_path}")
                engine.say(f"Back to {os.path.basename(current_path)}")
                engine.runAndWait()
            else:
                close_file_explorer(file_to_close=opened_file)
                parent_directory = os.path.abspath(os.path.join(current_path, os.pardir))
                if parent_directory != current_path:
                    os.startfile(parent_directory)
                    current_path = parent_directory
                    print(f"Going back to: {current_path}")
                    engine.say(f"Back to {os.path.basename(current_path)}")
                    engine.runAndWait()
                else:
                    print("Cannot go back. Already at the root directory.")
        else:
            print("Cannot go back. Current path is not set.")

    def search_and_open_file(starting_word):
        global current_path
        if current_path and os.path.isdir(current_path):
            print("Current path:", current_path)
            exact_match = os.path.join(current_path, starting_word)
            if os.path.exists(exact_match):
                open_drive(current_path[0], starting_word)
                return
            matching_items = [item for item in os.listdir(current_path) if starting_word.lower() in item.lower()]
            if matching_items:
                folders = [folder for folder in matching_items if os.path.isdir(os.path.join(current_path, folder))]
                full_path = os.path.join(current_path, folders[0]) if folders else os.path.join(current_path, matching_items[0])
                print("Checking starting word:", full_path)
                if os.path.exists(full_path):
                    try:
                        os.startfile(full_path)
                        print(f"Opened: {full_path}")
                        if os.path.isdir(full_path):
                            folder_name = os.path.basename(full_path)
                            engine.say(f"Opened folder {folder_name}")
                        elif os.path.isfile(full_path):
                            file_name = os.path.basename(full_path)
                            engine.say(f"Opened file {file_name}")
                        engine.runAndWait()
                        if os.path.isdir(full_path):
                            current_path = full_path
                            print(f"Updated current path: {current_path}")
                    except Exception as e:
                        print(f"Error opening file or folder: {e}")
                else:
                    print(f"Path not found: {full_path}")
            else:
                print(f"No matching directories or files found for '{starting_word}'.")
        else:
            print(f"Current path is not set. Please open a directory first.")

    def extract_drive_letter(command):
        match = re.search(r'\bopen ([a-zA-Z])[- ]?directory\b', command)
        return match.group(1).upper() if match else None

    def extract_file_name(command):
        match = re.search(r'\bopen\s+(.+)\b', command)
        return match.group(1) if match else None

    def main(timeout=35, current_path=None):
        global opened_file
        recognizer = sr.Recognizer()
        play_sound(SOUND_TUTURU)
        with sr.Microphone() as source:
            print("Listening in main...")
            recognizer.adjust_for_ambient_noise(source, duration=0)
            start_time = time.time()
            while True:
                try:
                    audio = recognizer.listen(source, timeout=timeout)
                except sr.WaitTimeoutError:
                    print("Timeout occurred. Continuing to listen...")
                    play_sound(SOUND_TIMEOUT)
                    return current_path
                except Exception as e:
                    print(f"Error in main function: {e}")
                    continue
                command = recognize_speech(recognizer, audio)
                if command is not None:
                    drive_letter = extract_drive_letter(command)
                    file_name = extract_file_name(command)
                    if drive_letter:
                        current_path = open_drive(drive_letter)
                    elif file_name and current_path:
                        search_and_open_file(file_name)
                    elif "eva" in command:
                        current_path = main(current_path=current_path)
                    elif "back" in command.lower():
                        go_back()
                        current_path = os.path.abspath(os.path.join(current_path, os.pardir))
                        print(f"Going back to: {current_path}")
                    elif "close" in command:
                        close_file_explorer(file_to_close=opened_file)
                    elif "shutdown the system" in command.lower():
                        confirmation = get_voice_confirmation("Are you sure you want to shutdown?")
                        if confirmation == 'yes':
                            print("Shutting down...")
                            subprocess.run(['shutdown', '/s', '/t', '1'])
                        else:
                            print("Shutdown canceled.")
                    elif "restart the system" in command.lower():
                        confirmation = get_voice_confirmation("Are you sure you want to shutdown?")
                        if confirmation == 'yes':
                            print("Restarting...")
                            subprocess.run(['shutdown', '/r', '/t', '1'])
                        else:
                            print("Restart canceled.")
                else:
                    continue
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    print("Timeout reached. Exiting main...")
                    play_sound(SOUND_SUCCESS)
                    return current_path

    def get_voice_confirmation(message):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0)
            audio = recognizer.listen(source, timeout=None)
        confirmation = recognize_speech(recognizer, audio)
        print("Your response:", confirmation)
        return confirmation.lower()

    def handle_command(command, current_path):
        if any(word in command.lower() for word in ["eva", "shiva", "fever", "vivah"]):
            return main(current_path=current_path)
        else:
            print("Eva not detected in the command.")
            return current_path

    def listen_eva(current_path=None):
        recognizer = sr.Recognizer()
        try:
            while True:
                with sr.Microphone() as source:
                    print("Listening for 'eva'...")
                    recognizer.adjust_for_ambient_noise(source, duration=0)
                    audio = recognizer.listen(source, timeout=None)
                command = recognize_speech(recognizer, audio)
                if command is not None:
                    current_path = handle_command(command, current_path)
        except KeyboardInterrupt:
            print("\nUser interrupted. Exiting...")
            pygame.mixer.music.stop()
            sys.exit(0)

    if __name__ == "__main__":
        current_path = None
        try:
            while True:
                current_path = listen_eva(current_path=current_path)
        except Exception as e:
            print(f"An error occurred: {e}")
