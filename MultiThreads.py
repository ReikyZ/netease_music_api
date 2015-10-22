#coding=utf-8
from time import sleep, ctime 
import threading
import time
import urllib.request
import json
import urllib
import socket
import os
import re

socket.setdefaulttimeout(4)

start = 100000
end   = 105000
threadNum = 4


list = []
for i in range(threadNum):
    list.append(i)


def download(a,b):
    t0 = time.time()
    errorNum = 0#连续错误计数
    file = open('LogError'+str(a)+'.txt','a')
    file = open('LogError'+str(a)+'.txt','r')
    dataFile = open('Database.txt','a')
    lines = file.readlines()

    if len(lines) < 1:
        begin = a

    else:
        lastLine = lines[-1]
        begin = re.findall(r"\d+\.?\d*",lastLine)[0]

    file.close()
    print(begin)
    print('>>>>START at '+ str(begin))

    for i in range(int(begin),b,1):
        try:
            
            resp = urllib.request.Request('http://music.163.com/api/song/detail/?ids=['+str(i)+']', headers = {
                'Connection': 'Keep-Alive',
                'Accept': 'text/html, application/xhtml+xml, */*',
                'Accept-Language': 'zh,zh-TW;q=0.8,en;q=0.6,zh-CN;q=0.4,ja;q=0.2',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
            })
            response = urllib.request.urlopen(resp)
            html = response.read()

            if len(html) > 1000:
                songInfo = " "
                
                timeCur = time.time()
                songJson = html.decode("utf8")
                objJson = json.loads(songJson)
                songInfo = objJson["songs"][0]  #Dic
                
                songName = songInfo['name']
                
                songID = songInfo['id']
                
                songUrl = songInfo['mp3Url']
                
                artist = songInfo['artists'][0]['name']
                
                albumName = songInfo['album']['name']
                
                albumCoverUrl = songInfo['album']['picUrl']
                
                score = songInfo['score']
                

                songInfo=str(songName)+','+str(songID)+','+str(songUrl)+','+str(artist)+','+str(albumName)+','+str(albumCoverUrl)+','+str(score)+','+';'
                dataFile.write('\n'+songInfo)
         

                timeCur = time.time()-timeCur
                print(str(timeCur)[0:4])

                
            else:
                print ("None reslut")

            response.close()
            
                
            if i%50 == 0:
                print ('>>>>>'+str(i)+'<<<<<')
                print (time.strftime("%H:%M:%S"))
                file = open('LogError'+str(a)+'.txt','a')
                file.write('\n'+ time.strftime("%H:%M:%S"))
                file.write('\nFinished at '+str(i))
                file.close();
            fin = i
        except socket.timeout as e: 
                    print(str(a)+"--"+str(b)+"-----socket timout on READ!!!-----timeout at:" + str(i))
                    file = open('LogError'+str(a)+'.txt','a')
                    file.write('\n'+str(i)+' on READ')
                    file.close();
                    
        except urllib.error.URLError as e: 
                    print(str(a)+"--"+str(b)+"-----urlError url:"+ str(i))
                    file = open('LogError'+str(a)+'.txt','a')
                    file.write('\n'+str(i)+' on REQUEST')
                    file.close();

                    errorNum= errorNum+1#被拒绝访问计数
                    while errorNum>3:#连续被超过3次
                        print ("DENY SHUTDOWN at "+time.strftime("%H:%M:%S"))
                        
                        file = open('LogError'+str(a)+'.txt','a')
                        file.write('\n'+ time.strftime("%H:%M:%S"))
                        file.write('\nTimeOut STOP at '+str(i))
                        file.close();
                        songInfo.close()
                        os._exit(0)


                    
    print('>>>>>'+'At'+str(fin)+'<<<<<')
    print('Finished')



def missioner(a,b):
    download(a,b)

def downloadTask(a,b):
    for i in range(a,b):
        print (str(i)+"-------"+str(a))
        time.sleep(1)


length = int((end-start)/len(list))

files = range(len(list))



threads = []
#创建线程
for i in files:
    #t = threading.Thread(target=player,args=(list[i],))
    t = threading.Thread(target=missioner,args=(list[i]*length+start,list[i]*length+length+start,))
    #t = threading.Thread(target=downloadTask(20*(i),30*(i)))
    threads.append(t)
if __name__ == '__main__': 
    #启动线程
    for i in files:
        threads[i].start()
        time.sleep(1)

    for i in files:
        threads[i].join()
        #主线程
    print ('ALL FINISHED: ' + time.strftime("%H:%M:%S"))
