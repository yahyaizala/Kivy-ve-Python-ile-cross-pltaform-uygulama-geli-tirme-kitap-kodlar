dict = {'Ad': 'Zara', 'Yas': 7, 'Sinif': '5B'}
print "dict['AD']: ", dict['Ad']
#dict['AD']:  Zara
print "dict['Yas']: ", dict['Yas']
#dict['Yas']:  7
dict["Ad"]="Zehra"
print dict
#{'Sinif': '5B', 'Ad': 'Zehra', 'Yas': 7}
del dict["Yas"]
scdic=dict.copy()
noncopy=dict
#{'Sinif': '5B', 'Ad': 'Zehra'}
dict.clear()
print dict
#{}
print scdic
print noncopy
#{'Sinif': '5B', 'Ad': 'Zehra'}
#{}
scdic.fromkeys("Sinif","6B")
print scdic