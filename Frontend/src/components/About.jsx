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
                                <thead>
                                    <tr>
                                        <th>Task</th>
                                        <th>Question</th>
                                        <th>Response</th>
                                        <th>Next</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>
                                            01
                                        </td>
                                        <td>
                                        Is the galaxy simply smooth
                                        and rounded, with no sign of
                                        a disk?
                                        </td>
                                        <td>
                                            smooth <br /> 
                                            featrure or disk <br /> 
                                            star or artifact
                                        </td>
                                        <td>
                                            07 <br />
                                            02 <br />
                                            end
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>02</td>
                                        <td>Could this be a disk viewed
                                    edge-on?</td>
                                        <td>yes<br/>no</td>
                                        <td>09 <br />03
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>03</td>
                                        <td>Is there a sign of a bar
                                    feature through the centre
                                    of the galaxy?</td>
                                        <td>yes <br />no</td>
                                        <td>04 <br />04</td>
                                    </tr>
                                    <tr>
                                        <td>04</td>
                                        <td>Is there any sign of a
                                    spiral arm pattern?</td>
                                        <td>yes <br />no</td>
                                        <td>10 <br />5</td>
                                        
                                    </tr>
                                    <tr>
                                        <td>05</td>
                                        <td>How prominent is the
                                    central bulge, compared
                                    with the rest of the galaxy?</td>
                                        <td>no bulge <br /> just noticeable <br />obvious <br />dominant</td>
                                        <td>06 <br />06 <br /> 06 <br /> 06 <br /> </td>
                                    </tr>
                                    <tr>
                                        <td>06</td>
                                        <td>Is there anything odd?</td>
                                        <td>yes<br />no</td>
                                        <td>08<br />end</td>
                                    </tr>
                                    <tr>
                                        <td>07</td>
                                        <td>How rounded is it?</td>
                                        <td>completly rounded <br />in between <br /> cigar-shaped</td>
                                        <td>06 <br />06 <br />06</td>
                                    </tr>
                                    <tr>
                                        <td>08</td>
                                        <td>Is the odd feature a ring,
                                    or is the galaxy disturbed
                                    or irregular?</td>
                                        <td>ring <br /> lens or arc <br /> disturbed <br /> irregular <br />other <br /> merger <br />dust lane</td>
                                        <td>end <br />end <br />end <br />end <br />end <br />end <br />end <br /></td>
                                    </tr>
                                    <tr>
                                        <td>09</td>
                                        <td>Does the galaxy have a
                                    bulge at its centre? If
                                    so, what shape?</td>
                                        <td>rounded <br /> boxy <br />no bulge</td>
                                        <td>06 <br />06 <br />06</td>
                                    </tr>
                                    <tr>
                                        <td>10</td>
                                        <td>How tightly wound do the
                                    spiral arms appear?</td>
                                        <td>tigtht <br /> medium <br /> loose</td>
                                        <td>11 <br />11 <br /> 11</td>
                                    </tr>
                                    <tr>
                                        <td>11</td>
                                        <td>How many spiral arms
                                        are there?</td>
                                        <td>1<br />2<br />3<br />4<br />more than four<br />can't tell</td>
                                        <td>05<br />05<br />05<br />05<br />05<br />05</td>
                                    </tr>
                                </tbody>
                            </table> 
                        </div>
                        <div className="description2">
                                <p>Continuacion de descripcion</p>
                        </div>
                    </div>
                </div>
            
            <div style={{ marginTop: "2rem" }}>
                <LinkToGalaxyZoo />
            </div>
        </div>
    )
}
