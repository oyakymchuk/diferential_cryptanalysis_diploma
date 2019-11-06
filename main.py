import time
from math import log
from operator import itemgetter
import matplotlib.pylab as plt

s = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]

def byte_plus(x, y):
    return (x + y) & ((1 << 8) - 1)

def modulo_plus(x, y):
    result = []
    mu = 0
    for i in range(4):
        X = (x & ((1 << 8) - 1))
        x = x >> 8
        Y = (y & ((1 << 8) - 1))
        y = y >> 8
        result.append((X + Y + mu) & ((1 << 8) - 1))
        # print(X, Y, mu,  ((1 << 8) - 1))
        mu = (X + Y + mu) >> 8
    return result[0] ^ (result[1] << 8) ^ (result[2] << 16) ^ (result[3] << 24)

def s_box(x):           #для 8 бітів
    return s[x]

def s_block(x):         #для х -  32 бітів
    Y = []
    for i in range(4):
        Y.append(s[x & ((1 << 8) - 1)])
        x = x >> 8
    return  Y[0] ^ (Y[1] << 8) ^ (Y[2] << 16) ^ (Y[3] << 24)

def simple_round_function(x, k):
    return s_block(modulo_plus(x, k))

def to_template_8(x):           #приймає байт і переводить його в шаблон
    if (x == 0):
        x_hat = '0'
    elif (x == 1):
        x_hat = '1'
    elif (x == 255):
        x_hat = '-1'
    else:
        x_hat = '*'
    return x_hat

def to_template_32(x):          #приймає 32-бітне число і повертає побайтовий його шаблон
    result = []
    x_in_byte_array = []
    for i in range(4):
        x_in_byte_array.append(x & ((1 << 8) - 1))
        x = x >> 8
    x_in_byte_array = x_in_byte_array[::-1]
    for i in x_in_byte_array:
        result.append(to_template_8(i))
    return result

def template_to_number(x_hat):
    if (x_hat == '0'):
        x = [0]
    elif (x_hat == '1'):
        x = [1]
    elif (x_hat == '-1'):
        x = [255]
    elif (x_hat == '2'):
        x = [2]
    elif (x_hat == '-2'):
        x = [254]
    else:
        x = []
        for i in range (2, 255):
            x. append(i)
    return x



def DP_s_xor(alpha_byte, beta_byte):            #приймає 8-бітні числа та повертає середню за входами імовірність диференціалу_{+,xor}^{s} (альфа, бета)
    x_byte = 0
    result = 0
    while x_byte < (1 << 8):
        result += s_box(byte_plus(x_byte,  alpha_byte)) == s_box(x_byte) ^ beta_byte
        x_byte += 1
    return result / 0x100

def DP_s_plus(alpha_byte, beta_byte):            #приймає 8-бітні числа та повертає середню за входами імовірність диференціалу_{+,+}^{s} (альфа, бета)
    x_byte = 0
    result = 0
    while x_byte < (1 << 8):
        result += s_box(byte_plus(x_byte,  alpha_byte)) == byte_plus(s_box(x_byte), beta_byte)
        x_byte += 1
    return result / 0x100


def UB_s_xor (alpha_hat, beta_hat):
    alpha_temp = template_to_number(alpha_hat)
    beta_temp = template_to_number(beta_hat)
    if (len(alpha_temp) != 1):
        if (len(beta_temp) != 1):
            DPs_temp = 0
            for alpha_byte in alpha_temp:
                for beta_byte in beta_temp:
                    if (DP_s_xor(alpha_byte, beta_byte) > DPs_temp):
                        DPs_temp = DP_s_xor(alpha_byte, beta_byte)
            return DPs_temp
        else:
            DPs_temp = 0
            for byte in alpha_temp:
                if (DP_s_xor(byte, beta_temp[0]) > DPs_temp):
                    DPs_temp = DP_s_xor(byte, beta_temp[0])
            return DPs_temp
    else:
        if (len(beta_temp) != 1):
            DPs_temp = 0
            for byte in beta_temp:
                if (DP_s_xor(alpha_temp[0], byte) > DPs_temp):
                    DPs_temp = DP_s_xor(alpha_temp[0], byte)
            return DPs_temp
        else:
            return DP_s_xor(alpha_temp[0], beta_temp[0])

