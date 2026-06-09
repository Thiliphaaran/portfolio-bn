import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def load_resume_data(filepath):
    """Loads JSON data from the specified filepath."""
    if not os.path.exists(filepath):
        print(f"Error: The file '{filepath}' was not found.")
        return None
        
    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON format.")
            return None

def display_resume_highlights(data):
    """Prints out key highlights from the resume data."""
    if not data:
        return

    # Accessing basic personal info
    name = data.get("personal_information", {}).get("name", "Unknown")
    email = data.get("personal_information", {}).get("email", "Unknown")
    
    print("=" * 40)
    print(f" RESUME DATA LOADED: {name}")
    print(f" Contact: {email}")
    print("=" * 40)
    
    # Accessing lists (Technical Skills)
    print("\n--- Top Technical Skills ---")
    skills = data.get("technical_skills", [])
    for skill in skills[:5]: # Printing just the first 5 for demonstration
        print(f"- {skill}")

    # Accessing nested dictionaries (Experience)
    print("\n--- Recent Experience ---")
    experience = data.get("experience", [])
    if experience:
        latest_job = experience[0]
        print(f"Role: {latest_job['role']} at {latest_job['company']}")
        print(f"Key Task: {latest_job['responsibilities'][0]}")

def initialize_gemini():
    """Initialize Gemini API with the API key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        return False
    
    genai.configure(api_key=api_key)
    print("✓ Gemini API initialized successfully")
    return True

if __name__ == "__main__":
    # Define the path to your JSON file
    json_filepath = "resume.json"
    
    # Initialize Gemini API
    if initialize_gemini():
        # Load and process the data
        resume_data = load_resume_data(json_filepath)
        display_resume_highlights(resume_data)
