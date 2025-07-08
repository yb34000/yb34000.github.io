#Projet : Exploration des données salariales
#Partie 2 : Créer un tableau de bord interactif avec Streamlit

#import des bibliothèques
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as pt
import seaborn as sn



#configuration de la page
st.set_page_config(
    page_title="Tableau de bord des salaires",
    page_icon="E:/formation_python_wildcodeschool/icon.JPG",
    layout="wide"
)

#titre et description du tableau de bord

st.title(":blue[TABLEAU DE BORD]")
st.markdown("*Tableau de bord pour visualiser de manière interactive les fourchettes salariales.*")


#chargement de données
data = pd.read_excel('data_salary.xlsx')
data = pd.DataFrame(data)
data['experience_level'] = data['experience_level'].replace(
    ["EN", "MI", "SE", "EX"],
    ["Junior", "Intermediaire", "Senior", "Executif"]
)

                     
#attribution du nom du titre de la section
st.header(":green[Base de données salaires & emplois]")

#ajout d'une case à cocher, permettant d'afficher ou ne pas afficher la base de données
if st.checkbox("Afficher la base de données"):
   with st.expander("Dérouler pour afficher la base de données"):
     st.dataframe(data)


################################# separateur ##################################
st.header(":green[LOCALISATION]")
#Filtre  de sélection de localisation :un filtre des données basées sur la localisation.
#création de la liste d'options
options = data['continent'].unique()

#création de filtre de sélection 
select_continent = st.pills("Localisation de l'entreprise (choix multiple possible)", options, selection_mode="multi")

if  not select_continent:
    data_base = data
else:
    data_base = data[data['continent'].isin(select_continent)]

################################# separateur ##################################

#Ajouter une en-tête des options de filtre
st.sidebar.header("Options de filtre")

#Filtres interactifs 
#Créez une barre latérale avec des filtres qui permettent aux utilisateurs d'explorer interactivement les données.
#la base de données filtrée data_base
#Filtre de titre de poste :  une sélection multiple pour filtrer par titres de poste spécifiques.
#création d'une liste de titre de poste
job_list = data_base['job_title'].unique().tolist()

#création de filtre de sélection multiple de titre de poste

select_job = st.sidebar.multiselect(
    "Sélectionner des titres de poste (choix multiple possible)",
    job_list,
    default=job_list
)


if  not select_job:
    data_base = data_base
else:
    data_base = data_base[data_base['job_title'].isin(select_job)]

    

################################# separateur ##################################
#Filtre de niveau d'expérience : Un menu déroulant pour filtrer par niveau d'expérience (par exemple, junior, intermédiaire, senior).
#création d'une liste de niveau d'expérience   
level_list = data_base['experience_level'].unique().tolist()

#création de filtre de sélection multiple de niveau d'expérience
select_experience = st.sidebar.multiselect(
    "Choisir le niveau d'expérience",
    level_list,
    default=None
)

if  not select_experience:
    data_base = data_base
else:
    data_base = data_base[data_base['experience_level'].isin(select_experience)]






################################# separateur ##################################
#Curseur de ratio de travail à distance : Un curseur pour filtrer les données basées sur le pourcentage de travail à distance (0%, 50%, 100%).
#valeurs min et max du curseur
value_min = data_base['remote_ratio'].min()
value_max = data_base['remote_ratio'].max()

#curseur de seection
select_ratio = st.sidebar.slider(
    "Choisir le ratio de télétravail (soit 0%;   50%;   ou 100%)",
    value_min,
    value_max,
    (value_min, value_max),
    step=50
)
data_base = data_base[(data_base['remote_ratio'] >= select_ratio[0]) & (data_base['remote_ratio'] <= select_ratio[1]) ]



    

################################# separateur ##################################
#Affichage des métriques & KPIs clés : Fournissez un aperçu des métriques clés pour donner aux utilisateurs des insights rapides basés sur leurs sélections :
st.header(":green[KPI]")

#caulcul des metriques
#salaire moyen en dollar des données filtrées
salaire_moyen = data_base['salary_in_usd'].mean()


#salaire median en dollars des données filtrées
salaire_median = data_base['salary_in_usd'].median()


