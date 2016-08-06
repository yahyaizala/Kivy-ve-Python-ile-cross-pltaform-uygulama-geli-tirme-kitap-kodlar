#:-*- coding:utf-8 -*-
import sqlite3
from time import sleep
dbname="kydemo.db"
con=sqlite3.connect(dbname)
sql="create table if not exists trking(id integer not null primary key autoincrement,turkce varchar,ingilizce varchar)"
con.execute(sql)
con.close()
print "===Veritabani Olusturuldu"
print "===Veritabani adi kydemo tablo adi trking"
sleep(1)
con=sqlite3.connect(dbname)
sql=["insert into trking(turkce,ingilizce) values('selam','hi')",
    "insert into trking(turkce,ingilizce) values('kaç','how much')",
    "insert into trking(turkce,ingilizce) values('bilgi','knowledge')",
    "insert into trking(turkce,ingilizce) values('kalem','pen')",
    "insert into trking(turkce,ingilizce) values('iletişim','contact')"]
for sq in sql:
    con.execute(sq)
con.commit()
con.close()
print "==veriler basariyle eklendi"
print "[+] Lütfen bekleyin işlem yapılıyor..."
sleep(1)
con=sqlite3.connect(dbname)
sql="update trking set turkce='Tükenmez Kalem' where ingilizce='pen'"
con.execute(sql)
con.commit()
con.close()
print "===Güncelleme başrıyla yapıldı"
print "[+] Lütfen bekleyin işlem yapılıyor..."
sleep(1)
con=sqlite3.connect(dbname)
sql="delete from trking where id='1'"
con.execute(sql)
con.commit()
con.close()
print "===başarıyla kayıt silindi"
print "[+] Lütfen bekleyin işlem yapılıyor..."
sleep(1)
con=sqlite3.connect(dbname)
sql="select * from trking"
cursor=con.cursor()
all_data=cursor.execute(sql).fetchall()
for data in all_data:
    print data[0],data[1],data[2]


