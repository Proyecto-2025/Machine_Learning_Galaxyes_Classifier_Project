import "./style/Predict.css";
import ImageUploader from "./ImageUploader";
import PredictResults from "./PredictResults";
import ErrorMessage from "./ErrorMessage";
import { useNavigate, Route , Routes } from "react-router-dom";

export default function Predict() {
    const navigate = useNavigate();
    const handleSuccess = (data) =>{
        navigate("results", {state:{data}});
    }
    const handleError = (msg) => {
        navigate("error",{state:{msg}});
    }
    return (
        <div className="predict-container">
      <Routes>
            <Route
            index
            element={<ImageUploader onSuccess={handleSuccess} onError={handleError} />}
            />
            <Route path="results" element={<PredictResults />} />
            <Route path="error" element={<ErrorMessage />} />
        </Routes>
        </div>
  );
}