def UB_s_plus (alpha_hat, beta_hat):
    alpha_temp = template_to_number(alpha_hat)
    beta_temp = template_to_number(beta_hat)
    if (len(alpha_temp) != 1):
        if (len(beta_temp) != 1):
            DPs_temp = 0
            for alpha_byte in alpha_temp:
                for beta_byte in beta_temp:
                    if (DP_s_plus(alpha_byte, beta_byte) > DPs_temp):
                        DPs_temp = DP_s_plus(alpha_byte, beta_byte)
            return DPs_temp
        else:
            DPs_temp = 0
            for byte in alpha_temp:
                if (DP_s_plus(byte, beta_temp[0]) > DPs_temp):
                    DPs_temp = DP_s_plus(byte, beta_temp[0])
            return DPs_temp
    else:
        if (len(beta_temp) != 1):
            DPs_temp = 0
            for byte in beta_temp:
                if (DP_s_plus(alpha_temp[0], byte) > DPs_temp):
                    DPs_temp = DP_s_plus(alpha_temp[0], byte)
            return DPs_temp
        else:
            return DP_s_plus(alpha_temp[0], beta_temp[0])



Omega_help_alphabet = ['0', '1', '2', '-1', '-2', '*']

# Omega_alphabet_prob_plus_virgin = [[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0]]
# Omega_alphabet_prob_xor_virgin = [[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0]]
# for i in range(6):
#     for j in range(6):
#         Omega_alphabet_prob_plus_virgin[i][j] = UB_s_plus(Omega_help_alphabet[i], Omega_help_alphabet[j])
# print(Omega_alphabet_prob_plus_virgin)

#Обраховані раніше значення імовірностей диференціалів відносно xor та + для шаблонів
DP_xor = [[1.0, 0.0, 0.0, 0.0, 0.0, 0], [0.0, 0.0078125, 0.0, 0.0078125, 0.00390625, 0.01953125], [0.0, 0.0, 0.00390625, 0.01171875, 0.00390625, 0.015625], [0.0, 0.0078125, 0.0, 0.0078125, 0.00390625, 0.01953125], [0.0, 0.0, 0.00390625, 0.01171875, 0.00390625, 0.015625], [0, 0.015625, 0.01953125, 0.01953125, 0.01953125, 0.02734375]]
DP_plus = [[1.0, 0.0, 0.0, 0.0, 0.0, 0], [0.0, 0.0078125, 0.00390625, 0.00390625, 0.0, 0.01953125], [0.0, 0.0, 0.00390625, 0.01171875, 0.0, 0.015625], [0.0, 0.00390625, 0.0, 0.0078125, 0.00390625, 0.01953125], [0.0, 0.01171875, 0.0, 0.0, 0.00390625, 0.015625], [0, 0.01953125, 0.01953125, 0.01953125, 0.01953125, 0.02734375]]

#for xor templates: 0,1,-1,*
# UB_matrix_xor = [[1, max([DP_xor[1][1], DP_xor[3][1]]), max([DP_xor[1][3], DP_xor[3][3]]), max([DP_xor[1][5], DP_xor[3][5]])],
#                  [1, max([DP_xor[1][1], DP_xor[2][1]]), max([DP_xor[1][3], DP_xor[2][3]]), max([DP_xor[1][5], DP_xor[2][5]])],
#                  [1, max([DP_xor[3][1], DP_xor[4][1]]), max([DP_xor[3][3], DP_xor[4][3]]), max([DP_xor[3][5], DP_xor[4][5]])],
                 # [0, max([DP_xor[5][1], DP_xor[1][1], DP_xor[3][1]]), max([DP_xor[5][3], DP_xor[3][3], DP_xor[1][3]]), max([DP_xor[5][5], DP_xor[3][5], DP_xor[1][5]])]]
# print(UB_matrix_xor)

UB_matrix_xor = [[1, 0.0078125, 0.0078125, 0.01953125], [1, 0.0078125, 0.01171875, 0.01953125], [1, 0.0078125, 0.01171875, 0.01953125], [0, 0.015625, 0.01953125, 0.02734375]]


