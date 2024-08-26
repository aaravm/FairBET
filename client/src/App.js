import React, {useEffect} from "react"

import { io } from 'socket.io-client'

import 'bootstrap/dist/css/bootstrap.min.css'
import "./css/fonts.css"
import "./css/special_occasions.css"
import "./css/style.css"

import Page from "./components/pages/page"

const socket = io()

function App(){
  	useEffect(() => {
		socket.connect()		
		return () => {
			socket.disconnect()
		}
	}, [])

  	setInterval(function(){		  
    	socket.emit('heartbeat', { data: "ping" })
  	}, 15000)

	return <Page socket={socket}/>
}

export default App