import React, from 'react'
import { Activity, Users, AlertTriangle, ShieldCheck } from 'lucide-react'

export const Dashboard = () => {
    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold text-slate-800 tracking-tight">Portfolio Summary</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                    { title: "Total Portfolio", value: "₹48.2Cr", icon: Activity, color: "text-blue-600", bg: "bg-blue-100" },
                    { title: "Avg PD Score", value: "18.2%", icon: ShieldCheck, color: "text-emerald-600", bg: "bg-emerald-100" },
                    { title: "Active Applications", value: "542", icon: Users, color: "text-purple-600", bg: "bg-purple-100" },
                    { title: "Critical EWS Alerts", value: "8", icon: AlertTriangle, color: "text-rose-600", bg: "bg-rose-100" }
                ].map((stat, i) => (
                    <div key={i} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center space-x-4 transition-all hover:shadow-md">
                        <div className={`p-4 rounded-full ${stat.bg}`}>
                            <stat.icon className={`h-6 w-6 ${stat.color}`} />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-slate-500">{stat.title}</p>
                            <p className="text-2xl font-bold text-slate-800">{stat.value}</p>
                        </div>
                    </div>
                ))}
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <h3 className="text-lg font-semibold mb-4 text-slate-800">Recent Applications</h3>
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-slate-200">
                                <th className="py-3 px-4 text-sm font-medium text-slate-500">App Ref</th>
                                <th className="py-3 px-4 text-sm font-medium text-slate-500">Applicant</th>
                                <th className="py-3 px-4 text-sm font-medium text-slate-500">Loan Amount</th>
                                <th className="py-3 px-4 text-sm font-medium text-slate-500">Rating</th>
                                <th className="py-3 px-4 text-sm font-medium text-slate-500">Status</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {[1, 2, 3, 4, 5].map((row) => (
                                <tr key={row} className="hover:bg-slate-50">
                                    <td className="py-3 px-4 font-medium text-slate-700">APP_{2026}_{1000 + row}</td>
                                    <td className="py-3 px-4 text-slate-600">Ramesh Kumar {row}</td>
                                    <td className="py-3 px-4 text-slate-600">₹{500000 + row * 1000}</td>
                                    <td className="py-3 px-4"><span className="px-2 py-1 bg-green-100 text-green-700 rounded-md text-xs font-semibold">B</span></td>
                                    <td className="py-3 px-4"><span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md text-xs font-semibold">scored</span></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}