# for_mod plus templates: 0,-1,*
# UB_matrix_mod_plus = [[1, 1, max([DP_plus[1][5], DP_plus[1][3]])],
#                       [1, 1, max([DP_plus[3][5], DP_plus[3][3]])],
#                       [0, max([DP_plus[5][3], DP_plus[3][3]]), max(DP_plus[5][5], DP_plus[3][5])]]
# print(UB_matrix_mod_plus)

UB_matrix_mod_plus = [[1, 1, 0.01953125], [1, 1, 0.01953125], [0, 0.01953125, 0.02734375]]


#for box plus templates: 0, 1, -1, *
# UB_matrix_box_plus = [[1, max([DP_plus[1][1], DP_plus[3][1]]), max([DP_plus[1][3], DP_plus[3][3]]), max([DP_plus[1][5], DP_plus[3][5]])],
#                  [1, max([DP_plus[1][1], DP_plus[2][1]]), max([DP_plus[1][3], DP_plus[2][3]]), max([DP_plus[1][5], DP_plus[2][5]])],
#                  [1, max([DP_plus[3][1], DP_plus[4][1]]), max([DP_plus[3][3], DP_plus[4][3]]), max([DP_plus[3][5], DP_plus[4][5]])],
#                  [0, max([DP_plus[5][1], DP_plus[1][1], DP_plus[3][1]]), max([DP_plus[5][3], DP_plus[3][3], DP_plus[1][3]]), max([DP_plus[5][5], DP_plus[3][5], DP_plus[1][5]])]]
# print(UB_matrix_box_plus)

UB_matrix_box_plus = [[1, 0.0078125, 0.0078125, 0.01953125], [1, 0.0078125, 0.01171875, 0.01953125], [1, 0.01171875, 0.0078125, 0.01953125], [0, 0.01953125, 0.01953125, 0.02734375]]

def get_template_index_xor(x):
    template_indexes = {'0': 0, '1': 1, '-1': 2, '*': 3}
    return template_indexes[x]

def get_template_index_mod_plus(x):
    template_indexes = {'0': 0, '-1': 1, '*': 2}
    return template_indexes[x]

#UB_F - для всього вектора омега, тобто для чотирьох шаблонів
def UB_F_xor(omega_vector_in, omega_vector_out):
    result = 1
    for i in range(4):
        in_index = get_template_index_xor(omega_vector_in[i])
        out_index = get_template_index_xor(omega_vector_out[i])
        result = result * UB_matrix_xor[in_index][out_index]
    return result

def UB_F_mod_plus(omega_vector_in, omega_vector_out):
    result = 1
    for i in range(4):
        in_index = get_template_index_mod_plus(omega_vector_in[i])
        out_index = get_template_index_mod_plus(omega_vector_out[i])
        result = result * UB_matrix_mod_plus[in_index][out_index]
    return result

def UB_F_box_plus(omega_vector_in, omega_vector_out):
    result = 1
    for i in range(4):
        in_index = get_template_index_xor(omega_vector_in[i])
        out_index = get_template_index_xor(omega_vector_out[i])
        result = result * UB_matrix_box_plus[in_index][out_index]
    return result

#UB_E - для кожного великого Омега
def UB_E_xor(omega_vector):
    result = 1
    for i in range(len(omega_vector) - 1):
        result = result * UB_F_xor(omega_vector[i], omega_vector[i + 1])
    return result

def UB_E_mod_plus(omega_vector):
    result = 1
    for i in range(len(omega_vector) - 1):
        result = result * UB_F_mod_plus(omega_vector[i], omega_vector[i + 1])
    return result

def UB_E_box_plus(omega_vector):
    result = 1
    for i in range(len(omega_vector) - 1):
        result = result * UB_F_box_plus(omega_vector[i], omega_vector[i + 1])
    return result

# тепер треба якось обрахувати для всіх можливих великих Омега UB_E...?


# all_omega_vectors було обраховано один раз - всі можливі шаблони
# alphabet = ['0','-1','*']
#
# all_omega_vectors_mod_plus = []
# for i in alphabet:
#     for j in alphabet:
#         for k in alphabet:
#             for l in alphabet:
#                 all_omega_vectors_mod_plus.append([i,j,k,l])
# print(all_omega_vectors_mod_plus)
# print(len(all_omega_vectors_mod_plus))

