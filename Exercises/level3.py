


def sort_people(people):
    return sorted(people, key=lambda p: (p[1], p[0]))


def is_palindrome(s):
    """Ignore case and anything that isn't a letter or digit.
    Hint: str.isalnum() and slicing with [::-1]."""
    s="".join(c for c in s if c.isalnum()).lower()
    if s==s[::-1]:return True
    else:return False


def to_dict(keys, values):
    return dict(zip(keys, values))


def index_of_max(nums):
    max_index,max_numbers=max(enumerate(nums),key=lambda x:x[1])
    return max_index


def chunk(items, size):
    
    chunks=[items[i:i+size] for i in range(0,len(items),size)]
    return chunks


def most_common_char(s):
    count={}
    s="".join(c for c in s if c.isalnum()).lower()
    for c in s:
        if c in count :
            count[c]+=1
        else:
            count[c]=1
    return max(count, key=lambda x:count[x])



assert sort_people([("Ravi", 30), ("Anu", 25), ("Bala", 30)]) == [("Anu", 25), ("Bala", 30), ("Ravi", 30)]
assert is_palindrome("A man, a plan, a canal: Panama")
assert not is_palindrome("hello")
assert to_dict(["a", "b"], [1, 2]) == {"a": 1, "b": 2}
assert index_of_max([3, 9, 2, 9]) == 1
assert chunk([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 2, 3], [4, 5, 6], [7]]
assert most_common_char("hello world") == "l"
assert most_common_char("abba") == "a"
print("Level 3 passed")
