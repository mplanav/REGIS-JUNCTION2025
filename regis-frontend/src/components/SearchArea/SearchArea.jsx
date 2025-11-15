import React, { useState } from "react";
import styles from "./SearchArea.module.css";

function SearchArea() {
    const [query, setQuery] = useState('');
    const [riskCategoryOpen, setRiskCategoryOpen] = useState(false);
    const [selectedRiskCategory, setSelectedRiskCategory] = useState('All');
    const [jurisdictionOpen, setJurisdictionOpen] = useState(false);
    const [selectedJurisdiction, setSelectedJurisdiction] = useState('EU');

    const suggestedRegulations = [
        {
            title: 'AML Risk Requirements under Basel III',
            badge: 'Gold',
            badgeStyle: 'gold',
            description: 'Banks must maintain robust anti-money laundering controls and monitoring systems to detect suspicious activities...',
            tag: 'Basel III'
        },
        {
            title: 'Cybersecurity Framework Guidelines',
            badge: 'Silver',
            badgeStyle: 'silver',
            description: 'Investment firms must implement comprehensive cybersecurity measures to protect against data breaches and cyber attacks...',
            tag: 'MiFID II'
        },
        {
            title: 'Privacy Protection Standards',
            badge: 'Gold',
            badgeStyle: 'gold',
            description: 'Comprehensive guidelines for protecting personal data and ensuring compliance with privacy regulations.',
            tag: 'GDPR'
        }
    ];

    return (
        <div className={styles.container}>
            <div className={styles.leftSection}>
                <div className={styles.inputRow}>
                    <svg width="18" height="18" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.searchIcon}>
                        <path d="M9 17C13.4183 17 17 13.4183 17 9C17 4.58172 13.4183 1 9 1C4.58172 1 1 4.58172 1 9C1 13.4183 4.58172 17 9 17Z" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        <path d="M19 19L14.65 14.65" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <input
                        type="text"
                        className={styles.input}
                        placeholder="Ask about risks..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </div>
            </div>

            <div className={styles.rightSection}>
                <div className={styles.filtersPanel}>
                    <h3 className={styles.filtersTitle}>Filters</h3>

                    <div className={styles.filterGroup}>
                        <label className={styles.filterLabel}>Risk Category</label>
                        <div className={styles.selectWrapper}>
                            <button className={styles.select} onClick={() => setRiskCategoryOpen(!riskCategoryOpen)}>
                                {selectedRiskCategory}
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.chevron}>
                                    <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </button>
                            {riskCategoryOpen && (
                                <div className={styles.dropdown}>
                                    {['All', 'AML', 'Fraud', 'Cybersecurity', 'Governance', 'Privacy', 'Operational', 'Compliance', 'Other'].map((category) => (
                                        <div
                                            key={category}
                                            className={styles.option + (selectedRiskCategory === category ? ' ' + styles.selected : '')}
                                            onClick={() => { setSelectedRiskCategory(category); setRiskCategoryOpen(false); }}
                                        >
                                            {category}
                                            {selectedRiskCategory === category && <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>

                    <div className={styles.filterGroup}>
                        <label className={styles.filterLabel}>Jurisdiction</label>
                        <div className={styles.selectWrapper}>
                            <button className={styles.select} onClick={() => setJurisdictionOpen(!jurisdictionOpen)}>
                                {selectedJurisdiction}
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" className={styles.chevron}>
                                    <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </button>
                            {jurisdictionOpen && (
                                <div className={styles.dropdown}>
                                    {['EU', 'US', 'UK', 'Global'].map((jurisdiction) => (
                                        <div
                                            key={jurisdiction}
                                            className={styles.option + (selectedJurisdiction === jurisdiction ? ' ' + styles.selected : '')}
                                            onClick={() => { setSelectedJurisdiction(jurisdiction); setJurisdictionOpen(false); }}
                                        >
                                            {jurisdiction}
                                            {selectedJurisdiction === jurisdiction && <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M13 4L6 11L3 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className={styles.suggestionsPanel}>
                    <h3 className={styles.suggestionsTitle}>Suggested Regulations</h3>
                    <div className={styles.suggestionsList}>
                        {suggestedRegulations.map((regulation, idx) => (
                            <div key={idx} className={styles.suggestionCard}>
                                <div className={styles.suggestionHeader}>
                                    <span className={styles.badge + ' ' + styles['badge' + regulation.badgeStyle]}>{regulation.badge}</span>
                                    <h4 className={styles.suggestionTitle}>{regulation.title}</h4>
                                </div>
                                <p className={styles.suggestionDescription}>{regulation.description}</p>
                                <div className={styles.suggestionFooter}>
                                    <span className={styles.suggestionTag}>{regulation.tag}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SearchArea;
