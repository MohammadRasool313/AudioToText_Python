import os
import requests

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxx"}  # Replace with the actual API key

def query(filename):
    try:
        # File existence check
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found!")
        
        # Automatic file format detection
        file_ext = os.path.splitext(filename)[1].lower().lstrip('.')
        content_type = f"audio/{file_ext}" if file_ext in ['flac', 'wav', 'mp3', 'ogg'] else "audio/*"
        
        with open(filename, "rb") as f:
            data = f.read()
        
        response = requests.post(
            API_URL,
            headers={"Content-Type": content_type, **headers},
            data=data
        )
        
        # API response review
        if response.status_code != 200:
            error_msg = response.json().get("error", "Unknown error")
            raise Exception(f"API Error ({response.status_code}): {error_msg}")
            
        return response.json()
    
    except Exception as e:
        return {"error": str(e)}

filename = input("Enter the path of audio file: ")
output = query(filename)

if "error" in output:
    print("Error:", output["error"])
else:
    print("Transcription:", output.get("text", "No text found"))
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(str(output.get("text", "No text found")))
    print("Saved in output.txt file")    

input()