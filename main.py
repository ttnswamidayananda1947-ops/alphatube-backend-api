from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ஹேக்கர்கள் எடுக்க முடியாத உங்களின் ரகசிய API Key
SECRET_API_KEY = "AlphaTube_Secure_Key_2026"

@app.get("/")
def home():
    return {"message": "AlphaTube Secure API is running!"}

@app.get("/extract")
def extract_media(url: str, x_api_key: str = Header(None)):
    # API Key சரியாக இருக்கிறதா என்று செக் செய்யும் லாஜிக்
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'AlphaTube_Video')
            thumbnail = info.get('thumbnail', '')
            
            video_url = info.get('url', '')
            
            if not video_url and 'formats' in info:
                for f in info['formats'][::-1]:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        video_url = f.get('url')
                        break
                        
            return {
                "status": "success",
                "title": title,
                "thumbnail": thumbnail,
                "download_url": video_url,
                "original_url": url
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
