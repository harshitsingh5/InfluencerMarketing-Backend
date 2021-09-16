ll=[]
def heapPermutation(a, size, n):
    global ll
    if (size == 1):
        ll.append(a[:n])
        return
    for i in range(size):
        heapPermutation(a,size-1,n)
        if size&1: 
            a[0], a[size-1] = a[size-1],a[0] 
        else: 
            a[i], a[size-1] = a[size-1],a[i]
def good_triplets (arr, n):
    # Write your code here
    count=0
    heapPermutation(arr,len(arr),3)
    for val in ll:
      sumv=sum(val)
      divi=0
      if sumv%val[0]==0:
          divi+=1
      if sumv%val[1]==0:
          divi+=1
      if sumv%val[2]==0:
          divi+=1
      if divi==1:
          count+=1
        print(val)
    return count
    
    
n = int(input())
arr = []
for i in range(n) : 
    x = int(input())
    arr.append(x)

out_ = good_triplets(arr, n)
print (out_)