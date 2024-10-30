import os 
import json
import google.generativeai as genai

# get the working directory

working_directory = os.path.dirname(os.path.abspath(__file__))

# Retrieve the API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the genai client with the API key
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    raise ValueError("API key not found in environment variables.")

# function to load gemini-pro model for chatbot
def load_gemini_pro_model() :
    gemini_pro_model = genai.GenerativeModel('gemini-pro')

    return gemini_pro_model


# function to load model for image captioning
def gemini_flash_response(prompt, image) :
    gemini_flash_model = genai.GenerativeModel('gemini-1.5-flash')
    res = gemini_flash_model.generate_content([prompt, image])

    result = res.text
    return result

# function for get embedding for text

def embedding_model_response(input_text) :
    embedding_model = 'models/embedding-001'
    embedding = genai.embed_content(model=embedding_model,
                                   content = input_text,
                                   task_type = 'retrieval_document')
    embedding_list = embedding['embedding']
    
    return embedding_list


# function to get a response from gemini-pro LLM

def gemini_LLM_response(user_prompt) :
    gemini_llm_model = genai.GenerativeModel('gemini-pro')

    response = gemini_llm_model.generate_content(user_prompt)

    result = response.text
    
    return result
