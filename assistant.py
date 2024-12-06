from gtts import gTTS
from playsound import playsound
import subprocess
import speech_recognition as sr
import os
import sys
import os

os.environ["PYTHONIOENCODING"] = "utf-8"

sys.stdout.reconfigure(encoding='utf-8')

def query_ollama(model_name, prompt):
    
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8'  
        )
        if result.returncode == 0:
            response = result.stdout.strip()
            print(f"Raw response from LLM: {response}")  
            return response
        else:
            print(f"Error: {result.stderr}")
            return "Jag har problem att förstå det."
    except FileNotFoundError:
        return "Ollama är inte installerat eller inte i PATH."


def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Lyssnar...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="sv-SE")  
            print(f"Du sa: {text}")
            return text
        except sr.UnknownValueError:
            return "Jag kunde inte förstå det. Kan du upprepa?"
        except sr.RequestError as e:
            return f"Fel vid taligenkänning: {e}"
        except sr.WaitTimeoutError:
            return "Jag hörde ingenting."

def speak_output(text):
    
    try:
        text = text.encode('utf-8').decode('utf-8')
        
        print(f"Speaking: {text}")

        tts = gTTS(text=text, lang="sv")
        file_path = "response.mp3"
        tts.save(file_path)
        
        playsound(file_path)
        
        os.remove(file_path)
        
    except Exception as e:
        print(f"Error with gTTS: {e}")
5

def main():
    
    model_name = "mistral"  #<--------skriv modell namnet på ollama modellen som du har laddat ner här.
    print("AI-assistent är redo. Säg 'avsluta' för att avsluta.")

    while True:
        user_input = listen_to_user()
        if user_input.lower() in ["avsluta", "sluta", "stäng av"]:
            print("Hejdå!")
            speak_output("Hejdå!")
            break

        response = query_ollama(model_name, user_input)

        print(f"AI: {response}")
        speak_output(response)

if __name__ == "__main__":
    main()
