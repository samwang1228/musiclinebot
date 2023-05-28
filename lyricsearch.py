import requests
from bs4 import BeautifulSoup
import sys
import codecs
import os
import textrazor
import time
def lyricsSearch(userid):
    output2=''
    path='share\\'+userid+'\\'
    textrazor.api_key = "5f5e9391fe74311e2321b31f50d34a87ccb1a86fa63e3a48c4a07ed2"
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    obj = os.scandir(path)
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    for entry in obj:
        if entry.name != "songs" :
            state = path + entry.name + '/computing2'
            output = path + entry.name + '/outputlyric.txt'
            inputs = path + entry.name + '/output.txt'
            if os.path.isfile(inputs):
                if((not os.path.isfile(state)) or (not os.path.isfile(output))):
                    fp = open(inputs,'r')
                    try:
                        lyric = fp.read().split('lyric:')[1]
                        # print('----------------------------------------------------------------',lyric, '----------------------------------------------------------------')
                        fp.close()
                        response = client.analyze(lyric)
                        word = response.entities()[0].id
                        # print("word",word)
                        fp = open(state,'x')
                        fp.close()
                        singers = []
                        song_namess = []
                        song_webss = []
                        url = "https://mojim.com/" + word + "/html?t4e"
                        # print(url)
                        resp = requests.get(url, headers=headers)
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        song_names = soup.find_all("span",'mxsh_ss2')
                        # print("song_names",song_names)
                        for song_name in song_names:
                            song_namess.append(song_name.getText())
                        song_lyricses = soup.find_all('span','mxsh_ss3')
                        song_webs = soup.find_all("span","mxsh_ss3")
                        for song_web in song_webs:
                            if(song_web.find("a", href = True)!= None):
                                song = song_web.find("a")
                                rr = requests.get("https://mojim.com" + song.get("href"), headers=headers)
                                song_webss.append("https://mojim.com" + song.get("href"))
                                soup2 = BeautifulSoup(rr.text,"html.parser")
                                singer_w = soup2.find("h1")
                                singer_w = singer_w.getText()
                                singers.append(singer_w)
                                # print(singer_w)
                        output2=output
                        fp = open(output,"w")
                        for i in range(min(10,len(song_namess))):
                            song_name_split = song_namess[i + 1].split(".")[1]
                            # print(str(i + 1) + " " + singers[i] + " " + song_name_split + " " + song_webss[i] + "\n")
                            fp.write(str(i + 1) + " " + singers[i] + " " + song_name_split + " " + song_webss[i] + "\n")
                        fp.close()
                        
                    except:
                        print("output.txt error")
                        continue
    return output2