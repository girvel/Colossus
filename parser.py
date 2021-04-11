import parsimonious as pm
import ast

with open('assets/grammar.txt') as f:
    grammar = pm.Grammar(f.read())

with open('assets/example.txt') as f:
    syntax_tree = grammar.parse(f.read())


class Translator(pm.NodeVisitor):
    def visit_expression(self, node, children):
        return "\n".join((children[0], *(pair[1] for pair in children[1])))
        
    def visit_cpp_call(self, node, children):
        _, string, _ = children
        return ast.literal_eval(string)

    def visit_string_literal(self, node, children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or None


with open('assets/template.cpp') as f:
    template = f.read()

result = template.format(Translator().visit(syntax_tree))
