def even_squares(nums):
   return [num**2 for num in nums if num%2==0]


def word_count(text):
    
    words=text.lower().split()
    word_counter={}
    for word in words:
        word_counter[word]=word_counter.get(word,0)+1
    return word_counter



def dedupe(items):
    seen=set()
    result=[]
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
            
    return result


def two_sum(nums, target):
    """Return the indices [i, j] of the two numbers that add up to target.
    Do it in a single pass using a dict (O(n))."""
    dict={}
    for index ,num in enumerate(nums):
        remaining=target-num
        if remaining in dict:
            return [dict[remaining],index]
        dict[num]=index
    return [-1,-1]


def invert(d):
    """{'a': 1, 'b': 2} -> {1: 'a', 2: 'b'}. Use a dict comprehension."""
    inverted_dict={}
    for key,value in d.items():
        inverted_dict[value]=key
    return inverted_dict


def common(a, b):
    """Sorted list of the items that appear in both lists. Use sets."""
    common_set=set(a)&set(b)
    return list(common_set)

assert even_squares([1, 2, 3, 4, 5, 6]) == [4, 16, 36]
assert word_count("the cat the") == {"the": 2, "cat": 1}
assert word_count("The THE the") == {"the": 3}
assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}
assert common([1, 2, 3, 4], [3, 4, 5]) == [3, 4]
print("Level 2 passed")
