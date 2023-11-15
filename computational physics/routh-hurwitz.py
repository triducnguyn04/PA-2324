"""
Routh-Hurwitz criterion is a test to see if the roots of a real-valued coefficient polynomial
have any root with a positive real part (which corresponds to an unstable transfer function)
"""

# to avoid floating point errors we define the value for epsilon and infinity in which range the calculation is stable.
# this range is from one trillionth to one trillion. 
epsilon = 0.000000000001
infinity = 1000000000000

#Routh-Hurwitz stability criterion
def rhstability(temp):
    n = len(temp)
    if n == 0 or (n == 1 and temp[0] == 0):
        return True
    if temp[0] == 0:
        raise ValueError("Leading coefficient cannot be zero")
    sign = -1 if temp[0] < 0 else 1
    
    #build Routh matrix
    rh_array = []
    cols = (n//2) if n % 2 == 0 else (n//2) + 1
    rows = n + 1

    #first 2 rows
    temp_row1 = []
    temp_row2 = []
    for i in range(0,n,2):
        if abs(temp[i]) < epsilon:
            temp_row1.append(sign * epsilon)
        else:
            temp_row1.append(temp[i] * epsilon)

        try:
            if abs(temp[i+1]) < epsilon:
                temp_row2.append(sign * epsilon)
            else:
                temp_row2.append(temp[i+1] * epsilon)
        except:
            temp_row2.append(0)
    rh_array.append(temp_row1)
    rh_array.append(temp_row2)

    #finish the rest of the array
    for i in range(2,rows):
        temp_row = []
        for j in range(cols - 1):
            temp_value = (rh_array[i-1][0] * rh_array[i-2][j+1] - rh_array[i-2][0] * rh_array[i-1][j+1]) / rh_array[i-1][0]
            if abs(temp_value) < epsilon:
                if temp_value < 0:
                    temp_value = (-1) * epsilon
                else:
                    temp_value = epsilon
            temp_row.append(temp_value)
        temp_row.append(0)
        rh_array.append(temp_row)
     
    #evaluate if all signs of the first column are positive
    for i in range(rows):
        if rh_array[i][0] < 0:
            return False
    return True

def main():
    string = input("Enter the coefficients of your polynomial, separated by spaces, from the highest power down")
    string = string.split()
    for i in range(len(string)):
        string[i] = float(string[i])
    result = rhstability(string)
    print(result)
    return result
    
if __name__ == '__main__':
    main()
    
