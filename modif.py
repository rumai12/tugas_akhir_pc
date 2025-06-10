import cv2
import mediapipe as mp
import pyautogui
import pyttsx3

# Inisialisasi
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Tambahan: Inisialisasi suara dan statistik
engine = pyttsx3.init()
engine.setProperty('rate', 150)
klik_kiri = 0
arah_pandang = "Tengah"

def ucapkan(teks):
    engine.say(teks)
    engine.runAndWait()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Tambahan: deteksi arah pandang (berdasarkan titik 1 dari id 474-478)
        pupil = landmarks[475]
        pupil_x = int(pupil.x * frame_w)
        if pupil_x < frame_w * 0.4:
            arah_pandang = "Kiri"
        elif pupil_x > frame_w * 0.6:
            arah_pandang = "Kanan"
        else:
            arah_pandang = "Tengah"

        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            ucapkan("Klik kiri")              # Tambahan: suara klik
            klik_kiri += 1                    # Tambahan: hitung klik
            pyautogui.sleep(1)

    # Tambahan: tampilkan statistik di GUI
    cv2.putText(frame, f"Klik kiri: {klik_kiri}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Arah pandang: {arah_pandang}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
