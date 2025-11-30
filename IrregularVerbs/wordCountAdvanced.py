import json
import subprocess
from datetime import datetime
from pathlib import Path
import argparse

REPO_ROOT = Path(__file__).resolve().parents[1]  # repo root (one level above scripts/)
DEFAULT_DATA = REPO_ROOT / "IrregularVerbs" / "IrregularVerbs.txt"
DEFAULT_STATE = REPO_ROOT / ".irregular_verbs_state.json"

def count_entries(data_path: Path) -> int:
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    count = 0
    with data_path.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            if line.startswith("//"):
                continue
            if i == 0 and "infinitiv" in line.lower():  # header line
                continue
            count += 1
    return count

def load_state(state_path: Path):
    if not state_path.exists():
        return {"count": None, "last_diff": None, "updated": None}
    return json.loads(state_path.read_text(encoding="utf-8"))

def save_state(state_path: Path, count: int, diff: int):
    state = {"count": count, "last_diff": diff, "updated": datetime.utcnow().isoformat() + "Z"}
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state

def git_add(path: Path):
    subprocess.run(["git", "add", str(path)], check=False)

def main(args):
    data_file = Path(args.data_file) if args.data_file else DEFAULT_DATA
    state_file = Path(args.state_file) if args.state_file else DEFAULT_STATE

    new_count = count_entries(data_file)
    state = load_state(state_file)
    old_count = state.get("count")

    if old_count is None:
        diff = new_count
    else:
        diff = new_count - old_count

    if old_count != new_count:
        save_state(state_file, new_count, diff)
        print(f"Updated count: {new_count} (diff {diff})")
        if args.git_add:
            # run git add from repo root
            subprocess.run(["git", "add", str(state_file)], cwd=REPO_ROOT, check=False)
            print(f"Staged {state_file.name} for commit")
    else:
        print(f"No change in count ({new_count})")

NEW_COUNT = 18  # <-- manually change this number to the desired max words

def get_new_count() -> int:
    """Return the manually configured count of irregular verb entries."""
    return int(NEW_COUNT)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Count irregular verbs and record diff vs previous run.")
    p.add_argument("--data-file", help="Path to IrregularVerbs.txt")
    p.add_argument("--state-file", help="Path to state file to read/write")
    p.add_argument("--git-add", action="store_true", help="Run `git add` on the updated state file (useful in pre-commit)")
    args = p.parse_args()
    main(args)