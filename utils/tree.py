from Leaf.Leaf import Leaf

precedences = {'*' : 2, '+' : 2, "•" : 1, "|" : 1, "?": 0}

def get_aumented_regex(regular_expression):
    regex = ''
    index = 0
    while (index!=len(regular_expression)):
        char = regular_expression[index]
        if(index==0):
            regex += char
            index += 1
        elif(index+1<len(regular_expression)):
            if(index+2<len(regular_expression) and regular_expression[index+1] == "*"):
                if(
                    regular_expression[index+2] != "*" and
                    regular_expression[index+2] != "?" and
                    regular_expression[index+2] != "+" and
                    regular_expression[index+1] != "|"):
                        regex += char + regular_expression[index+1] + "•"
                        index+=2
                else:
                    regex += char + regular_expression[index+1]
                    index += 2
            elif(
                regular_expression[index+1] == "?"):
                regex += char + "|ε"
                index += 2
            elif(
                regular_expression[index+1] == "|" or
                regular_expression[index+1] == "+" or
                regular_expression[index+1] == "*" ):
                regex += char + regular_expression[index+1]
                index += 2
            elif(regular_expression[index+1] == ")"):
                regex += char
                index += 1
            elif(regular_expression[index+1] and
                char != "(" ):
                regex += char + "•"
                index += 1
            else:
                regex += char
                index += 1
        else:
            regex += char + "#"
            index += 1
    return(regex)

def get_aphabet(regex):
    alphabet = []
    for char in regex:
        if(
            char!='*' and 
            char!='(' and 
            char!=')' and 
            char!='|' and 
            char!='?' and 
            char!='+' and 
            char!='•' and       
            char not in alphabet):
            alphabet.append(char)
    return alphabet
 
def greater_precedence(operator_1, operator_2):
    return precedences[operator_1] > precedences[operator_2]

def generate_Tree(regex):
    regex = get_aumented_regex(regex)
    alphabet = get_aphabet(regex)
    values = []
    stack = []
    for char in regex:
        if(char in alphabet):
            values.append(Leaf(char))
        elif char == '(':
            stack.append(char)
        elif char == ')':
            top = stack[-1] if stack else None
            while (top is not None and top != '('):
                operator = stack.pop()
                right = values.pop()
                left = None
                if(len(values)!=0):
                    left = values.pop()
                parent = Leaf(operator, right, left, id=operator)
                values.append(parent)
                top = stack[-1] if stack else None
            stack.pop()
        else:
            top = stack[-1] if stack else None
            while (top is not None and top not in "()" and greater_precedence(top, char)):
                operator = stack.pop()
                right = values.pop()
                left = None
                if(len(values)!=0):
                    left = values.pop()
                parent = Leaf(operator, right, left, id=operator)
                values.append(parent)
                top = stack[-1] if stack else None
            stack.append(char)
    while len(stack)!=0:
        operator = stack.pop()
        right = values.pop()
        left = None
        if(len(values)!=0):
            left = values.pop()
        parent = Leaf(operator, right, left, id=operator)
        values.append(parent)
    while(len(values)>1):
        right = values.pop()
        left = None
        if(len(values)!=0):
            left = values.pop()
        parent = Leaf("•", right, left, id="•")
        values.append(parent)
    return values[0], alphabet
            