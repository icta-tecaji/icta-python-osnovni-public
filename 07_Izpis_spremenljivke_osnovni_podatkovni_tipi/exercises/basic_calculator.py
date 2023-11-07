"""Basic sum calculator."""

# Naloga je napisati enostaven kalkulator, ki bo uporabnika vprašal po dveh
# številih in jih seštel.

# Uporabnika vprašajte po prvem številu.
first_number = float(input("Vnesi prvo število: "))

# Uporabnika vprašajte po drugem številu.
second_number = float(input("Vnesi drugo število: "))

# Glede na operacijo izvedite ustrezno računsko operacijo.
result = first_number + second_number

# Rezultat izpišite uporabniku.
print("Rezultat je", result)  # noqa: T201
