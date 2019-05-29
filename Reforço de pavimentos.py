import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from colorama import init, Fore

init(convert = True)

print(Fore.LIGHTYELLOW_EX + "\n\t\t========= PROGRAMA DE CÁLCULO DE REFORÇO DE PAVIMENTOS FLEXÍVEIS =========" + Fore.RESET)

# Pede para usuário informar dados um a um
S = int(input("\n\t-> Qual a porcetagem de silte passante pela peneira No. 200 do material? (%) "))
CBR = int(input("\n\t-> Qual o CBR (Índice Suporte Califórnia) do subleito? (%) "))
rev = int(input("\n\t-> Qual a espessura da camada de revestimento? (cm) "))
Hcg = int(input("\n\t-> Qual a espessura da camada granular do pavimento? (cm) "))
N = int(input("\n\t-> Qual o N? (Não utilize notação científica.) "))

deflexoes = []
num_deflexoes = int(input("\n\t->A partir do levantamento deflectométrico do segmento homogêneo, insira o número de deflexões que você deseja informar: "))

# A partir do número de deflexões informado pelo usuário, é pedido para informar cada deflexão na ordem
for i in range(num_deflexoes):
    print(Fore.YELLOW + "\n", i + 1, ":" + Fore.RESET)
    df = float(input("Deflexão em 0.01mm: "))
    # Armazena a deflexão informada
    deflexoes.append(df)

deflexoes = np.array(deflexoes)

# Calcula a média e o desvio padrão das deflexões para calcular dp
dm = np.mean(deflexoes)
std = np.std(deflexoes)
dp = dm + std

# Função para retornar tipo de solo dado S e CBR informado
def tipo_solo(S, CBR):
    if CBR >= 10:
        if S <= 35:
            return "Tipo I"
        elif 35 < S < 65:
            return "Tipo II"
        else:
            return "Tipo III"
    elif 6 <= CBR <= 9:
        if S <= 35:
            return "Tipo II"
        elif 35 < S < 65:
            return "Tipo II"
        else:
            return "Tipo III"
    elif 2 < CBR <= 5:
        if S <= 35:
            return "Tipo III"
        elif 35 < S < 65:
            return "Tipo III"
        else:
            return "Tipo III"
    else:
        return Fore.RED + "Ocorreu um erro! Verifique o valor de entrada do CBR."

solo = tipo_solo(S, CBR)

# Função para retornar constantes I1 e I2
def constantes(Hcg, solo):
    if Hcg <= 45:
        if solo == "Tipo I":
            return (0, 0)
        elif solo == "Tipo II":
            return (1, 0)
        elif solo == "Tipo III":
            return (0, 1)
        else:
            return Fore.RED + "Ocorreu algum erro!"

    else:
        return (0, 1)


# Função para realizar o dimensionamento pelo PRO 11/79
def pro_11_79(dp):
    Dadm = 10**(3.01 - 0.175*math.log10(N))
    HR = 40 * math.log10(dp / Dadm)
    print(Fore.LIGHTGREEN_EX + "\nRESULTADOS:")
    print(Fore.CYAN + "\n\t- A deflexão de projeto é" + Fore.LIGHTCYAN_EX + " {:.2f} x10^-2".format(dp))
    print(Fore.CYAN + "\t- A deflexão admissível é" + Fore.LIGHTCYAN_EX + " {:.2f} x10^-2 mm".format(Dadm) + Fore.CYAN + "\n\t- A espessura da camada de reforço deve ser de" + Fore.LIGHTCYAN_EX + " {:.2f} cm.".format(HR) + Fore.RESET)
    plt.style.use("ggplot")
    plt.plot(deflexoes)
    plt.ylabel("Deflexão em 0.01mm")
    plt.show()

# Função para realizar o dimensionamento pelo PRO 269/94
def pro_269_94(dp):
    I1, I2 = constantes(Hcg, solo)
    hef = -5.737 + 807.961/dp + 0.972*I1 + 4.101*I2
    hef_adot = hef if 0 < hef < rev else rev
    Dadm = 10**(3.148 - 0.188*math.log10(N))
    HR = -19.015 + 238.14/math.sqrt(Dadm) - 1.357*hef_adot + 1.016*I1 + 3.893*I2
    print(Fore.LIGHTGREEN_EX + "\nRESULTADOS:")
    print(Fore.CYAN + "\n\t- A deflexão de projeto Dp é " + Fore.LIGHTCYAN_EX + " {:.2f} x10^-2 mm.".format(dp))
    print(Fore.CYAN + "\t- O tipo de solo é do" + Fore.LIGHTCYAN_EX +" {}.".format(solo) + Fore.CYAN + "\n\t- A constante I1 recebe o valor" + Fore.LIGHTCYAN_EX + " {}".format(I1) + Fore.CYAN + " e a constante I2 recebe o valor" + Fore.LIGHTCYAN_EX + " {}.".format(I2))
    print(Fore.CYAN + "\t- Espessura equivalente ao revestimento betuminoso existente (antigo): " + Fore.LIGHTCYAN_EX + "{:.2f} cm.".format(hef_adot))
    print(Fore.CYAN + "\t- A deflexão admissível é de " + Fore.LIGHTCYAN_EX + "{:.2f} x10^-2 mm.".format(Dadm) + Fore.CYAN +  "\n\t- A espessura da camada de reforço deve ser de " + Fore.LIGHTCYAN_EX + "{:.2f} cm.".format(HR) + Fore.RESET)
    if HR <= 0:
        print(Fore.CYAN + "\n\t- Como o cálculo resultou em uma espessura negativa, conclue-se que não é necessário realizar um reforço no pavimento. Pode ser realizada alguma medida preventiva.\n" + Fore.RESET)
    plt.style.use("ggplot")
    plt.plot(deflexoes)
    plt.ylabel("Deflexão em 0.01mm")
    plt.show()

    
# Pede para usuário informar o que deseja fazer a partir das opções oferecidas
decisao = ""
def feedback():
    decisao = input("\n\tVocê deseja dimensionar a camada de reforço por qual método?\n(a) PRO 11/79\t\t(b) PRO 269/94\t\t(c) Sair do programa\n")
    if decisao == "a":
        pro_11_79(dp)
    elif decisao == "b":
        pro_269_94(dp)
    elif decisao == "c":
        sys.exit()
    else:
        print("Opção Inválida")

# Enquanto a decisão não for de sair, pedir o que o usuário deseja fazer
while decisao != "c":
    feedback()
