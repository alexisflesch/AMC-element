#!/usr/bin/python
# -*- coding: utf-8 -*-


""" This script will go through an entire folder and look for all your
    .tex files. It will open them, look for \element{foo}{bar} occurrences
    and replace them with \begin{qcm}{foo}bar\end{qcm}.
    
    If it can't find the definition of the environment qcm given below,
    it will add it to the file, just before \begin{document}
    
    It will then save the result to a new file (only if needs be, that is
    only if some modifications were made):
    file.tex -> file.texamator.tex
    
    Warning : 
     - if your braces don't match in your original tex file, the script
       won't work as expected.
     - the script counting braces doesn't ignore comments so the braces
       in your comments should also match.
"""

import os, codecs, sys

directory = '/path/to/your/tex/folder'

newEnv = r"""\NewEnviron{qcm}[1]{%
  \def\arg{#1}%
  \expandafter\element\expandafter\arg\expandafter{\BODY}}

\makeatletter
\renewcommand{\element}[2]{%
  \AMC@prepare@element{#1}%
  \global\csname #1@\romannumeral\AMCtok@k\endcsname={#2}%
}
\makeatother
"""


def addBeginQCM(texte):
    """looks for \element{foo}{bar} and change it to
       to \begin{qcm}{foo}bar}
    """
    g = []
    plop = texte.split('\n')
    for line in plop:
        splitted = line.split('%')
        noComment = splitted[0]
        if r'\element{' in noComment:
            group = findAMCGroup(noComment)
            a = noComment.replace(r'\element{'+group+'}{',r'\begin{qcm}{'+group+'}')
            if len(splitted)>1:
                a += '%'
                a += ''.join(splitted[1:])
            g.append(a)
        else:
            g.append(line)
    g = '\n'.join(g)
    return g


def addEndQCM(texte):
    """counts the number of curly braces and adds \end{qcm} where it should go"""
    cpt = 1
    res = ''
    for i in texte:
        if i=='}':
            cpt -= 1
        elif i=='{':
            cpt += 1
        if cpt==0:
            res += r'\end{qcm}'
            cpt = 1
        else:
            res += i
    return res


def findAMCGroup(noComment):
    """When given a line with '\element', tries to find
       the name of the element
    """
    a = noComment.split(r'\element{')[1]
    res = ''
    cpt = 1
    for i in a:
        if i=='}':
            cpt -= 1
        elif i=='{':
            cpt += 1
        if cpt==0:
            break
        else:
            res += i
    return res


def letsgo(directory):
    for fichier in os.listdir(directory):
        if fichier[-4:].lower() == ".tex":
            try:
                f = codecs.open(os.path.join(directory, fichier),'r','utf8')
                oldtex = f.read()
                f.close()
                newtex = addBeginQCM(oldtex)
                newtex = addEndQCM(newtex)
                if newEnv not in newtex:
                    newtex = newtex.replace(r'\begin{document}',newEnv+'\n'+r'\begin{document}')
                if newtex!=oldtex:
                    g = codecs.open(os.path.join(directory, fichier[:-4]+'.texamator.tex'), 'w', 'utf8')
                    g.write(newtex)
                    g.close()
                    print("Creating file " + os.path.join(directory, fichier[:-4]+'.texamator.tex'))
            except:
                print("Error : " + os.path.join(directory, fichier))


if __name__=='__main__':
    letsgo(directory)