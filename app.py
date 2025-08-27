import streamlit as st
from pytube import YouTube
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

        # Download audio with pytube
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(only_audio=True).first()
        temp_file = stream.download(filename="temp_audio.mp4")

        # Rename to mp3 (simple workaround for cloud)
        mp3_file = "audio.mp3"
        os.rename(temp_file, mp3_file)

        # Upload to Google Drive
        folder_id = "YOUR_ONLY_VOCALS_FOLDER_ID"
        gfile = drive.CreateFile({
            'title': mp3_file,
            'parents': [{'id': folder_id}]
        })
        gfile.SetContentFile(mp3_file)
        gfile.Upload()

        st.success(f"✅ {mp3_file} uploaded to Google Drive → only vocals")
        os.remove(mp3_file)
