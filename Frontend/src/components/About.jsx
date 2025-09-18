import Header from "./Header.jsx"
import LinkToGalaxyZoo from "./LinkToGalaxyZoo.jsx"
import "./style/About.css"
export default function About() {
    return (
        <div className="about">
                <div className="mldiv">
                    <h1>Machine Learning Model</h1>
                    <p> Una CNN (Convolutional Neural Network) es un modelo de machine learning especializado en procesar datos con estructura de grid, como imágenes.<br></br>Su idea principal es usar capas convolucionales que aplican filtros (o kernels) para extraer automáticamente características locales (bordes, texturas, formas), reduciendo la necesidad de diseñarlas manualmente. Luego, con capas de pooling, se resume la información más importante reduciendo la dimensionalidad. Finalmente, se usan capas totalmente conectadas (fully connected) para clasificar o predecir según las características aprendidas.</p>
                </div>
                <div className="howitwork">
                    <h1>How it works</h1>
                    <div id="descriptionQuestion">
                        <div className="description">
                            <p>Brief description of hot the model works on dataset</p>
                        </div>
                        <div className="questionsTable">
                            <table>
                                <tr>
                                    <th>
                                        <p>Task</p>
                                    </th>
                                </tr>
                                <tr>
                                    <th>
                                        <p>Question</p>
                                    </th>
                                </tr>
                                <tr>
                                    <th>
                                        <p>Response</p>
                                    </th>
                                </tr>
                                <tr>
                                    <th>
                                        <p>Next</p>
                                    </th>
                                </tr>
                            </table> 
                            <div>
                                <p>Continuacion de descripcion</p>
                            </div>
                        </div>
                    </div>
                </div>
            
            <div style={{ marginTop: "2rem" }}>
                <LinkToGalaxyZoo />
            </div>
        </div>
    )
}
