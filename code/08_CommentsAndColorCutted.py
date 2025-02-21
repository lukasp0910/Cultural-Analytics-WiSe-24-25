import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def plot_comments_vs_color_share(input_csv_path, output_path):
    try:
        df = pd.read_csv(input_csv_path)

        df['Datum'] = pd.to_datetime(df['Datum'])

        party_colors = {
            "afd.bund": (0/255, 33/255, 200/255),  
            "cdu": (18/255, 18/255, 18/255),  
            "csu": (0/255, 160/255, 233/255),
            "die_gruenen": (120/255, 188/255, 27/255),   
            "dielinke": (189/255, 48/255, 117/255),  
            "fdp": (255/255, 204/255, 0/255),  
            "spdde": (215/255, 31/255, 29/255)   
        }

        for party in df['Partei'].unique():
            party_data = df[df['Partei'] == party]

            # Remove rows with Farbanteil <= 0.1
            party_data = party_data[party_data['Farbanteil'] > 0.1]

            lower_percentile = party_data['Kommentare'].quantile(0.05)
            upper_percentile = party_data['Kommentare'].quantile(0.95)
            party_data_filtered = party_data[(party_data['Kommentare'] > lower_percentile) & (party_data['Kommentare'] < upper_percentile)]

            color = party_colors.get(party, (0, 0, 0))  

            plt.figure(figsize=(10, 6))
            plt.scatter(party_data_filtered['Farbanteil'], party_data_filtered['Kommentare'], label=party, color=color, alpha=0.6)

            x = party_data_filtered['Farbanteil']
            y = party_data_filtered['Kommentare']
            slope, intercept = np.polyfit(x, y, 1)  # Linear regression: y = mx + b


            plt.plot(x, slope * x + intercept, color='black', linestyle='-', linewidth=2, label='Regressionslinie')

            pearson_corr = np.corrcoef(x, y)[0, 1]
            spearman_corr, _ = stats.spearmanr(x, y)


            plt.xlabel('Farbanteil')
            plt.ylabel('Kommentare')
            plt.title(f'Kommentare vs Farbanteil für {party} (Farbanteil > 0.1)')
            
            text_annotation = (
                f"Pearson-Korrelationskoeffizient: {pearson_corr:.2f}\n"
                f"Spearman-Korrelationskoeffizient: {spearman_corr:.2f}"
            )
            plt.text(0.05, 0.95, text_annotation, fontsize=10, transform=plt.gca().transAxes, 
                     verticalalignment='top', bbox=dict(boxstyle="round", alpha=0.5, facecolor="white"))


            plt.legend()
            plt.grid(True)

            output_path_plot = os.path.join(output_path, f"{party}_CommentsAndColor_with_regression_cutted.jpg")
            plt.tight_layout()
            plt.savefig(output_path_plot)
            print(f"Das Diagramm für {party} wurde erfolgreich erstellt: {output_path_plot}")

            plt.close()

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


input_csv_path = r"C:\\Users\\pasol\\Pictures\\Database_CulturalAnalytics\\02_Processed\\result.csv"
output_path = r"C:\\Users\\pasol\\Pictures\\Database_CulturalAnalytics\\03_Analytics\\06_CommentsAndColorCutted"
plot_comments_vs_color_share(input_csv_path, output_path)
