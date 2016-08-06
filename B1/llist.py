list_a=["python","ruby","c#"]
print list_a
#['python', 'ruby', 'c#']
print  list_a[0]
#python
print  list_a[2]
#c#
list_a.extend([3,4])
print list_a
#['python', 'ruby', 'c#', 3, 4]
list_a.append(5)
print list_a
#['python', 'ruby', 'c#', 3, 4, 5]
list_a.remove("ruby")
print list_a
#['python', 'c#', 3, 4, 5]
list_a.insert(0,"yahya")
print list_a
#['yahya', 'python', 'c#', 3, 4, 5]
list_a[0]="siz"
print list_a
#['siz', 'python', 'c#', 3, 4, 5]
del list_a[3]
print list_a
['siz', 'python', 'c#', 4, 5]
idxsiz=list_a.index(4)
print idxsiz
#3
list_a[idxsiz]="android"
print list_a
#['siz', 'python', 'c#', 3, 'android', 5]
list_cnt=len(list_a)
print list_cnt
#5
print list_a.__len__()
#5

lst=["a","b","c","d","e"]
print lst
#['a', 'b', 'c', 'd', 'e']
print lst[-1]
#e
print lst[:2]
#['a', 'b']
print lst[:]
#['a', 'b', 'c', 'd', 'e']
print lst[-3:]

#['c', 'd', 'e']



