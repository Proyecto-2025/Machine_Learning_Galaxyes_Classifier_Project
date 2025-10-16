import "./style/Predict.css";
import ImageUploader from "./ImageUploader";
import Header from "./Header";
import ErrorMessage from "./ErrorMessage";
import {useState,useEffect} from "react"

export default function Predict() {
    
    return (
        <div className="predict">
            <div className="blur-background">
                <h1>Galaxy Classifier</h1>
                <p>Subí imágenes de galaxias para su posterior análisis.</p>
                <ImageUploader />
            </div>
        </div>
    );
}