all_omega_vectors_xor = [['0', '0', '0', '0'], ['0', '0', '0', '1'], ['0', '0', '0', '-1'], ['0', '0', '0', '*'], ['0', '0', '1', '0'], ['0', '0', '1', '1'], ['0', '0', '1', '-1'], ['0', '0', '1', '*'], ['0', '0', '-1', '0'], ['0', '0', '-1', '1'], ['0', '0', '-1', '-1'], ['0', '0', '-1', '*'], ['0', '0', '*', '0'], ['0', '0', '*', '1'], ['0', '0', '*', '-1'], ['0', '0', '*', '*'], ['0', '1', '0', '0'], ['0', '1', '0', '1'], ['0', '1', '0', '-1'], ['0', '1', '0', '*'], ['0', '1', '1', '0'], ['0', '1', '1', '1'], ['0', '1', '1', '-1'], ['0', '1', '1', '*'], ['0', '1', '-1', '0'], ['0', '1', '-1', '1'], ['0', '1', '-1', '-1'], ['0', '1', '-1', '*'], ['0', '1', '*', '0'], ['0', '1', '*', '1'], ['0', '1', '*', '-1'], ['0', '1', '*', '*'], ['0', '-1', '0', '0'], ['0', '-1', '0', '1'], ['0', '-1', '0', '-1'], ['0', '-1', '0', '*'], ['0', '-1', '1', '0'], ['0', '-1', '1', '1'], ['0', '-1', '1', '-1'], ['0', '-1', '1', '*'], ['0', '-1', '-1', '0'], ['0', '-1', '-1', '1'], ['0', '-1', '-1', '-1'], ['0', '-1', '-1', '*'], ['0', '-1', '*', '0'], ['0', '-1', '*', '1'], ['0', '-1', '*', '-1'], ['0', '-1', '*', '*'], ['0', '*', '0', '0'], ['0', '*', '0', '1'], ['0', '*', '0', '-1'], ['0', '*', '0', '*'], ['0', '*', '1', '0'], ['0', '*', '1', '1'], ['0', '*', '1', '-1'], ['0', '*', '1', '*'], ['0', '*', '-1', '0'], ['0', '*', '-1', '1'], ['0', '*', '-1', '-1'], ['0', '*', '-1', '*'], ['0', '*', '*', '0'], ['0', '*', '*', '1'], ['0', '*', '*', '-1'], ['0', '*', '*', '*'], ['1', '0', '0', '0'], ['1', '0', '0', '1'], ['1', '0', '0', '-1'], ['1', '0', '0', '*'], ['1', '0', '1', '0'], ['1', '0', '1', '1'], ['1', '0', '1', '-1'], ['1', '0', '1', '*'], ['1', '0', '-1', '0'], ['1', '0', '-1', '1'], ['1', '0', '-1', '-1'], ['1', '0', '-1', '*'], ['1', '0', '*', '0'], ['1', '0', '*', '1'], ['1', '0', '*', '-1'], ['1', '0', '*', '*'], ['1', '1', '0', '0'], ['1', '1', '0', '1'], ['1', '1', '0', '-1'], ['1', '1', '0', '*'], ['1', '1', '1', '0'], ['1', '1', '1', '1'], ['1', '1', '1', '-1'], ['1', '1', '1', '*'], ['1', '1', '-1', '0'], ['1', '1', '-1', '1'], ['1', '1', '-1', '-1'], ['1', '1', '-1', '*'], ['1', '1', '*', '0'], ['1', '1', '*', '1'], ['1', '1', '*', '-1'], ['1', '1', '*', '*'], ['1', '-1', '0', '0'], ['1', '-1', '0', '1'], ['1', '-1', '0', '-1'], ['1', '-1', '0', '*'], ['1', '-1', '1', '0'], ['1', '-1', '1', '1'], ['1', '-1', '1', '-1'], ['1', '-1', '1', '*'], ['1', '-1', '-1', '0'], ['1', '-1', '-1', '1'], ['1', '-1', '-1', '-1'], ['1', '-1', '-1', '*'], ['1', '-1', '*', '0'], ['1', '-1', '*', '1'], ['1', '-1', '*', '-1'], ['1', '-1', '*', '*'], ['1', '*', '0', '0'], ['1', '*', '0', '1'], ['1', '*', '0', '-1'], ['1', '*', '0', '*'], ['1', '*', '1', '0'], ['1', '*', '1', '1'], ['1', '*', '1', '-1'], ['1', '*', '1', '*'], ['1', '*', '-1', '0'], ['1', '*', '-1', '1'], ['1', '*', '-1', '-1'], ['1', '*', '-1', '*'], ['1', '*', '*', '0'], ['1', '*', '*', '1'], ['1', '*', '*', '-1'], ['1', '*', '*', '*'], ['-1', '0', '0', '0'], ['-1', '0', '0', '1'], ['-1', '0', '0', '-1'], ['-1', '0', '0', '*'], ['-1', '0', '1', '0'], ['-1', '0', '1', '1'], ['-1', '0', '1', '-1'], ['-1', '0', '1', '*'], ['-1', '0', '-1', '0'], ['-1', '0', '-1', '1'], ['-1', '0', '-1', '-1'], ['-1', '0', '-1', '*'], ['-1', '0', '*', '0'], ['-1', '0', '*', '1'], ['-1', '0', '*', '-1'], ['-1', '0', '*', '*'], ['-1', '1', '0', '0'], ['-1', '1', '0', '1'], ['-1', '1', '0', '-1'], ['-1', '1', '0', '*'], ['-1', '1', '1', '0'], ['-1', '1', '1', '1'], ['-1', '1', '1', '-1'], ['-1', '1', '1', '*'], ['-1', '1', '-1', '0'], ['-1', '1', '-1', '1'], ['-1', '1', '-1', '-1'], ['-1', '1', '-1', '*'], ['-1', '1', '*', '0'], ['-1', '1', '*', '1'], ['-1', '1', '*', '-1'], ['-1', '1', '*', '*'], ['-1', '-1', '0', '0'], ['-1', '-1', '0', '1'], ['-1', '-1', '0', '-1'], ['-1', '-1', '0', '*'], ['-1', '-1', '1', '0'], ['-1', '-1', '1', '1'], ['-1', '-1', '1', '-1'], ['-1', '-1', '1', '*'], ['-1', '-1', '-1', '0'], ['-1', '-1', '-1', '1'], ['-1', '-1', '-1', '-1'], ['-1', '-1', '-1', '*'], ['-1', '-1', '*', '0'], ['-1', '-1', '*', '1'], ['-1', '-1', '*', '-1'], ['-1', '-1', '*', '*'], ['-1', '*', '0', '0'], ['-1', '*', '0', '1'], ['-1', '*', '0', '-1'], ['-1', '*', '0', '*'], ['-1', '*', '1', '0'], ['-1', '*', '1', '1'], ['-1', '*', '1', '-1'], ['-1', '*', '1', '*'], ['-1', '*', '-1', '0'], ['-1', '*', '-1', '1'], ['-1', '*', '-1', '-1'], ['-1', '*', '-1', '*'], ['-1', '*', '*', '0'], ['-1', '*', '*', '1'], ['-1', '*', '*', '-1'], ['-1', '*', '*', '*'], ['*', '0', '0', '0'], ['*', '0', '0', '1'], ['*', '0', '0', '-1'], ['*', '0', '0', '*'], ['*', '0', '1', '0'], ['*', '0', '1', '1'], ['*', '0', '1', '-1'], ['*', '0', '1', '*'], ['*', '0', '-1', '0'], ['*', '0', '-1', '1'], ['*', '0', '-1', '-1'], ['*', '0', '-1', '*'], ['*', '0', '*', '0'], ['*', '0', '*', '1'], ['*', '0', '*', '-1'], ['*', '0', '*', '*'], ['*', '1', '0', '0'], ['*', '1', '0', '1'], ['*', '1', '0', '-1'], ['*', '1', '0', '*'], ['*', '1', '1', '0'], ['*', '1', '1', '1'], ['*', '1', '1', '-1'], ['*', '1', '1', '*'], ['*', '1', '-1', '0'], ['*', '1', '-1', '1'], ['*', '1', '-1', '-1'], ['*', '1', '-1', '*'], ['*', '1', '*', '0'], ['*', '1', '*', '1'], ['*', '1', '*', '-1'], ['*', '1', '*', '*'], ['*', '-1', '0', '0'], ['*', '-1', '0', '1'], ['*', '-1', '0', '-1'], ['*', '-1', '0', '*'], ['*', '-1', '1', '0'], ['*', '-1', '1', '1'], ['*', '-1', '1', '-1'], ['*', '-1', '1', '*'], ['*', '-1', '-1', '0'], ['*', '-1', '-1', '1'], ['*', '-1', '-1', '-1'], ['*', '-1', '-1', '*'], ['*', '-1', '*', '0'], ['*', '-1', '*', '1'], ['*', '-1', '*', '-1'], ['*', '-1', '*', '*'], ['*', '*', '0', '0'], ['*', '*', '0', '1'], ['*', '*', '0', '-1'], ['*', '*', '0', '*'], ['*', '*', '1', '0'], ['*', '*', '1', '1'], ['*', '*', '1', '-1'], ['*', '*', '1', '*'], ['*', '*', '-1', '0'], ['*', '*', '-1', '1'], ['*', '*', '-1', '-1'], ['*', '*', '-1', '*'], ['*', '*', '*', '0'], ['*', '*', '*', '1'], ['*', '*', '*', '-1'], ['*', '*', '*', '*']]

