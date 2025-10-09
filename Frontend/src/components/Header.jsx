import React from "react"
import { Link } from "react-router-dom"
import "./style/Header.css"

export default function Header() {
    const buttons = [
        {label: "Home", url: "/"},
        {label: "Predict", url: "/predict"},
        {label: "Play", url: "/play"},
        {label: "Learn", url: "/learn"},
        {label: "About", url: "/about"},
    ]

    return (
        <header className="header">
            { buttons.map((button,idx) => (
                <HeaderButton key={idx} label={button.label} url={button.url} />
            ))}
        </header>
    )
}

function HeaderButton({ label, url }) {
    return (
        <Link className="header-btn" to={url}>
            {label}
        </Link>
    )
}
