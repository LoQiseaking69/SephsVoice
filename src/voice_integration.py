import speech_recognition as sr
import pyttsx3
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
from textblob import TextBlob

class VoiceIntegration:
    def __init__(self, ai_model, voice_id=None, default_rate=125, default_pitch=100):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voice_id if voice_id else self.voices[0].id)
        self.engine.setProperty('rate', default_rate)
        self.engine.setProperty('pitch', default_pitch)
        self.ai_model = ai_model
        self.default_rate = default_rate
        self.executor = ThreadPoolExecutor(max_workers=1)

    def text_to_speech(self, text):
        rate, pitch = self.determine_speech_properties(text)
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('pitch', pitch)
        self.engine.say(text)
        self.engine.runAndWait()

    def determine_speech_properties(self, text):
        analysis = TextBlob(text)
        sentiment = analysis.sentiment.polarity
        rate = 150 if sentiment > 0 else self.default_rate
        pitch = 120 if sentiment > 0 else 100
        return rate, pitch

    def speech_to_text(self, audio_file_path=None):
        try:
            with (sr.AudioFile(audio_file_path) if audio_file_path else sr.Microphone()) as source:
                logging.info("Listening...")
                audio_data = self.recognizer.listen(source)
            return self.recognizer.recognize_google(audio_data)
        except (sr.UnknownValueError, sr.RequestError) as e:
            logging.error(f"Speech recognition error: {e}")
            raise

    def start_listening(self):
        if not self.executor.running():
            self.executor.submit(self.listen_and_respond)

    def listen_and_respond(self):
        while True:
            try:
                text = self.speech_to_text()
                response = self.ai_model.generate_text(text)
                self.text_to_speech(response)
            except Exception as e:
                logging.error(f"Error during listen and respond: {e}")
                self.text_to_speech("I'm sorry, I didn't catch that.")

    def stop_listening(self):
        self.executor.shutdown(wait=True)
        self.engine.stop()

# Example usage
# ai_model = AIModel(...)  # Assuming AIModel is defined elsewhere
# voice_integration = VoiceIntegration(ai_model)
# voice_integration.start_listening()
