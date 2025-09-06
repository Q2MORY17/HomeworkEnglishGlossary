import pytest
import pandas as pd
import random

# Mock data for testing
@pytest.fixture
def mock_df():
    # Column 0: English, Column 1: French
    data = [
        ["cat", "chat"],
        ["dog", "chien"],
        ["bird", "oiseau"],
        ["fish", "poisson"],
        ["horse", "cheval"]
    ]
    return pd.DataFrame(data)

def wordFinder(lottery, df, wordMemory, lengthOfThisWeeksEnglishGlossary):
    for i in wordMemory:
        if df.iat[lottery, 1] == i:
            lottery = random.randint(df.shape[0]-lengthOfThisWeeksEnglishGlossary, df.shape[0]-1)
            return wordFinder(lottery, df, wordMemory, lengthOfThisWeeksEnglishGlossary)
    return lottery

def test_wordFinder_unique(mock_df):
    wordMemory = ["chat", "chien"]
    lengthOfThisWeeksEnglishGlossary = 5
    # Pick index 0 ("chat"), which is in wordMemory, so should not be returned
    result = wordFinder(0, mock_df, wordMemory, lengthOfThisWeeksEnglishGlossary)
    assert mock_df.iat[result, 1] not in wordMemory

def test_wordFinder_not_in_memory(mock_df):
    wordMemory = ["chat", "chien"]
    lengthOfThisWeeksEnglishGlossary = 5
    # Pick index 2 ("oiseau"), which is not in wordMemory, so should be returned
    result = wordFinder(2, mock_df, wordMemory, lengthOfThisWeeksEnglishGlossary)
    assert result == 2

def test_wordFinder_all_in_memory(mock_df):
    wordMemory = ["chat", "chien", "oiseau", "poisson", "cheval"]
    lengthOfThisWeeksEnglishGlossary = 5
    # All words are in memory, so recursion may loop forever; test for exception
    with pytest.raises(RecursionError):
        wordFinder(0, mock_df, wordMemory, lengthOfThisWeeksEnglishGlossary)