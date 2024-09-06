import React, { useContext, createContext, useEffect, useState } from 'react';
import axios from "axios"
import { IndexService } from "@ethsign/sp-sdk";
import tokenABI from "../ABI/tokenAbi.json"
import { ethers } from "ethers"

const StateContext = createContext();

export const StateContextProvider = ({ children }) => {
    const [account, setAccount] = useState('')
    // const [pyodide, setPyodide] = useState(null);

    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false)
    const [ip, setIp] = useState('');

    useEffect(() => {
      // Fetch the user's IP address
      const getData = async () => {
        const res = await axios.get("https://api.ipify.org/?format=json");
        console.log(res.data);
        setIp(res.data.ip);
      };
      getData();
    }, []);

    const checkIfUserIsBanned = async (address) => {
        const indexService = new IndexService("testnet");
        const res = await indexService.queryAttestationList({
        schemaId : "onchain_evm_84532_0x1cc",
        attester:"0xBA2570e298E8111caB760b6614D84879D6957414",
        mode: "onchain",
        page: 1,
        });
        let count=0;
        let count1=0;
        console.log(ip);
        res.rows.forEach((element) => {
        console.log("element",element.indexingValue);
        if(element.indexingValue === address ){
            count++;
        }
        if(element.indexingValue === ip){
            count1++;
        }
        });
        console.log("count ",count," count1 ",count1);
        if(count>=3 || count1>=3){
        return true
        }
        return false
    }
    const connect = async () => {
        if (typeof window.ethereum !== "undefined") {
            const { ethereum } = window;
            try {
                await ethereum.request({ method: "eth_requestAccounts" })
            } catch (error) {
                console.log(error)
            }

            const accounts = await ethereum.request({ method: "eth_accounts" })
            console.log(accounts)
            window.location.reload(false);
        } else {
            alert("Please install MetaMask");
        }
    }
    
    
    // useEffect(() => {
    //     // Function to dynamically load the Pyodide script
    //     const loadPyodideScript = async () => {
    //       // Check if Pyodide is already loaded
    //       if (window.loadPyodide) {
    //         const pyodideInstance = await window.loadPyodide();
    //         setPyodide(pyodideInstance);
    //       } else {
    //         // Create a new script element
    //         const script = document.createElement('script');
    //         script.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.0/full/pyodide.js';
    //         script.async = true;
    //         script.onload = async () => {
    //           // After the script is loaded, initialize Pyodide
    //           const pyodideInstance = await window.loadPyodide();
    //           setPyodide(pyodideInstance);
    //         };
    //         script.onerror = () => {
    //           console.error('Failed to load Pyodide script');
    //         };
    //         console.log("pyodide is loaded");
    //         document.body.appendChild(script);
    //       }
    //     };
    
    //     loadPyodideScript();
    //   }, []);
    const tokenContract = "0x32efFB7E5D75d31D0674c0D3091A415115AF8204"

    const Address = async () => {
        const { ethereum } = window;
        if (!ethereum) {
            console.log("Make sure you have metamask!");
            return;
        } else {
            console.log("We have the ethereum object", ethereum);
        }
        const accounts = await ethereum.request({ method: "eth_accounts" });
        const chain = await window.ethereum.request({ method: "eth_chainId" });
        let chainId = chain;
        console.log("chain ID:", chain);
        console.log("global Chain Id:", chainId);
        if (accounts.length !== 0) {
            setAccount(accounts[0]);
            console.log("Found an authorized account:", accounts);
            const { ethereum } = window;
            if (ethereum) {
                const provider = new ethers.providers.Web3Provider(ethereum);
                const signer = provider.getSigner();
                const contract = new ethers.Contract(tokenContract, tokenABI, signer);
                contract.fundUser();
            }

        } else {
            console.log("No authorized account found");
        }
    }

    useEffect(() => {
        Address();
        console.log(account);
    }, [])


    // useEffect(() => {
    //     console.log("output:", output);

    //     const handleEthereum = async () => {
    //         if(output==='') return;
    //         if (!output) {
    //             alert("Fuck off from this website");
    //         } else {
    //             if (typeof window.ethereum !== "undefined") {
    //                 const { ethereum } = window;
    //                 try {
    //                     await ethereum.request({ method: "eth_requestAccounts" });
    //                 } catch (error) {
    //                     console.log(error);
    //                 }

    //                 const accounts = await ethereum.request({ method: "eth_accounts" });
    //                 console.log(accounts);
    //                 window.location.reload(false);
    //             } else {
    //                 alert("Please install MetaMask");
    //             }
    //         }
    //     };

    //     handleEthereum(); // Call the async function
    // }, [output]);



    return (
        <StateContext.Provider
            value={{
                account,
                setAccount,
                isLoading,
                setIsLoading,
                connect,
                ip,
                setIp
            }}
        >
            {children}
        </StateContext.Provider>
    )
}


export const useStateContext = () => useContext(StateContext);