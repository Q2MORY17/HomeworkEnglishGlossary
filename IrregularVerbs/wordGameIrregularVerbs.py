import sys
import random
import time
from datetime import datetime
from pathlib import Path
import csv

REPO_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_DIR / "IrregularVerbs" / "IrregularVerbs.txt"
TRACKER_FILE = REPO_DIR / "IrregularVerbs" / "IrregularVerbTracker.txt"

# Try to import get_new_count from wordCountAdvanced; if not available, fallback to counting lines here
try:
    sys.path.insert(0, str(REPO_DIR / "IrregularVerbs"))
    from wordCountAdvanced import get_new_count  # type: ignore
except Exception:
    def get_new_count(data_file: Path = None) -> int:
        data_path = Path(data_file) if data_file else DATA_FILE
        if not data_path.exists():
            return 0
        count = 0
        with data_path.open(encoding="utf-8") as fh:
            for i, raw in enumerate(fh):
                line = raw.strip()
                if not line:
                    continue
                if line.startswith("//"):
                    continue
                if i == 0 and "infinitiv" in line.lower():
                    continue
                count += 1
        return count

def parse_irregulars(max_items: int):
    entries = []
    if not DATA_FILE.exists():
        return entries
    with DATA_FILE.open(encoding="utf-8") as fh:
        reader = csv.reader(fh)
        for i, row in enumerate(reader):
            if not row:
                continue
            # Skip comment header line if present
            joined = ",".join(row).strip()
            if joined.startswith("//"):
                continue
            if i == 0 and "infinitiv" in joined.lower():
                continue
            # Ensure at least 3 columns; extra commas in fields handled by csv reader
            if len(row) < 3:
                continue
            infinitiv = row[0].strip()
            preteritum = row[1].strip().strip('"')
            perfekt = row[2].strip().strip('"')
            entries.append((infinitiv, preteritum, perfekt))
            if len(entries) >= max_items:
                break
    return entries

def normalize_answers(s: str):
    return s.strip().lower()

def matches(expected: str, given: str) -> bool:
    given_n = normalize_answers(given)
    # expected may contain alternatives separated by '/' or ';'
    alternatives = [alt.strip().lower() for sep in ("/", ";") for alt in expected.split(sep)]
    # also include expected as-is if no split happened
    if not alternatives:
        alternatives = [expected.strip().lower()]
    # remove empty alternatives
    alternatives = [a for a in alternatives if a]
    return given_n in alternatives

def prompt_name(default="Théodore"):
    newName = input(f"Press Enter if you are {default} otherwise enter your name and press Enter: ").strip()
    return default if newName == "" else newName.capitalize()

def list_this_weeks(entries):
    print("\nThis week's irregular verbs:")
    print("Infinitiv | Preteritum | Perfekt particip")
    print("-" * 60)
    for inf, pret, perf in entries:
        print(f"{inf} | {pret} | {perf}")
    print()

def run_game(player_name, entries):
    random.shuffle(entries)
    score = 0.0  # half-point increments: each correct answer = 0.5
    total_possible = len(entries) * 2 * 0.5  # equals number of words * 1.0 (but we'll report as halves)
    print(f"\nStarting game for {player_name}. You will be asked for preteritum and perfekt particip for each infinitive.")
    input("Press Enter to begin...")
    start = time.time()
    for infinitiv, preteritum, perfekt in entries:
        print("\nInfinitive:", infinitiv)
        a1 = input("Preteritum: ").strip()
        a2 = input("Perfekt particip: ").strip()
        if matches(preteritum, a1):
            score += 0.5
            print("  Preteritum: " + "Correct")
        else:
            print("  Preteritum: " + f"Incorrect (expected: {preteritum})")
        if matches(perfekt, a2):
            score += 0.5
            print("  Perfekt particip: " + "Correct")
        else:
            print("  Perfekt particip: " + f"Incorrect (expected: {perfekt})")
    end = time.time()
    elapsed = round(end - start, 2)
    print(f"\nFinished. Time: {elapsed}s. Score: {score} out of {len(entries)*1.0} (half-point increments).")
    # Append to tracker file: name,date,time_seconds,score,total_possible
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TRACKER_FILE.open("a", encoding="utf-8") as tf:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tf.write(f"{player_name},{now},{elapsed},{score},{len(entries)*1.0}\n")
    return score, elapsed

def menu():
    max_words = get_new_count()
    if max_words <= 0:
        print("No irregular verb entries found or get_new_count() returned 0.")
        return
    entries = parse_irregulars(max_words)
    if not entries:
        print("No valid entries parsed from data file.")
        return
    while True:
        print("\nIrregular Verbs - Menu")
        print("1) Play game")
        print("2) List this week's irregular verbs")
        print("3) Quit")
        choice = input("Choose 1, 2 or 3: ").strip()
        if choice == "1":
            player = prompt_name()
            # Make a copy limited to max_words and randomized inside run_game
            selected = entries.copy()
            run_game(player, selected)
        elif choice == "2":
            list_this_weeks(entries)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()