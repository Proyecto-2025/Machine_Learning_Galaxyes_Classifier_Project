import { Link } from 'react-router-dom'
import Header from "./Header.jsx"
import "./style/Home.css"

export default function Home() {
    const play = { 
        name: "Play",
        desc: "Play against our ML model.",
        to: "/play"
    }
    const predict = { 
        name: "Predict",
        desc: "Give a galaxy image to our ML model to see its morphology.",
        to: "/predict"
    }

    return (
        <div className="home">
            <h1> ChadIA- Galaxy Classifier </h1>
            <div className="home-applications">
                <ApplicationButton name={play.name} desc={play.desc} to={play.to}/>
                <ApplicationButton name={predict.name} desc={predict.desc} to={predict.to}/>
            </div>
        </div>
    )
}

function ApplicationButton({ name, desc, to }) {
    return (
        <Link to={to} className="blur-background">
            <h3> {name} </h3>
            <p> {desc} </p>
        </Link>
    )
}
