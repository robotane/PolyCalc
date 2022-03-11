from pyparsing import ParseException, Word, alphas, alphanums
from PolynomialBNF import get_BNF, expr_stack, evaluate_stack, prepare_input

# Debugging flag can be set to either "debug_flag=True" or "debug_flag=False"
debug_flag = False

variables = {}

arithExpr = get_BNF()
ident = Word(alphas, alphanums).setName("identifier")
assignment = ident("varname") + "=" + arithExpr
pattern = assignment | arithExpr

if __name__ == "__main__":
    # Display instructions on how to quit the program
    print("Type in the string to be parsed or 'quit' to exit the program")
    input_string = input("> ")

    while input_string.strip().lower() != "quit":
        if input_string.strip().lower() == "debug":
            debug_flag = True
            input_string = input("> ")
            continue

        # Reset to an empty expr_stack
        del expr_stack[:]

        if input_string != "":
            # try parsing the input string
            prepared_input = prepare_input(input_string)
            try:
                L = pattern.parseString(prepared_input, parseAll=True)
            except ParseException as err:
                L = ["Parse Failure", prepared_input, (str(err), err.line, err.column)]

            # show result of parsing the input string
            if debug_flag:
                print(input_string, "->", L)
            if len(L) == 0 or L[0] != "Parse Failure":
                if debug_flag:
                    print("expr_stack=", expr_stack)

                for i, ob in enumerate(expr_stack):
                    if isinstance(ob, str) and ob in variables:
                        expr_stack[i] = str(variables[ob])

                # calculate result , store a copy in ans , display the result to user
                try:
                    result = evaluate_stack(expr_stack)
                except Exception as e:
                    print(str(e))
                else:
                    variables["ans"] = result
                    print(result)

                    # Assign result to a variable if required
                    if L.varname:
                        variables[L.varname] = result
                    if debug_flag:
                        print("variables=", variables)
            else:
                print("Parse Failure")
                err_str, err_line, err_col = L[-1]
                print(err_line)
                print(" " * (err_col - 1) + "^")
                print(err_str)

        # obtain new input string
        input_string = input("> ")

    # if user type 'quit' then say goodbye
    print("Good bye!")
