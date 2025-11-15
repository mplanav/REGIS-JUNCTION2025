import React from 'react'
import Navbar from '../../components/Navbar/Navbar'
import styles from './AdminDashboard.module.css'


export default function AdminDashboard(){
return (
<div className="app-shell">
<Navbar />
<div className={styles.container}>
<h2 className="title">Administrator Console</h2>
<div className="row">
<div className="card" style={{flex:1}}>
<h3 className="small">Top Searches</h3>
<ul className="small">
<li>Credit risk - 124</li>
<li>Operational risk - 92</li>
<li>Liquidity risk - 58</li>
</ul>
</div>


<div className="card" style={{flex:1}}>
<h3 className="small">Contradictions - Hotspots</h3>
<p className="small">Sections in directives X, Y show overlaps</p>
</div>
</div>


<div className="row" style={{marginTop:16}}>
<div className="card" style={{flex:1}}>User activity heatmap placeholder</div>
<div className="card" style={{flex:1}}>System metrics placeholder</div>
</div>
</div>
</div>
)
}