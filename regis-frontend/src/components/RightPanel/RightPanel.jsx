import React, { useState, useEffect } from "react";
import styles from "./RightPanel.module.css";

export default function RightPanel() {
    const [riskCoverageData] = useState([
        { category: "AML", value: 75, color: "#0F5499" },
        { category: "Fraud", value: 90, color: "#0F5499" },
        { category: "Cybersecurity", value: 65, color: "#0F5499" },
        { category: "Governance", value: 80, color: "#0F5499" },
        { category: "Privacy", value: 85, color: "#0F5499" },
        { category: "Operational", value: 70, color: "#0F5499" },
        { category: "Compliance", value: 95, color: "#0F5499" },
        { category: "Other", value: 55, color: "#0F5499" }
    ]);

    const [regulationAnalysis, setRegulationAnalysis] = useState({
        overlaps: 50,
        conflicts: 50
    });

    const [selectedBar, setSelectedBar] = useState(null);
    const [selectedSegment, setSelectedSegment] = useState(null);
    const [segmentDetails, setSegmentDetails] = useState(null);
    const [loading, setLoading] = useState(false);

    // BASE URL (Docker / local / prod)
    const API_BASE_URL = import.meta.env.VITE_API_URL;

    // Fetch overlaps
    const fetchOverlaps = async () => {
        const url = `${API_BASE_URL}/overlaps/?limit=100&offset=0`;
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


    // Fetch regulation analysis data
    useEffect(() => {
        const fetchRegulationData = async () => {
            setLoading(true);
            try {
                console.log('Fetching regulation data...');

                const [overlapsRes, contradictionsRes] = await Promise.all([
                    fetch(`${API_BASE_URL}/overlaps/?limit=100&offset=0`, {
                        headers: { 'accept': 'application/json' }
                    }),
                    fetch(`${API_BASE_URL}/contradictions/?limit=100&offset=0`, {
                        headers: { 'accept': 'application/json' }
                    })
                ]);

                const overlapsData = await overlapsRes.json();
                const contradictionsData = await contradictionsRes.json();

                console.log('Overlaps API Response:', overlapsData);
                console.log('Contradictions API Response:', contradictionsData);

                if (overlapsData.detail || contradictionsData.detail) {
                    console.warn('API returned error details, using default values');
                    return;
                }

                const overlapsCount = overlapsData.count || (Array.isArray(overlapsData) ? overlapsData.length : 0);
                const contradictionsCount = contradictionsData.count || (Array.isArray(contradictionsData) ? contradictionsData.length : 0);

                const total = overlapsCount + contradictionsCount;

                if (total > 0) {
                    const overlapsPercent = Math.round((overlapsCount / total) * 100);
                    const conflictsPercent = 100 - overlapsPercent;

                    setRegulationAnalysis({
                        overlaps: overlapsPercent,
                        conflicts: conflictsPercent
                    });
                }
            } catch (err) {
                console.error('Error fetching regulation data:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchRegulationData();
    }, []);


    const handleBarClick = (category, value) => {
        setSelectedBar({ category, value });
        console.log(`Clicked on ${category}: ${value}%`);
    };

    const handleSegmentClick = async (segment, percentage) => {
        setSelectedSegment({ segment, percentage });
        setSegmentDetails(null);

        const endpoint = segment === 'overlaps'
            ? `${API_BASE_URL}/overlaps/?limit=10&offset=0`
            : `${API_BASE_URL}/contradictions/?limit=10&offset=0`;

        try {
            console.log(`Fetching ${segment} details from:`, endpoint);

            const response = await fetch(endpoint, {
                headers: { 'accept': 'application/json' }
            });

            const data = await response.json();
            console.log(`${segment} response:`, data);

            if (!data.detail) {
                const results = data.results || data;
                setSegmentDetails(Array.isArray(results) ? results : []);
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
