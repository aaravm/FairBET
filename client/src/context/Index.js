import React, { useContext, createContext, useEffect, useState } from 'react';


const StateContext = createContext();

export const StateContextProvider = ({ children }) => {
    const [account, setAccount] = useState('')
    const [pyodide, setPyodide] = useState(null);
    const [output, setOutput] = useState('');
    const [error, setError] = useState('');

    const runPythonFile = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/run-python', {
                method: 'POST'
            });
            console.log("jindagi acchi");
            if (!response.ok) {
                throw new Error('Failed to fetch Python results. Ensure the backend is running.');
            }
            else{
                console.log("python fetch is successful");
            }
    
            const result = await response.json();
            if (result.error) {
                throw new Error(result.error);
            }
    
            setOutput(result.output);
            console.log("Python script output:", result.output);
        } catch (err) {
            console.error('Error running Python code:', err);
            setError('Failed to run Python code. Check the console for more details.');
        }
    };

    const connect = async () => {
        await runPythonFile();
        if(!output)
        alert("Fuck off from this website");
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
        } else {
            alert("Please install MetaMask");
        }
    }
    
    
    useEffect(() => {
        // Function to dynamically load the Pyodide script
        const loadPyodideScript = async () => {
          // Check if Pyodide is already loaded
          if (window.loadPyodide) {
            const pyodideInstance = await window.loadPyodide();
            setPyodide(pyodideInstance);
          } else {
            // Create a new script element
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.0/full/pyodide.js';
            script.async = true;
            script.onload = async () => {
              // After the script is loaded, initialize Pyodide
              const pyodideInstance = await window.loadPyodide();
              setPyodide(pyodideInstance);
            };
            script.onerror = () => {
              console.error('Failed to load Pyodide script');
            };
            console.log("pyodide is loaded");
            document.body.appendChild(script);
          }
        };
    
        loadPyodideScript();
      }, []);
  
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

    useEffect(() => {
        Address();
        console.log(account);
    }, [])


    return (
        <StateContext.Provider
            value={{
                account,
                connect
            }}
        >
            {children}
        </StateContext.Provider>
    )
}


export const useStateContext = () => useContext(StateContext);