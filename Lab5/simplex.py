from fractions import Fraction
from warnings import warn
from prettytable import PrettyTable
from colorama import Fore, Style, Back

class Simplex(object):
    def __init__(self, num_vars, constraints, objective_function):
        self.num_vars = num_vars
        self.constraints = constraints
        self.objective_function = objective_function
        self.coeff_matrix, self.r_rows, self.num_s_vars, self.num_r_vars = self.construct_matrix_from_constraints()
        del self.constraints
        self.basic_vars = [0 for i in range(len(self.coeff_matrix))]
        self.phase1()
        r_index = self.num_r_vars + self.num_s_vars

        for i in self.basic_vars:
            if i > r_index:
                raise ValueError("Нездійсненне рішення")

        self.delete_r_vars()

        self.solution = self.objective_maximize()
        self.optimize_val = self.coeff_matrix[0][-1]

    def print_simplex_table(self):
        x = PrettyTable()
        x.field_names = ['Базис'] + ['y' + str(i + 1) for i in range(len(self.coeff_matrix[0]) - 1)] + ['B']
        for i in range(1, len(self.coeff_matrix)):
            x.add_row(['y' + str(i + self.num_vars)] + self.coeff_matrix[i])
        
        x.add_row(['Z(y)'] + self.coeff_matrix[0])
        print(x)


    def construct_matrix_from_constraints(self):
        num_s_vars = 0
        num_r_vars = 0
        for expression in self.constraints:
            if '>=' in expression:
                num_s_vars += 1

            elif '<=' in expression:
                num_s_vars += 1
                num_r_vars += 1

            elif '=' in expression:
                num_r_vars += 1
        total_vars = self.num_vars + num_s_vars + num_r_vars

        coeff_matrix = [[Fraction("0/1") for i in range(total_vars+1)] for j in range(len(self.constraints)+1)]
        s_index = self.num_vars
        r_index = self.num_vars + num_s_vars
        r_rows = []
        for i in range(1, len(self.constraints)+1):
            constraint = self.constraints[i-1].split(' ')

            for j in range(len(constraint)):

                if '_' in constraint[j]:
                    coeff, index = constraint[j].split('_')
                    if constraint[j-1] == '-':
                        coeff_matrix[i][int(index)-1] = Fraction("-" + coeff[:-1] + "/1")
                    else:
                        coeff_matrix[i][int(index)-1] = Fraction(coeff[:-1] + "/1")

                elif constraint[j] == '<=':
                    coeff_matrix[i][s_index] = Fraction("1/1")
                    s_index += 1

                elif constraint[j] == '>=':
                    coeff_matrix[i][s_index] = Fraction("-1/1")
                    coeff_matrix[i][r_index] = Fraction("1/1")
                    s_index += 1
                    r_index += 1
                    r_rows.append(i)

                elif constraint[j] == '=':
                    coeff_matrix[i][r_index] = Fraction("1/1")
                    r_index += 1
                    r_rows.append(i)

            coeff_matrix[i][-1] = Fraction(constraint[-1] + "/1")

        
        return coeff_matrix, r_rows, num_s_vars, num_r_vars

    def phase1(self):
        r_index = self.num_vars + self.num_s_vars
        for i in range(r_index, len(self.coeff_matrix[0])-1):
            self.coeff_matrix[0][i] = Fraction("-1/1")
        coeff_0 = 0
        for i in self.r_rows:
            self.coeff_matrix[0] = add_row(self.coeff_matrix[0], self.coeff_matrix[i])
            self.basic_vars[i] = r_index
            r_index += 1
        s_index = self.num_vars
        for i in range(1, len(self.basic_vars)):
            if self.basic_vars[i] == 0:
                self.basic_vars[i] = s_index
                s_index += 1

        key_column = max_index(self.coeff_matrix[0])
        condition = self.coeff_matrix[0][key_column] > 0

        while condition is True:

            key_row = self.find_key_row(key_column = key_column)
            self.basic_vars[key_row] = key_column
            pivot = self.coeff_matrix[key_row][key_column]
            self.normalize_to_pivot(key_row, pivot)
            self.make_key_column_zero(key_column, key_row)

            key_column = max_index(self.coeff_matrix[0])
            condition = self.coeff_matrix[0][key_column] > 0

    def find_key_row(self, key_column):
        min_val = float("inf")
        min_i = 0
        for i in range(1, len(self.coeff_matrix)):
            if self.coeff_matrix[i][key_column] > 0:
                val = self.coeff_matrix[i][-1] / self.coeff_matrix[i][key_column]
                if val <  min_val:
                    min_val = val
                    min_i = i
        if min_val == float("inf"):
            raise ValueError("Необмежене рішення")
        if min_val == 0:
            warn("Error")
        return min_i

    def normalize_to_pivot(self, key_row, pivot):
        for i in range(len(self.coeff_matrix[0])):
            self.coeff_matrix[key_row][i] /= pivot

    def make_key_column_zero(self, key_column, key_row):
        num_columns = len(self.coeff_matrix[0])
        for i in range(len(self.coeff_matrix)):
            if i != key_row:
                factor = self.coeff_matrix[i][key_column]
                for j in range(num_columns):
                    self.coeff_matrix[i][j] -= self.coeff_matrix[key_row][j] * factor

    def delete_r_vars(self):
        for i in range(len(self.coeff_matrix)):
            non_r_length = self.num_vars + self.num_s_vars + 1
            length = len(self.coeff_matrix[i])
            while length != non_r_length:
                del self.coeff_matrix[i][non_r_length-1]
                length -= 1

    def update_objective_function(self):
        objective_function_coeffs = self.objective_function.split()
        for i in range(len(objective_function_coeffs)):
            if '_' in objective_function_coeffs[i]:
                coeff, index = objective_function_coeffs[i].split('_')
                if objective_function_coeffs[i-1] == '-':
                    self.coeff_matrix[0][int(index)-1] = Fraction(coeff[:-1] + "/1")
                else:
                    self.coeff_matrix[0][int(index)-1] = Fraction("-" + coeff[:-1] + "/1")

    def objective_maximize(self):
        self.update_objective_function()

        for row, column in enumerate(self.basic_vars[1:]):
            if self.coeff_matrix[0][column] != 0:
                self.coeff_matrix[0] = add_row(self.coeff_matrix[0], multiply_const_row(-self.coeff_matrix[0][column], self.coeff_matrix[row+1]))

        key_column = min_index(self.coeff_matrix[0])
        condition = self.coeff_matrix[0][key_column] < 0

        print(Fore.WHITE + "Початкова симплекс-таблиця:" + Style.RESET_ALL)
        self.print_simplex_table()

        print(Fore.WHITE + "\nДалі покроково показано розв'язання симплекс методом:" + Style.RESET_ALL)
        while condition is True:
            key_row = self.find_key_row(key_column = key_column)
            self.basic_vars[key_row] = key_column
            pivot = self.coeff_matrix[key_row][key_column]
            self.normalize_to_pivot(key_row, pivot)
            self.make_key_column_zero(key_column, key_row)

            key_column = min_index(self.coeff_matrix[0])
            condition = self.coeff_matrix[0][key_column] < 0
            self.print_simplex_table()
    
        print("\n" + Fore.WHITE + 'Кінцева симплекс-таблиця має наступний вигляд:' + Style.RESET_ALL)
        self.print_simplex_table() 
        solution = {}
        for i, var in enumerate(self.basic_vars[1:]):
            if var < self.num_vars:
                solution['y_'+str(var+1)] = self.coeff_matrix[i+1][-1]

        for i in range(0, self.num_vars):
            if i not in self.basic_vars[1:]:
                solution['y_'+str(i+1)] = Fraction("0/1")
        
        count = 1
        for i in range(self.num_vars, len(self.coeff_matrix[0]) - 1):
            solution['x_' + str(count)] = self.coeff_matrix[0][i]
            count += 1

        return solution

def add_row(row1, row2):
    row_sum = [0 for i in range(len(row1))]
    for i in range(len(row1)):
        row_sum[i] = row1[i] + row2[i]
    return row_sum

def max_index(row):
    max_i = 0
    for i in range(0, len(row)-1):
        if row[i] > row[max_i]:
            max_i = i

    return max_i

def multiply_const_row(const, row):
    mul_row = []
    for i in row:
        mul_row.append(const*i)
    return mul_row

def min_index(row):
    min_i = 0
    for i in range(0, len(row)):
        if row[min_i] > row[i]:
            min_i = i

    return min_i
