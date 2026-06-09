import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
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
    github = data.get("personal_information", {}).get("github", "")
    
    print("=" * 50)
    print(f" RESUME DATA LOADED: {name}")
    print(f" Contact: {email}")
    if github:
        print(f" GitHub: {github}")
    print("=" * 50)
    
    # Accessing lists (Technical Skills)
    print("\n--- Top Technical Skills ---")
    skills = data.get("technical_skills", [])
    for skill in skills[:5]:
        print(f"  • {skill}")
    
    if len(skills) > 5:
        print(f"  ... and {len(skills) - 5} more skills")

    # Accessing nested dictionaries (Experience)
    print("\n--- Professional Experience ---")
    experience = data.get("experience", [])
    if experience:
        for idx, job in enumerate(experience, 1):
            print(f"\n  {idx}. {job.get('role', 'N/A')} at {job.get('company', 'N/A')}")
            print(f"     Duration: {job.get('duration', 'N/A')}")
            print(f"     Description: {job.get('description', 'N/A')}")
            responsibilities = job.get('responsibilities', [])
            if responsibilities:
                print(f"     Key Responsibilities:")
                for resp in responsibilities[:2]:
                    print(f"       - {resp}")

    # Education
    print("\n--- Education ---")
    education = data.get("education", [])
    if education:
        for edu in education:
            print(f"  • {edu.get('degree', 'N/A')} in {edu.get('field', 'N/A')}")
            print(f"    {edu.get('university', 'N/A')} ({edu.get('year', 'N/A')})")

def initialize_gemini():
    """Initialize Gemini API with the API key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  Warning: GEMINI_API_KEY not found in .env file")
        return False
    
    try:
        genai.configure(api_key=api_key)
        print("✓ Gemini API initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Error initializing Gemini API: {e}")
        return False

def main():
    """Main function to run the portfolio application."""
    print("\n" + "=" * 50)
    print("  PORTFOLIO BACKEND - RESUME DISPLAY")
    print("=" * 50 + "\n")
    
    # Define the path to your JSON file
    json_filepath = os.getenv("RESUME_FILE_PATH", "resume.json")
    
    # Initialize Gemini API
    if initialize_gemini():
        print("✓ API Configuration: Complete\n")
    
    # Load and process the data
    resume_data = load_resume_data(json_filepath)
    if resume_data:
        display_resume_highlights(resume_data)
        print("\n✓ Resume data processed successfully!")
    else:
        print("\n✗ Failed to load resume data.")
    
    print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
