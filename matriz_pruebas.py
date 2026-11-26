from escenarios import ESCENARIOS
MATRIZ=[{'id':'MP-'+c['id'][2:],'tipo':c['tipo'],'requisitos':c['requisitos'],'escenario':c} for c in ESCENARIOS]
