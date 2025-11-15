import React from 'react'
import { useNavigate } from 'react-router-dom'
import styles from './Navbar.module.css'


export default function Navbar() {
    const navigate = useNavigate()
    return (
        <header className={styles.navbar}>
            <div className={styles.left} onClick={() => navigate('/employee')}>
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.icon}>
                    <rect width="32" height="32" rx="6" fill="#0F5499" />
                    <path d="M16 8L14.4 9.6V14.4H12.8V22.4H19.2V14.4H17.6V9.6L16 8Z" fill="white" />
                    <rect x="11.2" y="19.2" width="9.6" height="3.2" fill="white" />
                    <rect x="14.4" y="11.2" width="3.2" height="8" fill="white" />
                </svg>
                <div className={styles.brand}>
                    <span className={styles.logo}>Regis</span>
                    <span className={styles.role}>Employee</span>
                </div>
            </div>
            <div className={styles.right}>
                <div className={styles.user} onClick={() => navigate('/login')}>
                    <div className={styles.avatar}>JD</div>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.logoutIcon}>
                        <path d="M6 13L5 12V10H2V6H5V4L6 3L10 7L6 11V9H4V8H6V13Z" fill="currentColor" />
                    </svg>
                    <span>Logout</span>
                </div>
            </div>
        </header>
    )
}