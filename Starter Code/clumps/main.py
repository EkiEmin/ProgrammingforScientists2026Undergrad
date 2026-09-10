import requests

def main():
    url = "https://bioinformaticsalgorithms.com/data/realdatasets/Replication/E_coli.txt"

    response = requests.get(url)
    
    response.raise_for_status()
    
    genome = response.text
        
    k = 9
    window_length = 500
    t = 3
    patterns = find_clumps(genome, k, window_length, t)

    print("we found", len(patterns))

# Pseudocode from the learning objectives (for reference)

"""
FindClumps(text, k, L, t)
    patterns ← an array of strings of length 0
    n ← length(text)
    for every integer i between 0 and n − L
        window ← text[i, i + L]
        freqMap ← FrequencyTable(window, k)
        for every key s in freqMap
            if freqMap[s] ≥ t and Contains(patterns, s) = false
                patterns ← append(patterns, s)
    return patterns
"""

"""
# text + "BANANASPLIT"
# window_length = 6
k = 3
first window: BANANA
"BAN"   1
"ANA"   2
"NAN"   1

# second window: ANANAS
"ANA" 2
"NAN" 1
"NAS" 1
"""

def find_clumps_faster(text: str, k: int, window_length: int, t: int) -> list[str]:
    """
    Finds a list of strings representing all k-mers that appear at least t times
    in a window of given length in the string.

    Parameters:
    - text (str): The input string.
    - k (int): The k-mer length.
    - window_length (int): Length L of the sliding window.
    - t (int): Frequency threshold within a window.

    Returns:
    - list[str]: All distinct k-mers forming (L, t)-clumps in text.

    Notes:
    - Follow the FindClumps pseudocode above.
    - Build a frequency table for each window using `frequency_table`.
    - Avoid duplicates by checking `s not in patterns` before appending.
    """

        # think about all the cheks that you would want to do about the paramters

    if len(text) == 0:
        raise ValueError("Empty string.")

    if k > window_length:
        raise ValueError("k too big")

    n = len(text)

    if t < 0 or k < 0 or n < 0:
        raise ValueError("negative input given")

def find_clumps(text: str, k: int, window_length: int, t: int) -> list[str]:
    """
    Finds a list of strings representing all k-mers that appear at least t times
    in a window of given length in the string.

    Parameters:
    - text (str): The input string.
    - k (int): The k-mer length.
    - window_length (int): Length L of the sliding window.
    - t (int): Frequency threshold within a window.

    Returns:
    - list[str]: All distinct k-mers forming (L, t)-clumps in text.

    Notes:
    - Follow the FindClumps pseudocode above.
    - Build a frequency table for each window using `frequency_table`.
    - Avoid duplicates by checking `s not in patterns` before appending.
    """
    # think about all the cheks that you would want to do about the paramters

    if len(text) == 0:
        raise ValueError("Empty string.")

    if k > window_length:
        raise ValueError("k too big")

    n = len(text)

    if t < 0 or k < 0 or n < 0:
        raise ValueError("negative input given")

    patterns: list[str] = [] # will store our frequent k-mers

    # range over all teh windows!
    # a string of length n has how many substring of lenth window_length
    # n - windows_length + 1
    for i in range(n-window_length+1):
        window = text[i:i+window_length]
        freq_map = frequency_table(window, k)

        # what are the patterns that appear at least t time in my freq_map AND 
        # that don't already occur in patterns?
        for s, val in freq_map.items():
            if val >= t and not (s in patterns):
                patterns.append(s)
                # this is what we are looking for ^

    return patterns


def frequency_table(text: str, k: int) -> dict[str, int]:
    """
    frequency_table finds the frequencies of each k-mer occurring in a given text, 
    including overlaps.

    Parameters:
    - text (str): The string text to search for k-mers.
    - k (int): The size of the k-mers.

    Returns:
    - dict[str, int]: The dictionary of k-mers to their frequencies in the given
    text string, including overlaps.
    """

    if k <= 0:
        raise ValueError("k must be positive")
    if k > len(text):
        return {}

    freq_map = {}
    n = len(text)

    # Range over all substrings of length k.
    for i in range(n - k + 1):
        # Grab current pattern
        pattern = text[i:i + k]

        # updating the value of freq_map associated with pattern
        freq_map[pattern] = freq_map.get(pattern, 0) + 1
        # if pattern is a key, this is what we want
        # if it's not, freq_map[pattern] gets created,
        # gets set equal to zero, then incremented.

    return freq_map


if __name__ == "__main__":
    main()