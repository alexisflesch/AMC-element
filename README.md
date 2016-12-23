#AMCelement.py

This script will help you set up TeXamator with AMC (auto multiple choice).
More information here :

http://alexisfles.ch/en

This script will go through an entire folder (and its subfolders) and look for all your
.tex files. It will open them, look for \element{foo}{bar} occurrences
and replace them with \begin{qcm}{foo}bar\end{qcm}.
    
If it can't find the definition of the environment qcm,
it will add it to the file, just before \begin{document}
    
It will then save the result to a new file (only if needs be, that is
only if some modifications were made):
file.tex -> file.texamator.tex
    
Warning : 
- if your braces don't match in your original tex file, the script
won't work as expected.
- the script counting braces doesn't ignore comments so the braces
in your comments should also match.