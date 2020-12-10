import os

import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt

silence_threshold = 0.01
min_silence_duration = 0.5
min_keep_duration = 0.2


def extract_silence():
    """
    音声トラックから無音部分の時間区間をsで返す
    :return: [{from: int, to: int, suffix: string}[], 長さ]
    """
    src_file = os.path.join("data", "_.wav")
    data, sample_rate = sf.read(src_file)
    # 時刻(s) = 音声データ / 周波数
    t = np.arange(0, len(data)) / sample_rate

    # 無音部分を特定
    silences = []
    prev_is_overed = 0
    entered = 0
    is_overeds = silence_threshold < np.abs(data)
    for i, is_overed in enumerate(is_overeds):
        if prev_is_overed and not is_overed:
            entered = i
        if not prev_is_overed and is_overed:
            duration = (i - entered) / sample_rate
            if min_silence_duration < duration:
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
            if interval < min_keep_duration:
                silence["to"] = silences[i + 1]["to"]
            else:
                masks.append(silence)
                silence = {"from": silences[i + 1]["from"], "to": silences[i + 1]["to"], "suffix": "cut"}
    else:
        masks = silences

    # グラフ表示用の処理
    cut_range = np.zeros(len(data))
    for mask in masks:
        cut_range[mask["from"]:mask["to"]] = silence_threshold
    plt.figure(figsize=(18, 6))
    plt.plot(t, data)
    plt.plot(t, cut_range)
    plt.show()

    for i in range(len(masks)):
        masks[i]["from"] = round(masks[i]["from"] / sample_rate, 3)
        masks[i]["to"] = round(masks[i]["to"] / sample_rate, 3)

    return [masks, max(t)]
