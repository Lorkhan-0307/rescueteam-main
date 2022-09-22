from youtubecapturepkg import *
from time import sleep

youtubelinklist = []
templist = []

f = open('ava_v2.2/ava_train_v2.2.csv', 'r')
rdr = csv.reader(f)
tempUrl = ''
low = 0
high = 0
index = -1
for line in rdr:
    if (line[0] not in templist):
        index += 1
        print("%ding"%index)
        low = line[1]
        high = line[1]
        youtubelinklist.append([line[0],low,high])
        templist.append(line[0])
        tempUrl = line[0]
    elif tempUrl == line[0]:
        if(youtubelinklist[index][1] >= line[1]):
            youtubelinklist[index][1] = line[1]
        elif(youtubelinklist[index][2] <= line[1]):
            youtubelinklist[index][2] = line[1]


for idx, url in enumerate(templist):

    sleep(1)
    try:
        # video_name = YouTube("https://www.youtube.com/watch?v="+url).streams.first().default_filename
        VideoDownload(url)
        print(f'\nDownload {idx} is finished.')
        sleep(1)
        capture_mp4(url,idx,youtubelinklist[idx][1],youtubelinklist[idx][2])
        print(f"\nCapture {idx} Done")
        # divide_by_10(idx)
        sleep(1)
    except:
        print(f"\n{idx} Failed")
        sleep(1)
    try:
        delete_temp(idx)
    except:
        print(f"\n{idx}Delete failed.")

