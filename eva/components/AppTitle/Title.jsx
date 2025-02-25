import styles from "./Title.module.css"
import Image from 'next/image'

export const Title = () => {
    return (
        <div className={ styles.container } >
            <div className= { styles.imageContainer }>
                 <Image
                            aria-hidden
                            src="/logo.svg"
                            alt="File icon"
                            width={100}
                            height={100}
                          />
            </div>
            <div>
                <h3 className = { styles.title }>Eva</h3>
                <h5 className = { styles.subtitle }> GUI for Walle </h5>
            </div>
        </div>
    )
}