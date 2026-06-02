import streamlit as st
import requests
st.set_page_config(page_title="FinAI Analyst", page_icon="📈", layout="centered")
st.title("📈 Financial AI Assistant")
st.markdown("Ask me to extract revenue data or plot 4-year trends for any stock ticker.")
if "messages" not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("chart"):
            st.image(message["chart"])
if prompt := st.chat_input("E.g., Can you plot the financial trends for Microsoft (MSFT)?"):


    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        with st.spinner("Agent is researching..."):
            try:

                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"query": prompt}
                )

                if response.status_code == 200:
                    data = response.json()
                    answer_text = data.get("answer", "Error: No answer returned.")
                    chart_url = data.get("chart_url")

                    # Render the text
                    st.markdown(answer_text)

                    if chart_url:
                        st.image(chart_url)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer_text,
                        "chart": chart_url
                    })
                else:
                    st.error(f"Backend Server Error: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend. Is your FastAPI server running?")

