

def divEntier(x: int, y: int) -> int:

    if y == 0:
        raise ValueError("Division par 0")


    if y < 0 or x < 0:
        raise ValueError("L'un des entiers est négatifs")
    
    elif y < 0 and x < 0:
        raise ValueError("Les deux entiers sont négatifs")
    
    if x < y:
        return 0
    else:
        x = x - y
        return divEntier(x, y) + 1
    


def main():
    x = int(input("Entrez un entier x: "))
    y = int(input("Entrez un entier y: "))
    print(divEntier(x, y))

if __name__ == '__main__':
    main()