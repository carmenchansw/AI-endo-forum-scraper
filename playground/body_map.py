import os
from dotenv import load_dotenv
import tomllib
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

if "GEMINI_API_KEY" not in os.environ:
    try:
        # Step back to the root directory to find the .streamlit folder
        secrets_path = os.path.join(os.path.dirname(__file__), "../.streamlit/secrets.toml")
        with open(secrets_path, "rb") as f:
            secrets = tomllib.load(f)
            os.environ["GEMINI_API_KEY"] = secrets.get("GEMINI_API_KEY", "")
    except FileNotFoundError:
        pass

# Initialise client
client = genai.Client()

# Define the BodyMAP model (Schema)
class PainLog(BaseModel):
    zone_id : Literal[ #Set to variable type annotation
        "uterus",
        "pelvis",
        "abdomen",
        "lower_back"
    ] = Field(description="The matching anatomical zone ID for the body map.")

    severity : Optional[int] = Field( #Set to variable type annotation
        default = None,
        ge = 1,
        le = 10,
        description="The severity of the pain in the specified zone, on a scale from 1 to 10."
    )

    # classify how the pain feels
    pain_type : Optional[Literal['sharp','dull','throbbing', #Set to variable type annotation
                                 'burning','stabbing']
                                 ] = Field(
                                 default = None,
                                 description="The type of pain experienced in the specified zone."        
                                 )
    
class PainExtractionResponse(BaseModel):
    user_message: str = Field(description="The comforting, conversational response back to the user.")
    pain_logs: List[PainLog] = Field(description="List of all extracted physical pain incidents.")

SYSTEM_PROMPT = """
You are a health data extraction engine and caring chatbot for an endometriosis symptom tracking app. 

Your job is twofold:
1. Generate a warm, concise, conversational message back to the user acknowledging their pain. Keep it under 2 sentences.
2. Extract the physical pain parameters (locations, severity, and types) and organize them into the schema.

Rules for Implicit Location Mapping:
- If user mentions "hip pain," map it to "pelvis".
- If user mentions "stomach pain" or "abdominal pain", map it to "abdomen".
- If user mentions "lower stomach pain", map it to "uterus".
- If user mentions "lower back pain" or "back pain", map it to "lower_back".

Severity Inference Guide:
- Mild/Dull/Manageable/Can move around = 1-3
- Hurting/Distracting/Cramping = 4-6
- Severe/Unbearable/Crying/Can't move/Stay in bed = 7-10
"""

# This is a mock user input
test_user_input = (
    "My lower back is absolutely killing me, like a sharp 8 out of 10. "
    "I can also feel a dull, heavy throbbing starting on my left side."
)

print("Parsing pain log with AI...")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=test_user_input,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        # Enforce the structured JSON output matching your Pydantic class
        response_mime_type="application/json",
        response_schema=PainExtractionResponse,
    ),
)

# Takes the raw text from Gemini and parses/validates it into the Pydantic class
parsed_result = PainExtractionResponse.model_validate_json(response.text)

print("\n--- CHATBOT MESSAGE TO USER ---")
# Now this will work perfectly because parsed_result is defined!
print(parsed_result.user_message)

print("\n--- STRUCTURED PAIN LOGS (For Frontend Body Map UI) ---")
for log in parsed_result.pain_logs:
    severity_str = f"{log.severity}/10" if log.severity is not None else "N/A"
    feeling_str = log.pain_type if log.pain_type is not None else "N/A"
    print(f"📍 Zone: {log.zone_id:<20} | Severity: {severity_str:<5} | Feeling: {feeling_str}")

print("\n--- RAW JSON DATA SENT TO FRONTEND ---")
print(parsed_result.model_dump_json(indent=2))