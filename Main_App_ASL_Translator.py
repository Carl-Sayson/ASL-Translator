# Main Application for ASL Translator
# Main Issue with the program is with the model used in order to predict the sign languages
# The model is not accurate because of lighting issues and camera angles. Recommended to produce your own data such as capturing self images to train

from main_hand_translator_ui import Ui_MainWindow as ASL_window
import mediapipe as mp

from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
from mediapipe.tasks.python.core.base_options import BaseOptions
import sys
import time
import numpy as np
import cv2
from keras.models import load_model

from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PySide6.QtCore import Qt, QTimer, Signal, QThread, QObject, QEvent
from PySide6.QtGui import QImage, QPixmap

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_window = ASL_window()
        self.main_window.setupUi(self)
        # for camera functions
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # loads the model
        self.load_model()

        # setup for hand detection
        self.hand_landmarker = self.setup_hand_landmarker("hand_landmarker.task")

        # setup ui and toggle
        self.main_window.stackedWidget.setCurrentIndex(0)
        self.main_window.toggle_cam.clicked.connect(self.toggle_cam)
        self.cap = None
        self.start_camera()

        # open text but would have function to prevent exit when ASL translation is active
        self.active_status_translation = False 
        self.main_window.open_text.clicked.connect(self.open_dock_text) 

        # clears text
        self.main_window.Clear_btn.clicked.connect(lambda: self.main_window.text_translation.clear())

        # for translation and loading of model
        self.labels = [chr(i) for i in range(65, 91) if i != 74 and i != 90]

        # For the detection 
        self.main_window.Start_translation.clicked.connect(self.start_detection)
        self.main_window.End_translation.clicked.connect(self.stop_detection)

        # delay to prevent freezing
        self.last_prediction_time = 0
        self.prediction_delay = 2
        self.last_prediction_letter = None
        
    def load_model(self):
        self.thread_model = QThread()
        self.worker_model = LoadModel()
        self.worker_model.moveToThread(self.thread_model)

        self.thread_model.started.connect(self.worker_model.run)

        self.worker_model.finished.connect(self.success_load)
        self.worker_model.error.connect(self.load_err)

        self.worker_model.finished.connect(self.thread_model.quit)
        self.worker_model.finished.connect(self.worker_model.deleteLater)
        self.thread_model.finished.connect(self.thread_model.deleteLater)

        self.thread_model.start()
   
    def success_load(self, model):
        self.model = model
        print('model loaded')

    def load_err(self, msg):
        QMessageBox.critical(None, "Load Error", msg)
        return

    def start_detection(self):
        self.active_status_translation = True

    def stop_detection(self):
        self.active_status_translation = False

    def open_dock_text(self):
        dock = self.main_window.dockWidget_text
        if not dock.isVisible():
            dock.show()

        dock.raise_()
        dock.activateWindow()

    def start_camera(self):
        try:
            self.loader_thread = QThread()
            self.camera_loader = Open_Cam_quick()
            self.camera_loader.moveToThread(self.loader_thread)

            self.loader_thread.started.connect(self.camera_loader.run)
            self.camera_loader.finished.connect(self.on_camera_ready)
            self.camera_loader.error.connect(self.on_camera_error)

            self.camera_loader.finished.connect(self.loader_thread.quit)
            self.camera_loader.finished.connect(self.camera_loader.deleteLater)
            self.loader_thread.finished.connect(self.loader_thread.deleteLater)

            self.loader_thread.start()
        except Exception as err:
            QMessageBox.warning(None, "Error video display", f"Error occurred in displaying video {err}")
            return

    def on_camera_ready(self, cap):
        self.cap = cap
        self.timer.start(30)

    def on_camera_error(self, message):
        QMessageBox.critical(None, "Camera Error", message)

    def setup_hand_landmarker(self, model_path):
        base_options = BaseOptions(model_asset_path=model_path)
        options = HandLandmarkerOptions(
            base_options=base_options,
            running_mode=RunningMode.IMAGE,
            num_hands=1
        )
        return HandLandmarker.create_from_options(options)# create a hand landmarker    

    def predict_sign(self, frame, current_time):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self.hand_landmarker.detect(mp_image)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                for landmark in hand_landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)
            # 👋 Create a bounding box around landmarks
            hand = result.hand_landmarks[0]
            h, w, _ = frame.shape
            xs = [lm.x * w for lm in hand]
            ys = [lm.y * h for lm in hand]
            x_min, x_max = int(min(xs)), int(max(xs))
            y_min, y_max = int(min(ys)), int(max(ys))

            # ✂️ Crop and resize the hand ROI
            margin = 20  # for padding
            roi = frame[max(0, y_min - margin):min(h, y_max + margin),
                        max(0, x_min - margin):min(w, x_max + margin)]
            
            if roi.size == 0:
                return

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (28, 28))
            normalized = resized / 255.0
            reshaped = normalized.reshape(1, 28, 28, 1)

            # 🧠 Predict using your trained model
            prediction = self.model.predict(reshaped, verbose=0)
            confidence = np.max(prediction)
            class_id = np.argmax(prediction)
            if confidence < 0.65:
                return # returns if low confidence with the letter

            letter = self.labels[class_id]
            print(letter)

            if letter != self.last_prediction_letter:
                self.main_window.text_translation.insertPlainText(letter)
                self.last_prediction_letter = letter
                self.last_prediction_time = current_time

            cv2.putText(frame, f"Prediction: {letter}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "No hand detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
        
    def update_frame(self):
        if not self.cap:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=50)

        current_time = time.time()
        # ✅ Only predict if translation is active
        if self.active_status_translation and current_time - self.last_prediction_time > self.prediction_delay:
            self.predict_sign(frame, current_time) # calls the prediction of hand

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        self.main_window.video_capture.setPixmap(pixmap.scaled(
        self.main_window.video_capture.size(),
        Qt.IgnoreAspectRatio,      # Or Qt.IgnoreAspectRatio for full stretch
        Qt.SmoothTransformation  # Optional: smoother scaling
    ))

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.main_window.video_capture.clear()

    def toggle_cam(self):
        if self.cap is None:
            self.start_camera()
        else:
            self.stop_camera()


class Open_Cam_quick(QObject):
    finished = Signal(cv2.VideoCapture)
    error = Signal(str)

    def run(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Camera failed to open.")
            self.finished.emit(cap)
        except Exception as e:
            self.error.emit(str(e))


class LoadModel(QObject):
    finished = Signal(object)
    error = Signal(str)

    def run(self):
        try:
            self.model = load_model('asl_alphabet_model.h5')
            self.finished.emit(self.model)
        except Exception as err:
            self.error.emit(err)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())   