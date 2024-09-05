import React from "react";
import { useStateContext } from "../context/index";

const Connect = () => {
    // const navigate = useNavigate();
    const { account, connect } = useStateContext();

    return (
        <div>

            <div>
                <button
                    className="connect"
                    type='button'
                    onClick={connect}
                >
                    {/* Connect Wallet  */}
                    {account === "" ? "Connect Wallet" : <h3>{account}</h3>}
                </button>
            </div>
        </div>
    )
}

export default Connect
