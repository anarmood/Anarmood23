import os
import asyncio
import schedule
import time
import yt_dlp
from telegram import Bot

# --- AYARLAR ---
# @BotFather-dən aldığınız kodu aşağıdakı dırnaqların arasına yapışdırın
TOKEN = "8523694849:AAEGB3IIg1amfXMcbklxxIX4OZ71uBcFtuU" 
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
    except Exception as e:
        print(f"Xəta: {e}")

def run_task():
    asyncio.run(download_and_send())

# SAATLAR
schedule.every().day.at("23:35").do(run_task)
schedule.every().day.at("21:00").do(run_task)

print("Bot aktivdir...")
while True:
    schedule.run_pending()
    time.sleep(60)
