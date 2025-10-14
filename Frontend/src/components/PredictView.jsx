import ImageUploader from "./ImageUploader";
import ErrorMessage from "./ErrorMessage";
import PredictResults from "./PredictResults";
import { useState } from "react";

export default function PredictView(){
    const [error, setError]= useState(null);
    const [results,setResults]= useState(null);

    if(error){
        return <ErrorMessage message={"Error al cargar la imagen"} onRetry={()=>setError(null)}/>
    }
    
    if(results){
        return (
            <PredictResults 
            data={results}
            onBack={()=>setResults(null)}
            onRetry={()=>{
                    setResults(null);
                    window.location.href ="/predict";
                }
            }/>
        )
    }
    return (
        <ImageUploader
            onSuccess={(data)=>setResults(data)}
            onError={(msg)=>setError(msg)}
        />
    );
}