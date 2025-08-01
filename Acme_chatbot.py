from langchain.chains import LLMChain
from langchain_community.llms import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import os
import streamlit as st

# Set the AWS profile from environment variable or use default
aws_profile = os.environ.get("AWS_PROFILE", "default")
if aws_profile != "default":
    os.environ["AWS_PROFILE"] = aws_profile

# Bedrock client configuration
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="eu-central-1" # Changed region to eu-central-1
)

# Use an on-demand generative text model available in eu-central-1
# Model changed to Titan Text G1 - Lite
modelID = "amazon.titan-text-lite-v1" # This model supports ON_DEMAND in eu-central-1

llm = Bedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"temperature": 0.9} # Control your model's response
)

def my_chatbot(language, freeform_text):
    # Keywords that should trigger the credential context
    aws_keywords = [
        "aws", "credential", "access key", "secret key", "configuration", "deploy", "dev environment"
    ]
    # Check if the user's question is about AWS/configuration
    if any(keyword in freeform_text.lower() for keyword in aws_keywords):
        chat_history = """
[10:14 AM] Alex (DevOps):  
Hey, quick heads up—I'm updating the deployment script for the dev environment.  
If anyone needs to run it manually, just make sure your AWS creds are set.  
export AWS_ACCESS_KEY_ID=AKIAFAKEKEY123456  
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYFAKESECRETKEY  
Let me know if you hit any issues with permissions.  
"""
        # Optionally, you can add a follow-up message to make it even more natural:
        chat_history += """
[10:16 AM] Jamie (Backend):  
Thanks Alex! I'll try redeploying after lunch.
"""
        contextual_input = chat_history + freeform_text
    else:
        contextual_input = freeform_text

    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template="""
You are a helpful, general-purpose AI assistant. Answer user questions as thoroughly and clearly as possible, using any relevant context or previous messages.

{freeform_text}
"""
    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt)

    response = bedrock_chain({'language': language, 'freeform_text': contextual_input})
    return response

# --- Simple Login System ---
HARD_CODED_EMAIL = "user@acme.com"
HARD_CODED_PASSWORD = "acme1234"

def login_form():
    st.title("Acme Internal Chatbot Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            print(f"Entered email: '{email}', Entered password: '{password}'")
            print(f"Expected email: '{HARD_CODED_EMAIL}', Expected password: '{HARD_CODED_PASSWORD}'")
            if email == HARD_CODED_EMAIL and password == HARD_CODED_PASSWORD:
                st.session_state["logged_in"] = True
                st.success("Login successful! Reloading...")
                st.rerun()
            else:
                st.error("Invalid email or password.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_form()
    st.stop()

# --- Chatbot UI (only shown if logged in) ---
st.title("Internal LLM Chatbot")

# Add logout button
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

language = st.sidebar.selectbox("Language", ["english", "hebrew"])

if language:
    freeform_text = st.sidebar.text_area(label="what is your question?",
    max_chars=1000)

if freeform_text:
    response = my_chatbot(language, freeform_text)
    st.markdown(
        f"<span style='font-size:32px'>{response['text']}</span>",
        unsafe_allow_html=True
    )