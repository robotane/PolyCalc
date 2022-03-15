from pyparsing import ParseException, Word, alphas, alphanums
from PolynomialBNF import get_BNF, expr_stack, evaluate_stack, prepare_input


class PolynomialParser:

    def __init__(self):
        # Debugging flag can be set to either "debug_flag=True" or "debug_flag=False"
        self.debug_flag = False
        self.variables = {}
        arith_expr = get_BNF()
        ident = Word(alphas, alphanums).setName("identifier")
        assignment = ident("varname") + "=" + arith_expr
        self.pattern = assignment | arith_expr

    def parse(self, input_string: str):  # TODO: raise exception instead of printing the exceptions message
        # Reset to an empty expr_stack
        del expr_stack[:]
        result = ""
        if input_string.strip().lower() == "debug":
            self.debug_flag = not self.debug_flag
            return f"debug_mode {'on' if self.debug_flag else 'off'}"
        if input_string != "":
            # try parsing the input string
            prepared_input = prepare_input(input_string)
            try:
                parsed_result = self.pattern.parseString(prepared_input, parseAll=True)
            except ParseException as err:
                parsed_result = ["Parse Failure", prepared_input, (str(err), err.line, err.column)]

            # show result of parsing the input string
            if self.debug_flag:
                result += f"{input_string} -> {parsed_result}\n"
            if len(parsed_result) == 0 or parsed_result[0] != "Parse Failure":
                if self.debug_flag:
                    result += f"expr_stack={expr_stack}\n"

                for i, ob in enumerate(expr_stack):
                    if isinstance(ob, str) and ob in self.variables:
                        expr_stack[i] = str(self.variables[ob])

                # calculate result , store a copy in ans , display the result to user
                try:
                    stack_eval = evaluate_stack(expr_stack)
                    result += stack_eval + "\n"
                except Exception as e:
                    result += str(e) + "\n"
                else:
                    self.variables["ans"] = stack_eval

                    # Assign result to a variable if required
                    if parsed_result.varname:
                        self.variables[parsed_result.varname] = stack_eval
                    if self.debug_flag:
                        result += f"variables={self.variables}\n"
            else:
                result += "Parse Failure\n"
                err_str, err_line, err_col = parsed_result[-1]
                result += err_line+"\n"
                result += " " * (err_col - 1) + "^\n"
                result += err_str
            return result


if __name__ == "__main__":
    pol_parser = PolynomialParser()
    # Display instructions on how to quit the program
    print("Type in the string to be parsed or 'quit' to exit the program")
    input_str = input("> ")

    while input_str.strip().lower() != "quit":
        # obtain new input string
        res = pol_parser.parse(input_str)
        print(res)
        input_str = input("> ")
    # if user type 'quit' then say goodbye
    print("Good bye!")
