import React, {useState, useEffect} from "react";
import cartt from "./../components/blackjack/Images"
import "./blackjack.css";
import Footer from "./../components/blackjack/Footer.jsx";
import Money from "./../components/blackjack/Money.jsx";
import Logo from "./../components/blackjack/Logo.jsx";
import ResultAlert from "./../components/blackjack/ResultAlert.jsx";
import BlockCarts from "./../components/blackjack/BlockCarts.jsx";
import Chat from '../components/Chat';
import Back from "../components/back.jsx";
import { ethers } from "ethers";
import tokenABI from "../ABI/tokenAbi.json"
import { useStateContext } from "../context/index.js";
import {
    SignProtocolClient,
    SpMode,
    EvmChains,
    IndexService,
    delegateSignAttestation,
    delegateSignRevokeAttestation,
    delegateSignSchema,
} from "@ethsign/sp-sdk";
import { privateKeyToAccount } from "viem/accounts";

const tokenContract = "0xFe7D1646B93cEb71347C823CaA04Ada19EC5DFA9";

function BlackJack() {
    const [result, setResult] = useState('')                // Результат исходя из хода игры
    const [botStop, setBotStop] = useState(false)           // Флаг бота, остановен он или нет
    const [pass, setPass] = useState(false)                 // Проверка на нажатие Pass
    const [continues, setContinue] = useState(false)        // Нажатие Кнокпи продолжить
    const [count_pl, setCount_pl] = useState(0)             // Количество  ходов игрока
    const [input, setInput] = useState(10)                  // Введеное число в инпуте
    const [money, setMoney] = useState(500)                 // Количество денег у игрока
    const [start, setStart] = useState(false)               // Нажата ли кнопка старт
    const [score, setScore] = useState(0);                  // Счет карт игрока
    const [score_bot, setScore_bot] = useState(0)           // Счет карт бота
    const [counter, setCounter] = useState(0);              // Номер карты в колоде увеличивается с каждым ходом
    const [deck, setDeck] = useState(cartt.slice(0,51));                         // Массив карт
    const {account, setAccount} = useStateContext();
    const {gameId, setGameId} = useStateContext();
    const privateKey = "0xdeb05e305a83f278a148ac5dd80106fd62828c087d439497c0e4170cf235a05a"; // Optional
    const client = new SignProtocolClient(SpMode.OnChain, {
        chain: EvmChains.baseSepolia,
        account: privateKeyToAccount(privateKey), // Optional if you are using an injected provider
      });
    async function createAttestationBlackJack(game_id,data){
        console.log("funciton called");
        try{

            const result=await client.createAttestation({
                schemaId: "0x249",
                data: { "Game_id":game_id,"User_address": account, "Current_State":data},
                indexingValue: account,
            })
            console.log(result);
        }catch(error){
            console.error(error);
        }
    };
    function random(n) {
        return Math.floor(Math.random() * Math.floor(n));
    }

    function shuffle(arr) {                               // Перемешивание карт
        for (let i = 0; i < arr.length; i++) {
            let j = random(arr.length);
            let k = random(arr.length);
            let t = arr[j];
            arr[j] = arr[k];
            arr[k] = t;
        }
        return arr;
    }

    const losing = () => {                                // Проигрыш
        setMoney((m) => {
            setResult('Lost')
            return m - input
        })
    }
    const victory = async () => {                               // Victory
        setMoney((m) => {
            setResult('Victory')
            return m + input*2
        })
        const tokenContract = "0xFe7D1646B93cEb71347C823CaA04Ada19EC5DFA9";
        const { ethereum } = window;
        if (ethereum) {
            const provider = new ethers.providers.Web3Provider(ethereum);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(tokenContract, tokenABI, signer);
            try {
                await contract.victorySend(2*input)
            }
            catch (error) {
                alert("Transaction failed, Pls check your balance")
                return
            }
        }
    }
    const Start = async (cart) => {                              // Запуск игры
        if(money<=0 || input>money){
            return;
        }
        const { ethereum } = window;
        if (ethereum) {
            const provider = new ethers.providers.Web3Provider(ethereum);
            const signer = provider.getSigner();
            const contract = new ethers.Contract(tokenContract, tokenABI, signer);
            try {
                await contract.transferTokens('0x56375D354043571d89bfcAeec1Ba0949007c529A', input)
            }
            catch (error) {
                alert("Transaction failed, Pls check your balance")
                return
            }
        }
        const newArr = shuffle(cart)                        // Перемешивание колоды
        setDeck(newArr)
        setStart(true)
        const prom = new Promise(((resolve, reject) => {       // Вызов в интервале ход игрока и ход бота
            let newCounter = counter;
            const timer = setTimeout(() => {
                player_step(newCounter)
                clearTimeout(timer)
                newCounter+=1
                resolve(newCounter)
            }, 300)
        }))
        prom.then((newCounter) => {
            const timer2 = setTimeout(() => {
                bot_step(newCounter)
                clearTimeout(timer2)
            }, 200)
        })
    }

    const player_step = (count) => {  // Player's move
        if (!pass) {
            if (score > 21) {
                losing();
                return;
            }
            if (score < 21) {
                const newDeck = [...deck];
                newDeck[count].st = 'player';
                setScore((s) => {  // Player's score
                    return s + newDeck[count].n;
                });
                setDeck(newDeck);
                setCounter((c) => {  // Total moves
                    return c + 1;
                });
    
                setCount_pl((c) => {  // Player's moves count
                    return c + 1;
                });
    
                // Create attestation after the player moves
                const obj={ 
                    move: count,  // The move number
                    player_score: score + newDeck[count].n,  // The updated player score

                };
                createAttestationBlackJack(gameId, JSON.stringify(obj));
            }
        }
    };
    




    const bot_step = (count) => {                           // Шаг бота

        if(score_bot<=16 && !botStop){
            const newDeck = [...deck];
            newDeck[count].st = 'bot';
            setDeck(newDeck);
            setCounter((c) => {                  //  Счет всех ходов
                return c + 1
            })
            setScore_bot((s) => {               // Счет очков бота
                return s + newDeck[count].n
            });
        }
    }

    const SetInput = (e) => {                                   // Ввод сумы ставки
        const  m = e.target.value
        if (m<= money) {
            setInput(m)
        }
    }

    const Restart =() =>{
        Continue()
        setMoney(200)
    }

    const Continue = () => {                                  // Продолжение игры после победы или пораженя
        //  Обнуление всех параметров
        setStart(false)
        const car = [...deck]
        car.map((el) => el.st = false)
        setDeck(car)
        setScore(0)
        setScore_bot(0)
        setCounter(0)
        setCount_pl(0)
        setContinue(!continues)
        setBotStop(false)
        setPass(false)
        setResult('')
    }

    const Pass = () => {                                    // Нажатие кнопки Pass
        setPass((p) => {
            return true
        })
        if (score <= 20 && !pass) {
            bot_step(counter)
        }
    }
    useEffect(() => {     // Вызов ходов бота в интервале
        if (score_bot <=16 && pass && !botStop) {
            const timer = setTimeout(() => {
                bot_step(counter)
                clearInterval(timer)
            }, 300)
        }
    }, [score_bot, botStop])

    useEffect(() => {                           // Прослушка счета бота и остановка его ходов и вывод результата
        if (score_bot >= 16) {
            setBotStop(true)
        }
        if (score_bot === score && botStop) {       // Если счета у игрока и бота совпадают - Draw
            setResult('Draw')
            return ;
        }
        if (score_bot === 21) {                    // Если у бота 21 Он победил, игрок lost
            setBotStop(true)
            losing()
            return;
        }
        if (botStop && score_bot > 21) {           // Если бот перебрал очков , игрок победил
            victory()
            return;
        }
        if (botStop && score > score_bot) {        // Если у игрока больше очков, он победил
            victory()
            return;
        }
        if (botStop && score < score_bot && score_bot <= 21) {  // Если у игрока меньше очков чем у бота = lost
            losing()
            return;
        }
        setGameId(gameId+1);       

    }, [score_bot, botStop])

    useEffect(() => {                       // Прослушка счета игрока, и изминение наличия денег
        if (score === 21) {                      // Если игрок набрал 21 , Victory
            victory()
        }
        if (score > 21) {                          // Если у игрока >21, Проигрыш
            losing()
        }
    }, [score])


    useEffect(() => {                       // Прослушка нажатия старта, и перерисовка поля игры
        if (start) {
            Start(deck)
        }
    }, [continues])


    const colors = score <= 21 ? "#2EFF5C" : "#FF4848";   // Цвет счета игрока,

    let color_res = {}     
    //                           
    switch (result) {
        
        case "Victory":
            color_res = {color: '#7BFF4D'};
            break;
        case "Lost":
            color_res = {color: '#FF4D4D'};
            break;
        case "Draw":
            color_res = {color: '#FFFFFF'};
            break;
    }

    return (
        <div style={color_res} className="game-box">
            <Back />
            <ResultAlert
                BotStop={botStop}
                Money={money}
                Result={result}
            />
            <Money
                Score_bot={score_bot}
                Money={money}
                Input={input}
            />
            <Logo/>
            <BlockCarts
                BG={cartt[52].src}
                Carts={deck}
                Count_pl={count_pl}
            />
            <Footer
                Counter={counter}
                Restart={Restart}
                Money={money}
                Start={Start}
                is_start={start}
                Carts={deck}
                OnChange={SetInput}
                Input={input}
                Continue={Continue}
                Pass={Pass}
                Player_step={player_step}
                Scor={score}
                Colors={colors}
                BotStop={botStop}
            />
          <Chat/>
        </div>
    );
}

export default BlackJack;