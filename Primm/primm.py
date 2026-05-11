import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("mapa3.PNG")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

vertices = np.load("verticeMapa3.npy")

R = img_rgb[:, :, 0]
G = img_rgb[:, :, 1]
B = img_rgb[:, :, 2]

# mascara para las calles. en este caso buscamos que las calles se noten con el color blanco en rgb (255, 255, 255)
tolerancia_calles = 4

mascara_calles = (
    (R >= 255 - tolerancia_calles) &
    (G >= 255 - tolerancia_calles) &
    (B >= 255 - tolerancia_calles)
)

# realizamos una lista con los colores exactos, extraidos de los mapas proporcionados.
colors = [
    ("#858d93", 0),
    ("#c5c9d9", 0),
    ("#c5c5c9", 0),
    ("#c5c9cd", 0),
    ("#c4c8d8", 0),
    ("#787c80", 0),
    ("#797d81", 0),
    ("#cdcdd1", 0),
    ("#a7a9ad", 10),
]

mascara_letras_calle = np.zeros(mascara_calles.shape, dtype=bool)

for hex_color, tolerance in colors:
    rgb_color = np.array([
        int(hex_color[1:3], 16),
        int(hex_color[3:5], 16),
        int(hex_color[5:7], 16)
    ])

    diff = np.abs(img_rgb.astype(int) - rgb_color)

    current_mask = (
        (diff[:, :, 0] <= tolerance) &
        (diff[:, :, 1] <= tolerance) &
        (diff[:, :, 2] <= tolerance)
    )

    mascara_letras_calle = mascara_letras_calle | current_mask

# combinar las mascaras que realizamos
mask = mascara_calles | mascara_letras_calle
mask = mask.astype(np.uint8) * 255

# limpiar y conectar
kernel = np.ones((3, 3), np.uint8)

mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
mask = cv2.dilate(mask, kernel, iterations=1)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

# mostrar mapa original con vertices y mascara con vertices
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(img_rgb)
plt.scatter(vertices[:, 1], vertices[:, 0], s=35)
plt.title("Original Map with Vertices")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(mask, cmap="gray")
plt.scatter(vertices[:, 1], vertices[:, 0], s=35)
plt.title("Road Mask with Vertices")
plt.axis("off")

plt.show()

cv2.imwrite("mask_roads.png", mask)