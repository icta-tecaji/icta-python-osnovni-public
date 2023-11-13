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

temperature = float(input("Input temperature: "))
unit = input("Input temperature unit [C/F]: ").upper()

if unit == "C":
    print(f"{temperature} °C is {(temperature * 9/5) + 32} °F.")
elif unit == "F":
    print(f"{(temperature - 32) * 5/9} °C is {temperature} °F.")
else:
    print(f"Error: {unit} is not a valid unit. Please use C or F.")
