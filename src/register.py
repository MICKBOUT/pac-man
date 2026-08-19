from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from monitor import Monitor


def register_json(monitor: Monitor, score: int) -> None:
    try:
        with open(monitor.config_data.highscore_filename, "r") as files:
            dic_score = json.load(files)
    except PermissionError:
        raise Exception("Can't open file "
                        f"{monitor.config_data.highscore_filename}")
    except Exception:
        with open(monitor.config_data.highscore_filename, "w") as files:
            dic_score = []
    dic_score.append({"name": monitor.register_txt, "score": score})
    dic_score = sorted(dic_score, key=lambda x: x["score"], reverse=True)
    if len(dic_score) > 10:
        dic_score.pop()
    with open(monitor.config_data.highscore_filename, "w") as files:
        json.dump(dic_score, files, indent="\t")
    monitor.height_score = dic_score


def takeHeightScore(namefile: str) -> list[dict[str, int]]:
    dic_score = []
    try:
        with open(namefile, "r") as files:
            dic_score = json.load(files)
    except PermissionError:
        raise Exception("Can't open file "
                        f"{namefile}")
    except Exception:
        with open(namefile, "w") as files:
            pass
    return dic_score
