import argparse
parser = argparse.ArgumentParser(description='original and plagiat')
parser.add_argument('indir', type=str, help='Input dir for two texts')
parser.add_argument('outdir', type=str, help='Output dir for results')
args = parser.parse_args()
inDir = args.indir
outDir = args.outdir

inDir = open(args.indir, "r")
finDir = inDir.read()
outDir = open(args.outdir, "w")

def redRange(S1, S2):  # вычисление редакционного расстояния методом Левенштейна
    S1 = list(S1)
    S2 = list(S2)
    def m(s1, s2):  # функция сравнения для Левенштейна
        if s1 == s2:
            return 0
        else:
            return 1

    D = []  # будущая матрица значений

    for i in range(len(S2) + 1):  # Заполнение главной строки и столбца матрицы(где вписываются исходные значения)
        D.append([0] * (len(S1) + 1))
    S1 = [0] + S1
    S2 = [0] + S2

    for i in range(len(D)):  # Заполнение матрицы методом Вагнера-Фишера
        for j in range(len(D[0])):
            if i == 0 and j == 0:
                D[i][j] = 0
            if j == 0 and i > 0:
                D[i][j] = i
            if i == 0 and j > 0:
                D[i][j] = j
            if j > 0 and i > 0:
                mnl1 = D[i][j - 1] + 1
                mnl2 = D[i - 1][j] + 1
                mnl3 = D[i - 1][j - 1] + m(S1[j], S2[i])
                D[i][j] = min(mnl1, mnl2, mnl3)
    return(D[len(D) - 1][len(D[0]) - 1])

def clean(l):  # функция очистки списка от пустых значений(в случае наличия больше одного пробела/переноса строки подряд)
    res = []
    for i in range(len(l)):
        if l[i] != '':
            res.append(l[i])
    return res


b = list(finDir.split("\n"))
b = clean(b)
c = []  # список списков пар адресов доков для сверки
for i in range(len(b)):
    c.append(b[i].split(' '))
for i in range(len(c)):
    c[i] = clean(c[i])

for i in range(len(c)):
    F1 = open(c[i][0], "r")
    file1 = F1.read()   # оригинал
    F2 = open(c[i][1], "r")
    file2 = F2.read()  # плагиат
    l1 = len(file1)
    l2 = len(file2)
    if l1 == 0 and l2 == 0:
        R = "100"
    elif redRange(file1, file2) == 0:
        R = "100"
    elif redRange(file1, file2) >= l1:
        R = "0"
    else:
        R = 1.0 - redRange(file1, file2) / l1
        R = R*100
        R = int(R)

    outDir.write(str(R))
    outDir.write("%")
    outDir.write("\n")

