import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { MessageSquare, Bookmark, Search, User } from 'lucide-react';
import Chatbot from '../components/Chatbot';

export default function Dashboard() {
    const { user, logout } = useContext(AuthContext);
    const navigate = useNavigate();
    const [schemes, setSchemes] = useState([]);
    const [isChatOpen, setIsChatOpen] = useState(false);

    useEffect(() => {
        if (!user) return;
        const fetchSchemes = async () => {
            try {
                const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/recommend`);
                setSchemes(res.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchSchemes();
    }, [user]);

    if (!user) return null;

    return (
        <div className="min-h-screen bg-slate-50 flex">
            {/* Sidebar */}
            <aside className="w-64 glass shadow-md hidden md:flex flex-col">
                <div className="p-6">
                    <h2 className="text-xl font-bold text-primary">JanSeva AI</h2>
                </div>
                <nav className="flex-1 px-4 flex flex-col gap-2">
                    <Link to="/dashboard" className="flex items-center gap-2 p-3 bg-primary/10 text-primary rounded-lg font-medium"><Search size={18}/> Recommended</Link>
                    <Link to="/profile" className="flex items-center gap-2 p-3 hover:bg-slate-100 rounded-lg text-slate-700 font-medium"><User size={18}/> Profile</Link>
                    <Link to="/bookmarks" className="flex items-center gap-2 p-3 hover:bg-slate-100 rounded-lg text-slate-700 font-medium"><Bookmark size={18}/> Saved Schemes</Link>
                </nav>
                <div className="p-4">
                    <button onClick={() => { logout(); navigate('/'); }} className="w-full p-2 text-red-500 font-medium hover:bg-red-50 rounded-lg">Logout</button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-8">
                <header className="mb-8 flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold">Welcome, {user.user.name}</h1>
                        <p className="text-slate-500">Here are the government schemes you are eligible for.</p>
                    </div>
                </header>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {schemes.length === 0 ? (
                        <div className="col-span-full p-8 text-center bg-white rounded-xl shadow-sm border border-slate-100">
                            <p className="text-slate-500 mb-4">Please update your profile to get personalized recommendations.</p>
                            <Link to="/profile" className="px-4 py-2 bg-primary text-white rounded-lg">Update Profile</Link>
                        </div>
                    ) : (
                        schemes.map(scheme => (
                            <div key={scheme.id} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 hover:shadow-md transition">
                                <span className="text-xs font-bold text-accent bg-accent/10 px-2 py-1 rounded-full uppercase">{scheme.category}</span>
                                <h3 className="text-lg font-bold mt-3 mb-2">{scheme.name}</h3>
                                <p className="text-sm text-slate-600 mb-4 line-clamp-2">{scheme.description}</p>
                                <Link to={`/scheme/${scheme.id}`} className="text-primary font-medium text-sm hover:underline">View Details →</Link>
                            </div>
                        ))
                    )}
                </div>
            </main>

            {/* Chatbot Toggle */}
            <button 
                onClick={() => setIsChatOpen(!isChatOpen)}
                className="fixed bottom-6 right-6 w-14 h-14 bg-primary text-white rounded-full flex items-center justify-center shadow-lg hover:bg-secondary transition z-50"
            >
                <MessageSquare />
            </button>
            
            {isChatOpen && <Chatbot close={() => setIsChatOpen(false)} />}
        </div>
    );
}
