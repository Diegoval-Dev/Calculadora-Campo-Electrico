import sympy as sp

radio1 = int(input("radio1 = "))
radio2 = int(input("radio2 = "))
altura = int(input("altura = "))
distancia = int(input("distancia = "))
carga = int(input("carga = "))

x = sp.Symbol('x')

funcionTrozo = 1 - (
    (altura - x + distancia) / (
        sp.sqrt(
            ((altura - x + distancia) ** 2) +
            ((((radio1-radio2)/altura)*x)+radio2) ** 2
        )
    )
)

integralTrozo = sp.integrate(funcionTrozo, (x, 0, altura))
print(integralTrozo)