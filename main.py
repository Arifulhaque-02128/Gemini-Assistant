# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:47:20 2024

@author: User
"""

import os
import streamlit as slit
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model, gemini_flash_response, embedding_model_response, gemini_LLM_response
from PIL import Image


working_directory = os.path.dirname(os.path.abspath(__file__))


# setting up the page configuration
slit.set_page_config(
    page_title='Gemini AI',
    page_icon='🧠',
    layout='centered'
)

with slit.sidebar :

    selected = option_menu( menu_title = 'Gemini AI',
                           options= ['ChatBot', 'Image Captioning', 'Embed Text', 'Ask Me Anything'],
                           menu_icon='robot',
                           icons=['chat-left-dots', 'card-image','textarea-t', 'patch-question'],
                           default_index= 0
                           )

def translate_role_for_streamlit(user_role) : 
    if user_role == 'model' : return 'assistant'
    else : return user_role

if selected == 'ChatBot' :
    model = load_gemini_pro_model()

    # initialize chat session in streamlit if not already present
    if 'chat_session' not in slit.session_state :
        slit.session_state.chat_session = model.start_chat(history=[])

    # streamlit page title
    slit.title('💬 ChatBot')

    # display the chat history
    for message in slit.session_state.chat_session.history :
            with slit.chat_message(translate_role_for_streamlit(message.role)) :

                slit.markdown(message.parts[0].text)

    # input field user's message
    user_prompt = slit.chat_input("Ask Gemini-Pro...")

    if user_prompt :
        slit.chat_message('user').markdown(user_prompt)

        gemini_res = slit.session_state.chat_session.send_message(user_prompt)

        # display gemini-pro response
        with slit.chat_message ('assistant') :
            slit.markdown(gemini_res.text)


# Image Captioning Page 
if selected == 'Image Captioning' :
     
     # streamlit page title
     slit.title('🖼️ Image Narrate')

     uploaded_img = slit.file_uploader('Upload an Image...', type = ['jpg', 'jpeg', 'png'])

     if slit.button('Generate Caption') :
          image = Image.open(uploaded_img)

          col1, col2 = slit.columns(2)


          with col1 :
               # Resize the image using a valid resampling filter
               resized_image = image.resize((800, 500), Image.Resampling.LANCZOS)
               slit.image(resized_image)

               default_prompt = 'Write a short caption for this image...'

               # getting the response from the gemini-pro-vision model
               caption = gemini_flash_response(default_prompt, image)


               with col2 :
                    slit.info(caption)


# text embedding page 

if selected == 'Embed Text' :
     slit.title('🖺 Embed Text')

     #image text box

     input_text = slit.text_area(label='', placeholder='Enter the text to get the embeddings.')

     if slit.button('Get Embedding') :
          res = embedding_model_response(input_text) 
          slit.markdown(res)

# ask me anything page

if selected == 'Ask Me Anything' :
     slit.title('❓ Ask Me Anything')

     # text box to enter prompt
     user_prompt = slit.text_area(label='', placeholder='Ask Gemini-Pro...')

     if slit.button("Get an answer") :
          response = gemini_LLM_response(user_prompt)

          slit.markdown(response)







            