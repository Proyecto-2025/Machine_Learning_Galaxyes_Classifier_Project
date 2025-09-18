import "./style/Predict.css";
import ImageUploader from "./ImageUploader";
import Header from "./Header";
import ErrorMessage from "./ErrorMessage";
import {useState,useEffect} from "react"

export default function Predict() {
    const mockImages = [
        { url: "https://placehold.co/200x200/000000/FFFFFF?text=Galaxy+1", name: "Galaxy 1" },
        { url: "https://placehold.co/200x200/222222/FFFFFF?text=Galaxy+2", name: "Galaxy 2" },
        { url: "https://placehold.co/200x200/444444/FFFFFF?text=Galaxy+3", name: "Galaxy 3" },
        { url: "https://placehold.co/200x200/666666/FFFFFF?text=Galaxy+4", name: "Galaxy 4" },
    ];

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

