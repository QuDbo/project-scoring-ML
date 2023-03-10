from IPython.display import Markdown as md
import re
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import plotly.subplots as splt

# Some utils function for the analysis, EDA or model

def enumType(df:pd.DataFrame)->dict:
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

def infoVars(df:pd.DataFrame,pattern="")->None:
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


def affich_hist(df:pd.DataFrame, var:str, **kwargs)->None:
    '''
    To display hist distribution of a var depending of the target.
    '''
    title = kwargs.get("title","")
    xtitle = kwargs.get("xtitle","")
    ytitle = kwargs.get("ytitle","")
    nbinsx = kwargs.get("nbinsx",100)
    xlog,ylog = kwargs.get("log",("linear","linear"))

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df[df["TARGET"] == 0][var],
        name="Target 0",
        nbinsx=nbinsx
    ))
    fig.add_trace(go.Histogram(
        x=df[df["TARGET"] == 1][var],
        name="Target 1",
        nbinsx=nbinsx
    ))
    fig.update_yaxes(type=ylog,title=ytitle)
    fig.update_xaxes(type=xlog,title=xtitle)
    fig.update_layout(title=title)
    fig.show()

def affich_cat(df:pd.DataFrame, var:str, **kwargs)->None:
    '''
    To display distribution of a category depending of the target
    '''
    title = kwargs.get("title","")
    xtitle = kwargs.get("xtitle","")
    ytitle = kwargs.get("ytitle","")
    ylog = kwargs.get("ylog","linear")

    fig=go.Figure()
    fig.add_trace(go.Histogram(
        x=df[df["TARGET"]==0][var],
        name="Target 0"
    ))
    fig.add_trace(go.Histogram(
        x=df[df["TARGET"]==1][var],
        name="Target 1"
    ))
    fig.update_yaxes(type=ylog,title=ytitle)
    fig.update_layout(title=title)
    fig.show()



def filtreSimple(df:pd.DataFrame,
                    fh=None,fb=None,
                    pattern=None,exclude=None
                    )->pd.DataFrame :
    df_modif = df.copy()
    if ((pattern==None) or (pattern=='')):
        print(f"Pattern non conforme\nReturning original dataframe")
        return df
    else:
        labs = [lab for lab in df.columns if pattern in lab]
        if exclude!=None:
            remov = [lab for lab in df.columns if exclude in lab]
            for rem in remov:
                try:
                    labs.remove(rem)
                except:
                    pass
        for lab in labs:
            if fb!=None:
                ser=pd.Series(df_modif[lab])
                ser.where(cond=(ser>=fb),other=np.nan,inplace=True)
                df_modif[lab]=ser
            if fh!=None:
                ser=pd.Series(df_modif[lab])
                ser.where(cond=(ser<=fh),other=np.nan,inplace=True)
                df_modif[lab]=ser
        return df_modif

def plot_eboulis(acp,nCompMax):
    scree = acp.explained_variance_ratio_*100
    max_rank = len(scree)+1
    screeValues = pd.DataFrame({'n':np.arange(len(scree))+1,"eigenvalue":scree}).to_numpy()
    screeCumsum = pd.DataFrame({'n':np.arange(len(scree))+1,"cumulative sum":scree.cumsum()}).to_numpy()

    ks = 100./nCompMax
    annot = [(i+1,val) for i,val in enumerate(scree.cumsum()) if scree[i]>ks]
    x_annot = annot[-1][0]
    y_annot = annot[-1][1]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=screeValues[:,0],
        y=screeValues[:,1],
        name='Eigenvalues',
    ))
    fig.add_trace(go.Scatter(
        x=screeCumsum[:,0],
        y=screeCumsum[:,1],
        name='Cumulative sum',
    ))
    # To be done, auto find the % of Eigenvalues for a fixed number of VP (or the inverse)
    fig.add_trace(go.Scatter(
        x=[0,x_annot,x_annot],
        y=[y_annot,y_annot,0],
        showlegend=False,
        line=dict(dash='dash',color='black',width=.5),
        marker=dict(size=.1)                        
    ))
    fig.add_annotation(
        x=x_annot, y=y_annot,
        text=f"{round(annot[-1][1],2)}%",
        showarrow=True,
        arrowhead=1
    )
    fig.add_annotation(
        x=x_annot, y=ks,
        text=f"Kaiser criteria : {round(ks,2)}%",
        showarrow=True,
        arrowhead=1
    )
    fig.update_layout(
        title = 'Eboulis des valeurs propres',
        xaxis=dict(
            title='Rang',
            titlefont_size=12,
            tickfont_size=12,
            range=[0,max_rank],
        ),
        yaxis=dict(
            title="% d'inertie",
            titlefont_size=12,
            tickfont_size=12,
            range=[0,100],
        ),
        width=800,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(showline=True,linewidth=1,linecolor='black')
    fig.update_yaxes(showline=True,linewidth=1,linecolor='black',gridcolor="lightgrey")
    fig.show()

def plot_projection(df_proj,axisRank,alpha=1):
    d1,d2=axisRank
    # affichage des points
    df_0 = df_proj[df_proj['TARGET']==0]
    df_1 = df_proj[df_proj['TARGET']==1]
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=df_0.iloc[:,d1-1],
        y=df_0.iloc[:,d2-1],
        name='Target 0',
        opacity=alpha,
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=df_1.iloc[:,d1-1],
        y=df_1.iloc[:,d2-1],
        name='Target 1',
        opacity=alpha,
        mode='markers'
    ))
    boundary = df_proj.iloc[:,d1-1:d2].abs().max(axis=1).max()*1.1
    fig.update_layout(
        title = f'Projection des valeurs sur les compostantes {d1} et {d2}',
        xaxis=dict(
            title=f'F{d1}',
            titlefont_size=12,
            tickfont_size=12,
            range=[-boundary,boundary],
        ),
        yaxis=dict(
            title=f"F{d2}",
            titlefont_size=12,
            tickfont_size=12,
            range=[-boundary,boundary],
        ),
        width=800,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(showline=True,linewidth=1,linecolor='black')
    fig.update_yaxes(showline=True,linewidth=1,linecolor='black',gridcolor="lightgrey")
    fig.show()