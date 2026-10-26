import "./Home.css";
import {useNavigate} from "react-router-dom";
import { useState } from "react";
import {useAuth} from "../context/AuthContext";

function Home(){
    const navigate = useNavigate();
    const [cart , setCart] = useState([]);
    const { logout } = useAuth();

    const products = [
        {id:1 , name : "Laptop" , price:50000},
        {id:2 , name : "Headphones" , price:5000},
        {id:3 , name : "Keyboard" , price:10000},
        {id:4 , name : "Mouse" , price:2000},
    ];

    function addToCart(product){
        setCart([...cart , product]);
    }
    return (
        <div className="home">
            <header className="navbar">
                <h2>Amazon Mini Store</h2>
                <div className="nav-buttons">
                    <button
                    className="cart-btn"
                    onClick={() => navigate("/payment")}>
                    🛒 Cart ({cart.length})
                </button>
                <button
                    className="logout-btn"
                    onClick={() => {
                        logout();
                        navigate("/login");
                    }}>
                Logout
                </button>

                </div>
                
            </header>

            <section className="hero">
                <h1>Welcome to Mini Store</h1>
                <p>Best Deals on Electronics</p>
                <input
                type="text"
                placeholder="Search Products"
                className="search"
                />
            </section>

            <section className="products">
                {products.map((product)=>(
                    <div className="card" key={product.id}>
                        <div className="image_placeholder">
                            📦
                        </div>
                        <h3>{product.name}</h3>
                        <p className="price">${product.price}</p>
                        <button className="add-btn" onClick={() => addToCart(product)}>
                            Add to Cart
                        </button>
                    </div>
                ))}
            </section>
        </div>
    );
}
export default Home;
