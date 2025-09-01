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


prompt_template = """
You are an Elemental Profiler. Your task is to categorize an individual into one of five core nature-based elements based on their provided birth information. Then, you will generate a clear, easy-to-understand, first-person personality description (addressing the individual directly as "you") for their assigned element. The language should be simple and accessible, avoiding complex jargon.

The five elements and their core associations are:
1.  **Fire (The Energetic Pioneer):** You are passionate, full of energy, confident, and inspiring. You love new beginnings and can be a strong leader, though sometimes a bit impulsive.
2.  **Water (The Caring Empath):** You are deeply emotional, intuitive, and compassionate. You adapt easily and care deeply for others, often feeling things very strongly.
3.  **Earth (The Steady Builder):** You are practical, reliable, and patient. You like stability, are very responsible, and tend to be grounded and resilient, though you can be set in your ways.
4.  **Air (The Bright Thinker):** You are smart, curious, and a great communicator. You love ideas, freedom, and connections, often thinking logically and sometimes appearing a bit detached.
5.  **Spirit/Aether (The Deep Seeker):** You are imaginative, spiritual, and insightful. You often look beyond the ordinary, valuing wisdom and connection to something greater, sometimes feeling out of touch with everyday things.

**Based on the provided details, determine the primary element and any strong secondary influences. Then, craft your response strictly in a dictionary format as below:**

**"Element": [Determined Element Name (and any strong secondary influence)]**

**"personality_description":**
(Start with "You are..." or "Your...")
(Describe the individual's core nature clearly, using simple language. Weave in their DOB ({dob}), Gender ({gender}), and Place of Birth ({place_of_birth}) subtly to add a unique flavor to their elemental description. Focus on explaining how these traits combine to make them who they are.)

---
**Input Details for Analysis:**
-   **Date of Birth:** {dob}
-   **Gender:** {gender}
-   **Place of Birth:** {place_of_birth}
"""

@app.get("/")
def read_root():
    return {"message": "Welcome to this simple fastapi application!. Use POST /generate with date, gender and place_of_birth to generate a response."}

@app.post("/generate")
async def generate_response(info: baseinfo):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in environment variables.")
    
    try:
        prompt = prompt_template.format(
            dob=info.date,
            gender=info.gender,
            place_of_birth=info.place_of_birth
        )

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = await model.generate_content_async(prompt)

        return {
            "input_params": {
                "dob": info.date,
                "gender": info.gender,
                "place_of_birth": info.place_of_birth
            },
            "description": response.text
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response :{str(e)}")
    

@app.get("/health")
def health_check():
    return {"status": "healthy", "gemini_configured": bool(GEMINI_API_KEY)}
