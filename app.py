import streamlit as st
from openai import OpenAI
import os
import json
import re
from datetime import datetime

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Viral Genie Pro", page_icon="🔥", layout="wide")

st.title("🔥 Viral Genie Pro - Fast Content Factory")
st.markdown("Create Viral Reels + Voiceover + Thumbnail in 1 Click")
st.markdown("---")

# ---------------- HISTORY FILE ----------------
HISTORY_FILE = "history.json"

def save_history(topic, platform, audience, content):
    data = {
        "time": str(datetime.now()),
        "topic": topic,
        "platform": platform,
        "audience": audience,
        "content": content
    }

    with open(HISTORY_FILE, "a") as f:
        json.dump(data, f)
        f.write("\n")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Settings")

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

if not api_key:
    st.info("Bhai sidebar me API key daal de fir tool start hoga.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("Topic kya hai?", placeholder="e.g. Paise kamane ke 3 tarike")
    platform = st.selectbox("Platform", ["Instagram Reels", "YouTube Shorts", "LinkedIn"])

with col2:
    audience = st.selectbox("Target Audience", ["Gen-Z / Students", "Working Professionals", "Tech Audience"])
    voice_type = st.selectbox("Voice Tone (Hindi Friendly)", ["nova", "shimmer", "alloy", "onyx"])

# ---------------- GENERATE BUTTON ----------------
if st.button("🚀 Generate Viral Content (Hinglish)"):
    
    if not topic:
        st.error("Topic likhna zaroori hai bhai!")
    else:
        try:
            with st.spinner("AI dimaag chala raha hai... Viral content ban raha hai 🔥"):

                # ---------------- BETTER PROMPT ----------------
                text_prompt = f"""
You are a viral content strategist.

Create highly viral {platform} content for {audience} about {topic}.

IMPORTANT RULES:
Write the SCRIPT in HINGLISH (Hindi words in English script).
Keep it short, fast and engaging.

Give output ONLY in this format:

HOOK:
SCRIPT:
CAPTION:
HASHTAGS:
"""

                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": text_prompt}],
                    temperature=0.7
                )

                content = res.choices[0].message.content

                # ---------------- SCRIPT EXTRACTION ----------------
                script_match = re.search(r"SCRIPT:\s*(.*)", content, re.DOTALL)
                script_text = script_match.group(1).strip() if script_match else content

                # ---------------- VOICE GENERATION ----------------
                audio_file = "voiceover.mp3"

                audio_res = client.audio.speech.create(
                    model="tts-1",
                    voice=voice_type,
                    input=script_text[:600]
                )

                audio_res.stream_to_file(audio_file)

                # ---------------- SAVE HISTORY ----------------
                save_history(topic, platform, audience, content)

                st.success("🔥 Viral Content Ready!")

                # ---------------- OUTPUT LAYOUT ----------------
                colA, colB = st.columns([1, 2])

                with colB:
                    st.subheader("📝 Viral Script (Hinglish)")
                    st.info(content)

                    with open(audio_file, "rb") as f:
                        st.audio(f.read())
                        st.download_button("Download Voiceover", f, "viral_voice.mp3")

                # ---------------- THUMBNAIL GENERATION ----------------
                with st.spinner("Thumbnail HD me ban raha hai..."):

                    img_res = client.images.generate(
                        model="dall-e-3",
                        prompt=f"""
Ultra realistic viral thumbnail about {topic},
emotional human face expression,
high contrast lighting,
cinematic background,
very clickable YouTube style,
4k quality,
no text
""",
                        size="1024x1024"
                    )

                    img_url = img_res.data[0].url

                with colA:
                    st.image(img_url, caption="AI Viral Thumbnail")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- VIEW HISTORY ----------------
st.markdown("---")
st.subheader("📁 Recent Generated Content")

if st.button("Show History"):
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f.readlines()[-5:]:
                data = json.loads(line)
                st.write("**Topic:**", data["topic"])
                st.write(data["content"])
                st.markdown("---")
    except:
        st.warning("Abhi history empty hai.")

st.markdown("---")
st.caption("Made with ❤️ by Piyush | Viral Content System")