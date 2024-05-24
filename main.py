import streamlit as st
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.openai import OpenAIChat
from openai import AuthenticationError

#Create  user interface
st.title("My AI Web Assistant")
st.caption("Search the web with AI!")

openai_access_token = st.text_input("OPEN AI API Key", type="password")

if openai_access_token:
    try:
        assistant = Assistant(
            llm=OpenAIChat(
                model="gpt-3.5-turbo-0125",
                max_tokens=1024,
                temperature=0.9,
                api_key=openai_access_token
            ),
            tools=[DuckDuckGo()],
            show_tool_calls=True
        )
        query = st.text_input("Enter Search Query Here", type="default")

        if query:
            response = assistant.run(query, stream=False)
            st.write(response)
    except AuthenticationError as e:

        error_message = e.response.json().get('error', {}).get('message', 'An error occurred')

        st.error(f"AuthenticationError: {error_message}")

    except Exception as e:

        st.error(f"An unexpected error occurred: {e}")

