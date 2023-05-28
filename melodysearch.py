import librosa
import numpy as np
import os
def melodySearch(userid):
    output2=''
    cnt=1
    path = 'share\\'+userid+'\\'
    obj = os.scandir(path)
    for entry in obj:
        if entry.name != "songs":
            state = path + entry.name + '\\computing3'
            output = path + entry.name + '\\outputmelody.txt'
            inputs = path + entry.name + "\\song.mp3"
            if os.path.isfile(inputs):
                if((not os.path.isfile(state)) or (not os.path.isfile(output))):
                    fp = open(state, 'x')
                    fp.close()
                    fp = open(output, 'w')
                    y, sr = librosa.load(inputs)
                    mfccs = librosa.feature.mfcc(y=y, sr=sr)
                    mean_mfccs = np.mean(mfccs, axis=1)
                    database_dir = 'share\\songs'
                    database = {}
                    # print('----------------------------------------------------------------')
                    for filename in os.listdir(database_dir):
                        # print('filename',filename)
                        file_path = os.path.join(database_dir, filename)
                        song,sample_rate = librosa.load(file_path)
                        song_mfccs = librosa.feature.mfcc(y=song, sr=sr)
                        song_mean_mfccs = np.mean(song_mfccs, axis=1)
                        database[filename] = song_mean_mfccs


                    similar_songs = []
                    for song_name, song_mfccs in database.items():
                        distance = np.linalg.norm(mean_mfccs - song_mfccs)
                        # print('distance',distance)
                        similar_songs.append((song_name, distance))


                    similar_songs = sorted(similar_songs, key=lambda x: x[1])
                    songs = []
                    for song, distance in similar_songs:
                        songs.append(song)
                        fp.write(str(cnt)+'.'+song + '\n')
                        if len(songs)>5:
                            break
                        cnt+=1
                        # print('song',song)
                    output2=output
    return output2