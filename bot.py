import os
import asyncio
import yt_dlp
from telegram import Bot
from flask import Flask
from threading import Thread

# Flask server (Render-in sönməməsi üçün vacibdir)
app = Flask('')

@app.route('/')
def home():
    return "Alfa Mood Bot Aktivdir!"

def run_web_server():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# --- SƏNİN MƏLUMATLARIN (TOKEN DAXİL) ---
TOKEN = "8523694849:AAEGB3IIg1amfXMcbklxxIX4OZ71uBcFtuU"
CHANNEL_ID = "@alfamood"
SIGNATURE = "🎵 @alfamood | Günün Trend Mahnısı"

async def download_and_send():
    print("Mahnı axtarılır və göndərilir...")
    # Trend mahnı axtarışı üçün ayarlar
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'music_file.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # YouTube-da 2026-nın trend mahnılarını axtarır
            info = ydl.extract_info("ytsearch1:trending music hits 2026", download=True)
            file_name = "music_file.mp3"
            title = info['entries'][0].get('title', 'Yeni Mahnı')
            
            bot = Bot(token=TOKEN)
            
            # Kanala göndərmə prosesi
            print(f"Mahnı tapıldı: {title}. Kanala göndərilir...")
            with open(file_name, 'rb') as audio:
                await bot.send_audio(
                    chat_id=CHANNEL_ID, 
                    audio=audio, 
                    caption=f"🎧 {title}\n\n{SIGNATURE}"
                )
            
            # Faylı təmizləyirik (yer tutmasın)
            os.remove(file_name)
            print("UĞURLA GÖNDƏRİLDİ! ✅")
            
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Botu işə salan əsas hissə
if __name__ == "__main__":
    # 1. Web serveri arxa fonda başladırıq
    t = Thread(target=run_web_server)
    t.start()
    
    # 2. Dərhal mahnı funksiyasını işə salırıq
    print("Bot başladılır...")
    asyncio.run(download_and_send())
