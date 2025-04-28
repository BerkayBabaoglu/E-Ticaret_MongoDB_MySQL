import pymysql

pymysql.install_as_MySQLdb() #proje ayaga kalkarken otomatik olarak pymysql ayarlanir

#djangoda genellikle uygulama baslarken bazi ayarlari yuklemek icin kullanilir.
#__init__'de olmasinin sebebi projenin ilk yuklenisinde bu kod calissin diye.