import app.helloworld
from app.helloworld import penjumlahan

print(penjumlahan(5, 10))
names = []
names.append("Budi")
names.append("Joko")

for i in names:
    i: str = i
    print(i.upper())
