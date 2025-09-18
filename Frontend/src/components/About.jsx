import Header from "./Header.jsx"
import LinkToGalaxyZoo from "./LinkToGalaxyZoo.jsx"
import "./style/About.css"
export default function About() {
    return (
        <div className="about">
            
            <h1> Hello About, with docker smooth tooned </h1>
            <h1> ChadIA- Galaxy Classifier </h1>
            <div style={{ marginTop: "2rem" }}>
                <LinkToGalaxyZoo />
            </div>
        </div>
    )
}
