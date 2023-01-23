from IPython.display import Markdown as md

# Some utils function for the analysis, EDA or model

def enumType(df):
    display(md(f"\n La base de données récupérée contient {df.shape[0]} entrées sur {df.shape[1]} variables.\n"))
    lgroup={}
    for name,typ in df.dtypes.items():
        if typ.name in lgroup.keys():
            lgroup[typ.name]+=[name]
        else:
            lgroup[typ.name]=[name]
    display(md("Les variables sont réparties en :"))
    md2display1 = "Type"
    mdInterligne = "----:"
    md2display2 = "Nombre"
    for key,nb in lgroup.items():
        md2display1+=f" | {key}"
        mdInterligne+=" | ----:"
        md2display2+=f" | {len(nb)}"
    display(md(md2display1+"\n"+mdInterligne+"\n"+md2display2))
    return lgroup
