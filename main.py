import streamlit as st
import os
import io
from PIL import Image  


import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# API configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
text_model= genai.GenerativeModel("gemini-pro")
image_model = genai.GenerativeModel("gemini-pro-vision")

def get_combinations(query, clothes_desc):
    if query == "":
         text = f"You are an amazing stylist who knows best color combinations for outfits. So Build me some good outfits with great color combinations from the clothes which i have uploaded, these are the descriptions of each item {clothes_desc}. Using the description of each item, I want you to generate some good outfits for me using the items which i have given you."
    elif clothes_desc == []:
        text = f"You are an amazing stylist who knows best color combinations for outfits. So Build me some good outfits with great color combinations using the description of each item, I want you to generate some good outfits for me along with the needs like {query}."
    else:
        text = f"You are an amazing stylist who knows best color combinations for outfits. So Build me some good outfits with great color combinations from the clothes which i have uploaded, these are the descriptions of each item {clothes_desc}. Using the description of each item, I want you to generate some good outfits for me along with the needs like {query}."
    response = text_model.generate_content(text)
    response.resolve()
    return response.text

    
def get_image_description(image):
    text = f"Describe the image in detail like what the piece is and what color it is."
    response = image_model.generate_content([text, image], stream=True)
    response.resolve()
    return response.text

print("hello")

st.set_page_config( page_title="Wardrobe Guru", page_icon="👕")

# Image upload sections
st.title("Wardrobe Guru 👕")
st.text("Upload pictures of your clothes and we'll suggest some great outfits! 🧍🏻")
st.text("You can also add some other description for the outfit you want to add on.")
# st.text("👨🏻\n👕\n👖\n👟")
st.text("Please upload at least one image to generate outfit suggestions.")

uploded_clothes = st.file_uploader("Upload Clothes", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

clothes_desc = []
query = ""
query = st.text_input("Enter some other description for the outfit you want to add on", key="other_desc")

# button click
if st.button("Generate Outfits"):
    if not uploded_clothes and query == "":
        st.error("Please upload at least one image or describe your needs in textbox to generate outfit suggestions.")
        exit()  # Or offer alternative actions like browsing pre-defined outfits

    for clothes in uploded_clothes:
        clothes_image = Image.open(clothes)
        clothes_desc.append(get_image_description(clothes_image))
    
    st.text("Almost there, please wait...")

    print(clothes_desc)

    final_combos = (get_combinations(query, clothes_desc))
    st.success("Here are some outfit suggestions for you!")
    st.subheader("👕👖👟")
    st.success(final_combos)
    print(final_combos)
    
st.markdown("***While uploading images it might take some more time to process the images. so please wait for some time.***")
