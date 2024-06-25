import ply.yacc as yacc
from lexer import tokens, lexer

defined_variables = {}

def p_program(p):
    '''program : function_definition'''
    p[0] = "La estructura del código es correcta."

def p_function_definition(p):
    '''function_definition : INT ID LPAREN RPAREN LBRACE function_body RBRACE'''

def p_function_body(p):
    '''function_body : declarations statements
                     | statements'''

def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration
                    | empty'''

def p_declaration(p):
    '''declaration : INT ID ASSIGN NUMBER SEMICOLON
                   | INT ID SEMICOLON'''
    if len(p) == 6:
        defined_variables[p[2]] = p[1]

def p_statements(p):
    '''statements : statements statement
                  | statement
                  | empty'''

def p_statement(p):
    '''statement : for_loop
                 | assignment_statement
                 | return_statement'''

def p_for_loop(p):
    '''for_loop : FOR LPAREN assignment_expression SEMICOLON condition SEMICOLON increment_expression RPAREN LBRACE statements RBRACE'''

def p_assignment_expression(p):
    '''assignment_expression : ID ASSIGN expression'''

def p_increment_expression(p):
    '''increment_expression : ID INCREMENTO
                            | assignment_expression'''

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression SEMICOLON'''
    validate_variable_definition(p[1])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''

def p_condition(p):
    '''condition : expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression
                 | expression EQ expression
                 | expression NE expression'''

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term'''

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''

def p_factor(p):
    '''factor : ID
              | NUMBER'''
    if isinstance(p[1], str) and p.slice[1].type == 'ID':
        validate_variable_definition(p[1])
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def validate_variable_definition(variable):
    if variable not in defined_variables:
        raise ValueError(f"Error semántico: Variable '{variable}' no definida correctamente.")

def p_error(p):
    if p:
        error_message = f"Línea {p.lineno}.- Error de sintaxis en '{p.value}'"
        raise SyntaxError(error_message)
    else:
        raise SyntaxError(f"Error de sintaxis al final del archivo en la línea {lexer.lineno}. Falta una llave de cierre o punto y coma.")

parser = yacc.yacc()

def parse_semantic(code):
    global defined_variables
    defined_variables = {}
    lexer.lineno = 1
    try:
        result = parser.parse(code, lexer=lexer)
        return result if result else 'La estructura del código es correcta'
    except (SyntaxError, ValueError) as e:
        raise e

def parse_code(code):
    global defined_variables
    defined_variables = {}
    lexer.lineno = 1
    try:
        result = parser.parse(code, lexer=lexer)
        return result if result else "La estructura del código es correcta."
    except (SyntaxError, ValueError) as e:
        raise e
