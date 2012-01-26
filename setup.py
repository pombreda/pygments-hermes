from setuptools import setup, find_packages
setup(
    name = "hermespygments",
    version = "0.1",
    packages = ['hermespygments',],
    install_requires = ['Pygments'],
    author = "Scott Frazer",
    author_email = "scott.d.frazer@gmail.com",
    description = "Pygments for Hermes grammar files, abstract syntax trees, and parse trees",
    entry_points={
      'pygments.lexers': [
          'zgr = hermespygments.hermes_lexer:HermesGrammarFileLexer', \
          'parsetree = hermespygments.hermes_lexer:HermesParseTreeLexer', \
          'ast = hermespygments.hermes_lexer:HermesAstLexer' \
        ]
    }
)
