import parsimonious as pm
import ast

with open('assets/grammar.txt') as _f:
    grammar = pm.Grammar(_f.read())

with open('assets/template.cpp') as _f:
    template = _f.read()


class Translator(pm.NodeVisitor):
    def visit_block_body(self, node, children):
        return "\n".join((
            children[0],
            *(pair[1] for pair in children[1])
        ))
        
    def visit_cpp_call(self, node, children):
        _, string, _ = children
        return ast.literal_eval(string)

    def visit_string_literal(self, node, children):
        return node.text

    def visit_block(self, node, children):
        return ''.join(children)

    def visit_expression(self, node, children):
        return children[0]

    def generic_visit(self, node, children):
        return children or node.text


def translate(source):
    return template.format(Translator().visit(grammar.parse(source)))
