import { useEffect, useState } from "react"
import "./style/Play.css"

export default function Play(){
    return (
        <div className="play">
            <div className="blur-background">
                <h2>
                    Play guessing between Elliptical, <br/>
                    Spiral or Lenticular Galaxies
                </h2>
                <h4>Image from backend</h4>
                <img src="http://127.0.0.1:5000/randomImage" />
            </div>
        </div>
    )
}

function CaracteristicSelector() {
    return (
        <div>
            <ul>
            </ul>
        </div>
    )
}