all_omega_vectors_mod_plus = [['0', '0', '0', '0'], ['0', '0', '0', '-1'], ['0', '0', '0', '*'], ['0', '0', '-1', '0'], ['0', '0', '-1', '-1'], ['0', '0', '-1', '*'], ['0', '0', '*', '0'], ['0', '0', '*', '-1'], ['0', '0', '*', '*'], ['0', '-1', '0', '0'], ['0', '-1', '0', '-1'], ['0', '-1', '0', '*'], ['0', '-1', '-1', '0'], ['0', '-1', '-1', '-1'], ['0', '-1', '-1', '*'], ['0', '-1', '*', '0'], ['0', '-1', '*', '-1'], ['0', '-1', '*', '*'], ['0', '*', '0', '0'], ['0', '*', '0', '-1'], ['0', '*', '0', '*'], ['0', '*', '-1', '0'], ['0', '*', '-1', '-1'], ['0', '*', '-1', '*'], ['0', '*', '*', '0'], ['0', '*', '*', '-1'], ['0', '*', '*', '*'], ['-1', '0', '0', '0'], ['-1', '0', '0', '-1'], ['-1', '0', '0', '*'], ['-1', '0', '-1', '0'], ['-1', '0', '-1', '-1'], ['-1', '0', '-1', '*'], ['-1', '0', '*', '0'], ['-1', '0', '*', '-1'], ['-1', '0', '*', '*'], ['-1', '-1', '0', '0'], ['-1', '-1', '0', '-1'], ['-1', '-1', '0', '*'], ['-1', '-1', '-1', '0'], ['-1', '-1', '-1', '-1'], ['-1', '-1', '-1', '*'], ['-1', '-1', '*', '0'], ['-1', '-1', '*', '-1'], ['-1', '-1', '*', '*'], ['-1', '*', '0', '0'], ['-1', '*', '0', '-1'], ['-1', '*', '0', '*'], ['-1', '*', '-1', '0'], ['-1', '*', '-1', '-1'], ['-1', '*', '-1', '*'], ['-1', '*', '*', '0'], ['-1', '*', '*', '-1'], ['-1', '*', '*', '*'], ['*', '0', '0', '0'], ['*', '0', '0', '-1'], ['*', '0', '0', '*'], ['*', '0', '-1', '0'], ['*', '0', '-1', '-1'], ['*', '0', '-1', '*'], ['*', '0', '*', '0'], ['*', '0', '*', '-1'], ['*', '0', '*', '*'], ['*', '-1', '0', '0'], ['*', '-1', '0', '-1'], ['*', '-1', '0', '*'], ['*', '-1', '-1', '0'], ['*', '-1', '-1', '-1'], ['*', '-1', '-1', '*'], ['*', '-1', '*', '0'], ['*', '-1', '*', '-1'], ['*', '-1', '*', '*'], ['*', '*', '0', '0'], ['*', '*', '0', '-1'], ['*', '*', '0', '*'], ['*', '*', '-1', '0'], ['*', '*', '-1', '-1'], ['*', '*', '-1', '*'], ['*', '*', '*', '0'], ['*', '*', '*', '-1'], ['*', '*', '*', '*']]




