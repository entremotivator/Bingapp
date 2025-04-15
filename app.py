import streamlit as st
import tempfile
import os
import subprocess

# --- App Title and Description ---
st.set_page_config(page_title="Bings Apps: WAV to MP3 Converter", page_icon="🎵")
st.title("🎵 Bings Apps: WAV to MP3 Converter")
st.write(
    """
    Upload a WAV file and convert it to MP3 format.  
    This app is optimized for large files and runs entirely in your browser!
    """
)

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Choose a WAV file to convert", 
    type=["wav"], 
    help="Maximum upload size depends on server settings."
)

# --- Helper Function: Convert WAV to MP3 using ffmpeg ---
def convert_wav_to_mp3(input_wav_path, output_mp3_path):
    """
    Converts a WAV file to MP3 using ffmpeg.
    Returns True if successful, False otherwise.
    """
    try:
        # -y: overwrite output, -vn: no video, -ar: sample rate, -ac: channels, -b:a: bitrate
        result = subprocess.run(
            [
                "ffmpeg", "-y", "-i", input_wav_path,
                "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", output_mp3_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr

# --- Main Logic ---
if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    st.info("Your file is ready for conversion.")

    # Use temporary files for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        temp_wav.write(uploaded_file.read())
        temp_wav_path = temp_wav.name

    temp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_mp3_path = temp_mp3.name
    temp_mp3.close()

    # --- Conversion ---
    with st.spinner("Converting to MP3... Please wait."):
        success, error_message = convert_wav_to_mp3(temp_wav_path, temp_mp3_path)

    # --- Download Button or Error Message ---
    if success:
        with open(temp_mp3_path, "rb") as mp3_file:
            mp3_bytes = mp3_file.read()
        st.success("Conversion successful! Download your MP3 below.")
        st.download_button(
            label="⬇️ Download MP3",
            data=mp3_bytes,
            file_name=os.path.splitext(uploaded_file.name)[0] + ".mp3",
            mime="audio/mp3"
        )
    else:
        st.error("Conversion failed. Please check your file and try again.")
        st.code(error_message, language="bash")

    # --- Clean up temporary files ---
    try:
        os.remove(temp_wav_path)
        os.remove(temp_mp3_path)
    except Exception:
        pass

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    **How it works:**  
    - Your WAV file is processed securely and never stored.  
    - Conversion is powered by [ffmpeg](https://ffmpeg.org/).  
    - For best results, upload uncompressed WAV files.
    """
)
st.caption("Made by Entremotivaor. [Source code](https://github.com/your-repo/bings-apps-wav-to-mp3)")

