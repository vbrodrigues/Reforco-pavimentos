import numpy as np
import math
import sys

S = int(input("\n\tQual a porcetagem de silte passante pela peneira No. 200 do material? (%) "))
CBR = int(input("\n\tQual o CBR (Índice Suporte Califórnia) do subleito? (%) "))
rev = int(input("\n\tQual a espessura da camada de revestimento? (cm) "))
Hcg = int(input("\n\tQual a espessura da camada granular do pavimento? (cm) "))
N = int(input("\n\tQual o N? (Não utilize notação científica.) "))
deflexoes = []
num_deflexoes = int(input("\n\tA partir do levantamento deflectométrico do segmento homogêneo, insira o número de deflexões que você deseja informar: "))

for i in range(num_deflexoes):
    df = float(input("Deflexão em 0.01mm: "))
    deflexoes.append(df)

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
        return "Ocorreu um erro! Verifique o valor de entrada do CBR."

solo = tipo_solo(S, CBR)

def constantes(Hcg, solo):
    if Hcg <= 45:
        if solo == "Tipo I":
            return (0, 0)
        elif solo == "Tipo II":
            return (1, 0)
        elif solo == "Tipo III":
            return (0, 1)
        else:
            return "Ocorreu algum erro!"

    else:
        return (0, 1)

deflexoes = np.array(deflexoes)
dm = np.mean(deflexoes)
std = np.std(deflexoes)
dp = dm + std

def pro_11_79(dp):
    Dadm = 10**(3.01 - 0.175*math.log10(N))
    HR = 40 * math.log10(dp / Dadm)
    print("\nRESULTADOS:")
    print("\n\t**A deflexão admissível é {:.2f} x10^2 mm**\n\t**A espessura da camada de reforço deve ser de {:.2f} cm.**".format(Dadm, HR))

def pro_269_94(dp):
    I1, I2 = constantes(Hcg, solo)
    hef = -5.737 + 807.961/dp + 0.972*I1 + 4.101*I2
    hef_adot = hef if 0 < hef < rev else rev
    Dadm = 10**(3.148 - 0.188*math.log10(N))
    HR = -19.015 + 238.14/math.sqrt(Dadm) - 1.357*hef_adot + 1.016*I1 + 3.893*I2
    print("\nRESULTADOS:")
    print("\n\t**A deflexão de projeto Dp é {:.2f} x10^-2 mm.**".format(dp))
    print("\n\t**O tipo de solo é do {}**.\n\t**A constante I1 recebe o valor {} e a constante I2 recebe o valor {}.**".format(solo, I1, I2))
    print("\n\t**Espessura equivalente ao revestimento betuminoso existente (antigo): {:.2f} cm.**".format(hef_adot))
    print("\n\t**A deflexão admissível é de {:.2f} x10^-2 mm.**\n\t**A espessura da camada de reforço deve ser de {:.2f} cm.**".format(Dadm, HR))
    if HR <= 0:
        print("Como o cálculo resultou em uma espessura negativa, conclue-se que não é necessário realizar um reforço no pavimento. Pode ser realizada alguma medida preventiva.")

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

while decisao != "c":
    feedback()
