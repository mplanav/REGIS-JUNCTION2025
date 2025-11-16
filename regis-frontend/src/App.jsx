import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login/Login'
import EmployeeDashboard from './pages/EmployeeDashboard/EmployeeDashboard'


export default function App() {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/employee" element={<EmployeeDashboard />} />
            <Route path="*" element={<div style={{ padding: 20 }}>Page not found</div>} />
        </Routes>
    )
}