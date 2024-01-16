import logging
from ai_model import AIModel
from voice_integration import VoiceIntegration
from knowledge_base_manager import KnowledgeBaseManager
from user_profile_manager import UserProfileManager
from ethical_guidelines_manager import EthicalGuidelinesManager

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Initialize Managers
        knowledge_base_manager = KnowledgeBaseManager('path_to_knowledge_base.json')
        user_profile_manager = UserProfileManager('path_to_user_profiles.json')
        ethical_guidelines_manager = EthicalGuidelinesManager('path_to_ethical_guidelines.json')

        # Initialize AI Model with user profiles and knowledge base
        ai_model = AIModel(user_profiles_manager=user_profile_manager, knowledge_base_manager=knowledge_base_manager, ethical_guidelines_manager=ethical_guidelines_manager)

        # Initialize Voice Integration with AI Model
        voice_integration = VoiceIntegration(ai_model)

        # Start voice interaction
        voice_integration.start_listening()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Clean up resources if necessary
        voice_integration.stop_listening()
        logging.info("Application stopped gracefully")

if __name__ == "__main__":
    main()
