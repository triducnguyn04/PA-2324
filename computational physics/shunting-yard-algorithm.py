# simple expression parser for basic functions (addition, subtraction, multiplication, division, power) with constants pi and e with examples.
import math
def precedence(operator):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    return precedence.get(operator, 0)

def is_operator(token):
    return token in '+-*/^'

def shunting_yard(expression):
    output_queue = []
    operator_stack = []
    i = 0
    token_list = expression.replace(' ','')
    while i < len(token_list):
        if token_list[i].isdigit() or (token_list[i] == '-' and (i == 0 or (i > 0 and token_list[i - 1] in '(+-*/^'))):
            if token_list[i] == '-' and not len(output_queue)==0:
                #handle multiple unary minus sign stacked together
                if output_queue[-1]=='-':
                    output_queue.pop()
                    i+=1
                else:
                    start = i
                    i += 1
                    while i < len(token_list) and (token_list[i].isdigit() or token_list[i] == '.'):
                        i += 1
                    output_queue.append(token_list[start:i])
            else:
                start = i
                i += 1
                while i < len(token_list) and (token_list[i].isdigit() or token_list[i] == '.'):
                    i += 1
                output_queue.append(token_list[start:i])

        #handling '-pi, -e' cases
        elif token_list[i] == 'p':
            if token_list[i+1]=='i':
                if len(output_queue)>0:
                    if output_queue[-1]=='-':
                        output_queue[-1]+=str(math.pi)
                        i+=2
                    else:
                        output_queue.append(str(math.pi))
                        i+=2
                else:
                    output_queue.append(str(math.pi))
                    i+=2
            else:
                raise ValueError("Unspecified Character")
            
        elif token_list[i] == 'e':
            if len(output_queue)>0:
                    if output_queue[-1]=='-':
                        output_queue[-1]+=str(math.e)
                        i+=1
                    else:
                        output_queue.append(str(math.e))
                        i+=1
            else:
                output_queue.append(str(math.e))
                i+=1

        elif token_list[i] == '(':
            operator_stack.append(token_list[i])
            i += 1
        elif token_list[i] == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
            else:
                raise ValueError("Mismatched parentheses")
            i += 1
        elif is_operator(token_list[i]):
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence(token_list[i]) <= precedence(operator_stack[-1])):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token_list[i])
            i += 1
        else:
            raise ValueError(f"Invalid token: {token_list[i]}")

    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output_queue.append(operator_stack.pop())

    return output_queue

def evaluate_rpn(output_queue):
    stack = []
    operators = {'+', '-', '*', '/', '^'}

    for token in output_queue:
        if token not in operators:
            if token.startswith('-'):
                # Handle negative numbers or unary minus
                if len(token) > 1:
                    stack.append(-float(token[1:]))
                else:
                    stack.append(float(token))
            elif token == 'u-':
                # Handle unary minus
                operand = -stack.pop()
                stack.append(operand)
            else:
                stack.append(float(token))
        else:
            if token == '+':
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = operand1 + operand2
                stack.append(result)
            elif token == '-':
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = operand1 - operand2
                stack.append(result)
            elif token == '*':
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = operand1 * operand2
                stack.append(result)
            elif token == '/':
                operand2 = stack.pop()
                operand1 = stack.pop()
                if operand2 == 0:
                    raise ValueError("Division by zero")
                result = operand1 / operand2
                stack.append(result)
            elif token == '^':
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = operand1 ** operand2
                stack.append(result)

    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]
    
    # Test cases
if __name__ == "__main__":
    test_cases = ["3 + 4 * 2 / (1 - 5)^2", "-pi * 5 + pi *e", "(-3)", "(--3)()", "5 * -3", "2 ^ (3 ^ 2)", "3 * (3 / -3)"]
    for test in test_cases:
        print(f"Input: {test}")
        output = shunting_yard(test)
        print(f"Output: {' '.join(output)}")
        result = evaluate_rpn(output)
        print(f"Result: {result}")
