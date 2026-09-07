from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from monitor import Monitor


def register_json(monitor: Monitor, score: int) -> None:
    """Append a new high-score entry and persist the updated list.

    The function loads the existing high-score list from
    `monitor.config_data.highscore_filename`, appends the supplied entry
    and writes the sorted, truncated list back to disk. The in-memory
    `monitor.height_score` is updated to reflect the saved state.

    Args:
        monitor: Monitor instance providing `config_data` and
            `register_txt` used for the name field.
        score: Integer score to record for the current player.

    Raises:
        Exception: If the high-score file cannot be opened due to
            insufficient permissions or other I/O errors.
    """
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
    """Load the high-score list from the given JSON file.

    Args:
        namefile: Path to the high-score JSON file.

    Returns:
        A list of dictionaries, each containing `name` and `score` keys.

    Raises:
        Exception: If the file exists but cannot be opened due to
            permissions.
    """
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
