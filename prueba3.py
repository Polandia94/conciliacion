import requests
n=0
while n < 100:
    algo = requests.get("https://www.pyphoy.com/cartagena/particulares/9")
    n = n +1
    if n%20==0:
        print(n)
print(algo)
print(algo.text)
