i = 0
saida = ''

def case_0():
    global saida
    saida = saida+" zero"
def case_1():
    global saida
    saida = saida+" um"
def case_2():
    global saida
    saida = saida+" dois"
def case_3():
    global saida
    saida = saida+" três"
def case_4():
    global saida
    saida = saida+" quatro"
def case_5():
    global saida
    saida = saida+" cinco"
def case_6():
    global saida
    saida = saida+" seis"
def case_7():
    global saida
    saida = saida+" sete"
def case_8():
    global saida
    saida = saida+" oito"
def case_9():
    global saida
    saida = saida+" nove"
def case_10():
    global saida
    saida = saida+" ponto"
def case_11():
    global saida
    saida = saida+" virgula"
def case_default():
    global saida
    saida = "você digitou caracteres inválidos"
    i += len(caractere)

dict = {'0' : case_0, '1' : case_1, '2' : case_2, '3' : case_3, '4' : case_4, '5' : case_5, '6' : case_6, '7' : case_7, '8' : case_8, '9' : case_9, '.' : case_10, ',' : case_11}

def switch(caractere):
    try:
        dict[caractere]()
    except:
        case_default()

entrada = str(input('Digite o valor desejado: '))

while i < len(entrada):
    caractere = entrada[i]
    switch(caractere)
    i += 1

print (saida)
