import cv2
import numpy as np
import os
from openvino.inference_engine import IECore
from scipy.spatial.distance import cosine

# === Percorsi modelli ===
det_model_xml = r"C:\Users\fabio\Documents\Lilly\face-detection-retail-0004\FP16\face-detection-retail-0004.xml"
reid_model_xml = r"C:\Users\fabio\Documents\Lilly\face-reidentification-retail-0095\FP16\face-reidentification-retail-0095.xml"

# === Immagini ===
input_image_path = "input.jpg"
reference_faces_folder = "reference_faces"
saved_embeddings_path = "ref_embeddings.npy"

# === Config ===
device = "MYRIAD"
similarity_threshold = 0.6

# === Inizializza OpenVINO ===
ie = IECore()

# Carica modelli
det_net = ie.read_network(model=det_model_xml, weights=det_model_xml.replace(".xml", ".bin"))
det_exec = ie.load_network(network=det_net, device_name=device)
det_input_blob = next(iter(det_net.inputs))
det_output_blob = next(iter(det_net.outputs))

reid_net = ie.read_network(model=reid_model_xml, weights=reid_model_xml.replace(".xml", ".bin"))
reid_exec = ie.load_network(network=reid_net, device_name=device)
reid_input_blob = next(iter(reid_net.inputs))
reid_output_blob = next(iter(reid_net.outputs))

def preprocess_for_detection(image):
    n, c, h, w = det_net.inputs[det_input_blob].shape
    resized = cv2.resize(image, (w, h))
    transposed = resized.transpose((2, 0, 1))  # HWC to CHW
    return transposed.reshape((n, c, h, w))

def preprocess_for_reid(face):
    resized = cv2.resize(face, (128, 128))
    transposed = resized.transpose((2, 0, 1))
    return transposed.reshape((1, 3, 128, 128))

def extract_faces(image, detections, conf_thresh=0.5):
    faces = []
    h, w = image.shape[:2]
    for det in detections[0][0]:
        conf = det[2]
        if conf > conf_thresh:
            xmin = int(det[3] * w)
            ymin = int(det[4] * h)
            xmax = int(det[5] * w)
            ymax = int(det[6] * h)
            face = image[ymin:ymax, xmin:xmax]
            if face.size != 0:
                faces.append((face, (xmin, ymin, xmax, ymax)))
    return faces

def get_embedding(face):
    blob = preprocess_for_reid(face)
    result = reid_exec.infer(inputs={reid_input_blob: blob})
    return result[reid_output_blob][0]

# === Carica o genera gli embedding di riferimento ===
if os.path.exists(saved_embeddings_path):
    ref_embeddings = np.load(saved_embeddings_path)
    print("✅ Embedding di riferimento caricati da file.")
else:
    print("⏳ Generazione embedding di riferimento...")
    ref_embeddings = []
    for filename in os.listdir(reference_faces_folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        path = os.path.join(reference_faces_folder, filename)
        ref_img = cv2.imread(path)
        if ref_img is None:
            continue
        blob = preprocess_for_detection(ref_img)
        detections = det_exec.infer(inputs={det_input_blob: blob})[det_output_blob]
        faces = extract_faces(ref_img, detections)
        if faces:
            embedding = get_embedding(faces[0][0])
            ref_embeddings.append(embedding)

    if not ref_embeddings:
        print("❌ Nessun volto trovato nelle immagini di riferimento.")
        exit()

    ref_embeddings = np.array(ref_embeddings)
    np.save(saved_embeddings_path, ref_embeddings)
    print(f"✅ Embedding salvati in {saved_embeddings_path}")

# Calcolo embedding medio
avg_embedding = np.mean(ref_embeddings, axis=0)

# === Analizza immagine input ===
img = cv2.imread(input_image_path)
blob = preprocess_for_detection(img)
detections = det_exec.infer(inputs={det_input_blob: blob})[det_output_blob]
faces = extract_faces(img, detections)

# === Confronta ===
found_match = False

for i, (face, box) in enumerate(faces):
    embedding = get_embedding(face)
    similarity = 1 - cosine(avg_embedding, embedding)
    xmin, ymin, xmax, ymax = box

    is_match = similarity > (1 - similarity_threshold)
    if is_match:
        found_match = True

    label = "MATCH" if is_match else "NO MATCH"
    color = (0, 255, 0) if is_match else (0, 0, 255)

    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)
    cv2.putText(img, f"{label} ({similarity:.2f})", (xmin, ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

cv2.imwrite("output.jpg", img)

if found_match:
    print(f"\n✔ MATCH trovato in {input_image_path}\n")
else:
    print(f"\n❌ NESSUN MATCH in {input_image_path}\n")
