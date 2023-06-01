from flask import Flask
app = Flask(__name__)

from flask import request, abort,session
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction
# public module
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
import jsonify
from ShazamAPI import Shazam
import os
from pytube import Search
from pytube import YouTube
import shutil
from fileinput import filename
import json
from datetime import datetime
from datetime import timedelta
import time
import librosa
import pathlib
import random 
import shutil
from lyricsearch import lyricsSearch
from flask import Flask, g, flash, url_for, redirect,  render_template, request, session, abort, redirect
# from flask_login import LoginManager, UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import os
import requests
from bs4 import BeautifulSoup
import librosa
import sys
import codecs
import os
import textrazor
from melodysearch import melodySearch
import time
 

# solve login status
app = Flask(__name__)
 
 
SRC_PATH =  pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads')
ALLOWED_EXTENSIONS = {'mp3','wav'}
# TODO: Change your key
line_bot_api = LineBotApi('你的 CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('你的 CHANNEL_SECRET')
ngrok_link='你的對外IP'
app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER          # 設置儲存上傳檔的資料夾 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024  * 1024 * 1024 # 上傳檔最大16GB
userID=''
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in  ALLOWED_EXTENSIONS

def send_response_to_line_bot(user_id, message,filedir):
    ryric=''
    info=[]
    cnt=0
    f = open(filedir,'r')  
    for line in f.readlines():
        cnt+=1
        # print('--------',cnt,'---------')
        if(cnt>=4):
            ryric+=str(line)
        info.append(line)
    # print('--------',ryric)
    # print('--------',info)
    f.close
    picUrl=str(info[2])
    title=str(info[0])
    title=title[11:len(title)-1]
    link=picUrl[6:len(picUrl)-1]
    message = TemplateSendMessage(
        alt_text='按鈕樣板',
        template=ButtonsTemplate(
            thumbnail_image_url=link,  #顯示的圖片
            title=title,  #主標題
            text=info[1],  #副標題
            actions=[
                MessageTemplateAction(  #顯示文字計息
                    label="以歌詞推薦",
                    text="@以歌詞推薦"
                ),
                MessageTemplateAction(  #顯示文字計息
                    label="以曲風推薦",
                    text='@以曲風推薦'
                ),
                PostbackTemplateAction(
                            label='查看完整歌詞',
                            data=f'!歌詞{filedir}'
                ),
                    
            ]
        )
    )
    line_bot_api.push_message(user_id, message)
    # except:
    #     line_bot_api.push_message(user_id, TextSendMessage(text='發生錯誤!'))
def history(userID):
    singer=[]
    song=[]
    melody=[]
    lyrics=[]
    picUrl=[]
    url=''
    output_path=[]
    path='share\\'+userID+'\\'
    obj = os.scandir(path)
    for entry in obj :
        cnt=0
        me=''
        ly=''
        info = path + entry.name + '\\output.txt'
        print(info)
        if(os.path.isfile(info)):
            output_path.append(info)
            with open(info, "r") as file:
                for line in file:
                    if(cnt==0):
                        song.append(line.strip())
                    if(cnt==1):
                        singer.append(line.strip())
                    if(cnt==2):
                        url=line.strip()
                        picUrl.append(url[6:len(url)])
                    cnt+=1
            file.close
        output_me = path + entry.name + '\\outputmelody.txt'
        if(not (os.path.isfile(output_me))):
           melodySearch(userID)

        cnt=0
        with open(output_me, "r") as file:
            for line in file:
                cnt+=1
                me+=line.strip()+'\n'
                if(cnt>2):
                    break
            melody.append(me)
        file.close 
        
            
        
        output_ly = path + entry.name + '/outputlyric.txt'
        if(not(os.path.isfile(output_ly))):
            lyricsSearch(userID)
        cnt=0
        with open(output_ly, "r") as file:
            for line in file:
                if(cnt>2):
                    break
                ly+=line.strip()+'\n'
                cnt+=1
            lyrics.append(ly)   
        file.close
       
    # print(song,singer,picUrl,url)
    return singer,song,melody,lyrics,picUrl,output_path     
def detect_song(path):
    # path = 'share'
    obj = os.scandir(path)
    print('---------------',path,'--------------------------------')
    print("Files and Directories in '% s':" % path)
    for entry in obj :
        if entry.name != "songs":  
            print(entry.name)
            state = path + entry.name + '\\computing'
            output = path + entry.name + '\\output.txt'
            inputfile = path + entry.name + '\\input.mp3'
            print("--------state",state)
            print("--------output",output)
            print("--------input",inputfile)
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
                    s = Search(t[1]['track']['title']+' '+t[1]['track']['subtitle'])
                    v = s.results
                    download_state = False
                    for tmp in v:
                        print(tmp.title)
                        yt = YouTube(tmp.watch_url)
                        target_path = path + entry.name
                        sname = 'song.mp3'
                        try:
                            yt.streams.filter().get_audio_only().download(filename = sname, output_path = target_path)
                            download_state = True
                            break
                        except:
                            continue
                    if download_state:
                        data_path = "share\\songs\\" + t[1]['track']['title']+'_'+t[1]['track']['subtitle']+'.mp3'
                        shutil.copyfile(target_path + '\\song.mp3',data_path)
                        break
                    else:
                        print('can not download')
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    global userID
    userID = event.source.user_id
    # session['UserId'] = event.source.user_id
    # profile = line_bot_api.get_profile(UserId)
    # print(profile)
    singer=[]
    song=[]
    melody=[]
    lyrics=[]
    # postback_data = event.message.text
    picUrl=[]
    output_path=[]
    if mtext == '@上傳檔案':
        try:
            # TODO: here
            message = TextSendMessage(  
                # text = f'https://ab2c-123-195-0-149.ngrok-free.app/user.html/{userID}'
                text=f'{ngrok_link}/user.html/{userID}'
                
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
    elif mtext == '@傳送圖片':
        try:
            message = ImageSendMessage(
                original_content_url = "https://i.imgur.com/4QfKuz1.png",
                preview_image_url = "https://i.imgur.com/4QfKuz1.png"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@以歌詞推薦':
        lyrics_path=lyricsSearch(userID)
        content = ""
        print('ly',lyrics_path,'--------------------------------')
        with open(lyrics_path, "r") as file:
            for line in file:
                content += line.strip()+'\n'

        print(content)

        message = TextSendMessage(  
            text = content
        )
        line_bot_api.reply_message(event.reply_token,message)
        # except:
            # line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif mtext == '@以曲風推薦':
            try:
                me_path=melodySearch(userID)
                content = ""

                with open(me_path, "r") as file:
                    for line in file:
                        content += line.strip()+'\n'

                print(content)

                message = TextSendMessage(  
                    text = content
                )
                line_bot_api.reply_message(event.reply_token,message)
            except:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
     
    elif mtext =='!help':
        try:
            # TODO: here
            message = TextSendMessage(  
                text = "我們提供以下功能\n1.@上傳檔案(也可以點擊左下角icon)將會回傳一個link給你請點擊此link到該網站上傳mp3檔案上傳完成後系統會幫你辨識歌曲此外也可以根據曲風或歌詞推薦歌給你\n2.@歷史紀錄(也可以點擊右下方icon)我們將會顯示你過往上傳的mp3並讓你可以選擇\n3.@以曲風推薦(點擊card button)會推薦曲風相似的歌曲\n4.@以歌詞推薦(點擊card button)會推薦歌詞相似的歌曲\n5.提供完整歌詞"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif mtext == '@傳送位置':
        try:
            message = LocationSendMessage(
                title='101大樓',
                address='台北市信義路五段7號',
                latitude=25.034207,  #緯度
                longitude=121.564590  #經度
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    if mtext == '@歷史紀錄':
            singer, song, melody, lyrics, picUrl, output_path = history(userID)
            columns = []
            print(singer,song,melody,lyrics,picUrl)
            for i in range(len(song)):
                columns.append(CarouselColumn(
                    thumbnail_image_url=picUrl[i],
                    title=song[i],
                    text=singer[i],
                    actions=[
                        PostbackTemplateAction(
                            label='以曲風推薦',
                            data=melody[i]
                        ),
                        PostbackTemplateAction(
                            label='以歌詞推薦',
                            data=lyrics[i]
                        ),
                        PostbackTemplateAction(
                            label='查看完整歌詞',
                            data=f'!歌詞{output_path[i]}'
                        ),
                         
                    ]
                ))

            message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=columns
                )
            )

            line_bot_api.reply_message(event.reply_token,message)
    
        # except:
            # line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

@handler.add(PostbackEvent)
def handle_postback(event):
    lyrics=''
    cnt=0
    postback_data = event.postback.data
    if '!歌詞' in postback_data:
        filename=postback_data[3:]
        f = open(filename,'r')  
        for line in f.readlines():
            cnt+=1
            # print('--------',cnt,'---------')
            if(cnt>=4):
                lyrics+=str(line)
        f.close
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=lyrics)
        )
    elif postback_data:
        reply_message = postback_data

        # 回應訊息給使用者
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
@app.route("/user.html/<user_id>",methods=['GET'])
def user(user_id):
    # username = current_user.get_id()
    with open("log.txt", "a") as file4:
        file4.write(str(user_id) + "\n")  # 將變數寫入檔案
    return render_template('user.html',user=user_id )
@app.route('/user.html', methods=['POST','GET'])
def upload_file():
    root=''
    info=[]
    filename=''
    
    user_id = request.form.get('name')
    
    with open("log.txt", "a") as file4:
        file4.write(str(user_id) + "\n")  # 將變數寫入檔案
    if 'filename' not in request.files:   # 如果表單的「檔案」欄位沒有'filename'
        flash('沒有上傳檔案')
        # return redirect(url_for('index'))

    file = request.files['filename']    # 取得上傳的檔案 
    if file.filename == '':           #  若上傳的檔名是空白的… 
        flash('請選擇要上傳的影像')   # 發出快閃訊息 
        
    if file and allowed_file(file.filename):   # 確認有檔案且副檔名在允許之列
        
        t=time.time()
        r=random.randrange(0, 101, 2)
   
        filepath=f'share/{user_id}/' + str(t)  +str(r)
        print('----------------------------',user_id,'----------------')
        with open("log.txt", "a") as file4:
            file4.write(str(user_id) + "\n")  # 將變數寫入檔案
        os.makedirs(filepath ,exist_ok=True)
        file.save(os.path.join(filepath, 'input.mp3'))
        
        info.clear()
        ryric=''
        filedir=filepath+'/output.txt'
        filename = 'output.txt'
        os.chmod(filepath, 0o777)
        os.chmod(filepath+'/input.mp3', 0o777)
        while(1):
            if(os.path.isfile(filepath +'/input.mp3')):
                break
            if not os.path.isdir(filepath):
                return render_template('index.html')
         
        detect_song(f'share\\{user_id}\\')
        flash('檔案上傳完畢！')
        while(1):
            if(os.path.isfile(filepath+'/output.txt')):
                break
        send_response_to_line_bot(user_id,'檔案上傳已完成',filedir=os.path.join(filepath, 'output.txt'))
        
        return render_template('user.html', filename=userID )
        # return render_template('user.html', user=username,filename=filename,name=data,songname=filedir,song=data,link=data)
    else:
        errorMsg='<i class="bi bi-exclamation-triangle-fill"></i> 僅允許上傳mp3、mov影像檔'
        return render_template('user.html',errorMsg=errorMsg)  # 令瀏覽器跳回首頁
if __name__ == '__main__':
    app.run(debug=True)
