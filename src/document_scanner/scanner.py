import cv2
import numpy as np
import os


class DocumentScanner:
    """
    SPACE → Cropped capture (locked)
    SPACE → Full capture (tracking OFF or no confidence)
    U     → Toggle detection tracking
    R     → Rotate preview & capture
    B     → Change basename (in-window)
    Q/ESC → Quit
    """

    def __init__(
        self,
        camera_index=0,
        canny_low=60,
        canny_high=150,
        min_contour_area=1500,
        confidence_threshold=0.75,
        confidence_decay=0.01,
        window_name="Detection",
        basename="capture",
        output_dir=".",
        ext=".jpg",
    ):
        self.camera_index = camera_index
        self.canny_low = canny_low
        self.canny_high = canny_high
        self.min_contour_area = min_contour_area
        self.confidence_threshold = confidence_threshold
        self.confidence_decay = confidence_decay
        self.window_name = window_name
        self.basename = basename
        self.output_dir = output_dir
        self.ext = ext

        os.makedirs(self.output_dir, exist_ok=True)

        # Detection state
        self.tracking_enabled = True
        self.locked = False
        self.confidence = 0.0
        self.locked_bbox = None

        # Rotation
        self.rotation = 0

        # Filename counter
        self.file_index = 1

        # Basename input
        self.naming_mode = False
        self.name_buffer = ""

        self.cap = None

    # -----------------------
    # ROTATION
    # -----------------------
    def rotate_frame(self, frame):
        if self.rotation == 90:
            return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif self.rotation == 180:
            return cv2.rotate(frame, cv2.ROTATE_180)
        elif self.rotation == 270:
            return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return frame

    def toggle_rotation(self):
        self.rotation = (self.rotation + 90) % 360
        print(f"🔄 Rotation: {self.rotation}°")

    # -----------------------
    # BASENAME INPUT WINDOW
    # -----------------------
    def start_basename_input(self):
        self.naming_mode = True
        self.name_buffer = self.basename
        cv2.namedWindow("Set Basename", cv2.WINDOW_NORMAL)

    def draw_basename_window(self):
        canvas = np.zeros((130, 520, 3), dtype=np.uint8)

        cv2.putText(canvas, "Enter new basename:", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(canvas, (20, 55), (500, 95), (255, 255, 255), 2)

        cv2.putText(canvas, self.name_buffer + "|", (25, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(canvas, "ENTER = OK     ESC = Cancel", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

        cv2.imshow("Set Basename", canvas)

    def handle_basename_keys(self, key):
        if key in (10, 13):  # ENTER
            if self.name_buffer.strip():
                self.basename = self.name_buffer.strip()
                self.file_index = 1
                print(f"📁 Basename set to: {self.basename}")
            self.naming_mode = False
            cv2.destroyWindow("Set Basename")

        elif key == 27:  # ESC
            self.naming_mode = False
            cv2.destroyWindow("Set Basename")

        elif key in (8, 127):  # BACKSPACE
            self.name_buffer = self.name_buffer[:-1]

        elif 32 <= key <= 126:
            self.name_buffer += chr(key)

    # -----------------------
    # TRACKING
    # -----------------------
    def toggle_tracking(self):
        self.tracking_enabled = not self.tracking_enabled
        self.locked = False
        self.locked_bbox = None
        self.confidence = 0.0
        print("🎯 Tracking:", "ON" if self.tracking_enabled else "OFF")

    # -----------------------
    # CAPTURE
    # -----------------------
    def capture(self, clean_frame):
        if not self.tracking_enabled or not self.locked:
            filename = self.make_filename()
            cv2.imwrite(filename, clean_frame)
            self.file_index += 1
            print(f"📸 Captured (full): {filename}")
            return

        x, y, w, h = self.locked_bbox
        cropped = clean_frame[y:y + h, x:x + w]
        filename = self.make_filename()
        cv2.imwrite(filename, cropped)
        self.file_index += 1
        print(f"📸 Captured (cropped): {filename}")

    def make_filename(self):
        parts = [self.basename]
        parts.append(f"{self.file_index:03d}")
        return os.path.join(self.output_dir, "_".join(parts) + self.ext)

    # -----------------------
    # DRAWING
    # -----------------------
    def draw_instructions(self, frame):
        lines = [
            "SPACE : Capture",
            "U     : Toggle Tracking",
            "R     : Rotate",
            "B     : Change Basename",
            "Q / ESC : Quit",
        ]

        x = frame.shape[1] - 260
        y = frame.shape[0] - 150

        cv2.rectangle(frame, (x - 10, y - 25), (x + 240, y + 105), (0, 0, 0), -1)

        for i, line in enumerate(lines):
            cv2.putText(frame, line, (x, y + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    def draw_filename(self, frame):
        suffix = "full" if not self.locked else "cropped"
        preview = self.make_filename()

        cv2.rectangle(frame, (10, 10), (frame.shape[1] - 10, 55), (0, 0, 0), -1)
        cv2.putText(frame, f"Next file: {os.path.basename(preview)}",
                    (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        cv2.putText(frame, f"Rotation: {self.rotation}°",
                    (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)

    # -----------------------
    # MAIN LOOP
    # -----------------------
    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        cv2.namedWindow(self.window_name)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            rotated = self.rotate_frame(frame)
            display = rotated.copy()

            if self.tracking_enabled:
                bbox = self._detect(rotated)
                self._update_confidence(bbox)
                self._draw_overlay(display, bbox)

            self.draw_filename(display)
            self.draw_instructions(display)
            cv2.imshow(self.window_name, display)
            self.draw_filename(display)
            cv2.imshow(self.window_name, display)

            key = cv2.waitKey(1) & 0xFF

            if self.naming_mode:
                self.draw_basename_window()
                self.handle_basename_keys(key)
                continue

            if key in (27, ord("q")):
                break
            elif key == ord("u"):
                self.toggle_tracking()
            elif key == ord("r"):
                self.toggle_rotation()
            elif key == ord("b"):
                self.start_basename_input()
            elif key == 32:
                self.capture(rotated)

        self.cap.release()
        cv2.destroyAllWindows()

    # -----------------------
    # DETECTION
    # -----------------------
    def _detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, self.canny_low, self.canny_high)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_bbox = None
        best_area = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < self.min_contour_area:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            if area > best_area:
                best_area = area
                best_bbox = (x, y, w, h)

        return best_bbox

    def _update_confidence(self, best_bbox):
        if self.locked:
            return

        if best_bbox is not None:
            self.confidence = min(1.0, self.confidence + 0.05)
        else:
            self.confidence = max(0.0, self.confidence - self.confidence_decay)

        if self.confidence >= self.confidence_threshold:
            self.locked = True
            self.locked_bbox = best_bbox
            print("🔒 Detection locked")

    def _draw_overlay(self, frame, best_bbox):
        if self.locked and self.locked_bbox is not None:
            x, y, w, h = self.locked_bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            status = "LOCKED"
            color = (0, 0, 255)
        elif best_bbox is not None:
            x, y, w, h = best_bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            status = "TRACKING"
            color = (0, 255, 0)
        else:
            status = "SEARCHING"
            color = (120, 120, 120)

        cv2.putText(frame, status, (20, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.putText(frame, f"Confidence: {self.confidence:.2f}",
                    (20, frame.shape[0] - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
