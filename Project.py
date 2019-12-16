def Program(exp, variables):
    while len(exp) > 0:
        exp = Assignment(exp, variables)
        if exp is False:
            return False
    return True

def Assignment(exp, variables):
    exp = exp.lstrip()
    new_exp, identify = Identifier(exp)
    if new_exp is False:
        return False
    exp = new_exp.lstrip()
    if exp[0] != '=':
        return False
    exp = exp[1:]
    new_exp, value = Expression(exp, variables)
    if new_exp is False:
        return False
    exp = new_exp.lstrip()
    if exp.startswith(';'):
        variables[identify] = value
        return exp[1:]
    return False

def Expression(exp, variables):
    exp = exp.lstrip()

    exp, value = Term(exp, variables)
    if exp is not False:
        exp = exp.lstrip()
        if exp.startswith("+"):
            new_exp, next_value = Expression(exp[1:], variables)
            if new_exp is not False:
                return new_exp, value + next_value
        if exp.startswith("-"):
            new_exp, next_value =Expression(exp[1:], variables)
            if new_exp is not False:
                return new_exp, value - next_value
        return exp, value
    return False, None

def Term(exp, variables):
    exp = exp.lstrip()
    exp, value = Fact(exp, variables)
    if exp is not False:
        exp = exp.lstrip()
        if exp.startswith("*"):
            new_exp, next_value = Term(exp[1:], variables)
            if new_exp is not False:
                return new_exp, value * next_value
        return exp, value
    return False, None

def Fact(exp, variables):
    exp = exp.lstrip()
    if exp.startswith('('):
        new_exp, value = Expression(exp[1:], variables)
        if new_exp is not False and new_exp.startswith(')'):
            return new_exp[1:], value
    if exp.startswith('-') or exp.startswith('+'):
        new_exp, value = Fact(exp[1:], variables)
        if new_exp is not False:
            if exp.startswith('-'):
                return new_exp, -value
            else:
                return new_exp, value
    new_exp, value = Literal(exp)
    if new_exp is not False:
        return new_exp, value
    new_exp, identify = Identifier(exp)
    if identify not in variables.keys():
        print(identify + " is not initialized")
        return False, None
    if new_exp is not False:
        return new_exp, variables[identify]
    return False, None

def Identifier(exp):
    exp = exp.lstrip()
    identify = ""
    if not ('a' <= exp[0] <= 'z') and not ('A' <= exp[0] <= 'Z'):
        return False, None
    identify += exp[0]
    exp = exp[1:]
    while len(exp) > 0:
        if 'a' <= exp[0] <= 'z' or 'A' <= exp[0] <= 'Z' or '0' <= exp[0] <= '9' or exp[0] == '_':
            identify += exp[0]
            exp = exp[1:]
            continue
        break
    return exp, identify

def Literal(exp):
    exp = exp.lstrip()
    if exp.startswith('0'):
        return exp[1:], 0
    if len(exp) == 0 or not '1' <= exp[0] <= '9':
        return False, None
    lit = exp[0]
    exp = exp[1:]
    while len(exp) > 0 and '0' <= exp[0] <= '9':
        lit += exp[0]
        exp = exp[1:]
    return exp, int(lit)

def main():
    exp = input(">> ")
    variables = dict()
    if Program(exp, variables):
        for variable, value in variables.items():
            print(variable + " = " + str(value))
    else:
        print("error")

if __name__ == '__main__':
    main()