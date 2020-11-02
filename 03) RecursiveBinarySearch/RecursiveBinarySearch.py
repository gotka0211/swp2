import time
import random

def seqsearch(nbrs, target): #선형탐색
    for i in range(0, len(nbrs)):
        if (target == nbrs[i]):
            return i
    return -1

"""def binsearch(nbrs, target): #이진탐색
    lower = 0
    upper = len(nbrs) -1
    idx= -1
    while (lower <= upper):
        middle = int((lower + upper) // 2)
        if nbrs[middle] == target :
            idx= middle
            break
        elif nbrs[middle] < target :
            lower = middle + 1
        else:upper = middle -1
    return idx"""

def recbinsearch(L, l, u, target): #재귀적 이진탐색
    middle = int((l+u)//2)
    if l>u: 
        return -1    
    if L[middle] == target:
        idx = middle
        return idx
    elif L[middle] < target:
        return recbinsearch(L, middle+1, u, target)
    else:
        return recbinsearch(L, l, middle-1, target)

###데이터 세팅###
numofnbrs = int(input("Enter a number: "))
numbers = []
for i in range(numofnbrs):
    numbers += [random.randint(0, 999999)]

numbers = sorted(numbers)

numoftargets = int(input("Enter the number of targets: "))
targets = []
for i in range(numoftargets):
    targets += [random.randint(0, 999999)]

#####이 아래로 각 함수별 시간 측정#####

# binary search - recursive
ts = time.time()
cnt = 0
for target in targets:
    idx = recbinsearch(numbers, 0, len(numbers)-1, target)
    if idx == -1:
        cnt += 1
ts = time.time() - ts
print("recbinsearch %d: not found %d time %.6f" % (numoftargets, cnt, ts))

# binary search - iterative
"""ts = time.time()
cnt = 0
for target in targets:
    idx = binsearch(numbers, target)
    if idx == -1:
        cnt += 1
ts = time.time() - ts
print("binsearch %d: not found %d time %.6f" % (numoftargets, cnt, ts))"""

# sequential search
ts = time.time()
cnt = 0
for target in targets:
    idx = seqsearch(numbers, target)
    if idx == -1:
        cnt += 1
ts = time.time() - ts
print("seqsearch %d: not found %d time %.6f" % (numoftargets, cnt, ts))

#결론) 속도: 반복적이진탐색 > 재귀적이진탐색 > 선형탐색  
