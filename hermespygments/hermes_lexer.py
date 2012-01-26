from pygments.lexer import include, bygroups, RegexLexer
from pygments.token import Token
import re

class HermesParseTreeLexer(RegexLexer):
  name = 'Hermes Parse Tree Lexer'
  aliases = ['parsetree']
  filenames = ['*.parsetree']
  mimetypes = []
  flags = re.DOTALL

  tokens = {
      'whitespace': [
        (r'\s+', Token.Text),
      ],

      'parsetree': [
        (r'(\()([a-zA-Z0-9_]+)(:)', bygroups(Token.Punctuation, Token.Name.Class, Token.Punctuation), 'children')
      ],

      'token': [
        (r'(<)([^>]*)(>)', bygroups(Token.Punctuation, Token.Number.Integer, Token.Punctuation))
      ],

      'children': [
        include('whitespace'),
        include('parsetree'),
        include('token'),
        (r',', Token.Punctuation),
        (r'\)', Token.Punctuation, '#pop')
      ],

      'root': [
        include('whitespace'),
        include('parsetree')
      ]
  }

class HermesAstLexer(RegexLexer):
  name = 'Hermes Abstract Syntax Tree Lexer'
  aliases = ['ast']
  filenames = ['*.ast']
  mimetypes = []
  flags = re.DOTALL

  tokens = {
      'whitespace': [
        (r'\s+', Token.Text),
      ],

      'ast': [
        (r'(\()([a-zA-Z_]+)(:)', bygroups(Token.Punctuation, Token.Name.Class, Token.Punctuation), 'ast_attrs')
      ],

      'attr': [
        (r'([a-zA-Z_]+)(=)', bygroups(Token.Name.Variable, Token.Punctuation), 'ast_attr')
      ],

      'token': [
        (r'(<)([^>]*)(>)', bygroups(Token.Punctuation, Token.Number.Integer, Token.Punctuation))
      ],

      'ast_attr_list': [
        include('whitespace'),
        include('ast'),
        include('attr'),
        include('token'),
        (r',', Token.Punctuation),
        (r'\[', Token.Punctuation, '#push'),
        (r'[\)\]]', Token.Punctuation, '#pop')
      ],

      'ast_attr': [
        include('whitespace'),
        include('ast'),
        include('token'),
        (r'\[', Token.Punctuation, 'ast_attr_list'),
        (r'(,|None|\)|\])', Token.Punctuation, '#pop')
      ],

      'ast_attrs': [
        include('whitespace'),
        include('ast'),
        include('attr'),
        (r',', Token.Punctuation),
        (r'[\)\]]', Token.Punctuation, '#pop'),
      ],

      'root': [
        include('whitespace'),
        include('ast')
      ]
  }

