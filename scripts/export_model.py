from ultralytics import YOLO

# 1. Download the base PyTorch model weights (yolov8n.pt) automatically
model = YOLO("yolov8n.pt")

# 2. Convert PyTorch model into Intel OpenVINO FP16 (half-precision) format
model.export(format="openvino", half=True)

print("--- OpenVINO Export Complete! ---")