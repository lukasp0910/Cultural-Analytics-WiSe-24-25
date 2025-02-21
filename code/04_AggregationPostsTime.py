import pandas as pd
import os
import matplotlib.pyplot as plt

def aggregate_color_share(input_csv_path, output_path):
    try:
        df = pd.read_csv(input_csv_path)

        df['Datum'] = pd.to_datetime(df['Datum'])

        df['Monat'] = df['Datum'].dt.to_period('M').astype(str)

        result = (
            df.groupby(['Partei', 'Monat']).size()
            .reset_index(name='Anzahl der Posts')
        )

        result['Kumulative Anzahl'] = result.groupby('Partei')['Anzahl der Posts'].cumsum()

        all_months = pd.period_range(result['Monat'].min(), result['Monat'].max(), freq='M').astype(str)

        all_parties = result['Partei'].unique()
        full_index = pd.MultiIndex.from_product([all_parties, all_months], names=['Partei', 'Monat'])
        full_df = pd.DataFrame(index=full_index).reset_index()

        result = pd.merge(full_df, result, on=['Partei', 'Monat'], how='left')
        result['Anzahl der Posts'] = result['Anzahl der Posts'].fillna(0)
        result['Kumulative Anzahl'] = result['Kumulative Anzahl'].fillna(0)


        result['Anzahl der Posts'] = result['Anzahl der Posts'].astype(int)
        result['Kumulative Anzahl'] = result['Kumulative Anzahl'].astype(int)

        output_path_csv = os.path.join(output_path, "CSV.csv")
        output_path_plot = os.path.join(output_path, "Plot_Anzahl.jpg")
        output_path_plot_cumulative = os.path.join(output_path, "Plot_Kumulative_Anzahl.jpg")

        result.to_csv(output_path_csv, index=False)
        print(f"Die aggregierte Datei wurde erfolgreich erstellt: {output_path_csv}")

        party_colors = {
            "afd.bund": (0/255, 33/255, 200/255),  
            "cdu": (18/255, 18/255, 18/255),
            "csu": (0/255, 160/255, 233/255),  
            "die_gruenen": (120/255, 188/255, 27/255),   
            "dielinke": (189/255, 48/255, 117/255),  
            "fdp": (255/255, 204/255, 0/255),  
            "spdde": (215/255, 31/255, 29/255)   
        }

        plt.figure(figsize=(10, 6))
        for party in result['Partei'].unique():
            party_data = result[result['Partei'] == party]
            party_data['Anzahl der Posts'] = party_data['Anzahl der Posts'].rolling(window=10, center=True).mean()
            color = party_colors.get(party, (0, 0, 0))  # Standardfarbe Schwarz, falls nicht definiert
            plt.plot(party_data['Monat'], party_data['Anzahl der Posts'], label=party, color=color)

        plt.xlabel('Monat')
        plt.ylabel('Anzahl der Posts')
        plt.title('Anzahl der Posts pro Partei über die Zeit (geglättet)')
        plt.legend()

        # Gitternetz hinzufügen
        plt.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.7)


        all_ticks = result['Monat'].unique()
        selected_ticks = all_ticks[::6]  # Select every 6th month
        plt.xticks(ticks=selected_ticks, labels=selected_ticks, rotation=45)

        plt.tight_layout()

        plt.savefig(output_path_plot)
        print(f"Das Diagramm der Anzahl der Posts wurde erfolgreich erstellt: {output_path_plot}")

        plt.figure(figsize=(10, 6))
        for party in result['Partei'].unique():
            party_data = result[result['Partei'] == party]
            party_data['Kumulative Anzahl'] = party_data['Kumulative Anzahl'].rolling(window=3, center=True).mean()
            color = party_colors.get(party, (0, 0, 0))  # Standardfarbe Schwarz, falls nicht definiert
            plt.plot(party_data['Monat'], party_data['Kumulative Anzahl'], label=party, color=color)

        plt.xlabel('Monat')
        plt.ylabel('Kumulative Anzahl der Posts')
        plt.title('Kumulative Anzahl der Posts pro Partei über die Zeit (geglättet)')
        plt.legend()

        plt.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.7)

        plt.xticks(ticks=selected_ticks, labels=selected_ticks, rotation=45)

        plt.tight_layout()

        plt.savefig(output_path_plot_cumulative)
        print(f"Das Diagramm der kumulativen Anzahl der Posts wurde erfolgreich erstellt: {output_path_plot_cumulative}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

input_csv_path = r"C:\\Users\\pasol\\Pictures\\Database_CulturalAnalytics\\02_Processed\\result.csv"
output_path = r"C:\\Users\\pasol\\Pictures\\Database_CulturalAnalytics\\03_Analytics\\02_AggregatedPostsTime"
aggregate_color_share(input_csv_path, output_path)
