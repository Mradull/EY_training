import { useNavigate } from "react-router-dom";
import "./Payment.css";

function Payment() {
  const navigate = useNavigate();

  // Temporary data
  const totalAmount = 67000;
  const totalItems = 4;

  function handlePayment() {
    navigate("/success");
  }

  return (
    <div className="payment-container">
      <div className="payment-card">
        <h1>Checkout</h1>

        <div className="order-summary">
          <h2>Order Summary</h2>

          <div className="row">
            <span>Total Items</span>
            <span>{totalItems}</span>
          </div>

          <div className="row">
            <span>Subtotal</span>
            <span>₹{totalAmount}</span>
          </div>

          <div className="row">
            <span>Delivery</span>
            <span>FREE</span>
          </div>

          <hr />

          <div className="row total">
            <span>Total</span>
            <span>₹{totalAmount}</span>
          </div>
        </div>

        <button
          className="payment-btn"
          onClick={handlePayment}
        >
          Proceed Payment
        </button>
      </div>
    </div>
  );
}

export default Payment;