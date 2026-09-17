import cv2
import torch
import time
from ultralytics import YOLO

CONF = 0.15
IOU = 0.4
IMGSZ = 480
FRAME_SKIP = 1
TRACKER_TYPE = "bytetrack.yaml"
LOST_THRESHOLD = 15

model = YOLO('yolov8n.pt')

if torch.backends.mps.is_available():
    model.to('mps')
    print("MPS Aktif")
else:
    print("CPU kullaniliyor")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera acilamadi")
    exit()

is_locked = False
locked_id_text = ""
input_buffer = ""
current_detections = {}
tracker = None
lost_target_counter = 0
frame_counter = 0
prev_time = 0

print("Uygulama basladi. q: cikis, c: takibi iptal, t: takip et, 0-9: ID gir, Backspace: sil")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Goruntu alinamadi")
        break

    display_frame = frame.copy()
    frame_counter += 1

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
    prev_time = curr_time

    if not is_locked:
        if frame_counter % FRAME_SKIP == 0:
            results = model.track(frame, persist=True, tracker=TRACKER_TYPE, conf=CONF, iou=IOU, imgsz=IMGSZ, verbose=False)
            current_detections.clear()
            if results[0].boxes is not None and results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                ids = results[0].boxes.id.cpu().numpy().astype(int)
                for box, obj_id in zip(boxes, ids):
                    current_detections[obj_id] = box

        for obj_id, (x1, y1, x2, y2) in current_detections.items():
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            id_text = f"ID: {obj_id}"
            (tw, th), _ = cv2.getTextSize(id_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(display_frame, (x1, max(0, y1 - th - 10)), (x1 + tw + 10, y1), (0, 0, 255), -1)
            cv2.putText(display_frame, id_text, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.putText(display_frame, f"ARAMA MODU | Hedef Sec: {input_buffer}_", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    else:
        if tracker is not None:
            success, bbox = tracker.update(frame)
            if success:
                lost_target_counter = 0
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                center_x, center_y = x + w // 2, y + h // 2
                cv2.circle(display_frame, (center_x, center_y), 5, (255, 0, 0), -1)
                cv2.putText(display_frame, f"KILITLENDI: {locked_id_text} (CSRT)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            else:
                lost_target_counter += 1
                cv2.putText(display_frame, f"HEDEF ARANIYOR... ({lost_target_counter}/{LOST_THRESHOLD})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                if lost_target_counter > LOST_THRESHOLD:
                    print(f"Hedef kayboldu: {locked_id_text}")
                    is_locked = False
                    tracker = None
                    locked_id_text = ""
        else:
            is_locked = False

    cv2.putText(display_frame, f"FPS: {fps:.1f}", (display_frame.shape[1] - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Aga - AI Radar", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print("Cikis yapiliyor")
        break

    elif key in [ord('c'), ord('C')]:
        if is_locked:
            print(f"Takip iptal: {locked_id_text}")
        is_locked = False
        tracker = None
        input_buffer = ""
        locked_id_text = ""

    elif key in [ord('t'), ord('T')] and not is_locked:
        if input_buffer != "" and input_buffer.isdigit():
            target_id = int(input_buffer)
            temp_results = model.track(frame, persist=True, tracker=TRACKER_TYPE, conf=CONF, iou=IOU, imgsz=IMGSZ, verbose=False)
            found = False
            if temp_results[0].boxes is not None and temp_results[0].boxes.id is not None:
                boxes = temp_results[0].boxes.xyxy.cpu().numpy().astype(int)
                ids = temp_results[0].boxes.id.cpu().numpy().astype(int)
                for box, obj_id in zip(boxes, ids):
                    if obj_id == target_id:
                        tx1, ty1, tx2, ty2 = box
                        w, h = tx2 - tx1, ty2 - ty1
                        tracker = cv2.TrackerCSRT_create()
                        init_success = tracker.init(frame, (tx1, ty1, w, h))
                        if init_success:
                            is_locked = True
                            lost_target_counter = 0
                            locked_id_text = input_buffer
                            input_buffer = ""
                            print(f"Takip basladi ID: {locked_id_text}")
                            found = True
                        else:
                            print("Tracker baslatilamadi, tekrar dene")
                        break
            if not found:
                print(f"ID {input_buffer} ekranda yok, tekrar dene")
        else:
            print("Gecerli bir ID gir (rakam)")

    elif ord('0') <= key <= ord('9') and not is_locked:
        if len(input_buffer) < 4:
            input_buffer += chr(key)

    elif key == 8 and not is_locked:
        input_buffer = input_buffer[:-1]

cap.release()
cv2.destroyAllWindows()
print("Uygulama kapandi")