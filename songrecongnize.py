from ShazamAPI import Shazam
import os
from pytube import Search
from pytube import YouTube
import shutil

def detect_song(path):
    path = 'share'
    obj = os.scandir(path)
    print("Files and Directories in '% s':" % path)
    for entry in obj :
        if entry.name != "songs":  
            print(entry.name)
            state = '/share/' + entry.name + '/computing'
            output = '/share/' + entry.name + '/output.txt'
            inputfile = '/share/' + entry.name + '/input.mp3'
            if ((not os.path.isfile(state)) or (not os.path.isfile(output))):
                fp = open(state,'x')
                fp.close()
                fp = open(output,'w')
                mp3_file_content_to_recognize = open(inputfile, 'rb').read()
                shazam = Shazam(mp3_file_content_to_recognize)
                recognize_generator = shazam.recognizeSong()
                t = next(recognize_generator)
                print('song title',t[1]['track']['title'],'\nsinger',t[1]['track']['subtitle'],'\nlyric',t[1]['track']['sections'][1]['text'])
                song_title = 'song title:' + t[1]['track']['title']
                singer = '\nsinger:' + t[1]['track']['subtitle']
                image = '\nimage:' + t[1]['track']['images']['background']
                fp.write(song_title)
                fp.write(singer)
                fp.write(image)
                fp.write('\nlyric:')
                for l in t[1]['track']['sections'][1]['text']:
                    fp.write(l)
                fp.close()
                while True:
                    s = Search(t[1]['track']['title'] + ' ' +  t[1]['track']['subtitle'])
                    v = s.results
                    download_state = False
                    for tmp in v:
                        print(tmp.title)
                        yt = YouTube(tmp.watch_url)
                        target_path = '/share/' + entry.name
                        sname = 'song.mp3'
                        try:
                            yt.streams.filter().get_audio_only().download(filename = sname, output_path = target_path)
                            download_state = True
                            break
                        except:
                            continue
                    if download_state:
                        data_path = "share\\songs\\" + t[1]['track']['title'] + '_' + t[1]['track']['subtitle'] + ".mp3"
                        shutil.copyfile(target_path + '\\song.mp3',data_path)
                        break
                    else:
                        print('can not download')