from transformers import TFAutoModelForCausalLM, AutoTokenizer
import json
import os
from textblob import TextBlob
import re
import logging

class AIModel:
    def __init__(self, model_name='gpt-4', user_profiles_path='user_profiles.json'):
        self.initialize_model(model_name)
        self.user_profiles_path = user_profiles_path
        self.user_profiles = self.load_user_profiles()
        self.setup_logging()

    def initialize_model(self, model_name):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = TFAutoModelForCausalLM.from_pretrained(model_name, pad_token_id=self.tokenizer.eos_token_id)
        except Exception as e:
            logging.error(f"Failed to load model {model_name}: {e}")
            raise

    def load_user_profiles(self):
        if os.path.exists(self.user_profiles_path):
            try:
                with open(self.user_profiles_path, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logging.error(f"Failed to load user profiles: {e}")
                return {}
        return {}

    def save_user_profiles(self):
        try:
            with open(self.user_profiles_path, 'w') as file:
                json.dump(self.user_profiles, file, indent=4)
        except Exception as e:
            logging.error(f"Failed to save user profiles: {e}")

    def setup_logging(self):
        logging.basicConfig(filename='ai_interactions.log', level=logging.INFO, format='%(asctime)s: %(message)s')

    def log_interaction(self, user_id, input_text, response):
        logging.info(f"User: {user_id}, Input: {input_text}, Response: {response}")
        self.update_interaction_history(user_id, input_text, response)

    def generate_text(self, prompt, user_id=None, max_length=50, **generation_params):
        context = self.get_user_context(user_id) if user_id else ""
        input_ids = self.tokenizer.encode(context + prompt, return_tensors='tf')
        try:
            output = self.model.generate(input_ids, max_length=max_length, **generation_params)
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            self.log_interaction(user_id, prompt, response)
            return response
        except Exception as e:
            logging.error(f"Text generation failed: {e}")
            return "I'm sorry, I couldn't process your request."

    def get_user_context(self, user_id):
        user_profile = self.user_profiles.get(user_id, {})
        return user_profile.get("last_interaction", "")

    def update_user_profile(self, user_id, data):
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        for key, value in data.items():
            self.user_profiles[user_id].setdefault(key, []).append(value)
        self.save_user_profiles()

    def update_interaction_history(self, user_id, input_text, response):
        if user_id in self.user_profiles:
            self.user_profiles[user_id].setdefault("interaction_history", []).append({"input": input_text, "response": response})
            self.save_user_profiles()

# Example usage
# ai_model = AIModel(user_profiles_path='path_to_user_profiles.json')
# response = ai_model.generate_text("Hello, how can I assist you today?", user_id='user123')
