"""Practice algorithms using dynamic programming.
"""
from functools import wraps
from itertools import chain

# functional helpers
fst = lambda x: x[0]
snd = lambda x: x[1]

inf = float('infinity')

def knapsack(items, max_weight):
    """Returns the maximum value attainable with the given (value, weight)
    pairs, without surpassing the maximum weight provided.
    >>> knapsack([], 1)
    0
    >>> knapsack([(1, 2)], 0)
    0
    >>> knapsack([(0, 1), (2, 3), (2, 1), (4, 1)], 3)
    6
    >>> knapsack([(1, 1)], -1)
    Traceback (most recent call last):
        ...
    ValueError: max_weight cannot be < 0 (got -1)
    >>> knapsack([(1, 1), (1, -1)], 2)
    Traceback (most recent call last):
        ...
    ValueError: item weights cannot be < 0 (got -1)
    """
    if max_weight < 0:
        raise ValueError(f'max_weight cannot be < 0 (got {max_weight})')
    if not items or not max_weight:
        return 0
    x = [[0 for _ in range(max_weight + 1)] for _ in range(len(items) + 1)]
    for i, (value, weight) in enumerate(items, start=1):
        if weight < 0:
            raise ValueError(f'item weights cannot be < 0 (got {weight})')
        for w in range(max_weight + 1):
            if weight > w:
                x[i][w] = x[i-1][w]
            else:
                x[i][w] = max(x[i-1][w], x[i-1][w-weight] + value)
    return x[len(items)][max_weight]

def memoize(f):
    """Generic memoization decorator, requires arguments to be hashable."""
    m = {}
    @wraps(f)
    def inner(*args, **kwargs):
        key = (tuple(args), tuple(kwargs.items()))
        try:
            return m[key]
        except KeyError:
            value = f(*args, **kwargs)
            m[key] = value
            return value
    return inner

@memoize
def fib(n):
    """Compute the nth Fibonacci number.
    >>> [fib(n) for n in range(10+1)]
    [1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    >>> fib(-1)
    Traceback (most recent call last):
        ...
    ValueError: Cannot compute Fibonacci number for n < 0 (got -1)
    """
    if n < 0:
        raise ValueError(f"Cannot compute Fibonacci number for n < 0 (got {n})")
    if n <= 2:
        return 1
    return fib(n-2) + fib(n-1)

def justify(text, line_width=80, add_spaces=True, badness=None):
    """Returns the text justified to the given line width."""
    if badness is None:
        badness = lambda w: (line_width - w)**3
    assert badness(line_width == 0) and badness(0) > badness(1), "Invalid badness function"
    text = " ".join([""] + text.split()) # normalize whitespace
    word_indices = [i+1 for i, (x, y) in enumerate(zip(text, text[1:])) if x == ' ' and y != ' ']

    @memoize
    def score_leading_word(i):
        if i == len(word_indices):
            return 0
        max_score = None
        for j in range(i+1, len(word_indices)+1):
            end = word_indices[j] if j < len(word_indices) else len(text)
            width = end - word_indices[i]
            score = score_leading_word(j) - badness(width) if width <= line_width else -inf
            if max_score is None or score > max_score:
                max_score = score
        return max_score

    # leading words will be those with a *larger* score than the previous
    scores = [(wi, -score_leading_word(i)) for i, wi in enumerate(word_indices)]
    xs = list(map(fst, filter(lambda iw: iw[1] < 0,
                              map(lambda wiw: (wiw[1][0], wiw[1][1] - wiw[0]),
                                  zip(chain([inf], map(snd, scores)), scores)))))

    # build the result, potentially adding spaces
    result = ""
    for i, j in zip(xs, chain(xs[1:], [len(text)])):
        if i > 1:
            result += "\n"
        line = text[i:j].strip()
        words = line.split()
        if add_spaces and len(words) > 1:
            i = 0
            nb_spaces_to_add = line_width - len(line)
            while nb_spaces_to_add > 0:
                words[i] += " "
                nb_spaces_to_add -= 1
                i = (i + 1) % (len(words) - 1)
            result += " ".join(words)
        else:
            result += line
    return result

def test_justification():
    given = ("In the common walks of life, with what delightful emotions does the "
            "youthful mind look forward to some anticipated scene of festivity! "
            "Imagination is busy sketching rose-tinted pictures of joy. In fancy, "
            "the voluptuous votary of fashion sees herself amid the festive "
            "throng, the observed of all observers. Her graceful form, arrayed in "
            "snowy robes, is whirling through the mazes of the joyous dance; her "
            "eye is brightest, her step is lightest in the gay assembly.")

    expected = ("In   the   common  walks  of  life,  with  what  delightful  emotions  does  the" "\n"
                "youthful  mind  look forward to some anticipated scene of festivity! Imagination" "\n"
                "is  busy  sketching rose-tinted pictures of joy. In fancy, the voluptuous votary" "\n"
                "of  fashion sees herself amid the festive throng, the observed of all observers." "\n"
                "Her  graceful form, arrayed in snowy robes, is whirling through the mazes of the" "\n"
                "joyous  dance;  her  eye is brightest, her step is lightest in the gay assembly.")

    reached = justify(given)
    if expected != reached:
        print("Failure when justifying:")
        print()
        print(given)
        print()
        print("The output should be:")
        print()
        print(expected)
        print()
        print("The output instead was:")
        print()
        print(reached)
        raise AssertionError

def max_profit_when_buying_and_selling_stock(prices, K):
    """Computes the maximum profit that can be made by buying/selling stock at
    most K times for the given prices, without overlap between transactions.
    >>> max_profit_when_buying_and_selling_stock([3, 2, 6, 5, 0, 3], 2)
    7
    >>> max_profit_when_buying_and_selling_stock([2, 4, 1], 2)
    2
    >>> max_profit_when_buying_and_selling_stock([6, 1, 3, 2, 4, 7], 2)
    7
    """
    if not prices or K == 0:
        return 0

    def profit(i, j):
        i1, j1 = i, i
        min_, max_ = prices[i1], prices[j1]
        while j1 <= j:
            if prices[j1] > max_:
                max_ = prices[j1]
                while i1 < j1:
                    if prices[i1] < min_:
                        min_ = prices[i1]
                        break
                    i1 += 1
                break
            j1 += 1
        return max_ - min_

    @memoize
    def recurse(i, j, k):
        if k == 0:
            return 0
        max_profit = profit(i, j)
        for x in range(i+1, j):
            split_profit = recurse(i, x, k-1) + recurse(x, j, 1)
            if split_profit > max_profit:
                max_profit = split_profit
            split_profit = recurse(i, x, 1) + recurse(x, j, k-1)
            if split_profit > max_profit:
                max_profit = split_profit
        return max_profit
    return recurse(0, len(prices)-1, K)

if __name__ == "__main__":
    import doctest; doctest.testmod()
    test_justification()
