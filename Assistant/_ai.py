import json
import google.generativeai as genai

with open("API_KEY.json","r") as api_dict:
    API = json.load(api_dict)


with open("_preprompt.txt", "r") as pre_file:
    pre_prompt = pre_file.read()

class Assistant:
    try:
        genai.configure(api_key=API['key'])
        model = genai.GenerativeModel('gemini-pro')
    except Exception:
        pass

    def generate(prompt:str):
        try:response = Assistant.model.generate_content(f"{pre_prompt} {prompt}")
        except Exception:return "Request handeling overloaded. Please wait until new key is initilized"
        else:return response.text