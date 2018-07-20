# -*- coding: utf-8 -*-
"""
    This is a modified version of the original script made by Guanghan Ning 
    This script is designed to convert txt annotation files to appropriate format needed by YOLO. 
    I do not take credit for any of the original work, only the modifications.
   @author: Guanghan Ning
    Email: gnxr9@mail.missouri.edu
   
   This script contains a process to delete .DS_Store files for mac and is already configured for the drone datasets. 
    
    """

import os
from os import walk, getcwd
from PIL import Image

classes = ["001", "002", "003", "010", "006", "007", "008", "009", "120"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


"""-------------------------------------------------------------------"""
cls = "001"

""" Configure Paths"""
mypath = "Labels/001/"
outpath = "Images/001/"

if cls not in classes:
    print "Class not found in classes"
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()
list_file = open('%s/%s_list.txt'%(wd, cls), 'w')

#Delete .DS_Store file
DS_file=str('%s/%s/.DS_Store'%(wd,mypath))
if os.path.isfile(DS_file):
    os.remove(DS_file)
    print "DS_Store file removed"
else:
    print "No DS_Store to remove at", DS_file

print "wd:", wd, "   cls_id:", cls_id, "DS file path:", DS_file

if os.path.isfile(DS_file):
    os.remove(DS_file)
    print "Its still in there"



""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")
    
    """ Open input text files """
    txt_path = mypath + txt_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\n')   #for ubuntu, use "\r\n" instead of "\n"
    
    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "w")
    
    
    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        #print('lenth of line is: ')
        #print(len(line))
        #print('\n')
        if(len(line) >= 2):
            ct = ct + 1
            print(line + "\n")
            elems = line.split(' ')
            print(elems)
            xmin = elems[0]
            xmax = elems[2]
            ymin = elems[1]
            ymax = elems[3]
            #
            img_path = str('Images/%s/%s.JPEG'%(cls, os.path.splitext(txt_name)[0]))
            #t = magic.from_file(img_path)
            #wh= re.search('(\d+) x (\d+)', t).groups()
            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])
            #w = int(xmax) - int(xmin)
            #h = int(ymax) - int(ymin)
            # print(xmin)
            print(w, h)
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w,h), b)
            print(bb)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('Images/%s/%s.JPEG\n'%(cls, os.path.splitext(txt_name)[0]))

list_file.close()
