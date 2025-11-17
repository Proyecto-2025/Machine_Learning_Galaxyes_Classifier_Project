import io
from unittest.mock import patch
from app import create_app
from PIL import Image

def test_predict_no_image():
    app = create_app()
    client = app.test_client()

    resp = client.post("/predict")
    assert resp.status_code == 400

def create_fake_png():
    img = Image.new("RGB", (1, 1), color="white")
    buf = io.BytesIO()
    buf.seek(0)
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def test_predict_ok():
    app = create_app()
    client = app.test_client()

    fake_img = (create_fake_png(), "test.png")

    with patch("model.PredictGalaxy.makePrediction") as mock_pred:
        mock_pred.return_value = [0.1, 0.8, 0.1]

        resp = client.post(
            "/predict",
            data={"image": fake_img},
            content_type="multipart/form-data"
        )

    assert resp.status_code == 200
    data = resp.get_json()
    assert "prediction" in data

def test_predict_model_error():
    app = create_app()
    client = app.test_client()

    fake_img = (io.BytesIO(b"fake"), "img.png")

    with patch("model.PredictGalaxy.makePrediction") as mock_pred:
        mock_pred.side_effect = Exception("boom")

        resp = client.post(
            "/predict",
            data={"image": fake_img},
            content_type="multipart/form-data"
        )

    assert resp.status_code == 500
