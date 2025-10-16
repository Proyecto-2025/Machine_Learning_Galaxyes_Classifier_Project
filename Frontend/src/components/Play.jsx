import { useEffect, useState } from "react"
import "./style/Play.css"

export default function Play(){
    const caracteristics = [
        {label: "Elliptical", marked: true},
        {label: "Lenticular", marked: false},
        {label: "Spiral", marked: false},
    ]

    return (
        <div className="play">
            <div className="blur-background">
                <h2>
                    Play guessing between Elliptical, <br/>
                    Spiral or Lenticular Galaxies
                </h2>
                <h4>Image from backend</h4>
                <img src="http://127.0.0.1:5000/randomImage" />
                <CaracteristicSelector list={caracteristics} />
            </div>
        </div>
    )
}

function CaracteristicSelector({ list }) {
    return (
        <div>
            {list.map((item,idx) => (
                <button className="btn"> {item.label} </button>
            ))}
        </div>
    )
}
