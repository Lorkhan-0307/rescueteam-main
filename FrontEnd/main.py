import csv
import pafy

youtubelinklist = []

f = open('ava_v2.2/ava_train_v2.2.csv', 'r')
rdr = csv.reader(f)
for line in rdr:
    if("www.youtube.com/watch?v="+line[0] not in youtubelinklist):
        youtubelinklist.append("www.youtube.com/watch?v="+line[0])

print(youtubelinklist)
print(len(youtubelinklist))

for url in youtubelinklist:
    if(pafy.new(url).likes):
        video = pafy.new(url)