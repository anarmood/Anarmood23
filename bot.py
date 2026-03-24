import os
import asyncio
import schedule
import time
import yt_dlp
from telegram import Bot
from flask import Flask
from threading import Thread

# --- RENDER ÜÇÜN SAXTA SERVER ---
app = Flask('')
@app.route('/')
def home():
    return "Bot oyaqdır!"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- BOT AYARLARI ---
TOKEN = "8523694849:AAEGB3IIg1amfXMcbklxxIX4OZ71uBcFtuU" # <--- Tokenini bura yazmağı unutma!
CHANNEL_ID = "@alfamood"        
SIGNATURE = "🎵 @alfamood | Günün Trend Mahnısı"

async def download_and_send():
    print("Mahnı axtarılır...")
    search_query = "ytsearch1:trending music hits 2026" 
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'alfamood_music.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            entry = info['entries'][0]
            file_name = "alfamood_music.mp3"
            title = entry.get('title', 'Yeni Mahnı')

            bot = Bot(token=TOKEN)
            with open(file_name, 'rb') as audio:
                await bot.send_audio(
                    chat_id=CHANNEL_ID, 
                    audio=audio, 
                    caption=f"🎧 {title}\n\n{SIGNATURE}"
                )
            os.remove(file_name)
            print("Mahnı uğurla göndərildi!")
    except Exception as e:
        print(f"Xəta: {e}")

def run_task():
    asyncio.run(download_and_send())

# İndidən etibarən hər 1 dəqiqədən bir yoxla (və ya saatlarını bura yaz)
schedule.every().day.at("23:45").do(run_task) # <--- Yoxlamaq üçün saatı dəyişə bilərsən

if name == "__main__":
    # Serveri ayrı bir "qolda" (thread) başlat
    t = Thread(target=run_web_server)
    t.start()
    
    # Botu başlat
    print("Bot aktivdir...")
    while True:
        schedule.run_pending()
        time.sleep(1)
