import React, { useEffect } from "react";
import { useStateContext } from "../context/index";
import { ClipLoader } from 'react-spinners';

const Connect = () => {
    // const navigate = useNavigate();
    const { account, connect, isLoading } = useStateContext();


    return (
        <div>
            {isLoading ?
                    < ClipLoader color="#3498db" size={50} />
                    :
                <button
                    className="connect"
                    type='button'
                    onClick={connect}
                >

                    {/* Connect Wallet  */}
                    {account === "" ? "Connect Wallet" : <h3>{account}</h3>}
                </button>
            }
        </div>
    )
}

export default Connect
