import streamlit as st

import os
from google.cloud import speech
from pydub import AudioSegment
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Google Speech-to-Text Configuration
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# ✅ Initialize Google Speech Client
speech_client = speech.SpeechClient()

# ✅ Convert MP3 to WAV (if needed)
def convert_audio(audio_bytes, format="mp3"):
    """Convert MP3 or other formats to WAV for transcription."""
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    return wav_io.getvalue()

# ✅ Speech-to-Text Function
def transcribe_audio(audio_bytes, format="mp3"):
    """Convert and transcribe audio using Google Speech-to-Text."""
    if format != "wav":
        audio_bytes = convert_audio(audio_bytes, format)

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    
    response = speech_client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else "No transcription available."

# ✅ OpenAI IELTS Feedback
def analyze_response(text):
    """Use GPT-4 to analyze the response based on IELTS criteria."""
    prompt = f"""
    Evaluate the following IELTS speaking response:

    "{text}"

    Provide feedback on:
    - Fluency & Coherence
    - Lexical Resource
    - Grammatical Range & Accuracy
    - Pronunciation (if possible)
    
    Give a score (0-9) for each category and concise improvement suggestions.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# ✅ Generate PDF Report
def generate_pdf_report(feedback):
    """Create a downloadable IELTS feedback report."""
    pdf_filename = "IELTS_Feedback_Report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    c.setFont("Helvetica", 12)
    y_position = 750  # Starting position

    c.drawString(100, y_position, "IELTS Speaking Test Feedback")
    y_position -= 20

    for part, feedback_text in feedback.items():
        c.drawString(100, y_position, f"{part}:")
        y_position -= 20
        for line in feedback_text.split("\n"):
            c.drawString(120, y_position, line)
            y_position -= 15

    c.save()
    return pdf_filename

# ✅ Streamlit UI
st.set_page_config(page_title="IELTS Speaking Test", layout="wide")

st.title("🎤 IELTS Speaking Test Simulation")
st.markdown(
    """
    <div style="
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 8px;
        border-left: 5px solid #ff6f61;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
    ">
        <h4 style="color: #ff6f61; font-size: 24px;">Welcome to the <b>IELTS Speaking Test Simulation</b>! 🎙️</h4>
        <p style="font-size: 16px; color: #333;">This app helps you practice for the IELTS Speaking exam by simulating real test conditions.</p>
        <b style="font-size: 18px;">✨ How It Works:</b>
        <p style="font-size: 16px; color: #333;">
            🎤 <b>Practice Mode</b>: Get instant feedback on your spoken responses.<br>
            📝 <b>Test Mode</b>: Complete a full IELTS Speaking test with AI-generated scoring.<br>
            📥 <b>Download Report</b>: Receive a detailed PDF performance report.
        </p>
        <p style="font-size: 16px; color: #333;">
            Upload your voice recordings and let AI evaluate your fluency, vocabulary, grammar, and pronunciation! 🚀
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



# 🎛️ Mode Selection
mode = st.radio("Select Mode", ["Practice Mode", "Test Mode"], index=0)

if mode == "Practice Mode":
    st.subheader("🗣️ Speak and Get Instant Feedback")

    audio_file = st.file_uploader("Upload your voice recording (MP3 or WAV)", type=["mp3", "wav"])

    if audio_file:
        audio_bytes = audio_file.read()
        file_extension = audio_file.type.split("/")[-1]  # Get file type

        with st.spinner("Transcribing... 📝"):
            transcribed_text = transcribe_audio(audio_bytes, format=file_extension)

        st.success("✅ Transcription Complete!")
        st.write("**Transcription:**", transcribed_text)

        if transcribed_text:
            with st.spinner("Analyzing response... 🤖"):
                feedback = analyze_response(transcribed_text)

            st.markdown("### 📌 Feedback")
            st.write(feedback)

elif mode == "Test Mode":
    st.subheader("📝 IELTS Speaking Test")
    st.markdown("This section simulates a full IELTS Speaking test.")

    st.markdown("### **Part 1: Introduction**")
    st.write("Tell me about yourself.")
    part1_audio = st.file_uploader("Upload your response (MP3/WAV)", key="part1", type=["mp3", "wav"])

    st.markdown("### **Part 2: Cue Card**")
    st.write("Describe a memorable trip you had.")
    part2_audio = st.file_uploader("Upload your response (MP3/WAV)", key="part2", type=["mp3", "wav"])

    st.markdown("### **Part 3: Discussion**")
    st.write("Do you think travel broadens the mind?")
    part3_audio = st.file_uploader("Upload your response (MP3/WAV)", key="part3", type=["mp3", "wav"])

    if part1_audio and part2_audio and part3_audio:
        st.write("Processing responses...")

        part1_text = transcribe_audio(part1_audio.read(), format=part1_audio.type.split("/")[-1])
        part2_text = transcribe_audio(part2_audio.read(), format=part2_audio.type.split("/")[-1])
        part3_text = transcribe_audio(part3_audio.read(), format=part3_audio.type.split("/")[-1])

        st.write("**Transcriptions:**")
        st.write(f"🔹 **Part 1:** {part1_text}")
        st.write(f"🔹 **Part 2:** {part2_text}")
        st.write(f"🔹 **Part 3:** {part3_text}")

        st.write("Generating feedback...")

        part1_feedback = analyze_response(part1_text)
        part2_feedback = analyze_response(part2_text)
        part3_feedback = analyze_response(part3_text)

        feedback_dict = {
            "Part 1": part1_feedback,
            "Part 2": part2_feedback,
            "Part 3": part3_feedback
        }

        st.markdown("### 📊 Final Assessment")
        for part, feedback_text in feedback_dict.items():
            st.write(f"#### {part} Feedback")
            st.write(feedback_text)

        # 📥 Generate and Download PDF Report
        pdf_file = generate_pdf_report(feedback_dict)
        with open(pdf_file, "rb") as file:
            st.download_button("📥 Download Feedback Report", file, file_name="IELTS_Report.pdf")
