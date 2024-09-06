import React, { useContext, createContext, useEffect, useState } from 'react';
import axios from "axios"
import { IndexService } from "@ethsign/sp-sdk";

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
        setIsLoading(true)
        let output=0;
        output=await checkIfUserIsBanned(account)
        
        
        console.log("output:", output)
        if(output)
        alert("You are banned");
        else
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
            await Address();
        } else {
            alert("Please install MetaMask");
        }

        setIsLoading(false)
    }
    
    
  
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

        } else {
            console.log("No authorized account found");
        }
    }

    // useEffect(() => {
    //     Address();
    //     console.log(account);
    // }, [])



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