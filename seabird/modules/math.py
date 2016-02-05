import ast
import math
import operator

from seabird.decorators import command
from seabird.plugin import Plugin


class MathPlugin(Plugin):
    # supported operators
    operators = {ast.Add: operator.add, ast.Sub: operator.sub,
                 ast.Mult: operator.mul, ast.Div: operator.truediv,
                 ast.Pow: operator.pow, ast.BitXor: operator.xor,
                 ast.USub: operator.neg}

    constants = {'PI': math.pi, 'E': math.e}

    functions = {'pow': math.pow}

    @command
    def math(self, msg):
        """[expr]

        Run some simple calculations.
        """
        try:
            val = self.eval(msg.trailing)
            self.bot.mention_reply(msg, "%s = %f" % (msg.trailing, val))
        except Exception as e:
            self.bot.mention_reply(msg, "Error: %s" % e)

    def eval(self, expr):
        return self._eval(ast.parse(expr, mode='eval').body)

    def _eval(self, node):
        if isinstance(node, ast.Num):
            # <number>
            return node.n
        elif isinstance(node, ast.BinOp):
            # <left> <operator> <right>
            op = MathPlugin.operators.get(type(node.op))
            if operator is None:
                raise Exception('Weird error')

            return op(self._eval(node.left), self._eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            # <operator> <operand> e.g., -1
            op = MathPlugin.operators.get(type(node.op))
            if operator is None:
                raise Exception('Weird error')

            return op(self._eval(node.operand))
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise Exception('Invalid function name')

            args = [self._eval(arg) for arg in node.args]

            f = MathPlugin.functions.get(node.func.id)
            if f is None:
                raise Exception('Function does not exist')

            return f(*args)

        elif isinstance(node, ast.Name):
            # <id>
            ret = MathPlugin.constants.get(node.id)
            if ret is None:
                raise Exception('Invalid constant')

            return ret
        else:
            raise TypeError(node)
