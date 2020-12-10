import os
import subprocess
import sys
from time import time

from extract_silence import extract_silence
from get_filter import gen_filter


def conv(file_path):
    masks, sound_time = extract_silence(file_path)
    # subprocessで渡す場合はfilter_complexの"は必要ない
    cmd = f"ffmpeg -i {file_path} -filter_complex "
    cmd += gen_filter(masks, sound_time)
    print(gen_filter(masks, sound_time).replace(';', '\n'))
    cmd += f" -preset superfast -profile:v baseline " \
           f"data/output_{os.path.basename(file_path)}_{time()}.mp4"
    subprocess.call(cmd.split(' '))
    subprocess.call('rm data/_.wav'.split(' '))
    print("出力完了！")


if __name__ == '__main__':
    args = sys.argv
    if 1 < len(args):
        conv(args[1])
    else:
        conv('data/3.mp4')
        print("動画のパスを記入して下さい。ex) data/test.mp4")
