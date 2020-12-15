import subprocess
from datetime import datetime

import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt

from settings import MIN_NOISE_DURATION, MIN_PADDING_DURATION, MIN_SILENCE_DURATION


def extract_silence(file_path, option):
    """
    音声トラックから無音部分の時間区間をsで返す
    :return: [{from: int, to: int, suffix: string}[], 長さ]
    """

    cmd = f"ffmpeg -i {file_path} -ac 1 -ar 44100 -acodec pcm_s16le data/_.wav"
    subprocess.call(cmd.split(' '))
    data, sample_rate = sf.read("data/_.wav")
    # 時刻(s) = 音声データ / 周波数
    t = np.arange(0, len(data)) / sample_rate

    # 無音部分を特定
    silences = []
    prev_is_overed = 0
    entered = 0
    silence_threshold = max(data) * option['silence_threshold_rate']
    is_overeds = silence_threshold < np.abs(data)
    for i, is_overed in enumerate(is_overeds):
        if prev_is_overed and not is_overed:
            entered = i
        if not prev_is_overed and is_overed:
            duration = (i - entered) / sample_rate
            if MIN_SILENCE_DURATION < duration:
                silences.append({"from": entered, "to": i, "suffix": "cut"})
                entered = 0
        prev_is_overed = is_overed

    if 0 < entered < len(data):
        silences.append({"from": entered, "to": len(data), "suffix": "cut"})

    # 無音区間の間隔が短い場合は、一つの無音区間として扱う。
    cut_blocks = []
    masks = []
    if len(silences) > 1:
        silence = {"from": silences[0]["from"], "to": silences[0]["to"], "suffix": "cut"}
        for i in range(len(silences) - 1):
            interval = (silences[i + 1]["from"] - silences[i]["to"]) / sample_rate
            if interval < MIN_NOISE_DURATION * 2:
                silence["to"] = silences[i + 1]["to"]
            else:
                masks.append(silence)
                silence = {"from": silences[i + 1]["from"], "to": silences[i + 1]["to"], "suffix": "cut"}
    else:
        masks = silences

    # 無音の前後に処理しない余白を追加
    for i in range(len(masks)):
        masks[i]["from"] += int(MIN_PADDING_DURATION * sample_rate)
        masks[i]["to"] -= int(MIN_PADDING_DURATION * sample_rate)

    # グラフ表示用の処理
    cut_range = np.zeros(len(data))
    for mask in masks:
        cut_range[mask["from"]:mask["to"]] = silence_threshold
    plt.figure(figsize=(18, 6))
    plt.plot(t, data)
    plt.plot(t, cut_range)
    plt.title(file_path + ' ' + datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    plt.show()

    for i in range(len(masks)):
        masks[i]["num_from"] = round(masks[i]["from"] / sample_rate, 3)
        masks[i]["num_to"] = round(masks[i]["to"] / sample_rate, 3)
        masks[i]["from"] = masks[i]["num_from"]
        masks[i]["to"] = masks[i]["num_to"]

    return [masks, max(t)]
