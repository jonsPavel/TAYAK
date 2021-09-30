# в Постфиксную запись.
def priority(z):
    if z in ['×', '*', '/']:
        return 2
    elif z in ['+', '-']:
        return 1


def in2post(expr):
    """: param expr: префиксное выражение
                 : return: постфиксное выражение

        Example：
            "1+((2+3)×4)-5"
            "1 2 3 + 4 × + 5 -"
    """
    stack = []  # Стек хранилища
    post = []  # Хранение выражений Postfix
    for z in expr:
        if z not in ['×', '*', '/', '+', '-', '(', ')']:  # Прямой вывод символов
            post.append(z)
            print(1, post)
        else:
            if z != ')' and (not stack or z == '(' or stack[-1] == '('
                             or priority(z) > priority(stack[-1])):  # стек не пуст; верх стека равен (; приоритет больше, чем
                stack.append(z)     # Оператор в стеке

            elif z == ')':  # Закрытие круглой скобки pop
                while True:
                    x = stack.pop()
                    if x != '(':
                        post.append(x)
                        print(2, post)
                    else:
                        break

            else:   # Приоритет оператора сравнения, чтобы узнать, помещен ли стек или нет
                while True:
                    if stack and stack[-1] != '(' and priority(z) <= priority(stack[-1]):
                        post.append(stack.pop())
                        print(3, post)
                    else:
                        stack.append(z)
                        break
    while stack:    # Операторы, которые не всплывали, необходимо добавить в конец выражения
        post.append(stack.pop())
    return post

def calculator(string):
    if not error_checking(string):
        return 'некорректная последовательность!'
    stack = []
    for i in range(len(string)):
        if string[i] in '+-*/':
            arithmetic_action(stack, string[i])
        else:
            stack.append(int(string[i]))
    return stack[0]


def arithmetic_action(stack, sign):
    second_number = stack.pop()
    first_number = stack.pop()
    if sign == '+':
        stack.append(first_number + second_number)
    elif sign == '-':
        stack.append(first_number - second_number)
    elif sign == '*':
        stack.append(first_number * second_number)
    else:
        stack.append(first_number / second_number)


def error_checking(string):
    if len(string) % 2 == 0:
        return False
    elif not string[0].isdigit() or not string[1].isdigit():
        return False
    elif string[-1].isdigit():
        return False
    count = 1
    for i in range(2, len(string) - 1):
        if string[i].isdigit():
            count += 1
        elif string[i] in '+-*/':
            count -= 1
        else:
            return False
    if count == 1:
        return True
    else:
        return False


if __name__ == '__main__':
    print('Введите выражение в инфиксной записи:')
    # s = "1+((2+3)×4)-5"
    post = in2post(input().split())
    print('Постфиксное выражение:',post)
    print('Ответ:',calculator(post))