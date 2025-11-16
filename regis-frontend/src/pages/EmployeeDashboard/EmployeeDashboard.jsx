import React, { useState, useEffect } from 'react'
import Navbar from '../../components/Navbar/Navbar'
import RightPanel from '../../components/RightPanel/RightPanel'
import styles from './EmployeeDashboard.module.css'


export default function EmployeeDashboard() {
    const [suggestedRegulations, setSuggestedRegulations] = useState([]);
    const [loading, setLoading] = useState(true);

    const REQUIREMENTS_API_URL = "https://turbosupercharged-superconfident-hayden.ngrok-free.dev/api/v1/requirements";

    useEffect(() => {
        const fetchSuggestedRegulations = async () => {
            try {
                console.log('Fetching suggested regulations...');
                const response = await fetch(`${REQUIREMENTS_API_URL}/requirements/list`, {
                    headers: {
                        'accept': 'application/json',
                        'ngrok-skip-browser-warning': 'true'
                    }
                });
                const data = await response.json();
                console.log('Requirements API Response:', data);

                if (data && data.items && Array.isArray(data.items)) {
                    // Take first 10 items and format them
                    const formattedRegs = data.items.slice(0, 10).map(item => ({
                        id: item.id,
                        title: item.short_description || 'Regulatory Requirement',
                        badge: item.risk_type,
                        badgeStyle: getBadgeStyle(item.risk_type),
                        description: item.text,
                        tag: item.jurisdiction
                    }));
                    setSuggestedRegulations(formattedRegs);
                }
            } catch (err) {
                console.error('Error fetching suggested regulations:', err);
                // Fallback to default data
                setSuggestedRegulations([
                    {
                        title: 'AML Risk Requirements under Basel III',
                        badge: 'AML',
                        badgeStyle: 'gold',
                        description: 'Banks must maintain robust anti-money laundering controls and monitoring systems to detect suspicious activities...',
                        tag: 'Basel III'
                    },
                    {
                        title: 'Cybersecurity Framework Guidelines',
                        badge: 'CYBERSECURITY',
                        badgeStyle: 'silver',
                        description: 'Investment firms must implement comprehensive cybersecurity measures to protect against data breaches and cyber attacks...',
                        tag: 'MiFID II'
                    },
                    {
                        title: 'Privacy Protection Standards',
                        badge: 'PRIVACY',
                        badgeStyle: 'gold',
                        description: 'Comprehensive guidelines for protecting personal data and ensuring compliance with privacy regulations.',
                        tag: 'GDPR'
                    }
                ]);
            } finally {
                setLoading(false);
            }
        };

        fetchSuggestedRegulations();
    }, []);

    const getBadgeStyle = (riskType) => {
        const styles = {
            'AML': 'gold',
            'FRAUD': 'red',
            'CYBERSECURITY': 'blue',
            'GOVERNANCE': 'green',
            'PRIVACY': 'purple',
            'OPERATIONAL': 'orange',
            'COMPLIANCE': 'teal',
            'OTHER': 'gray'
        };
        return styles[riskType] || 'gray';
    };

    const getBadgeColor = (badgeStyle) => {
        const colors = {
            'gold': { bg: '#fef3c7', text: '#92400e' },
            'red': { bg: '#fee2e2', text: '#991b1b' },
            'blue': { bg: '#dbeafe', text: '#1e40af' },
            'green': { bg: '#d1fae5', text: '#065f46' },
            'purple': { bg: '#e9d5ff', text: '#6b21a8' },
            'orange': { bg: '#fed7aa', text: '#9a3412' },
            'teal': { bg: '#ccfbf1', text: '#115e59' },
            'gray': { bg: '#e5e7eb', text: '#374151' }
        };
        return colors[badgeStyle] || colors.gray;
    };

    return (
        <div className="app-shell">
            <Navbar />
            <div className={styles.shell}>
                <RightPanel />
                <main className={styles.main}>
                    <div style={{ padding: '24px' }}>
                        <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#0f172a', marginBottom: '16px' }}>
                            Suggested Regulations {loading && <span style={{ fontSize: '14px', color: '#64748b' }}>(Loading...)</span>}
                        </h2>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            {suggestedRegulations.map((regulation, idx) => {
                                const badgeColor = getBadgeColor(regulation.badgeStyle);
                                return (
                                    <div key={regulation.id || idx} style={{ 
                                        backgroundColor: 'white', 
                                        border: '1px solid #e2e8f0', 
                                        borderRadius: '8px', 
                                        padding: '16px'
                                    }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                                            <span style={{ 
                                                fontSize: '12px', 
                                                fontWeight: '600', 
                                                padding: '4px 8px', 
                                                borderRadius: '4px',
                                                backgroundColor: badgeColor.bg,
                                                color: badgeColor.text
                                            }}>
                                                {regulation.badge}
                                            </span>
                                            <h4 style={{ fontSize: '16px', fontWeight: '600', color: '#0f172a' }}>{regulation.title}</h4>
                                        </div>
                                        <p style={{ fontSize: '14px', color: '#64748b', marginBottom: '12px' }}>{regulation.description}</p>
                                        <div>
                                            <span style={{ 
                                                fontSize: '12px', 
                                                color: '#0f5499', 
                                                backgroundColor: '#dbeafe', 
                                                padding: '4px 8px', 
                                                borderRadius: '4px' 
                                            }}>
                                                {regulation.tag}
                                            </span>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </main>
            </div>
        </div>
    )
}