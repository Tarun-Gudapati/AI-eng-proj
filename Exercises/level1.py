

def fizzBuzz(n:int)->list[str]:
    answer = []
    for i in range(1,n+1):
        if i%3==0 and i%5==0:
            answer.append("FizzBuzz")
        elif i%3==0:
            answer.append("Fizz")
        elif i%5==0:
            answer.append("Buzz")
        else:
            answer.append(f"{i}")
    return answer

def sum_digits(n:int)->int:
    totalSum = 0
    while n>0:
        totalSum+=n%10
        n=n//10
    return totalSum
def count_vowels(s:str)->int:
    count=0
    vowels = "aeiouAEIOU"
    for char in s:
        if char in vowels:
            count+=1
    return count

def grade(score:int)->str:
    if score>=90:
        return "A"
    elif score>=80:
        return "B"
    elif score>=70:
        return "C"
    elif score>=60:
        return "D"
    else:
        return "F"
def reverse_string(s:str)->str:
    reversedString=s.split() #split the string into a list of words
    reversedString.reverse()
    return " ".join(reversedString)


def main()->None:
    print("Hello, World!")
    print(fizzBuzz(15))
    print(sum_digits(1234))
    print(count_vowels("Hello, World!"))
    print(grade(95))
    print(reverse_string("Hello, World!"))
if __name__ == "__main__":
    main()