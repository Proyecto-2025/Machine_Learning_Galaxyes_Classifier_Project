from app.models.image_model import ImageModel
import json

def test_store_and_search_image(db_service, app):
    #Store image
    with app.app_context():
        new_image = db_service.save_prediction(filename = "test.jpg", features = ["SUAVE", "VISTA DE PERFIL"])
        
        #Verify image storage on db
        img = db_service.search_image_by_id(new_image.id)
        assert img is not None
        assert img.filename == "test.jpg"
        assert json.loads(img.features) == ["SUAVE", "VISTA DE PERFIL"]

def test_search_by_features(db_service, app):
    with app.app_context():
        db_service.save_prediction(filename = "picture1.jpg", features = ["SUAVE", "VISTA DE PERFIL"])
        db_service.save_prediction(filename = "picture2.jpg", features = ["ESTRELLA O ARTEFACTO"])
        db_service.save_prediction(filename = "picture3.jpg", features = ["SUAVE", "VISTA DE PERFIL"])
        
        features1 = db_service.search_image_by_features(["SUAVE", "VISTA DE PERFIL"])
        assert len(features1) == 2
        for img in features1:
            assert json.loads(img.features) == ["SUAVE", "VISTA DE PERFIL"]
            
def test_free_image_searching(db_service, app):
    with app.app_context():
        db_service.save_prediction(filename = "picture1.jpg", features = ["SUAVE", "VISTA DE PERFIL"])
        db_service.save_prediction(filename = "picture2.jpg", features = ["ESTRELLA O ARTEFACTO"])
        
        image_list = db_service.free_image_searching(image_url= "picture1")
        assert len(image_list) == 1
        assert image_list[0].filename == "picture1.jpg"
        assert json.loads(image_list[0].features) == ["SUAVE", "VISTA DE PERFIL"] 
        