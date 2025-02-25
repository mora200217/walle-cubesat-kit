import styles from "./Title.module.css"
import Image from 'next/image'

export const Title = () => {
    return (
        <div className={ styles.container } >
            <h3 className = { styles.title }>Eva</h3>
            <h5 className = { styles.title }> Hola </h5>
        </div>
    )
}