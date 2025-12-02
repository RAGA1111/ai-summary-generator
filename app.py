import streamlit as st
import requests
import json

# ---------------------- UI CONFIG ----------------------
st.set_page_config(page_title="Local AI Notes Generator", page_icon="🧠")
st.title("🧠 Local AI Notes Generator (Mistral - Offline)")
st.caption("Uses LM Studio running locally at http://localhost:1234")

# ---------------------- USER INPUT ----------------------
user_input = st.text_area("📄 Paste your study notes here:", height=250)

model_name = st.text_input("🤖 Model Name (as shown in LM Studio):", "mistral")

if st.button("Generate"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some notes first.")
        st.stop()

    with st.spinner("⏳ Summarizing using your local Mistral model..."):

        prompt = (
            "Summarize the following text into clean, concise bullet points. "
            "Prioritize clarity, exam-oriented structure, and remove unnecessary details.\n\n"
            f"{user_input}"
        )

        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "max_tokens": 1200,
            "stream": False
        }

        try:
            response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )

            # Validate response
            if response.status_code != 200:
                st.error(f"❌ Error: Received status code {response.status_code}")
                st.text(response.text)
                st.stop()

            data = response.json()

            if "choices" not in data or len(data["choices"]) == 0:
                st.error("❌ No output from model. Check LM Studio logs.")
                st.stop()

            summary = data["choices"][0]["message"]["content"]

            # ---------------------- OUTPUT ----------------------
            st.success("✅ Summary generated successfully!")
            st.subheader("📝 Summarized Notes:")
            st.markdown(summary)

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to LM Studio. Make sure:")
            st.markdown("""
            - LM Studio is running  
            - Server Mode is enabled (⚙️ > Developer > Enable Local Server)  
            - Running on port **1234**
            """)
        except Exception as e:
            st.error("Unexpected error occurred:")
            st.exception(e)

