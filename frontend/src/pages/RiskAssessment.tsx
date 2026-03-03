import React from 'react'
import { useParams } from 'react-router-dom'
import { CheckCircle, AlertOctagon, TrendingDown, DollarSign } from 'lucide-react'

export const RiskAssessment = () => {
    const { id } = useParams()

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
                <div className="flex justify-between items-start mb-8">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800">Assessment Result</h2>
                        <p className="text-slate-500">Application {id} • Ramesh Kumar</p>
                    </div>
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold border border-blue-200">
                        New-To-Credit
                    </span>
                </div>

                <div className="grid grid-cols-2 gap-8 mb-8">
                    <div className="p-6 bg-slate-50 rounded-lg border border-slate-200 text-center">
                        <p className="text-sm font-medium text-slate-500 uppercase tracking-wide mb-1">Probability of Default</p>
                        <p className="text-5xl font-bold text-slate-800">23.4%</p>
                    </div>
                    <div className="p-6 bg-amber-50 rounded-lg border border-amber-200 text-center flex flex-col justify-center items-center">
                        <p className="text-sm font-medium text-amber-700 uppercase tracking-wide mb-1">Risk Rating</p>
                        <div className="h-16 w-16 bg-amber-500 text-white rounded-full flex items-center justify-center text-3xl font-bold shadow-sm">
                            B
                        </div>
                    </div>
                </div>

                <div className="mb-8 p-6 bg-slate-50 rounded-lg border border-slate-200">
                    <h3 className="text-lg font-semibold text-slate-800 mb-4">Recommendation</h3>
                    <div className="flex justify-between items-center">
                        <div>
                            <p className="text-emerald-600 font-semibold flex items-center">
                                <CheckCircle className="w-5 h-5 mr-2" />
                                APPROVE (Standard Terms)
                            </p>
                            <p className="text-slate-600 mt-1">Suggested Interest Rate Band: <span className="font-bold">11-14%</span></p>
                        </div>
                    </div>
                </div>

                <div className="mb-8">
                    <h3 className="text-lg font-semibold text-slate-800 mb-4">Top Risk Factors</h3>
                    <div className="space-y-3">
                        <div className="p-3 bg-red-50 text-red-800 rounded flex justify-between items-center border border-red-100">
                            <span className="flex items-center"><AlertOctagon className="w-4 h-4 mr-2" /> Debt-to-Income Ratio</span>
                            <span className="font-semibold">1.8x (High)</span>
                        </div>
                        <div className="p-3 bg-amber-50 text-amber-800 rounded flex justify-between items-center border border-amber-100">
                            <span className="flex items-center"><TrendingDown className="w-4 h-4 mr-2" /> EMI Burden</span>
                            <span className="font-semibold">41% (Moderate)</span>
                        </div>
                        <div className="p-3 bg-green-50 text-green-800 rounded flex justify-between items-center border border-green-100">
                            <span className="flex items-center"><DollarSign className="w-4 h-4 mr-2" /> Lifestyle Assets</span>
                            <span className="font-semibold">5/7 (Good)</span>
                        </div>
                    </div>
                </div>

                <div className="pt-6 border-t flex space-x-4">
                    <button className="flex-1 py-3 bg-emerald-600 text-white rounded-md font-medium hover:bg-emerald-700 transition">
                        Finalize Approval
                    </button>
                    <button className="flex-1 py-3 bg-slate-100 text-slate-700 rounded-md font-medium hover:bg-slate-200 transition border border-slate-300">
                        Approve with Conditions
                    </button>
                    <button className="flex-1 py-3 bg-rose-50 text-rose-700 rounded-md font-medium hover:bg-rose-100 transition border border-rose-200">
                        Reject
                    </button>
                </div>
            </div>
        </div>
    )
}
