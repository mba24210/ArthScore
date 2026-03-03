import React, { useState } from 'react'

export const ApplicationForm = () => {
    const [step, setStep] = useState(1)

    const nextStep = () => setStep(s => Math.min(6, s + 1))
    const prevStep = () => setStep(s => Math.max(1, s - 1))

    return (
        <div className="max-w-4xl mx-auto">
            <div className="mb-8">
                <h2 className="text-3xl font-bold text-slate-800 tracking-tight">New Application</h2>
                <div className="flex space-x-2 mt-4">
                    {[1, 2, 3, 4, 5, 6].map(s => (
                        <div key={s} className={`h-2 flex-1 rounded-full ${step >= s ? 'bg-blue-600' : 'bg-slate-200'}`}></div>
                    ))}
                </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
                {step === 1 && (
                    <div className="space-y-6">
                        <h3 className="text-xl font-semibold text-slate-800 border-b pb-2">Step 1: Identity</h3>
                        <div className="grid grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                                <input type="text" className="w-full rounded-md border border-slate-300 p-2 outline-none focus:ring-2 focus:ring-blue-500" placeholder="Ramesh Kumar" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Phone Number</label>
                                <input type="tel" className="w-full rounded-md border border-slate-300 p-2 outline-none focus:ring-2 focus:ring-blue-500" placeholder="9876543210" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Age</label>
                                <input type="number" className="w-full rounded-md border border-slate-300 p-2 outline-none focus:ring-2 focus:ring-blue-500" placeholder="34" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Gender</label>
                                <select className="w-full rounded-md border border-slate-300 p-2 outline-none focus:ring-2 focus:ring-blue-500">
                                    <option>Male</option>
                                    <option>Female</option>
                                    <option>Other</option>
                                </select>
                            </div>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="space-y-6">
                        <h3 className="text-xl font-semibold text-slate-800 border-b pb-2">Step 2: Location & Household</h3>
                        <p className="text-slate-500">Form fields for location and dependents...</p>
                    </div>
                )}

                {step === 3 && (
                    <div className="space-y-6">
                        <h3 className="text-xl font-semibold text-slate-800 border-b pb-2">Step 3: Employment & Income</h3>
                        <p className="text-slate-500">Form fields for employment, income and expenses...</p>
                    </div>
                )}

                {step === 4 && (
                    <div className="space-y-6">
                        <h3 className="text-xl font-semibold text-slate-800 border-b pb-2">Step 4: Assets & Liabilities</h3>
                        <p className="text-slate-500">Form fields for diverse lifestyle assets...</p>
                    </div>
                )}

                {step === 5 && (
                    <div className="space-y-6">
                        <h3 className="text-xl font-semibold text-slate-800 border-b pb-2">Step 5: Loan Details</h3>
                        <p className="text-slate-500">Form fields for loan requirement and existing loans...</p>
                    </div>
                )}

                {step === 6 && (
                    <div className="space-y-6">
                        <h3 className="text-xl font-semibold text-slate-800 border-b pb-2">Step 6: Credit History (Optional)</h3>
                        <p className="text-slate-500">Form fields for past defaults and behavioral scores...</p>
                    </div>
                )}

                <div className="mt-8 pt-6 border-t flex justify-between">
                    <button
                        onClick={prevStep}
                        disabled={step === 1}
                        className="px-6 py-2 rounded-md border border-slate-300 text-slate-700 font-medium hover:bg-slate-50 disabled:opacity-50"
                    >
                        Back
                    </button>
                    {step < 6 ? (
                        <button
                            onClick={nextStep}
                            className="px-6 py-2 rounded-md bg-blue-600 text-white font-medium hover:bg-blue-700"
                        >
                            Next Step
                        </button>
                    ) : (
                        <button
                            className="px-6 py-2 rounded-md bg-emerald-600 text-white font-medium hover:bg-emerald-700"
                            onClick={() => window.location.href = '/assessment/APP_2026_00142'}
                        >
                            Submit & Score
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
