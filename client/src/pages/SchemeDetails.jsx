import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle, FileText, Globe } from 'lucide-react';
import axios from 'axios';

export default function SchemeDetails() {
    const { id } = useParams();
    const [scheme, setScheme] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Since we don't have a single scheme endpoint yet, we'll fetch all and filter
        // In a real app, you'd add a GET /api/schemes/:id endpoint
        axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/recommend`, {})
            .then((res) => {
                const found = res.data.find(s => s.id === parseInt(id));
                setScheme(found);
                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, [id]);

    if (loading) return <div className="text-center mt-20 text-white">Loading...</div>;
    if (!scheme) return <div className="text-center mt-20 text-white">Scheme not found.</div>;

    return (
        <div className="min-h-screen bg-slate-900 text-slate-100 p-8">
            <div className="max-w-4xl mx-auto">
                <Link to="/dashboard" className="inline-flex items-center text-blue-400 hover:text-blue-300 mb-6">
                    <ArrowLeft className="w-4 h-4 mr-2" /> Back to Dashboard
                </Link>
                
                <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 p-8 rounded-3xl shadow-2xl">
                    <div className="inline-block px-3 py-1 bg-blue-500/20 text-blue-300 rounded-full text-sm font-medium mb-4">
                        {scheme.category}
                    </div>
                    <h1 className="text-3xl font-bold mb-4">{scheme.name}</h1>
                    <p className="text-slate-300 text-lg mb-8 leading-relaxed">
                        {scheme.description}
                    </p>

                    <div className="grid md:grid-cols-2 gap-8 mb-8">
                        <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-700/50">
                            <h3 className="flex items-center text-xl font-semibold mb-4 text-emerald-400">
                                <CheckCircle className="w-5 h-5 mr-2" /> Eligibility
                            </h3>
                            <p className="text-slate-300">{scheme.eligibility}</p>
                        </div>
                        <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-700/50">
                            <h3 className="flex items-center text-xl font-semibold mb-4 text-purple-400">
                                <FileText className="w-5 h-5 mr-2" /> Benefits
                            </h3>
                            <p className="text-slate-300">{scheme.benefits}</p>
                        </div>
                    </div>

                    <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-700/50 mb-8">
                        <h3 className="text-xl font-semibold mb-4 text-amber-400">Required Documents</h3>
                        <p className="text-slate-300">{scheme.documents}</p>
                    </div>

                    {scheme.officialLink && (
                        <a 
                            href={scheme.officialLink} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="inline-flex items-center bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-xl font-semibold transition-colors"
                        >
                            <Globe className="w-5 h-5 mr-2" /> Apply on Official Portal
                        </a>
                    )}
                </div>
            </div>
        </div>
    );
}