start_time = time.time()
#
# #розподіл для xor
#
freq_xor = {}

for i in all_omega_vectors_xor:
    for j in all_omega_vectors_xor:
        a = UB_E_xor([ i, j])
        if (a not in freq_xor.keys()):
            freq_xor[a] = 1
        else:
            freq_xor[a] += 1


sorted_freq_xor = sorted(freq_xor.items(), key=itemgetter(0))
sorted_freq_xor = sorted_freq_xor[1:]
sorted_freq_xor_log = [(log(e1)/log(2), e2) for e1, e2 in sorted_freq_xor]

plt.scatter(*zip(*sorted_freq_xor_log), s=1)
plt.xlabel('імовірність')
plt.ylabel('кількість')
plt.grid(color='black', linestyle='-', linewidth=0.1)
plt.vlines([e1 for e1, e2 in sorted_freq_xor_log], [0 for e1,e2 in sorted_freq_xor_log], [e2 for e1,e2 in sorted_freq_xor_log])
plt.show()



# plt.bar(list(sorted_freq_xor.keys()), sorted_freq_xor.values(), color='g')
# plt.show()


print('time: {0}'.format(time.time() - start_time))
# start_time = time.time()
#
#
# freq_xor = {}
#
# for k in all_omega_vectors_xor:
#     for i in all_omega_vectors_xor:
#         for j in all_omega_vectors_xor:
#             a = UB_E_xor([ k, i, j])
#             if (a not in freq_xor.keys()):
#                 freq_xor[a] = 1
#             else:
#                 freq_xor[a] += 1
#
# print('xor 2: ', freq_xor)
#
# print('time: {0}'.format(time.time() - start_time))
# start_time = time.time()
#
#
# freq_xor = {}
# z=1
# for l in all_omega_vectors_xor:
#     print(z)
#     for k in all_omega_vectors_xor:
#         for i in all_omega_vectors_xor:
#             for j in all_omega_vectors_xor:
#                 a = UB_E_xor([l, k, i, j])
#                 if (a not in freq_xor.keys()):
#                     freq_xor[a] = 1
#                 else:
#                     freq_xor[a] += 1
#     z = z + 1
#     print('time: {0}'.format(time.time() - start_time))

