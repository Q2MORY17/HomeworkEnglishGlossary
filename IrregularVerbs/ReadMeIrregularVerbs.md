# WordGameIrregularVerbs

Simple command-line quiz that tests knowledge of irregular verbs.

## What it does
- Reads verbs from `IrregularVerbs/IrregularVerbs.txt` (CSV-like: `infinitiv,preteritum,perfekt particip`).
- Limits the number of words to the value returned by `get_new_count()` from `wordCountAdvanced.py`. If that module is missing, the script falls back to a local line-count routine.
- Presents a menu:
  1. Play the game (enter player name or press Enter to use "Théodore").
  2. List this week's irregular verbs (infinitives only).
  3. Quit.
- In the game each displayed infinitive requires two answers: preteritum and perfekt particip.
- Order is randomized and the same word will not appear twice in a single run.
- Scoring: each correct answer = 0.5 points (so each word can yield up to 1.0). Final score is reported and written to the tracker file.

## Files used
- Data file: `IrregularVerbs/IrregularVerbs.txt`  
  - Accepts an optional header line (e.g. `infinitiv,preteritum,perfekt particip`) and comment lines starting with `//`.
  - Fields may contain alternatives separated by `/` or `;` (the script will accept any alternative).
- Tracker file: `IrregularVerbs/IrregularVerbTracker.txt`  
  - Appends a CSV line per play: `player_name,YYYY-MM-DD HH:MM:SS,elapsed_seconds,score,total_possible`

## Matching rules
- Case-insensitive comparison.
- Whitespace is trimmed.
- Alternatives in expected answers are split on `/` and `;`.

## Requirements
- Python 3.x (no external packages required for the core script; uses only stdlib `csv`, `random`, `time`, `pathlib`, `datetime`).
- If you want `get_new_count()` from `wordCountAdvanced.py` to be used, keep that file in `IrregularVerbs/` and ensure it is importable.

## How to run
1. Open a terminal in the repository root (or the `IrregularVerbs` folder).
2. (Optional) Activate your virtual environment.
3. Run:
   ```sh
   python IrregularVerbs/WordGameIrregularVerbs.py
   ```
4. Use the menu to play or list verbs.

## Troubleshooting
- If the script reports "No irregular verb entries found":
  - Verify `IrregularVerbs/IrregularVerbs.txt` exists and is readable.
  - Ensure the file has valid lines (non-empty, at least 3 columns).
  - Check `wordCountAdvanced.py` if you rely on it — the fallback will still count entries if that module is absent.
- If answers with multiple valid forms are used in the data file, separate them with `/` or `;`.

## Notes
- The script appends results to `IrregularVerbTracker.txt`. Ensure you have write permission.
- The "max words" limit comes from `get_new_count()` — useful for weekly subsets.

# wordCountAdvanced.py — README

Purpose
- Count the number of irregular-verb entries in IrregularVerbs/IrregularVerbs.txt.
- Persist the last count and the diff versus the previous count to a JSON state file.
- Optionally stage the updated state file for commit (useful in a pre-commit hook).

Where files live (defaults)
- Data file: IrregularVerbs/IrregularVerbs.txt
- State file: .irregular_verbs_state.json (repo root)
These defaults are defined by DEFAULT_DATA and DEFAULT_STATE in the script.

How it works (high level)
1. count_entries(path) reads the data file, ignores blank lines, header (first line containing "infinitiv") and comment lines that start with `//`, and returns the number of valid entries.
2. load_state(path) loads the JSON state if present; otherwise returns an initial empty state.
3. save_state(path, count, diff) writes { "count": count, "last_diff": diff, "updated": ISO_TIMESTAMP } to the state file.
4. main(args) computes new_count, compares it to the stored count, computes diff, writes the updated state when counts differ, and (optionally) runs `git add` on the state file if `--git-add` is passed.
5. get_new_count() is provided as a small importable helper that returns the current count (so other scripts can limit behavior based on the number of entries).

Public functions to reuse
- get_new_count(data_file: Path|str = None) -> int
  - Returns the counted number of entries (uses DEFAULT_DATA when no argument is given).
- count_entries(data_path: Path) -> int
  - Low-level counter; can be reused for custom file paths.

CLI usage
- Run manually:
  - python IrregularVerbs\wordCountAdvanced.py
- With custom paths / staging:
  - python IrregularVerbs\wordCountAdvanced.py --data-file path\to\IrregularVerbs.txt --state-file .my_state.json --git-add

State file format
- JSON with fields:
  - count: integer (current total entries)
  - last_diff: integer (new_count - previous_count)
  - updated: ISO 8601 UTC string

Integration with git (recommended pre-commit)
- Add a pre-commit hook that runs the script and stages the state file, so commits that change the data file will automatically update and include the state file:
  - .git/hooks/pre-commit (example):
    ```sh
    #!/bin/sh
    python IrregularVerbs/wordCountAdvanced.py --git-add
    ```
  - Make it executable (Git Bash / WSL): chmod +x .git/hooks/pre-commit

Error handling & notes
- If the data file is missing, count_entries raises FileNotFoundError (or get_new_count returns 0 in the provided fallback).
- The script uses UTF-8 when reading/writing files.
- Designed to be importable: calling get_new_count() from another script returns the integer new_count.

Examples
- From another script:
  ```python
  from IrregularVerbs.wordCountAdvanced import get_new_count
  max_words = get_new_count()
  ```

This README explains expected behavior and how to