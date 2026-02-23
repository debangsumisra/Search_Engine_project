import sys as ss
import requests
from bs4 import BeautifulSoup
import re
def hash1(word):
    p = 0
    c = 53
    count = 0
    for i in word:  
        count += ord(i) * pow(c, p)
        p += 1
    hash_value = count % 2**64
    # these line i convert the hash value into 64 bit.
    return bin(hash_value)[2:].zfill(64)

def clean_text(text):
    text = text.lower()
    #this line it is basically requirement of the next step to clean the whole text only small letters .
    text = re.sub(r'[^a-z\s]', ' ', text)
    return text
def get_fingerprint(text):
    list1 = text.split()
    stop = {"the","is","and","a","an","of","to","in","on","for","with"}
    i = 0
    while i < len(list1):
        if list1[i] in stop:
            list1.pop(i)
        else:
            i += 1
    list2 = []
    for i in list1:
        list2.append(i.lower())

    dict1 = {}
    for i in list2:
        if i in dict1:
            dict1[i] += 1
        else:
            dict1[i] = 1

    c = {}
    for i in dict1:
        h=hash1(i)
        if h in c:
            c[h] += dict1[i]
        else:            
            c[h] = dict1[i]

    d = []
    for i in c:
        number = [0]*64
        for idx in range(64):
            if i[idx] == '0':
                number[idx] -= c[i]
            else:
                number[idx] += c[i]
        d.append(number)

    final = []
    for i in range(64):
        total = 0
        for j in range(len(d)):
            total += d[j][i]
        final.append(total)

    f2 = []
    for i in final:
        if i > 0:
            f2.append(1)
        else:
            f2.append(0)

    return f2



def search(url):
   
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    print("\n TITLE ")
    if soup.title:
        print(soup.title.get_text())
    else:
        print("No title found")

    
    print("\n BODY TEXT ")
    if soup.body:

        clean = soup.get_text(" ", strip=True)
        print(clean_text(clean))
        print(get_fingerprint(clean_text(clean)))
    else:
        print("No body text found")

   
    print("\n ALL LINKS ")
    if soup.find_all('a'):
        for link in soup.find_all('a'):
            print(link.get('href'))
    else:
        print("No links found") 


def fingerprint(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    clean = soup.get_text(" ", strip=True)
    cleaned_text = clean_text(clean)

    fingerprint = get_fingerprint(cleaned_text)

    return fingerprint
def hamming_distance(fingerprint1, fingerprint2):
    total=0
    for i in range(len(fingerprint1)):
        if fingerprint1[i] != fingerprint2[i]:
            total += 1
    return total

def chaeck_sim(url1, url2):
    fingerprint1 = fingerprint(url1)
    fingerprint2 = fingerprint(url2)

    distance = hamming_distance(fingerprint1, fingerprint2)
    print(f"Hamming Distance: {distance}")

    
    
args = ss.argv

if len(args) == 2:
    search(args[1])

elif len(args) == 3:
    chaeck_sim(args[1], args[2])

else:
    print("write the url in command line argument like this : python search.py <url> or python search.py <url1> <url2>")

