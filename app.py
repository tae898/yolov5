import logging
import argparse
from flask import Flask, request
import argparse
import jsonpickle
import io
from PIL import Image

import torch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

model = torch.hub._load_local("./", "yolov5s")

app = Flask(__name__)

names = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


@app.route("/", methods=["POST"])
def object_detection():
    """Receive everything in json!!!"""
    app.logger.debug(f"Receiving data ...")
    data = request.json
    data = jsonpickle.decode(data)

    app.logger.debug(f"decompressing image ...")
    image = data["image"]
    image = io.BytesIO(image)

    app.logger.debug(f"Reading a PIL image ...")
    image = Image.open(image)

    # Inference
    app.logger.debug(f"Running yolov5 ...")
    results = model(image)
    results = results.pred[0].cpu().detach().numpy().tolist()
    results = [
        {
            "bbox": [int(r) for r in result[:4]],
            "det_score": result[4],
            "label_num": int(result[5]),
            "label_string": names[int(result[-1])],
        }
        for result in results
    ]

    app.logger.info(f"Running yolov5 complete with the results:\n{results}")

    response = {"yolo_results": results}
    response_pickled = jsonpickle.encode(response)
    app.logger.info("json-pickle is done.")

    return response_pickled


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    app.run(host="0.0.0.0", port=10004)