#titre de poste uniques dans les données filtrés
count_job = data_base['job_title'].count()

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.info("SALAIRE MOYEN EN DOLLARS", icon="💰")
    st.metric("Salaire moyen", 
              value=f"{salaire_moyen:.2f}$")

with kpi2:
    st.info("SALAIRE MEDIAN EN DOLLARS", icon="💰")
    kpi2.metric("salaire median ", 
            value=f"{salaire_median:.2f}$")
with kpi3:
    st.info("TOTAL DES POSTES", icon="🔢")
    st.metric("Nombre de titre", count_job)







################################# separateur ##################################
#créer des visualisations basée sur les données filtrées

st.header(":green[Dataviz]")

left, right = st.columns(2, gap="small")


#distribution de salaire vs taille entreprise
with left:
    #st.subheader("Distribution de salaire vs taille entreprise")
    sn.set_theme()
    fig1 = pt.figure(figsize=[6, 3])
    se = sn.barplot(data_base, x='company_size', y='salary_in_usd', hue='job_title',
                    order=['S', 'M', 'L'],
                    errorbar=None)
    xticklabel = ["Small", "Medium", "Large"]

    se.set_xlabel("Taille entreprise", fontsize=11)
    se.set_ylabel("Salaire en dollar", fontsize=11)
    se.set_xticklabels(xticklabel,  fontsize=9,  ha='center')
    se.set_yticklabels(se.get_yticks(),  fontsize=9)
    se.set_title("Distribution salariale par taille de l'entreprise et selon le titre du poste", 
                fontsize=12, color='blue')

    handles, label_k = se.get_legend_handles_labels()

    hue_map_k = {
        "Data Scientist" : 'Data Scientist',
        "Data Analyst" : 'Data Analyst',
        "Applied Scientist" : 'Applied Scientist',
        "Research Scientist" : 'Research Scientist',
        "Business Intelligence Engineer" : 'BI Engineer'
        }

    handles, label_k = se.get_legend_handles_labels()

    se.legend(handles, [hue_map_k[j] for j in label_k],
              title="FONCTIONS",
              title_fontsize=8,
              loc='upper left', 
              bbox_to_anchor=(1, 1),
              fontsize = 7
            )
    st.pyplot(fig1)


#evolution annuelle de salaire moyen par niveau d'expérience(ea_el)
with right:
    x = data_base['work_year'].unique()
    #st.subheader("Evolution annuelle de salaire moyen par niveau d'expérience")
    fig2 = pt.figure(figsize=[6, 3])
    es_an = sn.lineplot(data=data_base, x="work_year", y="salary_in_usd",
                        hue="experience_level", 
                        hue_order=["Junior", "Intermediaire", "Senior", "Executif"],
                        errorbar=None)

    es_an.set_xticks(x)
    es_an.set_xlabel("Année ", fontsize=11)
    es_an.set_ylabel("Salaire moyen en dollar", fontsize=11)
    es_an.set_xticklabels(x,  fontsize=9,  ha='center')
    es_an.set_yticklabels(es_an.get_yticks(),  fontsize=9)
    es_an.set_title("Evolution du salaire moyen par année et par niveau d'expérience", 
                    fontsize=12, color='blue')

    handles, labels = es_an.get_legend_handles_labels()

    es_an.legend(
                 title="NIVEAU D'EXPERIENCE",
                 title_fontsize=7,
                 loc='upper left', 
                 bbox_to_anchor=(1, 1),
                 fontsize = 7
                )
    st.pyplot(fig2)




################################# separateur ##################################

#organisation graphique
#left, right = st.columns(2)
#left.plotly_chart(fig1, use_container_width=True)
#right.plotly_chart(fig2, use_container_width=True)



################################# separateur ##################################
#résultat de l'application des filtres et téléchargement du fichier
csv = data_base.to_csv(index=False).encode("utf-8") 

with st.sidebar:
    st.subheader('Résultat du filtre')  
    st.download_button(
        label="Télécharger", 
        data=csv , 
        file_name="file.csv", 
        key='download-csv'
    )
























    










                    





