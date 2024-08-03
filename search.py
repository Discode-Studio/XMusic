from pytube import Search
from pytube import YouTube
import os
import shutil    #Importing libs

#This is funcs file


# We are finding the addresses of the vids that we want to find. Basicly we are trying to download the desired vid.
def give_link(name): # Youtube has different ids for each video. So we are finding those to download vids.
    s = Search(f"{name}")  #searching from title of the yt vid
    yt_id = s.results #this gives us a list
    video_ids = [video.video_id for video in yt_id] #scraping the data that we want

    video_id = video_ids[0] #getting the first element
    base_url = f"https://www.youtube.com/watch?v={video_id}" #making our link ready
    return base_url

def delete_audio():
    shutil.rmtree('music')

def find_music_name():
    return (os.listdir("music")[0])

def remove_all_files(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def download_vid(name):
    s = Search(f"{name}") 
    yt_id = s.results
    video_ids = [video.video_id for video in yt_id]

    video_id = video_ids[0]
    base_url = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(base_url)
    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first() #downloading the first Result and only mp4
    audio_stream.download(output_path='music') # we are deciding where we want to install
