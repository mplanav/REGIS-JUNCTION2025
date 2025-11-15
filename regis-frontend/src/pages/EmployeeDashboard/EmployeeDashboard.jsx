import React from 'react'
import Navbar from '../../components/Navbar/Navbar'
import SearchArea from '../../components/SearchArea/SearchArea'
import RightPanel from '../../components/RightPanel/RightPanel'
import styles from './EmployeeDashboard.module.css'


export default function EmployeeDashboard() {
    return (
        <div className="app-shell">
            <Navbar />
            <div className={styles.shell}>
                <RightPanel />
                <main className={styles.main}>
                    <SearchArea />
                </main>
            </div>
        </div>
    )
}