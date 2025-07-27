import os
import requests
import argparse

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxx"}  # Replace with your actual API key

def query(filename):
    try:
        # Check if file exists
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
        
        # Check API response
        if response.status_code != 200:
            error_msg = response.json().get("error", "Unknown error")
            raise Exception(f"API Error ({response.status_code}): {error_msg}")
            
        return response.json()
    
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Convert speech to text using Whisper API')
    parser.add_argument('-i', '--input', required=True, help='Path to input audio file')
    parser.add_argument('-o', '--output', default='output.txt', help='Path to output text file (default: output.txt)')
    
    args = parser.parse_args()
    
    output = query(args.input)

    if "error" in output:
        print("Error:", output["error"])
    else:
        transcription = output.get("text", "No text found")
        print("Transcription:", transcription)
        
        try:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(transcription)
            print(f"\nResult saved to: {args.output}")
        except Exception as e:
            print(f"Error saving file: {str(e)}")

if __name__ == '__main__':
    main()
    input("Press Enter to exit...")  # To prevent window from closing immediately on Windows
