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
from pydub import AudioSegment
from pydub.silence import split_on_silence
from audio_config import min_silence_len,silence_thresh,keep_silence,filename_prefix


def export_audio(audio_chunk,filename_prefix="unit1_word",index=1,audio_format="mp3"):
    audio_chunk.export("{filename_prefix}{index}.mp3".format(filename_prefix=filename_prefix,index=i), format=audio_format)


if __name__ == '__main__':
    print u"你选择的参数为\nmin_silence_len : {min_silence_len}\nsilence_thresh : {silence_thresh}\nkeep_silence : {keep_silence}\nfilename_prefix : {filename_prefix}".format(min_silence_len=min_silence_len,silence_thresh=silence_thresh,keep_silence=keep_silence,filename_prefix=filename_prefix)
    print "*"*20
    audio_file = sys.argv[1]
    print u"正在为你切割{}文件".format(audio_file)
    myAudio = AudioSegment.from_mp3(audio_file)
    chunks = split_on_silence(myAudio,
        #保证可切部分的稳定性,是个稳定的背景音
        min_silence_len = min_silence_len,
        # dBFS是什么鬼，好像值越低代表越安静？ 最终的参数是实验得来的魔法数字。-39时正确率100%，猜测这个值接近背景噪音？
        silence_thresh = silence_thresh,
        keep_silence = keep_silence)

    #message
    total_words = len(chunks)
    print "一共将{0}切割为{1}个单词,文件正在生成中，请稍后......".format(audio_file,str(total_words))

    for i, chunk in enumerate(chunks):
        export_audio(chunk,filename_prefix=filename_prefix,index=i)

    print "OK~ 一共生成{total_words}个mp3文件，从{filename_prefix}1.mp3到{filename_prefix}{total_words}.mp3\n".format(total_words=str(total_words),filename_prefix=filename_prefix)
