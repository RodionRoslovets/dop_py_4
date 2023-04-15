import re

with open('table.txt', 'r') as f:
    inputLines = f.readlines()
    f.close()

# Находим индекс строки с текстом DmTag
descrEndIndex = inputLines.index([line for line in inputLines if 'DmTag' in line][0])

# Создаем новый файл для записи описания
with open('descr.txt', 'w') as f:
    f.writelines(inputLines[:descrEndIndex])
    f.close()

# Обновляем адресацию в таблице
for i in range(descrEndIndex + 1, len(inputLines)):
    line = inputLines[i]
    newLine = line

    # Ищем одиночную адресацию в строке
    match = re.search(r'(DB\d+,DW\d+|DB\d+,DD\d+)', line)
    if match:
        if line.find('in  Word') == -1:
            addr = match.group(0)
            addrTypeRight = re.search(r'DW|DD', addr.split(',')[1]).group(0)
            addrNumLeft = int(re.search(r'\d+', addr.split(',')[0]).group(0))
            addrNumRight = int(re.search(r'\d+', addr.split(',')[1]).group(0))
            
            if addrNumLeft > 100:
                addrNumLeft *= 2

            if addrTypeRight == 'DW':
                addrNumRight *= 2
                addrTypeRight = 'DBW'
            elif addrTypeRight == 'DD':
                addrNumRight *= 2
                addrTypeRight = 'DBD'

            newLine = line.replace(addr, f'DB{addrNumLeft},{addrTypeRight}{addrNumRight}')
        
    # Ищем адресацию вида "10 in word DB225,DW152"
    match2 = re.search(r'(\d+) in  Word (DB\d+,DW\d+|DB\d+,DD\d+)', line)

    if match2:
        wordNum = int(match2.group(1))
        addr = match2.group(0)
        data = re.search(r'(DB\d+,DW\d+|DB\d+,DD\d+)', addr)
        addrNumLeft = int(re.search(r'\d+', data.group(0).split(',')[0]).group(0))
        addrTypeRight = re.search(r'DW|DD', addr.split(',')[1]).group(0)

        if 8 < wordNum <= 15:
            wordNum -= 8
            addrNumLeft *= 2
        elif 0 <= wordNum <= 8:
            addrNumLeft *= 2
            addrNumLeft += 1

        if addrTypeRight == 'DW':
            addrTypeRight = 'DBW'
        elif addrTypeRight == 'DD':
            addrTypeRight = 'DBD'

        newLine = line.replace(addr, f'{wordNum} in  Word DB{addrNumLeft},{addr.split(",")[1].replace(re.search(r"DW|DD", addr.split(",")[1]).group(0), addrTypeRight)}')
    inputLines[i] = newLine
        
# Записываем обновленную таблицу в файл
with open('output.txt', 'w') as f:
    f.writelines(inputLines)
    f.close()