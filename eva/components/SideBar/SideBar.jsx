// SideBar.jsx 

import { useState } from "react"
import styles from "./SideBar.module.css"
import { Chart } from "../Chart/Chart";

export const SideBar = (props) => {
    const [plots, setPlots] = useState([1, 2, 3]); 
    

    const getPlots = () => {
        return plots.map( (el, idx) => {
            return(
                <div key={idx}>
                    <Chart key={idx}/> 
                </div>
            )
        })
    }
    
    return(
        <div className = { styles.sideBar }> 
            { getPlots() }
        </div> 
    )
}

