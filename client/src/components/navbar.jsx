import React from "react";
import { useStateContext } from "../context/index";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
    const navigate = useNavigate();
    const { account, connect } = useStateContext();

    return (
        <div>

            <div>
                <button
                    type='button'
                    // onClick={connect}
                >
                    {/* Connect Wallet  */}
                    {/* {account === "" ? "Connect Wallet" : <h3>{account}</h3>} */}
                </button>
            </div>
        </div>
    )
}

export default Navbar
