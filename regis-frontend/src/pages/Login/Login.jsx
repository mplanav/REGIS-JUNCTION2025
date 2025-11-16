import React from 'react'
import { useNavigate } from 'react-router-dom'
import styles from './Login.module.css'


export default function Login() {
    const navigate = useNavigate()


    function handleEmployeeLogin() {
        navigate('/employee')
    }


    return (
        <div className={styles.loginShell}>
            <div className={styles.card}>
                <div className={styles.icon}>
                    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="40" height="40" rx="20" fill="#0F5499" />
                        <path d="M20 10L18 12V18H16V28H24V18H22V12L20 10Z" fill="white" />
                        <rect x="14" y="24" width="12" height="4" fill="white" />
                        <rect x="18" y="14" width="4" height="10" fill="white" />
                    </svg>
                </div>

                <h1 className={styles.title}>Regis</h1>
                <p className={styles.subtitle}>Access your regulatory intelligence dashboard</p>

                <div className={styles.actions}>
                    <button className={styles.btn} onClick={handleEmployeeLogin}>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2L10 4L10 6C8.3 6.6 7 8.2 7 10V14L5 16V17H19V16L17 14V10C17 8.2 15.7 6.6 14 6V4L12 2ZM12 5C13.7 5 15 6.3 15 8V14.8L15.6 15.4H8.4L9 14.8V8C9 6.3 10.3 5 12 5Z" fill="currentColor" />
                            <path d="M10 18C10 19.1 10.9 20 12 20C13.1 20 14 19.1 14 18H10Z" fill="currentColor" />
                        </svg>
                        Enter Dashboard
                    </button>
                </div>
            </div>
        </div>
    )
}