def gen_filter(masks, sound_time, option):
    if option['silence_speed']:
        SILENCE_SPEED_RATE = option['silence_speed']
    base_speed = option['base_speed']
    silence_speed = base_speed * SILENCE_SPEED_RATE
    # TODO: もっとスマートな実装を考える
    txt = ""
    count = 0
    if masks[0]["num_from"] != 0:
        txt += f"[0:v]trim=0:{masks[0]['from']}," \
               f"setpts={1 / base_speed}*(PTS-STARTPTS)[v{count}];"
        txt += f"[0:a]atrim=0:{masks[0]['from']}," \
               f"asetpts=PTS-STARTPTS,atempo={base_speed}[a{count}];"
        count += 1

    for i in range(len(masks) - 1):
        txt += f"[0:v]trim={masks[i]['from']}:{masks[i]['to']}," \
               f"setpts={1 / silence_speed}*(PTS-STARTPTS)[v{count}];"
        txt += f"[0:a]atrim={masks[i]['from']}:{masks[i]['to']}," \
               f"asetpts=PTS-STARTPTS,atempo={silence_speed}[a{count}];"
        count += 1
        txt += f"[0:v]trim={masks[i]['to']}:{masks[i + 1]['from']}," \
               f"setpts={1 / base_speed}*(PTS-STARTPTS)[v{count}];"
        txt += f"[0:a]atrim={masks[i]['to']}:{masks[i + 1]['from']}," \
               f"asetpts=PTS-STARTPTS,atempo={base_speed}[a{count}];"
        count += 1

    txt += f"[0:v]trim={masks[-1]['from']}:{masks[-1]['to']}," \
           f"setpts={1 / silence_speed}*(PTS-STARTPTS)[v{count}];"
    txt += f"[0:a]atrim={masks[-1]['from']}:{masks[-1]['to']}," \
           f"asetpts=PTS-STARTPTS,atempo={silence_speed}[a{count}];"
    count += 1
    if masks[-1]["num_to"] < sound_time:
        txt += f"[0:v]trim={masks[-1]['to']}:{sound_time}," \
               f"setpts={1 / base_speed}*(PTS-STARTPTS)[v{count}];"
        txt += f"[0:a]atrim={masks[-1]['to']}:{sound_time}," \
               f"asetpts=PTS-STARTPTS,atempo={base_speed}[a{count}];"

    for n in range(count + 1):
        txt += f"[v{n}][a{n}]"

    txt += f"concat=n={count + 1}:v=1:a=1"

    return txt
