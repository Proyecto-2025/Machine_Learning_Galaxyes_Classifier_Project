import { useEffect, useState } from "react"
import "./style/Play.css"

export default function Play(){
    const [image,setImage] = useState(null);
    const [caracteris,setCaracteristics] = useState("");
    const [guess,setGuess] = useState(null);
    
    const [options, setOptions] = useState([
        { label: "Spiral", selected: false },
        { label: "Elliptical", selected: false },
        { label: "Lenticular", selected: false },
    ]);

    useEffect(() => {
        async function fetchImageData() {
            try {
                const res = await fetch("https://galaxies-backend.onrender.com/api/v1/play");
                const json = await res.json();
                setImage(json.url);
                setCaracteristics(json.hubblesequence);
            } catch (error) {
                console.error("Error fetching image:", error);
            }
        }
        fetchImageData();
    }, []);

    const handleClick = (id) => {
        setOptions(prev =>
            prev.map((btn,idx) => (
                id === idx 
                    ? {...btn,selected:true}
                    : {...btn,selected:false}
            ))
        );
    };

    const handleGuess = () => {
        const selected = options.find(opt => opt.selected == true)?.label;
        if (!selected) {
            alert("Please select a options first");
            return
        }

        if (selected[0] == caracteris[0]) {
            setGuess(true);
        } else {
            setGuess(false);
        }
    };

    return (
        <div className="play">
            <div className="blur-background">
                <h2> Guess the type of Galaxy </h2>
                <img src={image} />
                <OptionSelector list={options} onClick={handleClick} />

                <button className="btn" onClick={handleGuess}>Guess</button>

                {guess !== null && (
                    <p className="result">
                        {guess ? "✅ Correct!" : "❌ Wrong!"}
                    </p>
                )}
            </div>
        </div>
    )
}

function OptionSelector({ list, onClick}) {
    return (
        <div className="option-selector">
            {list.map((item,idx) => (
                <button className={`btn ${item.selected ? "btn-selected" : ""}`} onClick={ () => onClick(idx)}> 
                    {item.label} 
                </button>
            ))}
        </div>
    )
}
