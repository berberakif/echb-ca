import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np
from pathlib import Path

@st.cache_data
def load_pca_data():
    DATA_FILENAME = Path(__file__).resolve().parent.parent / 'data' / 'PCA_Analysis.json'
    with open(DATA_FILENAME, 'r') as f:
        return json.load(f)

@st.cache_data
def load_component_ranking_data():
    DATA_FILENAME = Path(__file__).resolve().parent.parent / 'data' / 'PCA_Components_Ranking_By_Role.json'
    with open(DATA_FILENAME, 'r') as f:
        return json.load(f)

def pca_analysis():
    # Display the explanatory paragraph at the top
    st.markdown("""
    **PCA Analysis Overview**

    We used Principal Component Analysis (PCA) to simplify the survey data and find the most important factors that affect participant satisfaction. 
    The analysis identified five key components:

    1. **Academic Quality:** Participants care a lot about the depth and quality of the academic content.
    2. **Practical Sessions:** How well-organized and effective the practical sessions are matters greatly to participants.
    3. **Technical and Operational Support:** While important, technical and operational aspects are less influential than academic and practical content.
    4. **Financial and Administrative Processes:** These are important but not as critical as academic and practical components.
    5. **Usability and Accessibility:** Participants value easy access to resources and user-friendly platforms.

    The results suggest that focusing on improving academic content and practical sessions will have the biggest impact on overall satisfaction. Other areas like technical support and administrative processes should still be maintained at a high standard but are secondary to the main content and structure of the program.
    """)

    # Load data
    pca_data = load_pca_data()
    component_ranking_data = load_component_ranking_data()

    # Component Ranking by Role
    st.subheader("Component Ranking by Role")
    for role, data in component_ranking_data.items():
        df_role = pd.DataFrame(data)
        st.write(f"### {role}")
        st.bar_chart(df_role.set_index("PCA_Component")["Average_Score"])

    # Scree Plot
    st.subheader("Scree Plot")
    explained_variance = pd.Series(pca_data['Explained_Variance'])
    plt.figure(figsize=(10, 6))
    plt.plot(explained_variance.index, explained_variance.values, 'o-', color='b')
    plt.title('Scree Plot')
    plt.xlabel('Principal Component')
    plt.ylabel('Variance Explained')
    plt.grid()
    st.pyplot(plt)

    # Biplot for PC1 and PC2 (Simplified)
    st.subheader("Biplot of PC1 and PC2")
    pca_components = pd.DataFrame(pca_data['PCA_Components'])
    loadings = pd.DataFrame(pca_data['Loadings'])

    plt.figure(figsize=(10, 10))
    plt.scatter(pca_components['PC1'], pca_components['PC2'])

    # Simplify by showing only a few components with the highest loadings
    top_loadings = loadings.abs().sum(axis=1).sort_values(ascending=False).head(5).index
    for i in top_loadings:
        plt.arrow(0, 0, loadings['PC1'][i], loadings['PC2'][i], color='r', alpha=0.5)
        plt.text(loadings['PC1'][i] * 1.15, loadings['PC2'][i] * 1.15, i, color='g', ha='center', va='center')

    plt.xlabel(f"PC1 - {explained_variance['PC1']:.2%} Variance Explained")
    plt.ylabel(f"PC2 - {explained_variance['PC2']:.2%} Variance Explained")
    plt.title('Biplot of PC1 and PC2')
    plt.grid()
    st.pyplot(plt)

    # Heatmap of Component Loadings (Simplified)
    st.subheader("Heatmap of Component Loadings")
    # Focus on top components and features
    top_features = loadings.abs().sum(axis=1).sort_values(ascending=False).head(10).index
    loadings_transposed = loadings.loc[top_features].transpose()

    plt.figure(figsize=(12, 8))
    sns.heatmap(loadings_transposed, annot=True, cmap='coolwarm')
    plt.title('Heatmap of Component Loadings')
    st.pyplot(plt)
