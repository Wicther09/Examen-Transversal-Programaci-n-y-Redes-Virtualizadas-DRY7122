while True:
    print("\n--------------------------------------------------------")
    print("Examen Transversal Programación y Redes Virtualizadas")
    print("Script desarrollado por:")
    print("Héctor Moisés Araujo Bastidas")
    print("Héctor Santiago Orellana Gacitua")
    print("--------------------------------------------------------")
    
    try:
        x = int(input("Ingrese el número de la Sistema Autonomo (AS) (Ej = 1 - 65534): "))
        
        if x in range (0, 64495):
            print("Este es un Sistema Autonomo Publico")
            z = input("Desea continuar? S/N:")
            if z.lower() in ["si","s"]:
                print("")
            elif z.lower() in ["no","n"]:
                print("Terminando Programa")
                break
                
        elif x in range(64512, 65535): 
            print("Este es un Sistema Autonomo Privado")
            z = input("Desea continuar? S/N:")
            if z.lower() in ["si","s"]:
                print("")
            elif z.lower() in ["no","n"]:
                print("Terminando Programa")
                break  
        else:
            print("AS erroneo o reservado")

    except ValueError:
        print("El Sistema Autonomo (AS) ingresado no es válido. Solo ingrese números.")