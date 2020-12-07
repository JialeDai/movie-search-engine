import os
for filename in os.listdir("D:\VSCode\python\IR\\assignment1\data"):
    print("D:\VSCode\python\IR\\assignment1\data\\" + filename) 
    with open("D:\VSCode\python\IR\\assignment1\data\\" + filename,encoding='utf8') as f:
        for line in f.readlines():
            with open("D:\VSCode\python\IR\\assignment1\data\collection.txt","a",encoding='utf8') as mom:
                mom.write(line) 
