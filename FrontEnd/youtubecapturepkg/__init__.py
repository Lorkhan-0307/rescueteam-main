import csv
from pytube import YouTube
import cv2
import os
from pytube import YouTube
from PIL import Image
from tqdm import tqdm
import cv2, os, pathlib, glob, shutil

def VideoDownload():
    youtubelinklist = []

    f = open('ava_v2.2/ava_train_v2.2.csv', 'r')
    rdr = csv.reader(f)
    for line in rdr:
        if ("www.youtube.com/watch?v=" + line[0] not in youtubelinklist):
            youtubelinklist.append("www.youtube.com/watch?v=" + line[0])

    print(youtubelinklist)
    print(len(youtubelinklist))
    ncount = 0

    for url in youtubelinklist:
        try:
            video = YouTube(url)
            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
            os.rename(video.streams.first().default_filename, '%s.mp4'%url.index())
            print('Download is finished.')
            return
        except:
            continue

    print(ncount)


def capture_mp4():
    folder = '.\\temp_yt_capture\\'
    cap = cv2.VideoCapture('yt_temp.mp4')
    if not os.path.isdir(folder):
        os.mkdir(folder)

    interval = 1  # 몇 초 간격으로 캡쳐를 할지 결정합니다.
    success = True
    count = 0
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count / fps) + 1
    fill_zero = len(str(duration))

    progress = ['-', '/', '|', '\\']
    print('Capture :  ', end='')
    while success:
        success, image = cap.read()
        if count % (interval * fps) == 0:
            second = str(int(count / fps)).zfill(fill_zero)
            prefix = 'temp_'
            extension = '.jpg'
            filename = prefix + second + extension
            cv2.imwrite(folder + filename, image)
        print('\b' + progress[count % 4], end='')
        count += 1

    list = []
    for path, subdirs, files in os.walk(folder):
        for name in files:
            list.append(os.path.join(path, name))

    ext_list = ['.jpg']
    for file in list:
        if os.path.getsize(file) == 0:
            if any(ext.lower() in pathlib.Path(file).suffix.lower() for ext in ext_list):
                print('\nDeleted file(s) : ', file)
                os.remove(file)

    cap.release()
    cv2.destroyAllWindows()
    return


### 다운받은 영상을 merge합니다. ###
def img_merge(list_img, number, total_number):
    images = map(Image.open, list_img)
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    total_height = sum(heights) + (len(list_img) - 1) * 50

    new_im = Image.new('RGB', (max_width, total_height), (255, 255, 255))
    images = map(Image.open, list_img)
    y = 0
    for im in images:
        x = int((max_width - im.size[0]) / 2)
        new_im.paste(im, (x, y))
        y += im.size[1] + 50
    new_im.save('result' + str(number).zfill(len(str(total_number))) + '.jpg', quality=95)
    return


### 사진을 10장씩 묶습니다. ###
def divide_by_10():
    list_jpg = glob.glob('.\\temp_yt_capture\\*.jpg')
    list_jpg.sort()
    cuts = len(list_jpg) // 10 + 1 if len(list_jpg) / 10 != len(list_jpg) // 10 else len(list_jpg) // 10
    print('\nMerge : ')
    for i in tqdm(range(0, cuts)):
        temp_list = list_jpg[i * 10: (i + 1) * 10]
        img_merge(temp_list, i + 1, cuts)
    return


### 임시파일을 삭제합니다. ###
def delete_temp():
    os.remove('yt_temp.mp4')
    shutil.rmtree('.\\temp_yt_capture\\')
    return


if __name__ == '__main__':
    VideoDownload()
    capture_mp4()
    divide_by_10()
    delete_temp()