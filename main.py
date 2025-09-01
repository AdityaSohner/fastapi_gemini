from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import google.generativeai as genai

load_dotenv()

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application with CORS and environment variable loading.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class baseinfo(BaseModel):
    date: str
    gender: str
    place_of_birth: str

def load_prompt():
    with open("prompt_template.txt", "r") as file:
        return file.read()
    

def get_json(response):
    json_obj = {}
    for string in response.split("\\"):
        if ':' in string:
            key, value = string.strip('"').strip('"').split(':', 1)
            key.strip('"').strip('"')
            print(key)
            json_obj[key] = list(map(str,value.split("*")))
    
    return json_obj


@app.get("/")
def read_root():
    return {"message": "Welcome to this simple fastapi application!. Use POST /generate with date, gender and place_of_birth to generate a response."}

@app.post("/generate")
async def generate_response(info: baseinfo):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in environment variables.")
    
    try:
        prompt_template = load_prompt()
        prompt = prompt_template.format(
            dob=info.date,
            gender=info.gender,
            place_of_birth=info.place_of_birth
        )

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = await model.generate_content_async(prompt)
        json_response = get_json(response.text)
        print(json_response)
        return {
            "input_params": {
                "dob": info.date,
                "gender": info.gender,
                "place_of_birth": info.place_of_birth
            },
            "Archetype": json_response["Archetype"][0],
            "personality_description": json_response["personality_description"][0],
            "list_songs": {
                "suggestion_txt": json_response["list_songs"][0],
                "song_1": json_response["list_songs"][1],
                "song_2": json_response["list_songs"][2],
                "song_3": json_response["list_songs"][3],
                "song_4": json_response["list_songs"][4],
                "song_5": json_response["list_songs"][5]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response :{str(e)}")
    

@app.get("/health")
def health_check():
    return {"status": "healthy", "gemini_configured": bool(GEMINI_API_KEY)}
