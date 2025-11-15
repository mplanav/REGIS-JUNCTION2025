import React, { useState } from 'react'
import styles from './Sidebar.module.css'


export default function Sidebar() {
    const [categoryOpen, setCategoryOpen] = useState(false)
    const [tierOpen, setTierOpen] = useState(false)
    const [jurisdictionOpen, setJurisdictionOpen] = useState(false)
    const [selectedCategory, setSelectedCategory] = useState('All Categories')
    const [selectedTier, setSelectedTier] = useState('All Tiers')
    const [selectedJurisdiction, setSelectedJurisdiction] = useState('European Union')

    return (
        <aside className={styles.sidebar}>
            <div className={styles.header}>
                <h3 className={styles.title}>Filters</h3>
            </div>

            <div className={styles.section}>
                <label className={styles.label}>Risk Category</label>
                <div className={styles.selectWrapper}>
                    <button className={styles.select} onClick={() => setCategoryOpen(!categoryOpen)}>
                        {selectedCategory}
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.chevron}>
                            <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </button>
                    {categoryOpen && (
                        <div className={styles.dropdown}>
                            <div className={styles.option + (selectedCategory === 'All Categories' ? ' ' + styles.selected : '')} onClick={() => { setSelectedCategory('All Categories'); setCategoryOpen(false); }}>
                                All Categories
                                {selectedCategory === 'All Categories' && <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>}
                            </div>
                            <div className={styles.option} onClick={() => { setSelectedCategory('Operational'); setCategoryOpen(false); }}>Operational</div>
                            <div className={styles.option} onClick={() => { setSelectedCategory('Credit'); setCategoryOpen(false); }}>Credit</div>
                            <div className={styles.option} onClick={() => { setSelectedCategory('Market'); setCategoryOpen(false); }}>Market</div>
                            <div className={styles.option} onClick={() => { setSelectedCategory('Liquidity'); setCategoryOpen(false); }}>Liquidity</div>
                            <div className={styles.option} onClick={() => { setSelectedCategory('Compliance'); setCategoryOpen(false); }}>Compliance</div>
                        </div>
                    )}
                </div>
            </div>

            <div className={styles.section}>
                <label className={styles.label}>Tier</label>
                <div className={styles.selectWrapper}>
                    <button className={styles.select} onClick={() => setTierOpen(!tierOpen)}>
                        {selectedTier}
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.chevron}>
                            <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </button>
                    {tierOpen && (
                        <div className={styles.dropdown}>
                            <div className={styles.option + (selectedTier === 'All Tiers' ? ' ' + styles.selected : '')} onClick={() => { setSelectedTier('All Tiers'); setTierOpen(false); }}>
                                All Tiers
                                {selectedTier === 'All Tiers' && <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>}
                            </div>
                            <div className={styles.option} onClick={() => { setSelectedTier('Gold'); setTierOpen(false); }}>Gold</div>
                            <div className={styles.option} onClick={() => { setSelectedTier('Silver'); setTierOpen(false); }}>Silver</div>
                            <div className={styles.option} onClick={() => { setSelectedTier('Bronze'); setTierOpen(false); }}>Bronze</div>
                        </div>
                    )}
                </div>
            </div>

            <div className={styles.section}>
                <label className={styles.label}>Jurisdiction</label>
                <div className={styles.selectWrapper}>
                    <button className={styles.select} onClick={() => setJurisdictionOpen(!jurisdictionOpen)}>
                        {selectedJurisdiction}
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.chevron}>
                            <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </button>
                    {jurisdictionOpen && (
                        <div className={styles.dropdown}>
                            <div className={styles.option + (selectedJurisdiction === 'European Union' ? ' ' + styles.selected : '')} onClick={() => { setSelectedJurisdiction('European Union'); setJurisdictionOpen(false); }}>
                                European Union
                                {selectedJurisdiction === 'European Union' && <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>}
                            </div>
                            <div className={styles.option} onClick={() => { setSelectedJurisdiction('United States'); setJurisdictionOpen(false); }}>United States</div>
                            <div className={styles.option} onClick={() => { setSelectedJurisdiction('United Kingdom'); setJurisdictionOpen(false); }}>United Kingdom</div>
                            <div className={styles.option} onClick={() => { setSelectedJurisdiction('Global'); setJurisdictionOpen(false); }}>Global</div>
                        </div>
                    )}
                </div>
            </div>
        </aside>
    )
}