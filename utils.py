import subprocess
import re


def find_czur_camera(max_index=10):
    """
    Try to auto-detect CZUR camera by device name.
    Returns camera index or None.
    """

    try:
        result = subprocess.run(
            ["system_profiler", "SPCameraDataType"],
            capture_output=True,
            text=True,
        )
        output = result.stdout.lower()
        print("Camera info:\n", output)
        czur_keywords = ["czur", "shine", "aura", "et"]

        # Split by camera blocks
        blocks = re.split(r"\n\s*\n", output)

        czur_found = False
        for block in blocks:
            if any(k in block for k in czur_keywords):
                czur_found = True
                break

        if not czur_found:
            return None

    except Exception:
        return None

    # If CZUR is present, probe indices
    import cv2

    for idx in range(max_index):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print(f"Detected camera at index {idx}")
                return idx

    return None

# find_czur_camera()