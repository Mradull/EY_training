import {Routes , Route} from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Payment from "./pages/Payment";
import Success from "./pages/Success";
import NotFound from "./pages/NotFOund";

export default function App(){
    return(
        <Routes>
          <Route path="/" element = {<Home/>}/>
          <Route path="login" element={<Login />} />
          <Route
            path="payment"
            element={
              <ProtectedRoute>
                <Payment />
              </ProtectedRoute>
            }
          />
          <Route path="success" element={<Success />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
    );
}