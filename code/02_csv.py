import os
import csv
import re
import json
from PIL import Image, ImageDraw
import numpy as np

def calculate_color_percentage(image_path, target_rgb_list, overlay_folder, delta):
    """
    Berechnet den Anteil der Pixel, die mit einem der Ziel-RGB-Werte innerhalb eines Deltas übereinstimmen,
    und erzeugt ein Overlay-Bild zur Visualisierung.

    """
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    image_array = np.array(image)
    
    mask = np.zeros(image_array.shape[:2], dtype=bool)

    # Iteriere über Ziel-RGB-Werte und aktualisiere die Maske
    for target_rgb in target_rgb_list:
        diff = np.abs(image_array - target_rgb)
        mask |= np.all(diff <= delta, axis=-1)
    
    # Zähle, wie viele Pixel innerhalb des Deltas liegen
    target_pixel_count = np.sum(mask)
    # Gesamtanzahl der Pixel im Bild
    total_pixel_count = image_array.shape[0] * image_array.shape[1]
    
    if True:
        overlay_image = image.copy()
        draw = ImageDraw.Draw(overlay_image)
        # Färbe die Ziel-Pixel
        for y in range(image_array.shape[0]):
            for x in range(image_array.shape[1]):
                if mask[y, x]:
                    draw.point((x, y), fill=(252, 10, 228))  # Markierung
        
        # Speichere das bearbeitete Bild im Overlay-Ordner
        if not os.path.exists(overlay_folder):
            os.makedirs(overlay_folder)
        
        base_filename = os.path.basename(image_path)
        overlay_filename = f"{os.path.splitext(base_filename)[0]}_delta{delta}.jpg"
        overlay_filepath = os.path.join(overlay_folder, overlay_filename)
        
        overlay_image.save(overlay_filepath)
    
    # Berechne den Anteil der Ziel-Pixel
    result = target_pixel_count / total_pixel_count
    return round(result, 4)

def create_csv_from_project(project_path, parties, target_rgb_dict):
    if os.path.exists(os.path.join(project_path, "Database")):
        database_folder = os.path.join(project_path, "Database")
    else:
        print(f"Es existiert keine Database in: {project_path}")
        return

    # Ausgabe-Datei
    output_file = os.path.join(project_path, "output.csv")
    # Ordner für Overlay-Bilder
    overlay_folder = os.path.join(project_path, "Overlay_Images")

    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL, escapechar='\\')
        csv_writer.writerow(["Partei", "Datum", "Uhrzeit", "Slideshow", "Slide", "Likes", "Kommentare", "Dateiname", "RGB Anteil Delta 50" , "RGB Anteil Delta 70", "RGB Anteil Delta 90"])
        
        # Iteriere durch alle Parteiordner im Projektordner
        for party_folder in os.listdir(database_folder):
            if party_folder not in parties:
                continue

            party_path = os.path.join(database_folder, party_folder)

            target_rgb_list = target_rgb_dict[party_folder]
            print(party_folder)
            print(target_rgb_list)

            if os.path.isdir(party_path):
                jpg_folder = os.path.join(party_path, "jpg")
                json_folder = os.path.join(party_path, "json")

                for filename in os.listdir(jpg_folder):
                    if filename.endswith(".jpg"):                        
                        base_filename = os.path.splitext(filename)[0]  
                        split_base_filename = base_filename.split('_')  
                        date = split_base_filename[0]  
                        time = split_base_filename[1]  

                        
                        slideshow = 0
                        slide = 1

                        match = re.search(r'_(\d+)$', base_filename)
                        if match:
                            slideshow = 1
                            slide = int(match.group(1))  

                        # Likes und Kommentarzahl aus Json auslesen
                        json_file_path = os.path.join(json_folder, filename.replace(".jpg", ".json"))
                        if os.path.exists(json_file_path):
                            with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
                                data = json.load(jsonfile)
                                if 'node' in data and 'edge_media_preview_like' in data['node']:
                                    likes = data['node']['edge_media_preview_like']['count']
                                if 'node' in data and 'comments' in data['node']:
                                    comments = data['node']['comments']

                        
                        jpg_file_path = os.path.join(jpg_folder, filename)
                        color_percentage_50 = calculate_color_percentage(jpg_file_path, target_rgb_list, overlay_folder, 40)
                  

                        print(f"Schreibe Zeile: {[party_folder, date, time, slideshow, slide, likes, comments, filename,color_percentage_50]}")#, color_percentage_70, color_percentage_90]}")
                        csv_writer.writerow([party_folder, date, time, slideshow, slide, likes, comments, filename,color_percentage_50])#, color_percentage_70, color_percentage_90])
                        
    print(f"CSV-Datei wurde erstellt: {output_file}")

if __name__ == "__main__":
    project_path = r"C:\Users\pasol\Pictures\Database_CulturalAnalytics"
    
    # Ziel-RGB-Werte für die Parteifarben
    target_rgb_dict = {
        "afd.bund" : [(19,155,217),(254,0,0),(226,1,1),(3,70,122),(90,204,255)],
        "cdu" : [(82,183,193),(63,137,198),(249,180,0),(225,0,24)],
        "csu" : [(154,201,21),(33,131,206),(19,230,249),(0,125,184),(16,228,249),(72,199,240),(117,184,255),(36,180,145),(214,249,23)],
        "die_gruenen" : [(255,239,38),(74,150,41),(230,0,126),(158,200,102),(18,96,50),(255,241,122),(139,188,37),(0,137,57)],
        "dielinke" : [(226,6,18),(79,187,199),(112,0,59),(232,78,68)],
        "fdp" : [(254,237,1),(0,159,227),(227,1,126),(166,2,125),(254,138,173)],
        "spdde" : [(224,0,26),(255,89,49),(166,26,1)]     
    }

    parties = ["csu"]

    if os.path.exists(project_path):
        create_csv_from_project(project_path, parties, target_rgb_dict)
    else:
        print(f"Pfad existiert nicht: {project_path}")
