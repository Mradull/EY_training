import {Link} from "react-router-dom"

export default function Home(){
    return (
        <div className="container">
            <h1>Autenticagion demo</h1>
            <p>Learn how react protects private pages</p>
            <nav>
                <Link to="/login">Login</Link>
                {" | "}
                <Link to= "/dashboard">open dashboard</Link>
            </nav>
        </div>
    );
}