#!/usr/bin/env python
# encoding: utf-8
#author : wwj718
#2015-12-17 21:03

'''
#任务
切割一段单词朗读文件，得到每个单词的音频文件（mid格式size最小）

#思路：
1.观察波形模式，以图像识别思路识别出word的音频模式（用概率的思路会更捷径）
2.观察波形规律，以切割字符串的方式切割“空白”时间

'''
import sys
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from audio_config import min_silence_len,silence_thresh,keep_silence,filename_prefix


def export_audio(audio_chunk,filename,index=1,audio_format="mp3"):
    audio_chunk.export(filename,format=audio_format)

def split_audio(path_to_file):
    #找到当前目录下的所有MP3，在同级目录下生成
    print u"你选择的参数为\nmin_silence_len : {min_silence_len}\nsilence_thresh : {silence_thresh}\nkeep_silence : {keep_silence}".format(min_silence_len=min_silence_len,silence_thresh=silence_thresh,keep_silence=keep_silence)
    print "*"*20
    #audio_file = sys.argv[1]
    audio_file = path_to_file
    print "正在为你切割{}文件".format((path_to_file))
    myAudio = AudioSegment.from_mp3(path_to_file)
    chunks = split_on_silence(myAudio,
        #保证可切部分的稳定性,是个稳定的背景音
        min_silence_len = min_silence_len,
        # dBFS是什么鬼，好像值越低代表越安静？ 最终的参数是实验得来的魔法数字。-39时正确率100%，猜测这个值接近背景噪音？
        silence_thresh = silence_thresh,
        keep_silence = keep_silence)

    #message
    total_words = len(chunks)
    print "一共将{0}切割为{1}个单词,文件正在生成中，请稍后......".format(audio_file,str(total_words))

    dirname = os.path.dirname(path_to_file)
    basename = os.path.basename(path_to_file)
    prefix = basename.split(".")[0]
    for i, chunk in enumerate(chunks):
        filename = os.path.join(dirname,"{filename_prefix}_w{index}.mp3".format(filename_prefix=prefix,index=str(i).zfill(3)))
        export_audio(chunk,filename,index=i+1)

    print "OK~ 一共生成{total_words}个mp3文件，从{filename_prefix}1.mp3到{filename_prefix}{total_words}.mp3\n".format(total_words=str(total_words),filename_prefix=filename_prefix)

if __name__ == '__main__':
    # python split_audio.py [path]
    begin_path = sys.argv[1]
    for dirname, dirnames, filenames in os.walk(begin_path):
    # print path to all subdirectories first.
        #for subdirname in dirnames:
        #    print os.path.join(dirname, subdirname)
        #print path to all filenames.
        for filename in filenames:
            #print os.path.join(dirname, filename)
            if "mp3" in filename:
                #print os.path.join(dirname, filename)
                split_audio(os.path.join(dirname, filename))

