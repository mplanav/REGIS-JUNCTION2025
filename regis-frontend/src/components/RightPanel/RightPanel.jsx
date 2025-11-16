import React, { useState, useEffect } from "react";
import styles from "./RightPanel.module.css";

export default function RightPanel() {
    const [riskCoverageData, setRiskCoverageData] = useState([]);

    const [regulationAnalysis, setRegulationAnalysis] = useState({
        overlaps: 50,
        conflicts: 50
    });

    const [selectedBar, setSelectedBar] = useState(null);
    const [selectedSegment, setSelectedSegment] = useState(null);
    const [segmentDetails, setSegmentDetails] = useState(null);
    const [segmentDescription, setSegmentDescription] = useState(null);
    const [loading, setLoading] = useState(false);
    const [barDescription, setBarDescription] = useState(null);

    // BASE URL (Docker / local / prod)
    const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://turbosupercharged-superconfident-hayden.ngrok-free.dev/api/v1';
    const RISKS_API_URL = "https://turbosupercharged-superconfident-hayden.ngrok-free.dev/api/v1/risks";
    const CONFLICTS_API_URL = "https://turbosupercharged-superconfident-hayden.ngrok-free.dev/api/v1/conflicts";

    // Fetch overlaps
    const fetchOverlaps = async () => {
        const url = `${API_BASE_URL}https://turbosupercharged-superconfident-hayden.ngrok-free.dev/api/v1/conflicts/conflicts/detail/overlap`;
        console.log("Fetching overlaps:", url);

        const res = await fetch(url, { headers: { "accept": "application/json" } });
        return await res.json();
    };

    // Fetch contradictions
    const fetchContradictions = async () => {
        const url = `${API_BASE_URL}/contradictions/?limit=100&offset=0`;
        console.log("Fetching contradictions:", url);

        const res = await fetch(url, { headers: { "accept": "application/json" } });
        return await res.json();
    };

    // Fetch details dynamically
    const fetchSegmentDetails = async (segment) => {
        const endpoint = `${API_BASE_URL}/${segment}`;
        console.log(`Fetching ${segment} details from:`, endpoint);

        const response = await fetch(endpoint, { headers: { "accept": "application/json" } });
        return await response.json();
    };


    // Fetch risk coverage data
    useEffect(() => {
        const fetchRiskCoverageData = async () => {
            try {
                console.log('Fetching risk coverage summary...');
                const response = await fetch(`${RISKS_API_URL}/risks/summary`, {
                    headers: { 
                        'accept': 'application/json',
                        'ngrok-skip-browser-warning': 'true'
                    }
                });
                const data = await response.json();
                console.log('Risk Coverage API Response:', data);

                if (data && data.risks && Array.isArray(data.risks)) {
                    const formattedData = data.risks.map(risk => ({
                        category: risk.risk_type,
                        value: risk.percentage,
                        color: "#0F5499"
                    }));
                    setRiskCoverageData(formattedData);
                } else {
                    // Fallback if API format is different
                    setRiskCoverageData([
                        { category: "AML", value: 75, color: "#0F5499" },
                        { category: "Fraud", value: 90, color: "#0F5499" },
                        { category: "Cybersecurity", value: 65, color: "#0F5499" },
                        { category: "Governance", value: 80, color: "#0F5499" },
                        { category: "Privacy", value: 85, color: "#0F5499" },
                        { category: "Operational", value: 70, color: "#0F5499" },
                        { category: "Compliance", value: 95, color: "#0F5499" },
                        { category: "Other", value: 55, color: "#0F5499" }
                    ]);
                }
            } catch (err) {
                console.error('Error fetching risk coverage data:', err);
                // Fallback to default data
                setRiskCoverageData([
                    { category: "AML", value: 75, color: "#0F5499" },
                    { category: "Fraud", value: 90, color: "#0F5499" },
                    { category: "Cybersecurity", value: 65, color: "#0F5499" },
                    { category: "Governance", value: 80, color: "#0F5499" },
                    { category: "Privacy", value: 85, color: "#0F5499" },
                    { category: "Operational", value: 70, color: "#0F5499" },
                    { category: "Compliance", value: 95, color: "#0F5499" },
                    { category: "Other", value: 55, color: "#0F5499" }
                ]);
            }
        };

        fetchRiskCoverageData();
    }, []);

    // Fetch regulation analysis data
    useEffect(() => {
        const fetchRegulationData = async () => {
            setLoading(true);
            try {
                console.log('Fetching regulation data...');

                const response = await fetch(`${CONFLICTS_API_URL}/conflicts/summary`, {
                    headers: { 
                        'accept': 'application/json',
                        'ngrok-skip-browser-warning': 'true'
                    }
                });

                const data = await response.json();
                console.log('Conflicts Summary API Response:', data);

                if (data && data.items && Array.isArray(data.items) && data.items.length > 0) {
                    const contradictionItem = data.items.find(item => item.type === 'contradiction');
                    const overlapItem = data.items.find(item => item.type === 'overlap');

                    if (contradictionItem && overlapItem) {
                        setRegulationAnalysis({
                            overlaps: overlapItem.percentage,
                            conflicts: contradictionItem.percentage
                        });
                    }
                } else if (data && data.total === 0) {
                    console.log('No conflicts data available yet - using default mock data');
                    // Keep default 50/50 split when no data
                } else {
                    console.warn('API returned unexpected format, using default values');
                }
            } catch (err) {
                console.error('Error fetching regulation data:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchRegulationData();
    }, []);


    const handleBarClick = async (category, value) => {
        setSelectedBar({ category, value });
        setBarDescription(null);
        console.log(`Clicked on ${category}: ${value}%`);

        try {
            // Convert category to uppercase for the API
            const categoryUpper = category.toUpperCase();
            console.log(`Fetching details for ${categoryUpper}...`);
            const response = await fetch(`${RISKS_API_URL}/risks/detail/${categoryUpper}`, {
                headers: { 
                    'accept': 'application/json',
                    'ngrok-skip-browser-warning': 'true'
                }
            });
            
            const contentType = response.headers.get('content-type');
            console.log('Response content-type:', contentType);
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log(`${category} details response:`, data);

            if (data && data.description) {
                setBarDescription(data.description);
            } else {
                console.warn('No description field found in response');
            }
        } catch (err) {
            console.error(`Error fetching ${category} details:`, err);
            setBarDescription(`Error loading description: ${err.message}`);
        }
    };

    const handleSegmentClick = async (segment, percentage) => {
        setSelectedSegment({ segment, percentage });
        setSegmentDetails(null);
        
        // Set default descriptions for each segment type
        const defaultDescriptions = {
            overlaps: "Cases where two requirements are redundant or partially duplicate the same regulatory obligations.",
            conflicts: "Cases where two requirements conflict or impose opposing obligations that cannot be satisfied simultaneously."
        };
        
        setSegmentDescription(defaultDescriptions[segment]);

        // Map segment name to API parameter - use singular forms 'overlap' and 'contradiction'
        const conflictType = segment === 'overlaps' ? 'overlap' : 'contradiction';
        const endpoint = `${CONFLICTS_API_URL}/conflicts/detail/${conflictType}`;

        try {
            console.log(`Fetching ${segment} details from:`, endpoint);

            const response = await fetch(endpoint, {
                headers: { 
                    'accept': 'application/json',
                    'ngrok-skip-browser-warning': 'true'
                }
            });

            const data = await response.json();
            console.log(`${segment} response:`, data);

            if (data && data.items && Array.isArray(data.items)) {
                setSegmentDetails(data.items);
                
                // Override with specific description from first item if available
                if (data.items.length > 0 && data.items[0].description) {
                    setSegmentDescription(data.items[0].description);
                }
            } else if (Array.isArray(data)) {
                // Handle case where response is directly an array
                setSegmentDetails(data);
                if (data.length > 0 && data[0].description) {
                    setSegmentDescription(data[0].description);
                }
            } else if (data && data.count === 0) {
                // No data available - keep default description
                console.log(`No ${segment} data available`);
                setSegmentDetails([]);
            } else {
                setSegmentDetails([]);
            }
        } catch (err) {
            console.error(`Error fetching ${segment} details:`, err);
            setSegmentDetails([]);
        }
    };


    const maxValue = Math.max(...riskCoverageData.map(d => d.value));
    const chartHeight = 180;
    const barWidth = 36;
    const spacing = 10;
    const startX = 18;

    return (
        <aside className={styles.rightPanel}>
            <div className={styles.section}>
                <h3 className={styles.title}>Risk Coverage Analysis</h3>
                <div className={styles.chartContainer}>
                    <svg width="100%" height={chartHeight + 50} viewBox="0 0 420 250" className={styles.barChart} preserveAspectRatio="xMidYMid meet">
                        {riskCoverageData.map((item, idx) => {
                            const x = startX + idx * (barWidth + spacing);
                            const barHeight = (item.value / maxValue) * chartHeight;
                            const y = chartHeight - barHeight + 20;
                            const isSelected = selectedBar?.category === item.category;

                            return (
                                <g key={item.category}>
                                    <rect
                                        x={x}
                                        y={y}
                                        width={barWidth}
                                        height={barHeight}
                                        fill={isSelected ? "#2563eb" : item.color}
                                        rx="4"
                                        className={styles.barRect}
                                        onClick={() => handleBarClick(item.category, item.value)}
                                        style={{ cursor: 'pointer' }}
                                    />
                                    <text
                                        x={x + barWidth / 2}
                                        y={chartHeight + 35}
                                        fontSize="8"
                                        fill="#64748b"
                                        textAnchor="middle"
                                    >
                                        {item.category}
                                    </text>
                                </g>
                            );
                        })}

                        <text x="5" y={chartHeight + 15} fontSize="9" fill="#64748b">0</text>
                        <text x="2" y={(chartHeight / 2) + 20} fontSize="9" fill="#64748b">50</text>
                        <text x="0" y="25" fontSize="9" fill="#64748b">100</text>
                    </svg>
                    <div className={styles.coverageLegend}>
                        <span className={styles.coverageDot}></span>
                        <span className={styles.coverageLabel}>coverage</span>
                    </div>
                </div>
                {selectedBar && (
                    <div className={styles.infoBox}>
                        <strong>{selectedBar.category}</strong>: {selectedBar.value}% coverage
                        {barDescription && (
                            <div style={{ marginTop: '8px', fontSize: '13px', color: '#64748b', lineHeight: '1.5' }}>
                                {barDescription}
                            </div>
                        )}
                    </div>
                )}
            </div>

            <div className={styles.section}>
                <h3 className={styles.title}>Regulation Analysis</h3>
                <div className={styles.chartContainer}>
                    <div className={styles.donutWrapper}>
                        <svg width="200" height="200" viewBox="0 0 200 200" className={styles.donut}>
                            <circle
                                cx="100"
                                cy="100"
                                r="75"
                                fill="none"
                                stroke={selectedSegment?.segment === 'overlaps' ? "#2563eb" : "#3b82f6"}
                                strokeWidth="38"
                                strokeDasharray={`${(regulationAnalysis.overlaps / 100) * 471} 471`}
                                transform="rotate(-90 100 100)"
                                className={styles.donutSegment}
                                onClick={() => handleSegmentClick('overlaps', regulationAnalysis.overlaps)}
                                style={{ cursor: 'pointer' }}
                            />
                            <circle
                                cx="100"
                                cy="100"
                                r="75"
                                fill="none"
                                stroke={selectedSegment?.segment === 'conflicts' ? "#dc2626" : "#ef4444"}
                                strokeWidth="38"
                                strokeDasharray={`${(regulationAnalysis.conflicts / 100) * 471} 471`}
                                strokeDashoffset={`-${(regulationAnalysis.overlaps / 100) * 471}`}
                                transform="rotate(-90 100 100)"
                                className={styles.donutSegment}
                                onClick={() => handleSegmentClick('conflicts', regulationAnalysis.conflicts)}
                                style={{ cursor: 'pointer' }}
                            />
                        </svg>
                    </div>
                    <div className={styles.pieLabels}>
                        <div className={styles.pieLabel}>
                            <span className={styles.pieValue}>Overlaps {regulationAnalysis.overlaps}%</span>
                        </div>
                        <div className={styles.pieLabel}>
                            <span className={styles.pieValue} style={{ color: '#ef4444' }}>Contradictions {regulationAnalysis.conflicts}%</span>
                        </div>
                    </div>
                </div>

                {segmentDetails && (
                    <div className={styles.detailsBox}>
                        <h4 className={styles.detailsTitle}>
                            {selectedSegment.segment.charAt(0).toUpperCase() + selectedSegment.segment.slice(1)} Details
                        </h4>

                        {segmentDescription && (
                            <div style={{ 
                                marginBottom: '12px', 
                                padding: '12px', 
                                backgroundColor: '#f8fafc', 
                                borderRadius: '6px',
                                fontSize: '13px',
                                color: '#475569',
                                lineHeight: '1.5'
                            }}>
                                {segmentDescription}
                            </div>
                        )}

                        {segmentDetails.length > 0 ? (
                            <>
                                <div className={styles.detailsList}>
                                    {segmentDetails.slice(0, 3).map((item, idx) => (
                                        <div key={idx} className={styles.detailItem}>
                                            <div className={styles.detailNumber}>{idx + 1}</div>
                                            <div className={styles.detailContent}>
                                                {item.description || item.title || item.text || item.summary ||
                                                    (typeof item === 'string'
                                                        ? item
                                                        : JSON.stringify(item).substring(0, 150) + '...')}
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                {segmentDetails.length > 3 && (
                                    <div className={styles.moreItems}>
                                        +{segmentDetails.length - 3} more items
                                    </div>
                                )}
                            </>
                        ) : (
                            <div className={styles.noData}>
                                No {selectedSegment.segment} data available at the moment.
                            </div>
                        )}
                    </div>
                )}
            </div>
        </aside>
    );
}
