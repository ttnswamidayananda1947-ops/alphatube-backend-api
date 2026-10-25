from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# ஆப் எரர் இல்லாமல் கம்யூனிகேட் செய்ய CORS அனுமதி
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AlphaTube API is successfully running!"}

@app.get("/extract")
def extract_media(url: str):
    try:
        # எந்த வெப்சைட்டாக இருந்தாலும் சிறந்த குவாலிட்டி லிங்கை எடுக்க yt-dlp செட்டிங்ஸ்
        ydl_opts = {
            'format': 'best', # சிறந்த வீடியோ/ஆடியோ குவாலிட்டி
            'quiet': True,
            'no_warnings': True,
            'skip_download': True, # டவுன்லோட் செய்யாமல் லிங்கை மட்டும் எடுக்கும்
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'AlphaTube_Video')
            thumbnail = info.get('thumbnail', '')
            
            # நேரடியான MP4 லிங்கை எடுப்பது
            video_url = info.get('url', '')
            
            # சில நேரங்களில் URL நேரடியாக இருக்காது, அப்போது formats-ல் இருந்து எடுக்க வேண்டும்
            if not video_url and 'formats' in info:
                for f in info['formats'][::-1]:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        video_url = f.get('url')
                        break
                        
            return {
                "status": "success",
                "title": title,
                "thumbnail": thumbnail,
                "download_url": video_url, # இதுதான் உண்மையான Direct MP4 லிங்க்
                "original_url": url
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
              
