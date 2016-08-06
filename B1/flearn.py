lst=["ahmet","yahya","serkan","selim","umuttepe","wing tsun"]
nb=range(19)
print nb
for names in lst:
    print names
for nums in range(1,10,3):
    print nums
for k in range(10):
    print k
numlist=[num for num in range(10)]
print numlist
words=["hi","from","kocaeli","Turkey"]
kelimeler=["selam","ey","kocaeli","Turkiye"]
_dict=dict()
for w in range(len(words)):
    _dict[words[w]]=kelimeler[w]
print _dict["hi"]
print _dict["Turkey"]

