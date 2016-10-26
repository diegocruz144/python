# Cria o arquivo csv e o cabeçário
arquivocsv = 'Deferimentos de vistos.csv'
saida = open(arquivocsv,'w')
saida.write("Conselho Nacional de Imigração Deferiu\n")
saida.write("Ano - Número do DOU - Data;Estrangeiro(a);Passaporte;Liberação;Observar\n")
# Define variável global para contar entradas
qtd = 0
# Abre uma lista de arquivos a serem lidos, criado para ler vários DOU's
listaarquivos = input("Digite o nome do arquivo: ")
arqnomes = open(listaarquivos+'.txt', 'r')
# Armazena os nomes por linhas
texto = arqnomes.readlines()
for linha in texto:
    # Retira a quebra de linha padrão windows e armazena só o nome do arquivo a ser lido
    nomedoarquivo = linha[0:len(linha)-1]
    # Concatena com a extenção do arquivo a ser lido (deixei separado pois vou utilizar o nome para identificar o DOU)
    arquivotxt = nomedoarquivo+'.txt'
    # Abre o texto e em seguida lê o texto armazenando na variável "texto"
    arq = open(arquivotxt, 'r')
    texto = arq.read()
    # retira as vírgulas
    texto = texto.replace(',','')
    # mantém os pontos porém separa das palavras (Gambiarra para corrigir alguns erros em passaportes)
    texto = texto.replace('.',' .')
    # Separa o texto em um vetor de strings
    texto = texto.split()

    item = 1
    combinacao = 0
    nome = ''
    liberacao = ''
    passaporte = ''
    inome = 0
    ipassaporte = 0
    obs = ''

    # Para cada palavra no texto ele irá executar as seguintes verificações
    for p in texto:
        # Precisamos identificar as deferições de vistos pelo conselho nacional de imigração
        # porém como ele lê palavra por palavra precisei criar um método de saber se a combinação procede
        # acrecentando 1 a cada palavra aceita lida ou zerando caso apareça uma palavra não aceita
        if p == 'Conselho':
            combinacao = 1
        elif combinacao == 1:
            if p == 'Nacional':
                combinacao += 1
            else:
                combinacao = 0
        elif combinacao == 2:
            if p == 'de':
                combinacao += 1
            else:
                combinacao = 0
        elif combinacao == 3:
            if p == 'Imigração':
                combinacao += 1
            else:
                combinacao = 0
        elif combinacao == 4:
            if p == 'deferiu':
                combinacao += 1
            else:
                combinacao = 0
        elif combinacao == 5:
            # Zera a informação de prazo para receber um novo ao identificar esta palavra
            if p == 'Prazo' or p == 'Prazo:':
                liberacao = ''
                combinacao += 1
            # As vezes o prazo é individual, outras é determinado no processo para vários imigrantes neste caso ele não zera a informação e
            # vai direto para coleta do nome do imigrante
            elif p == 'Estrangeiro:' or p == 'Estrangeira:':
                combinacao += 2
        elif combinacao == 6:
            # ele fica na coleta do prazo até que a palavra seja uma das opções, então vai para a coleta do nome.
            if p == 'Estrangeiro:' or p == 'Estrangeira:':
                combinacao += 1
            else:
                liberacao = liberacao+' '+p
        elif combinacao == 7:
            # se a palavra for passaporte ele vai para coleta do passaporte (alguns casos não tem)
            if p ==  'Passaporte:' or p == 'Passaporte':
                combinacao += 1
            # quando não há passaporte e é encotrado uma das opções abaixo ele imprime as informações no csv caso contrário fica armazenando as informações na variável nome
            elif p == 'Permanência' or p == 'Permanente' or p == 'Processo:' or p == 'Estrangeiro:' or p == 'Estrangeira:' or p == 'Temporário' or p == 'Visto':
                saida.write(nomedoarquivo+';'+nome+';'+passaporte+';'+liberacao+obs+'\n')
                qtd += 1
                nome = ''
                passaporte = ''
                inome = 0
                combinacao -= 2
            else:
                if inome == 0:
                    nome = p
                    inome = 1
                else:
                    nome = nome+' '+p
        elif combinacao == 8:
            # quando é encontrado uma dessas palavras encerra a busca e imprime a informação
            if p == 'Permanência' or p == 'Permanente' or p == 'Processo:' or p == 'Estrangeiro:' or p == 'Estrangeira:' or p == 'Temporário' or p == 'Visto' or p == 'Conselho':
                # adiciona o "*" para verificação de passaporte com menos que 6 dígitos (ex DOU 55 - 21 MAR 2014)
                if len(passaporte) < 6:
                        obs = "*"
                saida.write(nomedoarquivo+';'+nome+';'+passaporte+';'+liberacao+';'+obs+'\n')
                qtd += 1
                nome = ''
                inome = 0
                passaporte = ''
                ipassaporte = 0
                obs = ''
                # Existem 4 possíveis saídas:
                # quando identificar a palavra prazo tem que ir para a parte de armazena-lo
                if p == 'Prazo' or p == 'Prazo:':
                    combinacao -= 2
                # quando identificar a palavra Estrangeiro(a) tem que ir para a parte de armazenar o nome
                elif p == 'Estrangeiro:' or p == 'Estrangeira:':
                    combinacao -= 1
                # quando identificar a palavra Conselho tem que voltar ao início
                elif p == 'Conselho':
                    combinacao = 1
                # qualquer outra volta para o estágio 5
                else:
                    combinacao -= 3
            # alguns passaportes são o final de um processo então eles vem seguidos de um ponto final porém
            # outros vem com pontuação (ex 000.000.000 encontrado no DOU 185 - 24 SET 2012 - página 81 a 85) com o replace ele passa a ficar 000 .000 .000 então
            # essa condição faz com que ele identifique o ponto final.
            elif p == '.':
                obs = '**'
                saida.write(nomedoarquivo+';'+nome+';'+passaporte+';'+liberacao+';'+obs+'\n')
                qtd += 1
                nome = ''
                passaporte = ''
                inome = 0
                obs = ''
                combinacao -= 3
            # se não for nenhuma das anteriores é armazenado a informação do passaporte.
            else:
                if ipassaporte == 0:
                    passaporte = p
                    ipassaporte = 1
                else:
                    #tratamento dos passaportes com pontuação
                    if p[0] == '.':
                        passaporte = passaporte+p
                    else:
                        passaporte = passaporte+' '+p
    #Fecha o arquivo limpa o nome e vai para o próximo.
    arq.close()
    nomedoarquivo = ''

#transforma a quantidade em string para que possa ser concatenada com a escrita
qtde = str(qtd)
#escreve algumas informações e fecha o arquivo.
saida.write('\nQuantidade de estrangeiros:'+qtde+'\n')
saida.write('* Passaporte com menos que 6 caracteres'+'\n')
saida.write('** Verificar passaporte'+'\n')
saida.close()




