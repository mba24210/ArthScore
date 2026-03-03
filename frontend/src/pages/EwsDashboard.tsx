import React from 'react'
import { AlertTriangle, Clock, Activity } from 'lucide-react'

export const EwsDashboard = () => {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold text-slate-800 tracking-tight">EWS Alerts</h2>

            <div className="flex space-x-4 border-b border-slate-200 mb-6">
                <button className="px-4 py-2 border-b-2 border-blue-600 text-blue-600 font-medium">All Open</button>
                <button className="px-4 py-2 text-slate-500 font-medium hover:text-slate-700">Critical (8)</button>
                <button className="px-4 py-2 text-slate-500 font-medium hover:text-slate-700">Warning (23)</button>
                <button className="px-4 py-2 text-slate-500 font-medium hover:text-slate-700">Resolved</button>
            </div>

            <div className="space-y-4">
                {[1, 2, 3].map((alert) => (
                    <div key={alert} className="bg-white rounded-xl shadow-sm border border-l-4 border-l-rose-500 border-slate-200 p-6 flex flex-col md:flex-row gap-6">
                        <div className="flex-1 space-y-3">
                            <div className="flex items-center space-x-3">
                                <span className="px-2 py-0.5 bg-rose-100 text-rose-700 rounded text-xs font-bold uppercase tracking-wider">Critical</span>
                                <h3 className="text-lg font-bold text-slate-800">Suresh Patel</h3>
                                <span className="text-sm text-slate-500">APP_{2026}_{3089 + alert}</span>
                            </div>

                            <div className="flex gap-2">
                                <span className="px-2 py-1 bg-slate-100 text-slate-700 rounded-md text-sm font-medium border border-slate-200">EMI 12 days late</span>
                                <span className="px-2 py-1 bg-slate-100 text-slate-700 rounded-md text-sm font-medium border border-slate-200">Balance dropped 43%</span>
                            </div>

                            <p className="text-sm text-slate-600 bg-amber-50 border border-amber-100 p-3 rounded-md">
                                <span className="font-semibold text-amber-800">Action:</span> Call borrower immediately to understand payment difficulty. Consider restructuring.
                            </p>
                        </div>

                        <div className="w-full md:w-64 bg-slate-50 rounded-lg p-4 border border-slate-200">
                            <div className="mb-2 pb-2 border-b border-slate-200">
                                <p className="text-xs text-slate-500 uppercase tracking-wide">PD Score Details</p>
                            </div>
                            <div className="flex justify-between text-sm mb-1">
                                <span className="text-slate-500">Current PD</span>
                                <span className="font-bold text-rose-600 border-b border-rose-200">41.2%</span>
                            </div>
                            <div className="flex justify-between text-sm mb-3">
                                <span className="text-slate-500">Baseline</span>
                                <span className="font-semibold text-slate-700">18.5%</span>
                            </div>
                            <div className="flex justify-between text-sm items-center">
                                <span className="text-slate-500">Delta</span>
                                <span className="px-2 py-0.5 bg-rose-100 text-rose-700 rounded text-xs font-bold">Δ +22.7%</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
