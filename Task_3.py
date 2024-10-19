import timeit

def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1

    last = {}
    for i in range(m):
        last[pattern[i]] = i

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return i
        shift = last.get(text[i + m - 1], -1) - last.get(pattern[j], -1)
        i += max(1, shift) 

    return -1

def knuth_morris_pratt(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0

    lps = [0] * m
    compute_lps(pattern, lps)

    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def compute_lps(pattern, lps):
    length = 0
    i = 1
    lps[0] = 0

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

def rabin_karp(text, pattern):
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1

    d = 256
    q = 101
    p = 0
    t = 0
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q

    return -1

texts = [
    "Це приклад тексту, в якому ми будемо шукати підрядки.",
    "Це ще один текст, що містить різні підрядки для тестування."
]
existing_substring = "приклад"
non_existing_substring = "вигаданий"

def time_algorithm(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=1000)

def get_results(text):
    results = {}
    results['приклад'] = {
        'Boyer-Moore': time_algorithm(boyer_moore, text, existing_substring),
        'Knuth-Morris-Pratt': time_algorithm(knuth_morris_pratt, text, existing_substring),
        'Rabin-Karp': time_algorithm(rabin_karp, text, existing_substring)
    }
    results['вигаданий'] = {
        'Boyer-Moore': time_algorithm(boyer_moore, text, non_existing_substring),
        'Knuth-Morris-Pratt': time_algorithm(knuth_morris_pratt, text, non_existing_substring),
        'Rabin-Karp': time_algorithm(rabin_karp, text, non_existing_substring)
    }
    return results

results = {text: get_results(text) for text in texts}

for text, result in results.items():
    print(f"\nРезультати для тексту:\n{text}\n")
    for condition in result:
        print(f"Час виконання для '{condition}' підрядка:")
        for algorithm, time in result[condition].items():
            print(f"{algorithm}: {time:.5f} секунд")