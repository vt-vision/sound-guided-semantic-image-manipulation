import pandas as pd
import os
from tqdm import tqdm
from glob import glob
import youtube_dl

import os
import librosa
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

def trim_audio_data(audio_file, save_file, start):
    sr = 44100

    y, sr = librosa.load(audio_file, sr=sr)
    print("Save!")
    ny = y[sr*start:sr*(start+10)]
    librosa.write_wav(save_file + '.wav', ny, sr)

ydl_opts = {
    'format': 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<=1440]',
}

# vggsound.csv : https://www.robots.ox.ac.uk/~vgg/data/vggsound/
vgg = pd.read_csv("vggsound.csv", names=["YouTube ID", "start seconds", "label", "train/test split"])

slink = "https://www.youtube.com/watch?v="

sumofError = 0
cnt = 0

os.makedirs("/storage/vggsound-new/audio", exist_ok=True)
os.makedirs("/storage/vggsound-new/video", exist_ok=True)
os.makedirs("/storage/vggsound-new/image", exist_ok=True)

for idx, row in tqdm(enumerate(vgg.iterrows())):
    if idx < 21677:
        continue
    _, row = row 
    url, sttime, label, split = row["YouTube ID"], row["start seconds"], row["label"], row["train/test split"] 
    endtime = int(sttime) + 10 
            
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([slink + url])

        # Save 10 sec Wav File with Text Prompt
        path = glob("*.mp4")[0]

        video = VideoFileClip(path)
        clip = video.subclip(int(sttime), min(int(endtime), video.end))
        clip.write_videofile("/storage/vggsound-new/video/"+str(idx)+str("_")+label+".mp4")
        clip.audio.write_audiofile("/storage/vggsound-new/audio/"+str(idx)+str("_")+label+".mp3")
        clip.save_frame("/storage/vggsound-new/image/"+str(idx)+str("_")+label+".png", t=7)
        #sound = AudioSegment.from_file(path, "mp4")
        #sound = sound[int(sttime) * 1000:int(endtime) * 1000]
        #sound.export("/storage/vggsound/audio/"+str(idx)+str("_")+label+".mp3")

        os.remove(path)
    
    except:
        sumofError += 1
        continue

    
print(sumofError , "The number of error cases")
