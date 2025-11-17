import { Routes,Route, Router } from 'react-router-dom'
import Header from "./Header";
import Predict from './Predict.jsx'
import About from './About.jsx'
import Home from './Home.jsx'
import Learn from './Learn.jsx'
import Play from './Play.jsx'
import SignIn from "./SignIn.jsx";
import SignUp from "./SignUp.jsx";
import Footer from "./Footer.jsx"
export default function AppRoutes() {
    return (
        <>
            <Header />
            <div className='routes-container'>
                <Routes>    
                    <Route path="/" element={<Home />} />
                    <Route path="/predict/*" element={<Predict />} />
                    <Route path="/about" element={<About />} />
                    <Route path="/learn" element={<Learn />} />
                    <Route path="/play" element={<Play />} />
                    <Route path="/signin" element={<SignIn />} />
                    <Route path="/signup" element={<SignUp />} />
                </Routes>
            </div>
            <Footer/>

        </>
    );
}
