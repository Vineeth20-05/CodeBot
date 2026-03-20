import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="Code Assistant", page_icon="💻")
st.title("💻 Multilanguage Code Assistant (GPT-4o)")

# API Key
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not api_key:
    st.warning("Enter API Key")
    st.stop()

# LLM
llm = ChatOpenAI(
    openai_api_key=api_key,
    model="gpt-4o-mini",
    temperature=0.3
)

# User Inputs
task = st.selectbox("Select Task", [
    "Explain Code",
    "Convert Code",
    "Debug Code",
    "Optimize Code"
])

language = st.selectbox("Target Language", [
    "Python", "Java", "C++", "JavaScript"
])

code_input = st.text_area("Enter your code or question")

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert coding assistant. "
     "Support multiple programming languages and provide clean, correct responses."),
    
    ("user",
     "Task: {task}\n"
     "Target Language: {language}\n"
     "Code/Input:\n{code}")
])

# LCEL Chain
chain = prompt | llm

# Button
if st.button("Run"):

    if not code_input:
        st.error("Enter code or query")
    else:
        with st.spinner("Processing..."):

            response = chain.invoke({
                "task": task,
                "language": language,
                "code": code_input
            })

            st.success("✅ Result")
            st.code(response.content)