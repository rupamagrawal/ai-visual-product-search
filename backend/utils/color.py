import cv2
import numpy as np


def _map_hsv_to_color_name(hsv_pixel: np.ndarray) -> str:
    h, s, v = hsv_pixel

    if v < 40:
        return "black"
    if s < 25 and v > 200:
        return "white"
    if s < 35:
        return "gray"

    if h < 10 or h >= 170:
        return "red"
    if h < 25:
        return "orange"
    if h < 35:
        return "yellow"
    if h < 85:
        return "green"
    if h < 100:
        return "cyan"
    if h < 130:
        return "blue"
    if h < 160:
        return "purple"
    return "pink"


def _upper_body_crop(image: np.ndarray) -> np.ndarray:
    h, w = image.shape[:2]
    y1 = int(h * 0.12)
    y2 = int(h * 0.72)
    x1 = int(w * 0.15)
    x2 = int(w * 0.85)
    crop = image[y1:y2, x1:x2]
    return crop if crop.size else image


def _run_kmeans(crop: np.ndarray, k: int = 4):
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # Keep informative pixels; reduce plain background impact.
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    useful_mask = (saturation > 40) | (value < 200)

    pixels = crop[useful_mask].reshape((-1, 3)).astype(np.float32)
    if pixels.shape[0] < 200:
        pixels = crop.reshape((-1, 3)).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.2)
    k = 3
    _, labels, centers = cv2.kmeans(
        pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    return labels, centers


def _detect_vertical_stripes(crop: np.ndarray) -> bool:
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Strong vertical transitions indicate stripe-like texture.
    sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    edge_strength = np.abs(sobel_x)
    
    # Folded clothes have shadows (weak edges). Actual stripes have high contrast.
    # We increase the strength required dramatically to ignore wrinkles/shadows.
    strong_edges = edge_strength > 100
    edge_ratio = float(np.count_nonzero(strong_edges)) / float(strong_edges.size)

    return edge_ratio > 0.12


def detect_color_details(image_path: str) -> dict:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read uploaded image")

    crop = _upper_body_crop(image)
    crop = cv2.resize(crop, (180, 180), interpolation=cv2.INTER_AREA)
    labels, centers = _run_kmeans(crop, k=4)
    label_counts = np.bincount(labels.flatten())
    sorted_indices = np.argsort(label_counts)[::-1]

    dominant_bgr = centers[sorted_indices[0]].astype(np.uint8)
    secondary_bgr = centers[sorted_indices[1]].astype(np.uint8)

    dominant_hsv = cv2.cvtColor(np.uint8([[dominant_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    secondary_hsv = cv2.cvtColor(np.uint8([[secondary_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

    dominant_color = _map_hsv_to_color_name(dominant_hsv)
    secondary_color = _map_hsv_to_color_name(secondary_hsv)

    has_stripes = _detect_vertical_stripes(crop)

    return {
        "dominant_color": dominant_color,
        "secondary_color": secondary_color,
        "has_stripes": has_stripes,
    }


def detect_dominant_color(image_path: str) -> str:
    details = detect_color_details(image_path)
    return details["dominant_color"]
