import hashlib
import glob
import ntpath
import functools
import os
from PIL import Image, ExifTags

import matplotlib.pyplot as plt
#import matplotlib.image as mpimg


def file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

#image = Image.open('C:\\Users\\aroczniak\\Dev\\python-dev\\tarball\\data\\pics\\IMG_20191119_123752.jpg')
#exif = {
#    ExifTags.TAGS[k]: v
#    for k, v in image.getexif().items()
#    if k in ExifTags.TAGS
#}

#print(exif)

#print(file_hash("C:\\Users\\aroczniak\\Dev\\python-dev\\tarball\\data\\pics\\a.png"))
#print(file_hash("C:\\Users\\aroczniak\\Dev\\python-dev\\tarball\\data\\pics\\a - Copy.png"))

#print(exif['DateTime'])
#print(exif['ImageLength'])
#print(exif['ImageWidth'])

def split_path(path):
    head, tail = ntpath.split(path)
    if (tail):
        return (head, tail)
    return (ntpath.dirname(head), ntpath.basename(head))

def find_dupes(res, x):
    k, v = x
    if v in res:
        res[v].append(k)
    else:
        res[v] = [k]
    return res

def basic_test(root, *argv):
    roots = {root}.union(set(argv))
    filehashes = map(lambda x: {f:file_hash(f) for f in glob.iglob(x + '**/*', recursive=True)}, roots)
    filenames = functools.reduce(lambda res, x: {**res, **x}, filehashes, {})
    inverted = functools.reduce(find_dupes, filenames.items(), {})
    return [v for k, v in inverted.items() if len(v) > 1]

def gen_plot(data):
    fig = plt.figure()
    rows = len(data)
    cols = functools.reduce(lambda res, x: len(x) if len(x) > res else res, data, 0)
    index = 1
    for i in range(0, rows):
        index = 1 + i * cols
        for j in range(0, len(data[i])): 
            name = data[i][j]
            a = fig.add_subplot(rows, cols, index)
            img = Image.open(name)
            img.thumbnail((100, 100), Image.ANTIALIAS)  # resizes image in-place
            imgplot = plt.imshow(img)
            a.set_title(split_path(name)[1])
            index = index + 1
    plt.show()


def move_file(data):
    for a in data:
        p, n = split_path(a[1])
        os.rename(a[1], "D:\\Andrew\Memo\\photos\\dup\\" + n)
        

#res = basic_test("C:\\Users\\aroczniak\\Dev\\python-dev\\tarball\\data\\pics\\", 
#                "C:\\Users\\aroczniak\\Dev\\python-dev\\tarball\\data\\pics - Copy\\",
#                "C:\\Users\\aroczniak\\Dev\\python-dev\\tarball\\data\\pics - Copy - Copy\\")

res = basic_test("D:\\Andrew\\Memo\\photos\\uploaded\\")
move_file(res)

#gen_plot(res)
