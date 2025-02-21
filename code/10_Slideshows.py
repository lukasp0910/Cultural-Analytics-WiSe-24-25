import pandas as pd
import os
import matplotlib.pyplot as plt

def analyse_farbanteile(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    df_slideshow = df[df["Slideshow"] == 1]
    
    parteien = df_slideshow["Partei"].unique()
    ergebnisse = []
    
    for partei in parteien:
        partei_df = df_slideshow[df_slideshow["Partei"] == partei]
        
        # Mittelwerte der Farbanteile pro Slide-Position berechnen (1-10)
        farbanteile = []
        for i in range(1, 11):
            mittelwert = partei_df[partei_df["Slide"] == i]["Farbanteil"].mean()
            farbanteile.append(round(mittelwert, 3) if not pd.isna(mittelwert) else 0)
        
        # Durchschnittlicher Farbanteil der Bilder ab Position 2 bis 10
        relevante_werte = [x for x in farbanteile[1:] if x != 0]
        mittelwert_2_10 = round(sum(relevante_werte) / len(relevante_werte), 3) if relevante_werte else 0
        
        ergebnisse.append([partei] + farbanteile + [mittelwert_2_10])
    
    spalten = [f"Slide_{i}" for i in range(1, 11)] + ["Durchschnitt_2_10"]
    df_output = pd.DataFrame(ergebnisse, columns=["Partei"] + spalten)
    

    output_path_csv = os.path.join(output_csv, "CSV.csv")
    df_output.to_csv(output_path_csv, index=False)
    print(f"Analyse abgeschlossen. Datei gespeichert unter: {output_path_csv}")
    
    party_colors = {
        "afd.bund": (0/255, 103/255, 150/255),  
        "cdu": (18/255, 18/255, 18/255),
        "csu": (0/255, 160/255, 233/255), 
        "die_gruenen": (120/255, 188/255, 27/255),   
        "dielinke": (189/255, 48/255, 117/255),  
        "fdp": (255/255, 204/255, 0/255),  
        "spdde": (215/255, 31/255, 29/255)   
    }
    
    plt.figure(figsize=(12, 6))
    for index, row in df_output.iterrows():
        partei = row["Partei"]
        color = party_colors.get(partei, (0, 0, 0))  # Standardfarbe schwarz, falls nicht definiert
        plt.plot(range(1, 11), row[spalten[:-1]], marker="o", label=partei, color=color)
    
    plt.xlabel("Slide-Position")
    plt.ylabel("Durchschnittlicher Farbanteil")
    plt.title("Verlauf der Farbanteile in Karussell-Posts")
    plt.xticks(range(1, 11))
    plt.legend(title="Partei")
    plt.grid(True)
    
    output_plot_path = os.path.join(output_csv, "Farbanteile_Slides.png")
    plt.savefig(output_plot_path, dpi=300, bbox_inches='tight')
    print(f"Plot gespeichert unter: {output_plot_path}")
    

if __name__ == "__main__":
    input_csv = r"C:\\Users\\pasol\\Pictures\\Database_CulturalAnalytics\\02_Processed\\result.csv"
    output_csv = r"C:\\Users\\pasol\\Pictures\\Database_CulturalAnalytics\\03_Analytics\\08_Slideshows"
    analyse_farbanteile(input_csv, output_csv)
