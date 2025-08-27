import streamlit as st
import yt_dlp
import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# --- Authenticate Google Drive ---
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens Google login in browser
    return GoogleDrive(gauth)

drive = authenticate_drive()

st.title("🎵 YouTube → Google Drive (Only Vocals)")

youtube_url = st.text_input("Paste YouTube Link:")

if st.button("Download to Google Drive"):
    if not youtube_url.strip():
        st.warning("⚠️ Please paste a valid YouTube link.")
    else:
        st.info("⬇️ Downloading audio...")

        # Temp filename
        output_file = "temp_audio.%(ext)s"

        # yt-dlp options (extract MP3)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_file,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Find MP3 file
        mp3_file = None
        for f in os.listdir():
            if f.endswith(".mp3"):
                mp3_file = f
                break

        if mp3_file:
            # Upload into Google Drive → "only vocals" folder
            # Replace with your actual folder ID from Drive URL
            folder_id = "https://drive.google.com/drive/u/0/folders/1lMxZn5YV3DHmv90il3zOWHlQvBk2u24A"

            gfile = drive.CreateFile({
                'title': mp3_file,
                'parents': [{'id': folder_id}]
            })
            gfile.SetContentFile(mp3_file)
            gfile.Upload()

            st.success(f"✅ {mp3_file} uploaded to Google Drive → only vocals")
            os.remove(mp3_file)

