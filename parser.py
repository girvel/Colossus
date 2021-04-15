import parsimonious as pm
import ast

with open('assets/grammar.txt') as _f:
    grammar = pm.Grammar(_f.read())

with open('assets/template.cpp') as _f:
    template = _f.read()


class Translator(pm.NodeVisitor):
    def generic_visit(self, node, children):
        return children or node.text

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

    def visit_statement(self, node, children):
        return children[0]

    def visit_function_definition(self, node, children):
        return '{} {}{} {{ return ({}); }}'.format(
            children[4],
            children[0],
            children[2],
            children[6],
        )

    def visit_identifier(self, node, children):
        return replace_characters(node.text)

    def visit_arguments_definition(self, node, children):
        print(children)
        if children[0] == "()":
            return "()"

        children = children[0]
        return "({})".format(
            ", ".join((children[1], *(p[1] for p in children[2])))
        )
            
    def visit_argument_definition(self, node, children):
        return f'{children[0][0]} {children[2]}'


def replace_characters(identifier):
    return identifier


def translate(source):
    return template.format(Translator().visit(grammar.parse(source)))
