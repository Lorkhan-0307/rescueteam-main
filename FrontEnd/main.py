from youtubecapturepkg import *
from pytube import YouTube

youtubelinklist = []

f = open('ava_v2.2/ava_train_v2.2.csv', 'r')
rdr = csv.reader(f)
for line in rdr:
    if ("www.youtube.com/watch?v=" + line[0] not in youtubelinklist):
        youtubelinklist.append("www.youtube.com/watch?v=" + line[0])

for url in youtubelinklist:
    VideoDownload(url)
    capture_mp4(url.index())
    divide_by_10(url.index())
    delete_temp(url.index())