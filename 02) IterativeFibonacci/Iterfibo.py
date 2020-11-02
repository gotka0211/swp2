import time

def fibo(n): #슬라이드에 있는 재귀적 피보나치수열 
    if n <= 1:
        return n
    return fibo(n -1) + fibo(n -2)

def iterfibo(n): #반복 피보나치수열 
    if n==0: #n이 0일 경우 0을 반환합니다.
        return 0
    FList=[0,1] 
    while (len(FList) <=n): #리스트에 반복적으로 뒤에서 첫번째와 두번째수를 더하여 추가합니다. 
        FList.append(FList[-1]+FList[-2])
    return FList[-1]

if __name__ == '__main__':
    while True: #재귀피보와 반복피보 실행 시간비교
        nbr= int(input("Enter a number: "))
        if nbr== -1:
            break
        ts= time.time()
        fibonumber= iterfibo(nbr)
        ts= time.time() -ts
        print("IterFibo({})={}, time {:6f}".format(nbr, fibonumber, ts))
        ts= time.time()
        fibonumber= fibo(nbr)
        ts= time.time() -ts
        print("Fibo({})={}, time {:6f}".format(nbr, fibonumber, ts))
