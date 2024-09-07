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
        console.log("address",address);
        if(element.indexingValue === address ){
            count++;
        }
        if(element.indexingValue === ip){
            count1++;
        }
        });
        console.log("count ",count," count1 ",count1);
        if(count>=30 || count1>=30){
        return true
        }
        return false
    }
    const connect = async () => {
   
        setIsLoading(true)
        if (typeof window.ethereum !== "undefined") {
            const { ethereum } = window;
            try {
                await ethereum.request({ method: "eth_requestAccounts" })
            } catch (error) {
                console.log(error)
            }

            const accounts = await ethereum.request({ method: "eth_accounts" })
            console.log("aa", accounts)
            const chain = await window.ethereum.request({ method: "eth_chainId" });
            let chainId = chain;
            console.log("chain ID:", chain);
            console.log("global Chain Id:", chainId);
            if (accounts.length !== 0) {
                const output = await checkIfUserIsBanned(accounts[0]);
                console.log("output",output);
                if(output){
                    alert("user is banned");
                    return;
                }
                setAccount(accounts[0]);
                console.log("Found an authorized account:", accounts);
                try{
                    if (ethereum) {
                        const provider = new ethers.providers.Web3Provider(ethereum);
                        const signer = provider.getSigner();
                        const contract = new ethers.Contract(tokenContract, tokenABI, signer);
                        try{
                            const result =await contract.fundUser();
                            console.log("result:::", result);
                        }
                        catch(e){
                            console.log(e);
                        }
                       
                    }

                }
                catch (error) {
                    if (error?.data?.message.includes("revert")) {
                        console.error("Transaction reverted: User already funded.");
                        setError("You have already been funded. No need for further funding.");
                    } else {
                        console.error("Error occurred during funding:", error);
                        setError("An unexpected error occurred. Please try again later.");
                    }
                }
                

            } else {
                console.log("No authorized account found");
            }
        } else {
            alert("Please install MetaMask");
        }
        setIsLoading(false)
    }
    
    const tokenContract = "0x7055954033A08De3b8Db8242F0d6383B21e31963"

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
            // const output = await checkIfUserIsBanned(accounts[0]);
            // console.log("output",output);
            // if(output){
            //     alert("user is banned");
            //     return;
            // }
            setAccount(accounts[0]);
            console.log("Found an authorized account:", accounts);
            const { ethereum } = window;
            if (ethereum) {
                const provider = new ethers.providers.Web3Provider(ethereum);
                const signer = provider.getSigner();
                const contract = new ethers.Contract(tokenContract, tokenABI, signer);
                try{
                    contract.fundUser();
                }
                catch(e){
                    console.error("user already funded", e)
                }
            }

        } else {
            console.log("No authorized account found");
        }
    }



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