import { useState } from 'react'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'; 

import './App.css'
import ObjectDetection from './components/ObjectDetection'

function App() {
  const [count, setCount] = useState(0)

  return (
   <div>
    <ToastContainer autoClose={1000}/> 
    <ObjectDetection/>
   </div>
  )
}

export default App
