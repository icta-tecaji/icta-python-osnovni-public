"""Napišite program, ki bo pretvoril stopinje Celzija v Fahrenheit ali obratno.

Uporabnik naj vnese številko. Nato naj vnese v katerih enotah nam je podal
vrednost (**C** ali **F**). Glede na vnešeno črko naj vaš program
uporabi pravilno formulo za pretvorbo.
```
T(°F) = T(°C) × 9/5 + 32

T(°C) = (T(°F) - 32) x 5/9
```
Če uporabnik ni vnesel **C** ali **F** naj program izpiše
*Prišlo je do napake.*

Primer:
```
Vnesi vrednost: 12
Vnesi enoto: C
```
Rešitev:
```
12 stopinj celzija je enako 53.6 fahrenheit.
```
"""

stopinje = float(input("Vnesi vrednost: "))
enota = input("V katerih enotah je podana vrednost? [C/F]: ")

if enota == "C":
    fahrenheit = stopinje * 9 / 5 + 32
    print(f"{stopinje} {enota} je enako {fahrenheit} fahrenheit.")
elif enota == "F":
    celsius = (stopinje - 32) * 5 / 9
    print(f"{stopinje} {enota} je enako {celsius} celsius.")
else:
    print("Prišlo je do napake")
