import json


def register_json(monitor: Monitor, score: int) -> None:
    try:
        with open("score.json", "r") as files:
            dic_score = json.load(files)
    except Exception:
        with open("score.json", "w") as files:
            dic_score = []
    dic_score.append({"name": monitor.register_txt, "score": score})
    dic_score = sorted(dic_score, key=lambda x: x["score"],
                       reverse=True)
    if len(dic_score) > 10:
        dic_score.pop()
    with open("score.json", "w") as files:
        json.dump(dic_score, files, indent="\t")
    monitor.height_score = dic_score


def takeHeightScore(namefile):
    try:
        with open(namefile, "r") as files:
            dic_score = json.load(files)
    except Exception:
        with open(namefile, "w") as files:
            dic_score = []
    return dic_score
