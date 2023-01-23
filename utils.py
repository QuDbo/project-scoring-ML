from IPython.display import Markdown as md
import re
import pandas as pd

# Some utils function for the analysis, EDA or model

def enumType(df):
    '''
    List type,s in dataframe df and count the number of var per types
    '''
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

def infoVars(df,pattern=""):
    '''
    Give informations of select var of a dataframe df filtered by the pattern (regex identification)
    '''
    lcol = [col for col in df.columns if re.search(pattern,col)]
    serTyp = pd.Series(df[lcol].dtypes)
    serNan = pd.Series(df[lcol].isna().sum(axis=0))
    serCat = pd.Series([list(df[col].unique()) if df[col].dtype=='object' else pd.NA for col in lcol],index=lcol)
    serNCat = pd.Series([len(l) if l is not pd.NA else 0 for l in serCat],index=lcol)
    dfInfo = pd.DataFrame(data={"Type":serTyp,"Nb de NaN":serNan,"Nb de cat":serNCat,"Catégories":serCat},index=df[lcol].columns)
    display(dfInfo)
    display(md(f"Taille de la DB : {df[lcol].shape}"))
    display(md(f"Taille (lignes complètes uniquement) : {df[lcol].dropna(how='any').shape}"))
    display(md(f"Taille (lignes partielles et complètes) : {df[lcol].dropna(how='all').shape}"))
