
from ai_model import AIModel
from voice_integration import VoiceIntegration

def main():
    # Initialize AI Model
    ai_model = AIModel(user_profiles_path='path_to_user_profiles.json')

    # Initialize Voice Integration with AI Model
    voice_integration = VoiceIntegration(ai_model)

    # Start voice interaction
    voice_integration.start_listening()

if __name__ == "__main__":
    main()
