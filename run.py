# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# load_dotenv()
# # Configure with your key
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=GEMINI_API_KEY)

# try:
#     # First, let's see what models are available
#     print("Available models:")
#     for model in genai.list_models():
#         if 'generateContent' in model.supported_generation_methods:
#             print(f"- {model.name}")

#     # Try using gemini-2.0-flash model (correct name)
#     model = genai.GenerativeModel('gemini-2.0-flash')
#     response = model.generate_content("Hello, are you working?")
#     print("\nSuccess! Response:", response.text)
    
# except Exception as e:
#     print("Error:", e)

# '''
# Mainstream Indian Hip Hop Song Pool (for generating 'list_songs' - pick 5 relevant to the archetype or generally popular):
# "Bana hi nahi tha jana" by dinojames,
# "Duniya Makkar" by karma, 
# "Kuch Aur" by emiway,
# "Saari Saari Raat" by karma,
# "Pal Pal" by afusic and talwinder,
# "Aina" by afkap,
# "Aksar-unplugged" by emiway and rish,
# "mohabbat" by kaam bhari,
# "snake" by mc stan,
# "I wanna know" by agsy,
# "I'm done" by mc stan,
# "bliss" by gurbax,
# "untitled" by krsna,
# "no cap" by krsna ,
# "woh raat" by krsna and raftaar,
# "rashaah" by raftaar and badshah,
# "nanchaku" by seedhe maut and mc stan,
# "101" by seedhe maut,
# "ek do ek" by tsumyoki and rawal,
# "100 million" by divine and karan aujla,
# "w" by emiway,
# "hisaab" by divine and karan aujla, 
# "4.10" by divine,
# "no mercy" by deep kalsi ,
# "chorni" by divine and sidhu moosewala,
# "softly" by karan aujala,
# '''


import json
import re

def load_prompt():
    with open("prompt_template.txt", "r") as file:
        return file.read()
    
def fix_json_string(json_string):
    """Convert the malformed JSON string to valid JSON"""
    # Remove leading/trailing whitespace and escape sequences
    cleaned = json_string.strip()
    
    # Remove the problematic \n and \" sequences
    cleaned = cleaned.replace('\\n', '').replace('\\"', '"')
    
    # Fix the list_songs array by adding missing commas
    # This is a bit complex, so let's parse and rebuild properly
    try:
        # First, try to parse as-is (might work after basic cleaning)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # If that fails, use a more robust approach
        return manually_fix_json(cleaned)

def manually_fix_json(json_string):
    """Manually reconstruct the JSON"""

    
    # Extract archetype
    archetype_match = re.search(r'"Archetype":\s*"([^"]+)"', json_string)
    archetype = archetype_match.group(1) if archetype_match else ""
    
    # Extract description
    desc_match = re.search(r'"personality_description":\s*"([^"]+)"', json_string)
    description = desc_match.group(1) if desc_match else ""
    
    # Extract songs list
    songs_match = re.search(r'"list_songs":\s*\[([\s\S]*?)\]', json_string)
    if songs_match:
        songs_text = songs_match.group(1)
        # Extract individual song items
        songs = re.findall(r'"([^"]+)"', songs_text)
    else:
        songs = []
    
    # Build proper JSON
    return {
        "Archetype": archetype,
        "personality_description": description,
        "list_songs": songs,
        "message": "As you step into the world of Indian Hip Hop, here are 5 mainstream songs from this archetype, or generally popular ones you might enjoy:"
    }


fixed_json = fix_json_string(load_prompt())

# Convert back to proper JSON string
perfect_json_string = json.dumps(fixed_json, indent=2, ensure_ascii=False)
print(perfect_json_string)