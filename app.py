import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key, openai_api_key
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Configure the generative AI model
genai.configure(api_key=google_gemini_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Setting up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Set app to wide layout
st.set_page_config(layout="wide")

# Title of the app
st.title('MemoiryMingle: Write your next thought with AI 🧠🦾🤺')

# Create a subheader
st.subheader('Now you can craft a perfect blog with the help of AI-MemoiryMingle is your Blog Companion')

# Sidebar for user input
with st.sidebar:
    st.title("Input your Blog details")
    st.subheader("Provide a brief description of your blog you want to generate")

    # Blog Title
    blog_title = st.text_input("BLOG TITLE")

    # Keywords input
    keywords = st.text_area("Keywords (comma-separated)")

    # Number of words
    num_words = st.slider("Number of words", min_value=250, max_value=1000, step=250)

    # Number of images
    num_images = st.number_input("Number of images", min_value=1, max_value=7, step=1)

# Submit button
submit_button = st.button("Generate my Blog")

if submit_button:
    try:
        # Create image variation
        image_response  = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)
        # Extract image URL
        image_url = image_response.data[0].url
        
        print(image_url)

        # Display the generated image
        st.image(image_url, caption="Generated Image")
    except Exception as e:
        st.error(f"Error generating image: {e}")

    # Starting chat session
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Write a blog on {blog_title} with keywords: {keywords}.",
                ],
            },
        ]
    )

    # Sending message to the model
    response = chat_session.send_message(
        f"Write a detailed blog post titled '{blog_title}' with the following keywords: {keywords}. The blog should be around {num_words} words long and discuss relevant topics in detail."
    )

    # Access and display the response message correctly
    try:
        content = response.candidates[0].content.parts[0].text
        st.write(content)
    except Exception as e:
        st.error(f"Error accessing the response content: {e}")