class HermesGrammarFileLexer(RegexLexer):
  name = 'Hermes Grammar File Lexer'
  aliases = ['zgr']
  filenames = ['*.zgr']
  mimetypes = []
  flags = re.DOTALL

  tokens = {
      'whitespace': [
        (r'\s+', Token.Text),
      ],

      # represents a simple terminal value
      'simplevalue':[
        (r'(true|false|null)\b', Token.Keyword.Constant),
        (r'-?[0-9]+', Token.Number.Integer),
        (r'"(\\\\|\\"|[^"])*"', Token.String.Double),
      ],


      # the right hand side of an object, after the attribute name
      'objectattribute': [
        include('value'),
        (r':', Token.Punctuation),
        # comma terminates the attribute but expects more
        (r',', Token.Punctuation, '#pop'),
        # a closing bracket terminates the entire object, so pop twice
        (r'}', Token.Punctuation, ('#pop', '#pop')),
      ],

      'll1_grammar_nonterminal': [
        include('whitespace'),
        (r':', Token.Punctuation),
        (r'"[a-zA-Z0-9_-]+"', Token.Number.Integer, ('#pop'))
      ],

      'll1_rule_ast': [
        include('whitespace'),
        (r'\)', Token.Punctuation, ('#pop')),
        (r'"', Token.Punctuation, ('#pop', '#pop')),
        (r'[^"\)]', Token.Number.Integer),
      ],

      'll1_rule_start': [
        include('whitespace'),
        (r'[a-zA-Z0-9_]+', Token.Name.Class),
        (r"'[a-zA-Z0-9_]+'", Token.Name.Variable),
        (ur'(_empty|\u03b5)', Token.Number.Integer),
        (r'"', Token.Punctuation, '#pop'),
        (r'->', Token.Punctuation, 'll1_rule_ast'),
        (r':=', Token.Punctuation),
        (r'[\|\+\(\),{}]', Token.Punctuation),
      ],

      'll1_grammar_rules_list': [
        include('whitespace'),
        (r',', Token.Punctuation),
        (r'"', Token.Punctuation, 'll1_rule_start'),
        (r'\]', Token.Punctuation, ('#pop'))
      ],

      'll1_grammar_rules': [
        include('whitespace'),
        (r':', Token.Punctuation),
        (r'\[', Token.Punctuation, 'll1_grammar_rules_list'),
        (r'}', Token.Punctuation, ('#pop', '#pop', '#pop'))
      ],

      'll1_grammar_obj': [
        include('whitespace'),
        (r',', Token.Punctuation),
        (r'"start"', Token.Name.Tag, 'll1_grammar_nonterminal'),
        (r'"rules"', Token.Name.Tag, 'll1_grammar_rules'),
      ],

      'll1_grammar': [
        include('whitespace'),
        (r':', Token.Punctuation),
        (r'{', Token.Punctuation, 'll1_grammar_obj'),
        (r'[^{]', Token.Punctuation, ('#pop'))
      ],

      'expr_grammar_rules_list': [
        include('whitespace'),
        (r',', Token.Punctuation),
        (r'"', Token.Punctuation, 'll1_rule_start'),
        (r'\]', Token.Punctuation, ('#pop', '#pop'))
      ],

      'expr_rules': [
        include('whitespace'),
        (r'[:,]', Token.Punctuation),
        (r'\[', Token.Punctuation, 'expr_grammar_rules_list'),
        (r'}', Token.Punctuation, ('#pop'))
       ],

      'terminals': [
        include('whitespace'),
        (r'[\[:,]', Token.Punctuation),
        (r'("[a-zA-Z_]+")', Token.Name.Class),
        (r'\]', Token.Punctuation, '#pop'),
      ],

      'associativity': [
        include('whitespace'),
        (r':', Token.Punctuation),
        (r'("(left|right|unary)")', Token.Name.Class, '#pop')
      ],

      'binding_power': [
        include('whitespace'),
        (r',', Token.Punctuation),
        (r'"associativity"', Token.Name.Tag, 'associativity'),
        (r'"terminals"(?=\s*:\s*\[)', Token.Name.Tag, 'terminals'),
        (r'}', Token.Punctuation, ('#pop'))
       ],

      'expr_binding_powers': [
        include('whitespace'),
        (r'[:,\[]', Token.Punctuation),
        (r'{', Token.Punctuation, 'binding_power'),
        (r'\]', Token.Punctuation, '#pop')
      ],

      'expr_grammar': [
        include('whitespace'),
        (r',', Token.Punctuation),
        (r'}', Token.Punctuation, '#pop'),
        (r'"nonterminal"', Token.Name.Tag, 'll1_grammar_nonterminal'),
        (r'"binding_power"(?=\s*:\s*\[)', Token.Name.Tag, 'expr_binding_powers'),
        (r'"rules"(?=\s*:\s*\[)', Token.Name.Tag, 'expr_rules'),
        (r'"extends"', Token.Name.Tag, 'll1_grammar_nonterminal'),
      ],

      'expr_grammar_list': [
        include('whitespace'),
        (r',', Token.Punctuation),
        (r'{', Token.Punctuation, 'expr_grammar'),
        (r'\]', Token.Punctuation, '#pop'),
      ],

      'expr': [
        include('whitespace'),
        (r'\[', Token.Punctuation, 'expr_grammar_list'),
        (r':', Token.Punctuation),
        (r'}', Token.Punctuation, '#pop')
      ],

      # a json object - { attr, attr, ... }
      'objectvalue': [
        include('whitespace'),
        (r'"ll1"', Token.Name.Tag, 'll1_grammar'),
        (r'"(\\\\|\\"|[^)"])*"', Token.Name.Tag, 'objectattribute'),
        (r'}', Token.Punctuation, '#pop'),
      ],

      # json array - [ value, value, ... }
      'arrayvalue': [
        include('whitespace'),
        include('value'),
        (r',', Token.Punctuation),
        (r']', Token.Punctuation, '#pop'),
      ],

      # a json value - either a simple value or a complex value (object or array)
      'value': [
        include('whitespace'),
        include('simplevalue'),
        (r'{', Token.Punctuation, 'objectvalue'),
        (r'\[', Token.Punctuation, 'arrayvalue'),
      ],

      'grammar': [
        include('whitespace'),
        (r',', Token.Punctuation),
        (r'"ll1"', Token.Name.Tag, 'll1_grammar'),
        (r'"expr"', Token.Name.Tag, 'expr'),
        (r'}', Token.Punctuation, '#pop')
      ],

      # the root of a json document whould be a value
      'root': [
        include('whitespace'),
        (r'{', Token.Punctuation, 'grammar')
      ],

  }

