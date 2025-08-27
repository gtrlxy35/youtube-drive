iimport yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename
st.title("🎵 YouTube → Google Drive (Only Vocals)")

# --- Authenticate Google Drive using Secrets ---
if "drive" not in st.session_state:
    creds_json = st.secrets["GOOGLE_CREDENTIALS"]  # Entire JSON content
    with open("client_secrets.json", "w") as f:
        f.write(creds_json)

    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("client_secrets.json")
    gauth.LocalWebserverAuth()  # Authenticate with Google
    drive = GoogleDrive(gauth)
    st.session_state.drive = drive

drive = st.session_state.drive

# --- YouTube URL input ---
youtube_url = st.text_input("Paste YouTube Link:")

if st.button("Download to Google Drive"):
    if not youtube_url.strip():
        st.warning("⚠️ Please paste a valid YouTube link.")
    else:
        st.info("⬇️ Downloading audio...")

        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(only_audio=True).first()
            temp_file = stream.download(filename="audio.mp4")

            # Rename to mp3 (Streamlit Cloud workaround)
            mp3_file = "audio.mp3"
            os.rename(temp_file, mp3_file)

            # Upload to Google Drive
            folder_id = st.secrets["1lMxZn5YV3DHmv90il3zOWHlQvBk2u24A"]# Folder ID stored in secrets
            gfile = drive.CreateFile({
                'title': mp3_file,
                'parents': [{'id': folder_id}]
            })
            gfile.SetContentFile(mp3_file)
            gfile.Upload()

            st.success(f"✅ {mp3_file} uploaded to Google Drive → only vocals")
            os.remove(mp3_file)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")



