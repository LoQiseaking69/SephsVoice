
import speech_recognition as sr
import pyttsx3
import threading

class VoiceIntegration:
    def __init__(self, ai_model):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.ai_model = ai_model

    def text_to_speech(self, text):
        if "excited" in text or "happy" in text:
            rate = 150
        else:
            rate = 125
        self.engine.setProperty('rate', rate)
        self.engine.say(text)
        self.engine.runAndWait()

    def speech_to_text(self, audio_file_path=None):
        if audio_file_path:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)
        else:
            with sr.Microphone() as source:
                audio_data = self.recognizer.listen(source)
        return self.recognizer.recognize_google(audio_data)

    def start_listening(self):
        threading.Thread(target=self.listen_and_respond).start()

    def listen_and_respond(self):
        while True:
            try:
                text = self.speech_to_text()
                response = self.ai_model.generate_text(text)
                self.text_to_speech(response)
            except sr.UnknownValueError:
                self.text_to_speech("Sorry, I did not understand that.")
            except Exception as e:
                self.text_to_speech("An error occurred. Please try again.")

# Example usage
# ai_model = AIModel(user_profiles_path='path_to_user_profiles.json')
# voice_integration = VoiceIntegration(ai_model)
# voice_integration.start_listening()
