import "./style/Footer.css"
export default function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p>© {new Date().getFullYear()} IA Chads Team — All rights reserved.</p>
            </div>
        </footer>
    );
}
