import React from "react";
import { useStateContext } from "../context/Index";
import { useNavigate } from "react-router-dom";

export const Navbar = () => {
    const navigate = useNavigate();
    const { account, connect } = useStateContext();

    return (
        <div className="flex md:flex-row flex-col-reverse justify-between mb-[35px] px-5 gap-10 bg-[#1c1c24] rounded-[20px]">

            <div className="sm:flex hidden flex-row justify-end gap-4">
                <button
                    type='button'
                    className={"font-epilogue font-bold text-[16px] leading-[26px] text-white min-h-[52px] px-4 rounded-[10px] hover:text-[#1dc071] "}
                    onClick={connect}
                >
                    {/* Connect Wallet  */}
                    {account === "" ? "Connect Wallet" : <h3>{account}</h3>}
                </button>
            </div>
        </div>
    )
}

