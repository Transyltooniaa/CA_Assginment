clock_cycle = 0

dictionary = {
    '00000': 'zero',
    '00001': 'at',
    '00010': 'v0',
    '00011': 'v1',
    '00100': 'a0',
    '00101': 'a1',
    '00110': 'a2',
    '00111': 'a3',
    '10000': 's0',
    '10001': 's1',
    '10010': 's2',
    '10011': 's3',
    '10100': 's4',
    '10101': 's5',
    '10110': 's6',
    '10111': 's7',
    '01000': 't0',
    '01001': 't1',
    '01010': 't2',
    '01011': 't3',
    '01100': 't4',
    '01101': 't5',
    '01110': 't6',
    '11000': 't8',
    '11001': 't9',
    '01111': 't7',
    '11010': 'gp',
    '11011': 'sp',
    '11100': 'fp',
    '11101': 'sp',
    '000000': 'sll',
    '000010': 'srl',
    '000011': 'sra',
    '000100': 'sllv',
    '000110': 'srlv',
    '000111': 'srav',
    '001010': 'slti',
    '100000': 'add',
    '100001': 'addu',
    '100011': 'subu',
    '100100': 'and',
    '100101': 'or',
    '100001': 'move', # function
    '001000': 'addi',
    '001001': 'addiu', 
    '100010': 'sub',  # function
    '100011': 'lw',
    '101011': 'sw',
    '101010': 'slt',  # function
    '000100': 'beq',
    '000101': 'bne',
    '000010': 'j',
    '000011': 'jal',
    '11111': 'ra',
    '011100': 'mul'
}

def binaryToDecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return str(decimal)


def flip(c): 
    return '1' if (c == '0') else '0' 


def twos_comp(bin): # Function prints the one's and two's complement of binary number bin
    n = len(bin)
    ones = ""
    twos = "" 
    for i in range(n): # Compute the one's complement by flipping the bits
        ones += flip(bin[i])

    ones = list(ones.strip("")) 
    twos = list(ones) # Compute 2's complement by adding 1 to the one's complement

    for i in range(n - 1, -1, -1):  # Start from the rightmost bit and keep flipping the bits until we find a 1 
        if (ones[i] == '1'):
            twos[i] = '0'

        else:
            twos[i] = '1'
            break

    i -= 1
    if (i == -1):
        twos.insert(0, '1')

    return twos # Return the 2's complement

def rTypeDecoder(machineCode):
    rs = machineCode[6:11]
    rt = machineCode[11:16]
    rd = machineCode[16:21]
    shamt = machineCode[21:26]
    funct = machineCode[26:32]

    if(funct == '001000'):
        return ["jr", dictionary[rs]]

    if(dictionary[funct] == 'move'):
        return [dictionary[funct],dictionary[rd] ,dictionary[rt]]
    
    return [dictionary[funct],dictionary[rd] ,dictionary[rs] , dictionary[rt]]

def iTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    rs = machineCode[6:11]
    rt = machineCode[11:16]
    immediate = machineCode[16:32]

    if(dictionary[opcode] == 'sw' or dictionary[opcode] == 'lw'):
        return [dictionary[opcode],dictionary[rt], binaryToDecimal(immediate), dictionary[rs]]
    
    elif(dictionary[opcode] == "slti" or dictionary[opcode] == "addi" or dictionary[opcode] == "addiu" ):
        return [dictionary[opcode],dictionary[rt], dictionary[rs], binaryToDecimal(immediate)]
    
    elif(dictionary[opcode] == "mul"):
        return [dictionary[opcode],dictionary[rs], dictionary[rt], dictionary[rt]]
    
    if(immediate[0] == "0"):
        return [dictionary[opcode],dictionary[rs], dictionary[rt], binaryToDecimal(immediate)]
    
    return [dictionary[opcode],dictionary[rs], dictionary[rt], str(-1*int(binaryToDecimal(twos_comp(immediate))))]


def jTypeDecoder(machineCode):
    opcode = machineCode[0:6]
    address = machineCode[6:32]

    return [dictionary[opcode], binaryToDecimal(address)]


def instructionDecoder(machineCode):
    # clock_cycle += 1
    if(machineCode[0:6] == '000000'):
        return rTypeDecoder(machineCode)
    
    elif(machineCode[0:6] == '000010' or machineCode[0:6] == '000010' or machineCode[0:6] == '000011') :
        return jTypeDecoder(machineCode)
    
    else:
        return iTypeDecoder(machineCode)

pc = 4194380

#Fibonacci
#f(0) = 1, f(1) = 1
# The last 5 digits of the first line are the input for the fibonacci function
listOfInstructions = []
InstructionHashmap = {} # Key: PC, Value:
dave_list = [] # loop names , Pc address

#Read input from file
def Fetch_Phase(file_path):
    input_data = []
    with open(file_path, 'r') as file:
        input_data = file.read()
        input_data = input_data.split()
        for i in range(len(input_data)):
            input_data[i] = input_data[i].strip()
    return input_data

file_path = "Fibonacci.txt"  # Replace with the actual file path
input_data = Fetch_Phase(file_path)

for i in input_data:
    clock_cycle += 1
    listOfInstructions.append(instructionDecoder(i))
    InstructionHashmap[pc] = instructionDecoder(i)
    pc += 4


def identify_labels(InstructionHashmap):
    labels = {}
    loop_count = 0 # for naming the labels
    loop_count_2 = 0 # for naming the la

    for i in InstructionHashmap:
        loop_count_2 += 1
        if(InstructionHashmap[i][0] == 'beq' or InstructionHashmap[i][0] == 'bne'):
            loop_count += 1
            pc_key = int(i) + 4 + (4 * int(InstructionHashmap[i][3]))
            labels[str(pc_key)] = f"loop{loop_count}"
            InstructionHashmap[i][3] = labels[str(pc_key)]
            listOfInstructions[loop_count_2-1][3] = labels[str(pc_key)] 

        elif(InstructionHashmap[i][0] == 'j' or InstructionHashmap[i][0] == 'jal'):
            loop_count += 1
            pc_key = int(InstructionHashmap[i][1]) * 4
            if(str(pc_key) not in labels.keys()):
                labels[str(pc_key)] = f"loop{loop_count}"
                InstructionHashmap[i][1] = labels[str(pc_key)]
                listOfInstructions[loop_count_2-1][1] = labels[str(pc_key)]
            elif(str(pc_key) in labels.keys()):
                InstructionHashmap[i][1] = labels[str(pc_key)]
                listOfInstructions[loop_count_2-1][1] = labels[str(pc_key)]

            else:
                continue    
    
    sorted_labels = dict(sorted(labels.items()))
    return sorted_labels

label_dict = identify_labels(InstructionHashmap)

for i in label_dict:
    temp = [label_dict[i], [i]]
    dave_list.append(temp)