from datetime import datetime
from pathlib import Path
import sys
import random
import time
import os
import csv
from colorama import init, Fore, Style

REPO_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = REPO_DIR / "IrregularVerbs" / "IrregularVerbs.txt"
TRACKER_FILE = REPO_DIR / "IrregularVerbs" / "IrregularVerbTracker.txt"

init()  # colorama

# Try to import get_new_count from wordCountAdvanced; fallback to simple constant
try:
    sys.path.insert(0, str(REPO_DIR / "IrregularVerbs"))
    from wordCountAdvanced import get_new_count  # type: ignore
except Exception:
    def get_new_count() -> int:
        # change this value manually if you don't use wordCountAdvanced.py
        return 18

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_name(default="Théodore"):
    newName = input(f"Press Enter if you are {default} otherwise enter your name and press Enter: ").strip()
    return default if newName == "" else newName.capitalize()

def parse_irregulars(max_items: int):
    entries = []
    if not DATA_FILE.exists():
        return entries
    with DATA_FILE.open(encoding="utf-8") as fh:
        reader = csv.reader(fh)
        all_entries = []
        for i, row in enumerate(reader):
            if not row:
                continue
            joined = ",".join(row).strip()
            if joined.startswith("//"):
                continue
            if i == 0 and "infinitiv" in joined.lower():
                continue
            if len(row) < 3:
                continue
            infinitiv = row[0].strip()
            preteritum = row[1].strip().strip('"')
            perfekt = row[2].strip().strip('"')
            all_entries.append((infinitiv, preteritum, perfekt))
    if max_items <= 0:
        return []
    if max_items >= len(all_entries):
        return all_entries
    return all_entries[-max_items:]  # last N entries

def normalize_answers(s: str):
    return s.strip().lower()

def matches(expected: str, given: str) -> bool:
    given_n = normalize_answers(given)
    # split alternatives on / or ;
    alts = []
    for part in expected.replace(';', '/').split('/'):
        part = part.strip().lower()
        if part:
            alts.append(part)
    if not alts:
        alts = [expected.strip().lower()]
    return given_n in alts

def list_this_weeks(entries):
    clear_screen()
    print("\nThis week's irregular verbs (all rows):\n")
    print("Infinitiv | Preteritum | Perfekt particip")
    print("-" * 60)
    for inf, pret, perf in entries:
        print(f"{inf} | {pret} | {perf}")
    print()
    input("Press Enter to return to menu...")

def wordFinder(lottery, entries, wordMemory):
    # ensure unique infinitive in wordMemory, re-roll if duplicate
    if entries[lottery][0] in wordMemory:
        lottery = random.randint(0, len(entries) - 1)
        return wordFinder(lottery, entries, wordMemory)
    return lottery

def run_game(player_name, entries):
    clear_screen()
    init()
    resultTracker = 0.0  # half-point increments
    wordMemory = []
    length = len(entries)
    print(f"\nStarting game for {player_name}. You will be asked for preteritum and perfekt particip for each infinitive.")
    input("Press Enter to begin...")
    start = time.time()
    for i in range(length):
        lottery = wordFinder(random.randint(0, length - 1), entries, wordMemory)
        inf, pret, perf = entries[lottery]
        wordMemory.append(inf)
        clear_screen()
        print(Fore.MAGENTA + inf + Fore.RESET)
        a1 = input("Preteritum: ").strip()
        a2 = input("Perfekt particip: ").strip()
        if matches(pret, a1):
            resultTracker += 0.5
            print("  Preteritum: " + Fore.GREEN + "Correct" + Fore.RESET)
        else:
            print("  Preteritum: " + Fore.RED + "Incorrect" + Fore.RESET + " (expected: " +
                  Fore.CYAN + Style.BRIGHT + pret + Style.NORMAL + Fore.RESET + ")")
        if matches(perf, a2):
            resultTracker += 0.5
            print("  Perfekt particip: " + Fore.GREEN + "Correct" + Fore.RESET)
        else:
            print("  Perfekt particip: " + Fore.RED + "Incorrect" + Fore.RESET + " (expected: " +
                  Fore.CYAN + Style.BRIGHT + perf + Style.NORMAL + Fore.RESET + ")")
        input("Press Enter for next word...")
    end = time.time()
    timeOfPlay = round(end - start, 2)
    clear_screen()
    total_possible = float(length)  # each word can give 1.0 (two halves)
    print(f"\nFinished. Time: {timeOfPlay}s. Score: {resultTracker} out of {total_possible} (half-point increments).")
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TRACKER_FILE.open("a", encoding="utf-8") as tf:
        now = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        tf.write(player_name + "," + now + "," + str(resultTracker) + "," + str(timeOfPlay) + "\n")
    input("Press Enter to return to menu...")
    return resultTracker, timeOfPlay

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
        clear_screen()
        print("\nIrregular Verbs - Menu")
        print("1) Play game")
        print("2) List this week's irregular verbs (all rows)")
        print("3) Quit")
        choice = input("Choose 1, 2 or 3: ").strip()
        if choice == "1":
            player = prompt_name()
            run_game(player, entries.copy())
        elif choice == "2":
            list_this_weeks(entries)
        elif choice == "3":
            clear_screen()
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    menu()