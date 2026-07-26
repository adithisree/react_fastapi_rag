import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import CBC from './CBC.jsx'
import FBC from './FBC.jsx'
import Hiadithi from './Hiadithi.jsx'

createRoot(document.getElementById('root')).render(
     <StrictMode>
    <App />
    <CBC/>
    <FBC/>
    <Hiadithi/>
     </StrictMode>
    

)
