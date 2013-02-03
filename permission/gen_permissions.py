#!/usr/bin/env python

import collections, os, sys, shutil

paper_authors = {
    "tritonsort" : [
        "George Porter", "Michael Conley", "Harsha Madhyastha",
        "Radhika Niranjan Mysore", "Alexander Pucher", "Amin Vahdat"],
    "themis" : [
        "Michael Conley", "Rishi Kapoor", "Vinh The Lam", "George Porter",
        "Amin Vahdat"],
    "themis-ft" : ["George Porter", "Amin Vahdat"]
}

co_authors = collections.defaultdict(list)

for paper, authors in paper_authors.items():
    for author in authors:
        co_authors[author].append(paper)

parent_permissions_dir = os.path.join(os.path.dirname(__file__), "individual")

os.makedirs(parent_permissions_dir)

permissions_files = []

for author in co_authors:
    permissions_file = "permissions_%s.tex" % (author.split(' ')[0].lower())

    permissions_files.append(permissions_file)

    permissions_file = os.path.join(parent_permissions_dir, permissions_file)

    with open(permissions_file, 'w') as fp:
        print >>fp, r"""
\documentclass{article}
\usepackage{parskip}
\usepackage[margin=1in]{geometry}
\usepackage{mathptmx}
\usepackage{courier}
\usepackage[scaled=.92]{helvet}
\usepackage[T1]{fontenc}
\pagestyle{empty}

\newcommand{\signature}[1]{

\vskip3\baselineskip
\makebox[2in]{\hrulefill}

#1}

\begin{document}
\today

"""

        for paper in co_authors[author]:
            print >>fp, r"\input{../%s_permission}" % (paper)
            print >>fp, ""

        print >>fp, r"""

\vskip3\baselineskip
\makebox[2in]{\hrulefill}

"""
        print >>fp, author
        print >>fp, r"\end{document}"

shutil.copyfile(os.path.join(os.path.dirname(__file__), "Makefile"),
                os.path.join(parent_permissions_dir, "Makefile"))

with open(os.path.join(parent_permissions_dir, "Makefile.ini"), 'w') as fp:
    print >>fp, """
onlysources.tex := %s
LATEX_COLOR_WARNING := 'bold orange'
""" % (' '.join(permissions_files))
