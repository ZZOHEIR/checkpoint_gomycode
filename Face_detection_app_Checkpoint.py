import cv2
import streamlit as st
import os

# Charger le classificateur de cascade de visages
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if st.button('instructions'):
    st.write('How to use the app:')
    st.write('1. Press the camera button to detect your face')
    st.write('2. Use the MinNeighbour slider to adjust how many neighbors each candidate rectangle should have to retain it')
    st.write('3. Use the Scaler slider to specify how much the image size is reduced at each image scale')

def detect_faces(scaleFactor, minNeighbors, color):
    # Initialiser la webcam
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    
    while True:
        # Lire les images de la webcam
        ret, frame = cap.read()
        
        # Vérifier si la capture de la trame a réussi
        if not ret:
            st.error('Failed to capture frame!')
            break

        # Convertir les images en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détecter les visages à l'aide du classificateur de cascade de visages
        faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
        
        # Dessiner des rectangles autour des visages détectés
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Convertir l'image en RGB pour l'affichage avec Streamlit
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(rgb_frame, channels='RGB', use_container_width=True)

        # Save the frame if the user clicked the save button
        if st.session_state.get('save_image', False):
            save_image(frame)
            st.session_state['save_image'] = False
        
        # Sortir de la boucle lorsque 'q' est pressé
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérer la webcam et fermer toutes les fenêtres
    cap.release()
    cv2.destroyAllWindows()

def save_image(frame):
    filename = st.text_input("Enter the filename (with .jpg extension):", "detected_faces.jpg")
    directory = st.text_input("Enter the directory path to save the image:", os.getcwd())
    
    if st.button("Confirm Save"):
        full_path = os.path.join(directory, filename)
        cv2.imwrite(full_path, frame)
        st.success(f"Image saved successfully as '{full_path}'")

def app():
    st.title("Face Detection using Viola-Jones Algorithm")
    
    # Sliders for adjusting face detection parameters
    scaleFactor = st.slider("Scale Factor", 1.05, 1.5, 1.1)
    minNeighbors = st.slider("Min Neighbors", 3, 10, 5)
    
    # Couleur du rectangle ... le bleu et le rouge sont inverse
    color = st.color_picker("Choose the color for the rectangles around detected faces", "#00FF00")
    color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    st.write("Appuyez sur le bouton ci-dessous pour commencer à détecter des visages à partir de votre webcam")

    # Ajouter un bouton pour commencer à détecter les visages
    if st.button("Camera button"):
        detect_faces(scaleFactor, minNeighbors, color)

    # Section pour sauvegarder l'image détectée
    if st.button("Save Image"):
        st.session_state['save_image'] = True
        save_image()

if __name__ == "__main__":
    app()
