import { useEffect, useState } from "react"
import "./style/Play.css"

export default function Play(){
    const [options, setOptions] = useState([
        { label: "Spiral", selected: false },
        { label: "Elliptical", selected: false },
        { label: "Lenticular", selected: false },
    ]);

    const handleClick = (id) => {
        setOptions(prev =>
            prev.map((btn,idx) =>
                id === idx ? { ...btn, selected: !btn.selected } : btn
            )
        );
    };

    return (
        <div className="play">
            <div className="blur-background">
                <h2>
                    Play guessing between Elliptical, <br/>
                    Spiral or Lenticular Galaxies
                </h2>
                <h4>Image from backend</h4>
                <img src="http://127.0.0.1:5000/randomImage" />
                <OptionSelector list={options} onClick={handleClick} />
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
