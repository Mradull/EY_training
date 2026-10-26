import { useState } from "react";
import {useNavigate} from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Login.css";

function Login(){
    const [email , setEmail] = useState("");
    const [password,setPassword] = useState("");

    const {login} = useAuth();
    const navigate = useNavigate();

    function handleSubmit(e) {
        e.preventDefault();
        const result = login(email,password);
        console.log(result);
        if(result){
            console.log("Navigating to payment...");
            navigate("/payment");
        }
        else{
            alert("Invalid Credentials");
        }
    }

    return (
  <div className="login-container">
    <div className="login-card">
      <h2>Login</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  </div>
);
}

export default Login;