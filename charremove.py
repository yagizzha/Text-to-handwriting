import io

f = io.open("C:/Users/yagiz/Desktop/Self/handwriting/full.txt", mode="r", encoding="utf-8")
full=f.read()
full = full.replace("â", "a")
full = full.replace("î", "i")
    
print(full)
#î â
f.close()
fa = io.open("C:/Users/yagiz/Desktop/Self/handwriting/full.txt", mode="a+", encoding="utf-8")
fa.close()
