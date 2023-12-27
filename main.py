import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
from components.sidebar import sidebar

st.set_page_config(page_title="HanwhaGPT", page_icon="📁", layout="centered", initial_sidebar_state="auto", menu_items=None)
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

openai.api_key = st.secrets.openai_key

st.title("HanwhaGPT")
st.info("Built by [tylertaewook](https://tylertaewook.com) for Hanwha GIP AI Track's Case Study. View source code at [Github](https://github.com/tylertaewook/hanwha-ai-case-study)", icon="📃")

model: str = st.selectbox("Model", options=MODEL_LIST)


if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about President Biden's State of the Union address in 2022!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model=model, temperature=0.5, system_prompt="You are an expert on the the content of President Biden's State of the Union address in 2022. You are aware of the United States' position on Russia's invasion of Ukraine, as well as the economic achievements of the past year and future plans. Assume that all questions are related to the President Biden's speech. Keep your answers based on facts – do not hallucinate features. When asked unrelated question, refuse to answer."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

if prompt := st.selectbox("Questions from Instructions", ("What is mentioned as the cause for the distance between people last year?",
            "What is described as prevailing over tyranny in the speech?",
            "Which leader is accused of misjudging the global response to their actions?",
            "Which country and its people are commended for their resistance and bravery?",
            "How did President Biden describe the American Rescue Plan?",
            "What were the plans to combat inflation?",
            "What did President Biden propose regarding energy and child care costs in his 2022 State of the Union Address?")):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
