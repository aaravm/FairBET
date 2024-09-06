import React, { useEffect } from "react";
import { useStateContext } from "../context/index";
import { ClipLoader } from 'react-spinners';
import tokenABI from "../ABI/tokenAbi.json"
import {ethers} from "ethers"
const Connect = () => {
    // const navigate = useNavigate();
    const { account, connect, isLoading } = useStateContext();

    const tokenContract = "0x32efFB7E5D75d31D0674c0D3091A415115AF8204"

    useEffect( () =>{
        
        const handleFunding = (e) => {
            if(account === '') return;
            e.preventDefault()
            const { ethereum } = window;
            if (ethereum) {
                const provider = new ethers.providers.Web3Provider(ethereum);
                const signer = provider.getSigner();
                const contract = new ethers.Contract(tokenContract, tokenABI, signer);
                contract.fundUser();
            }
        }

        handleFunding();
    }, [account])

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