# print('xor 3: ', freq_xor)
#
# print('time: {0}'.format(time.time() - start_time))
# start_time = time.time()
#
#
# freq_xor = {}
#
# for x in all_omega_vectors_xor:
#     for l in all_omega_vectors_xor:
#         for k in all_omega_vectors_xor:
#             for i in all_omega_vectors_xor:
#                 for j in all_omega_vectors_xor:
#                     a = UB_E_xor([x, l, k, i, j])
#                     if (a not in freq_xor.keys()):
#                         freq_xor[a] = 1
#                     else:
#                         freq_xor[a] += 1
#
# print('xor 4: ', freq_xor)




#розподіл для mod_plus

# freq_mod_plus = {}
#
# for y in all_omega_vectors_xor:
#     for x in all_omega_vectors_xor:
#         for l in all_omega_vectors_xor:
#             for k in all_omega_vectors_xor:
#                 for i in all_omega_vectors_xor:
#                     for j in all_omega_vectors_xor:
#                         a = UB_E_mod_plus([y, x, l, k, i, j])
#                         if (a not in freq_xor.keys()):
#                             freq_xor[a] = 1
#                         else:
#                             freq_xor[a] += 1
#
# print('mod plus 6: ', freq_mod_plus)



#розподіл для box plus

# freq_box_plus = {}
# for y in all_omega_vectors_xor:
#     for x in all_omega_vectors_xor:
#         for l in all_omega_vectors_xor:
#             for k in all_omega_vectors_xor:
#                 for i in all_omega_vectors_xor:
#                     for j in all_omega_vectors_xor:
#                         a = UB_E_box_plus([y, x, l, k, i, j])
#                         if (a not in freq_xor.keys()):
#                             freq_xor[a] = 1
#                         else:
#                             freq_xor[a] += 1
# print('box plus 6: ', freq_box_plus)


# print('time: {0}'.format(time.time() - start_time))