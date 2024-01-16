
from transformers import TFAutoModelForCausalLM, AutoTokenizer
import json
from textblob import TextBlob

class AIModel:
    def __init__(self, model_name='gpt-2', user_profiles_path=None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = TFAutoModelForCausalLM.from_pretrained(model_name)
        self.user_profiles = self.load_user_profiles(user_profiles_path)

    def load_user_profiles(self, path):
        if path and os.path.exists(path):
            with open(path, 'r') as file:
                return json.load(file)
        return {}

    def save_user_profiles(self, path):
        if path:
            with open(path, 'w') as file:
                json.dump(self.user_profiles, file)

    def generate_text(self, prompt, user_id=None, max_length=50):
        context = self.get_user_context(user_id) if user_id else ""
        input_ids = self.tokenizer.encode(context + prompt, return_tensors='tf')
        output = self.model.generate(input_ids, max_length=max_length)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def get_user_context(self, user_id):
        return self.user_profiles.get(user_id, {}).get("context", "")

    def update_user_profile(self, user_id, data):
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        self.user_profiles[user_id].update(data)
        self.save_user_profiles(user_profiles_path)

    def analyze_interaction(self, interaction):
        analysis = TextBlob(interaction)
        sentiment = analysis.sentiment.polarity
        sarcasm_detected = self.detect_sarcasm(interaction)
        return {
            "sentiment": "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral",
            "sarcasm": sarcasm_detected
        }

    def detect_sarcasm(self, interaction):
        return "not really" in interaction or "just kidding" in interaction

# Example usage
# ai_model = AIModel(user_profiles_path='path_to_user_profiles.json')
# response = ai_model.generate_text("Hello, how can I assist you today?")
