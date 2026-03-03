import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Dashboard } from './pages/Dashboard'
import { ApplicationForm } from './pages/ApplicationForm'
import { RiskAssessment } from './pages/RiskAssessment'
import { EwsDashboard } from './pages/EwsDashboard'

const AppLayout = ({ children }: { children: React.ReactNode }) => (
    <div className="min-h-screen bg-slate-50 flex">
        <nav className="w-64 bg-slate-900 text-white p-6">
            <h1 className="text-2xl font-bold mb-8 text-blue-400">CreditVision AI</h1>
            <ul className="space-y-4">
                <li><a href="/" className="hover:text-blue-300 transition-colors">Dashboard</a></li>
                <li><a href="/apply" className="hover:text-blue-300 transition-colors">New Application</a></li>
                <li><a href="/ews" className="hover:text-blue-300 transition-colors">EWS Alerts</a></li>
            </ul>
        </nav>
        <main className="flex-1 p-8">
            {children}
        </main>
    </div>
)

function App() {
    return (
        <BrowserRouter>
            <AppLayout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/apply" element={<ApplicationForm />} />
                    <Route path="/assessment/:id" element={<RiskAssessment />} />
                    <Route path="/ews" element={<EwsDashboard />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </AppLayout>
        </BrowserRouter>
    )
}

export default App
