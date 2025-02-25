// Chart.jsx 
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import styles from "./Chart.module.css"
import { useState } from "react";

export const Chart = (props) => {
    const [data, setData] = useState([1, 2, 3, 4, 5]); 

    return (
                <div className={styles.chartOverlay}>
                    
                <ResponsiveContainer width="100%" height="100%">
                {/* <h4>Gráfica</h4> */}
                    <LineChart data={data} title="Hola mundo" margin={{ top: 0, right: 0, left: 0, bottom: 5 }} onClick={() => {alert("asd")}}>
                        
                        <CartesianGrid strokeDasharray="1" />
                        <XAxis dataKey="time" label={"Time (s)"}/>
                        <YAxis label="Height" />
                        
                        {/* <Tooltip /> */}
                        <Line type="natural" dataKey="value" stroke="#8884d8" strokeWidth={3} dot={true} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
    )

}