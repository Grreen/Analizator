
keywords = {'or', 'and'}
exps = []
operators = []
del_br = 0


class Error():
    def __init__(self, name, position):
        self.name = name
        self.index = position

    def __str__(self):
        return f'Ошибка: {self.name}, позиция {self.index}.'

class Expression():
    errors = []
    name = ''
    body = ''

def del_side_brackets(text):
    new_text = text
    ind = 0
    while new_text[ind] == ' ':
        ind+=1
    if(new_text[ind] == '('):
        global del_br
        del_br += 1
        new_text = new_text[ind+1:]
        ind = 0
        while (new_text[-ind-1] == ' '):
            ind+=1
        if (new_text[-ind-1] == ')'):
            new_text = new_text[:-ind-1]

    return new_text


def check_name(text, name = 'выражения', position = 0):
    if(len(text) == 0):
        return 0

    global del_br

    if(text[0].isalpha()):
        _string = True
        error_position = 0
        space_error = False
        name_error = False
        for i in text:
            if(_string and i.isalpha()):
                pass
            elif(i.isdigit()):
                if(_string):
                    _string = False
                    error_position = text.index(i)
            elif(i == ' '):
                if(not space_error):
                    Expression.errors.append(Error('Имя {} не должно содержать пробелов'.format(name), text.index(i)+position+del_br))
                    space_error = True
            else:
                if(not name_error):
                    Expression.errors.append(Error('Ошибка в имени {}'.format(name), error_position+position+del_br))
                    _string = True
    else:
        Expression.errors.append(Error('Имя {} не может начинаться с символа {}'.format(name,text[0]), position+del_br))


def check_exp_body(body_exp, body_index = 0):
    if(not body_exp):
        return 0

    global exps
    global  del_br
    ind =0
    _str = ''
    exp_bool = False
    operator_bool = False
    exp_value = ''

    body_exp = del_side_brackets(body_exp)

    print('Body exp: {}'.format(body_exp))

    while ind < len(body_exp):

        while(ind < len(body_exp) and body_exp[ind] == ' '):
            ind+=1

        if(ind < len(body_exp) and (body_exp[ind] == '(' or body_exp[ind] == ')')):
            if (('(' in body_exp) and (')' in body_exp) and (not exp_bool)):
                left_bracket_index = body_exp.rfind('(')
                right_bracket_index = body_exp.find(')')
                if(right_bracket_index-left_bracket_index > 1):
                    check_exp_body(body_exp[left_bracket_index:right_bracket_index+1],body_index+ind)
                    exp_bool = True
                else:
                    Expression.errors.append(Error(name='Пустые скобки', position=left_bracket_index+body_index+del_br))

                ind += body_exp.find(')')
        elif ('(' in body_exp and not ')' in body_exp):
            Expression.errors.append(Error(name='Отcутствует закрывающая скобка', position=body_exp.rfind('(') + body_index+del_br))
        elif (')' in body_exp and not '(' in body_exp):
            Expression.errors.append(Error(name='Отсутствует открывающая скобка', position=body_exp.find(')') + body_index +del_br))

        # else:
        #     if ('(' in body_exp):
        #         Expression.errors.append(Error(name='Отсутствует закрывающая скобка',position=body_index+body_exp.rfind('(')))
        #     elif (')' in body_exp):
        #         Expression.errors.append(Error(name='Отсутствует открывающая скобка',position=body_index+body_exp.rfind(')')))



        while(ind < len(body_exp) and body_exp[ind] != ' ' and body_exp[ind] != '(' and body_exp[ind] != ')'):
            _str+=body_exp[ind]
            ind+=1

        if(_str in keywords):
            operator_bool = True
            operators.append(_str)
            if(not exp_bool):
                Expression.errors.append(Error(name='Отсутствует выражение перед оператором "{}"'.format(_str),
                                               position=body_index+body_exp.find(_str)+del_br))
            check_exp_body(body_exp[ind:], body_index+ind)
            return 1
        elif (_str and (not exp_bool)):
            check_name(text=_str, position=body_index+ind-len(_str))
            exps.append(_str)
            exp_value = _str
            exp_bool = True
        elif(_str and exp_bool and not operator_bool):
            print('_str : {}'.format(_str))
            Expression.errors.append(Error(name='Отсутствует оператор между выражением "{}" и "{}"'.format(exp_value, body_exp[body_exp.index(exp_value)+len(exp_value):]),
                                           position=body_index+body_exp.index(exp_value)+len(exp_value)+del_br))
            check_exp_body(body_exp[body_exp.index(exp_value)+len(exp_value):], body_index+ind)
            return 1

        _str = ''
        ind+=1


def check_expression(line_exp):
    if(len(line_exp) == 0):
        Expression.errors.append(Error('Отсутствует выражние', 0))
        return 0

    if ((':=' in string) or (':' in string) or ('=' in string)):
        global name
        if (':=' in string):
            Expression.name = line_exp[0:line_exp.index(':=')]
            Expression.body = line_exp[line_exp.index(':=') + 2:len(line_exp)]
        elif (':' in string):
            Expression.name = line_exp[0:line_exp.index(':')]
            Expression.body = line_exp[line_exp.index(':') + 1:len(line_exp)]
            Expression.errors.append(Error('Неправильная запись операции', line_exp.find(':')))
        else:
            Expression.name = line_exp[0:line_exp.index('=')]
            Expression.body = line_exp[line_exp.index('=') + 1:len(line_exp)]
            Expression.errors.append(Error('Неправильная запись операции', line_exp.find('=')))

        check_name(text=Expression.name)

    else:
        Expression.errors.append(Error('Отсутствует имя выражния', 0))
        Expression.body = line_exp

    check_exp_body(body_exp = Expression.body, body_index = line_exp.index(Expression.body))


if __name__ == '__main__':
    string = input()
    check_expression(string)
    if(len(Expression.errors)>0):
        print('Количество ошибок: {}'.format(len(Expression.errors)))
        for error in Expression.errors:
            print(error)
    else: print('Всё введено правильно!')
    if(len(exps)>0):
        print('Expressions:')
        print(exps)
    if(len(operators)>0):
        print('Operators:')
        print(operators)

