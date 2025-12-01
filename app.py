import streamlit as st

st.set_page_config(page_title="Local AI Notes Generator", page_icon="🧠")
st.title("🧠 Local AI Notes Generator (Mistral - Offline)")

user_input = st.text_area("📄 Paste your study notes here:")

if st.button("Generate"):
    if user_input.strip() == "":
        st.warning("Please enter some notes first.")
    else:
        with st.spinner("⏳ Summarizing using Mistral from LM Studio..."):
            prompt = f"Summarize the following text into clear bullet points for easy study:\n\n{user_input}"

            try:
                response = requests.post(
                    "http://localhost:1234/v1/chat/completions",  # LM Studio default local server
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "mistral",  # LM Studio uses 'mistral' for Mistral 7B Instruct
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.5,
                        "max_tokens": 1000
                    }
                )

                summary = response.json()["choices"][0]["message"]["content"]
                st.success("✅ Summary generated successfully!")
                st.subheader("📝 Summarized Notes:")
                st.markdown(summary)

            except Exception as e:
                st.error("❌ Failed to connect to LM Studio. Is it running with the server enabled?")
                st.exception(e)
