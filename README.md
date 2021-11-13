# YOLO v5 RESTful API server

This repo is forked form https://github.com/ultralytics/yolov5.
It's nothing but a RESTful API server that is dockerized.

## [app.py](app.py)

This is the flask api server. It returns the following values:

```pyhon
results = [
    {
        "bbox": [int(r) for r in result[:4]],
        "det_score": result[4],
        "label_num": int(result[5]),
        "label_string": names[int(result[-1])],
    }
    for result in results
]
```

## docker

Checkout the [Dockerfile](Dockerfile).

You don't have to build the docker image. You can just pull it from [the docker hub](https://hub.docker.com/repository/docker/tae898/yolov5).

This repo contains the weight file `yolov5s.pt` so that docker does not need an Internet access to download the weights.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
4. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the Branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## Authors

* [Taewoon Kim](https://taewoonkim.com/) 