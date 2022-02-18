from manim import *

_my_ctex_preamble = r"""
\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{dsfont}
\usepackage{setspace}
\usepackage{tipa}
\usepackage{relsize}
\usepackage{textcomp}
\usepackage{mathrsfs}
\usepackage{calligra}
\usepackage{wasysym}
\usepackage{ragged2e}
\usepackage{physics}
\usepackage{xcolor}
\usepackage{microtype}
\usepackage[UTF8]{ctex}
\linespread{1}
\setlength{\textwidth}{%dem}
"""

# tex_compiler = "xelatex",
# output_format = ".xdv",

my_ctex = lambda x=22: TexTemplate(
    preamble=_my_ctex_preamble%x
)
