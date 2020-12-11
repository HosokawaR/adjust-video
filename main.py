import argparse
import os
import subprocess
from time import time

from extract_silence import extract_silence
from get_filter import gen_filter


def conv(file_path, option):
    subprocess.call('rm data/_.wav'.split(' '))
    masks, sound_time = extract_silence(file_path)
    # subprocessで渡す場合はfilter_complexの"は必要ない
    cmd = f"ffmpeg -i {file_path} -filter_complex "
    cmd += gen_filter(masks, sound_time, option)
    print(gen_filter(masks, sound_time, option).replace(';', '\n'))
    cmd += f" -preset superfast -profile:v baseline " \
           f"data/output_{os.path.basename(file_path)}_{time()}.mp4"
    subprocess.call(cmd.split(' '))
    subprocess.call('rm data/_.wav'.split(' '))
    print("出力完了！")


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')

    parser = argparse.ArgumentParser(
        prog='main.py',
        usage='python main.py -i [変換したい動画への相対パス] [オプション]',
        epilog='data/output_[変換元動画名]_[タイムスタンプ] に変換した動画が出力されます。'
               '詳しくは、https://github.com/HosokawaR/adjust-video を見てくれるとなにか分かったり分からなかったりするかも。',
        add_help=True,
    )
    parser.add_argument('-i', '--input', help="処理したい動画への相対パスを入力")
    parser.add_argument('-ss', '--silence-speed', help="遊音部分に対する無音部分の速度倍数を指定 ex) 4", type=float)
    parser.add_argument('-bs', '--base-speed', help="動画全体の速度倍数を指定 ex) 1.5", type=float, default=1.0)
    args = parser.parse_args()
    if args.input:
        conv(args.input, {
            'silence_speed': args.silence_speed,
            'base_speed': args.base_speed
        })
    else:
        conv('data/4.mp4')
        print("動画のパスを記入して下さい。ex) data/test.mp4")
