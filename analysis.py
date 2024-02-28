import utils
import cv2

# Load radar image
image = cv2.imread("radar.png")

# Initialisation
fenetre = []
fixations = []
fixation_temp = []
D = 20  # seuil de déviation
aois = utils.load_aoi_file()  # Charger les AOIs
fixations_aoi = {}  # Pour stocker les fixations correspondant aux AOIs

# FIXATIONS
for t, x, y in utils.read_data_file(real_time=False):
    fenetre.append([t, x, y])

    if fenetre[-1][0] - fenetre[0][0] > 150:
        fenetre.pop(0)

        # centroïde et déviation maximale
        centroid, deviation = utils.calculate_centroid_deviation(fenetre)

        # gérer les fixations
        if deviation <= D:
            if not fixation_temp:
                fixation_temp = fenetre.copy()
            else:
                fixation_temp.append(fenetre[-1])
        else:
            if fixation_temp:
                fixations.append(fixation_temp)
                fixation_temp = []
                fenetre.clear()

# afficher les résultat des fixations
print("FIXATIONS:")
print(f"nombre de fixations : {len(fixations)}")
durations = [fixation[-1][0] - fixation[0][0] for fixation in fixations]
moyenne_duree = sum(durations) / len(durations) if durations else 0
print(f"durée moyenne des fixations : {moyenne_duree} ms")
print("-----------------------------------------")

#AOIs (aires d’intérêt correspondant aux étiquettes des avions sur l’image radar)
# Gestion des AOIs pour chacune des fixations
for fixation in fixations:
    centroid, _ = utils.calculate_centroid_deviation(fixation)
    x_centroid, y_centroid = centroid
    for aoi_name, (x_left, y_top, x_right, y_bottom) in aois.items():
        if x_left <= x_centroid <= x_right and y_top <= y_centroid <= y_bottom:
            cv2.rectangle(image, (x_left, y_top), (x_right, y_bottom), (255, 0, 0), 2)
            if aoi_name not in fixations_aoi:
                fixations_aoi[aoi_name] = {'count': 0, 'total_duration': 0}
            fixations_aoi[aoi_name]['count'] += 1
            fixations_aoi[aoi_name]['total_duration'] += fixation[-1][0] - fixation[0][0]
            break  # on arrête la boucle dès qu'une AOI correspondante est trouvée

# Affichage des positions du regard comme saccades
previous_position = None
for _, x, y in utils.read_data_file(real_time=False):
    if previous_position is not None:
        cv2.line(image, previous_position, (x, y), (0, 255, 0), 1)
    previous_position = (x, y)

# Affichage des fixations
for fixation in fixations:
    centroid, deviation = utils.calculate_centroid_deviation(fixation)
    x_centroid, y_centroid = centroid
    cv2.circle(image, (int(x_centroid), int(y_centroid)), int(deviation), (0, 0, 255), 2)

# Calculs supplémentaires pour répondre aux questions
nombre_total_fixations = sum(data['count'] for data in fixations_aoi.values())
duree_totale_fixation = sum(data['total_duration'] for data in fixations_aoi.values())

print(f"nombre des fixations sur les AOIs: {nombre_total_fixations}")
print(f"durée des fixation sur les AOIs: {duree_totale_fixation} ms")
print("-----------------------------------------")

# Save the final visualisation
cv2.imwrite("Radar_visualisation_eye_tracking.png", image)
