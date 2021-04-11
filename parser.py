import parsimonious as pm
import ast

with open('assets/grammar.txt') as f:
    grammar = pm.Grammar(f.read())

with open('assets/example.txt') as f:
    syntax_tree = grammar.parse(f.read())


class Translator(pm.NodeVisitor):
    def visit_block_body(self, node, children):
        return "\n".join((
            children[0],
            *(
                (pair[1] for pair in children[1])
                if children[1] else
                ()
            )
        ))
        
    def visit_cpp_call(self, node, children):
        _, string, _ = children
        return ast.literal_eval(string)

    def visit_string_literal(self, node, children):
        return node.text

    def visit_block(self, node, children):
        return ''.join(children)

    def generic_visit(self, node, children):
        if children is not None and len(children) == 1:
            return children[0]
        
        return children or node.text


with open('assets/template.cpp') as f:
    template = f.read()

result = template.format(Translator().visit(syntax_tree))
