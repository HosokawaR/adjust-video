import sys
import subprocess
from time import time
from extract_silence import extract_silence
from get_filter import gen_filter


def conv(file_name):
    cmd = f"ffmpeg -i data/{file_name} -ac 1 -ar 44100 -acodec pcm_s16le data/_.wav"
    res = subprocess.call(cmd.split(' '))
    print(res)
    masks, sound_time = extract_silence()
    # subprocessで渡す場合はfilter_complexの"は必要ない
    cmd = f"ffmpeg -i data/{file_name} -filter_complex "
    cmd += gen_filter(masks, sound_time)
    cmd += f" -preset superfast -profile:v baseline data/output_{time()}.mp4"
    res = subprocess.call(cmd.split(' '))
    print(res)
    res = subprocess.call('rm data/_.wav'.split(' '))


if __name__ == '__main__':
    args = sys.argv
    if 1 < len(args):
        conv(args[1])
    else:
        print("動画の名前を記述して下さい。ex) test.mp4")
