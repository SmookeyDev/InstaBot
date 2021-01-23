lista = []

filex = open('categories.txt', 'r')
for line in filex.readlines():
    lista.append(line.replace('\n', '').split(','))


print(lista)
