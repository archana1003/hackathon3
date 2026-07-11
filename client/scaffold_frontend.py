import os

dirs = [
    "src/components",
    "src/pages",
    "src/context",
    "src/services",
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# context/AuthContext.jsx
with open("src/context/AuthContext.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState(localStorage.getItem('token'));

    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            fetchProfile();
        } else {
            localStorage.removeItem('token');
            delete axios.defaults.headers.common['Authorization'];
            setUser(null);
            setLoading(false);
        }
    }, [token]);

    const fetchProfile = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/profile');
            setUser(res.data);
        } catch (error) {
            console.error('Error fetching profile', error);
            setToken(null);
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        const res = await axios.post('http://localhost:8000/api/login', { email, password });
        setToken(res.data.access_token);
    };

    const register = async (name, email, password) => {
        const res = await axios.post('http://localhost:8000/api/register', { name, email, password });
        setToken(res.data.access_token);
    };

    const logout = () => {
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ user, token, login, register, logout, loading, fetchProfile }}>
            {children}
        </AuthContext.Provider>
    );
};
""")

# pages/Landing.jsx
with open("src/pages/Landing.jsx", "w", encoding="utf-8") as f:
    f.write("""import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ShieldCheck, Search, FileText } from 'lucide-react';

export default function Landing() {
    return (
        <div className="min-h-screen flex flex-col">
            <header className="glass fixed w-full top-0 z-50 p-4">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <h1 className="text-2xl font-bold text-primary flex items-center gap-2">
                        <ShieldCheck className="text-accent" /> JanSeva AI
                    </h1>
                    <div className="flex gap-4">
                        <Link to="/login" className="px-4 py-2 text-primary font-medium">Login</Link>
                        <Link to="/register" className="px-4 py-2 bg-primary text-white rounded-lg font-medium shadow-md hover:bg-secondary transition">Register</Link>
                    </div>
                </div>
            </header>
            
            <main className="flex-1 mt-24">
                <section className="py-20 text-center px-4">
                    <motion.h2 
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-5xl font-extrabold text-slate-900 mb-6"
                    >
                        Enter Your Details. <br/>
                        <span className="text-primary">Discover Your Eligible Government Schemes.</span>
                    </motion.h2>
                    <motion.p 
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="text-xl text-slate-600 max-w-2xl mx-auto mb-10"
                    >
                        JanSeva AI is an intelligent assistant that helps Indian citizens discover, understand, and apply for government welfare schemes without uploading sensitive documents.
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 }}
                    >
                        <Link to="/register" className="px-8 py-4 bg-accent text-white text-lg font-bold rounded-full shadow-lg hover:shadow-xl hover:bg-emerald-600 transition">
                            Get Started for Free
                        </Link>
                    </motion.div>
                </section>

                <section className="py-20 bg-white">
                    <div className="max-w-7xl mx-auto px-4 grid md:grid-cols-3 gap-8">
                        <div className="p-8 glass rounded-2xl text-center">
                            <Search className="w-12 h-12 text-primary mx-auto mb-4" />
                            <h3 className="text-xl font-bold mb-2">Smart Eligibility Match</h3>
                            <p className="text-slate-600">Enter basic details to instantly see schemes you qualify for.</p>
                        </div>
                        <div className="p-8 glass rounded-2xl text-center">
                            <FileText className="w-12 h-12 text-accent mx-auto mb-4" />
                            <h3 className="text-xl font-bold mb-2">Simple Explanations</h3>
                            <p className="text-slate-600">Complex government rules rewritten in plain, easy-to-understand language.</p>
                        </div>
                        <div className="p-8 glass rounded-2xl text-center">
                            <ShieldCheck className="w-12 h-12 text-secondary mx-auto mb-4" />
                            <h3 className="text-xl font-bold mb-2">AI Chatbot Assistant</h3>
                            <p className="text-slate-600">Ask any questions and get answers from verified government data.</p>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
""")

# pages/Login.jsx
with open("src/pages/Login.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
    const { login } = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(email, password);
            navigate('/dashboard');
        } catch (err) {
            alert('Login failed');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="glass p-8 rounded-2xl w-full max-w-md">
                <h2 className="text-2xl font-bold text-center mb-6 text-primary">Login to JanSeva AI</h2>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <input type="email" placeholder="Email" required className="p-3 border rounded-lg" value={email} onChange={e=>setEmail(e.target.value)} />
                    <input type="password" placeholder="Password" required className="p-3 border rounded-lg" value={password} onChange={e=>setPassword(e.target.value)} />
                    <button type="submit" className="p-3 bg-primary text-white rounded-lg font-bold hover:bg-secondary">Login</button>
                </form>
                <p className="mt-4 text-center text-sm">Don't have an account? <Link to="/register" className="text-accent">Register</Link></p>
            </div>
        </div>
    );
}
""")

# pages/Register.jsx
with open("src/pages/Register.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Register() {
    const { register } = useContext(AuthContext);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(name, email, password);
            navigate('/dashboard');
        } catch (err) {
            alert('Registration failed');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <div className="glass p-8 rounded-2xl w-full max-w-md">
                <h2 className="text-2xl font-bold text-center mb-6 text-primary">Create an Account</h2>
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <input type="text" placeholder="Full Name" required className="p-3 border rounded-lg" value={name} onChange={e=>setName(e.target.value)} />
                    <input type="email" placeholder="Email" required className="p-3 border rounded-lg" value={email} onChange={e=>setEmail(e.target.value)} />
                    <input type="password" placeholder="Password" required className="p-3 border rounded-lg" value={password} onChange={e=>setPassword(e.target.value)} />
                    <button type="submit" className="p-3 bg-accent text-white rounded-lg font-bold hover:bg-emerald-600">Register</button>
                </form>
                <p className="mt-4 text-center text-sm">Already have an account? <Link to="/login" className="text-primary">Login</Link></p>
            </div>
        </div>
    );
}
""")

# pages/Dashboard.jsx
with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useContext, useEffect, useState } from 'react';
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
                const res = await axios.post('http://localhost:8000/api/recommend');
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
""")

# pages/Profile.jsx
with open("src/pages/Profile.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Profile() {
    const { user, fetchProfile } = useContext(AuthContext);
    const profile = user?.profile || {};
    const [formData, setFormData] = useState({
        age: profile.age || '',
        gender: profile.gender || '',
        state: profile.state || '',
        district: profile.district || '',
        occupation: profile.occupation || '',
        income: profile.income || '',
        category: profile.category || '',
        farmer: profile.farmer || false,
        student: profile.student || false,
        disabled: profile.disabled || false,
        widow: profile.widow || false,
        seniorCitizen: profile.seniorCitizen || false,
    });
    const navigate = useNavigate();

    const handleChange = (e) => {
        const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setFormData({ ...formData, [e.target.name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/api/profile', {
                ...formData,
                age: formData.age ? parseInt(formData.age) : null,
                income: formData.income ? parseInt(formData.income) : null,
            });
            await fetchProfile();
            alert('Profile updated successfully!');
            navigate('/dashboard');
        } catch (err) {
            alert('Error updating profile');
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-8 mt-10 bg-white rounded-xl shadow-sm border border-slate-100">
            <h2 className="text-2xl font-bold mb-6 text-primary">Edit Profile</h2>
            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-slate-700">Age</label>
                    <input type="number" name="age" value={formData.age} onChange={handleChange} className="mt-1 p-2 w-full border rounded-lg" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-700">Gender</label>
                    <select name="gender" value={formData.gender} onChange={handleChange} className="mt-1 p-2 w-full border rounded-lg">
                        <option value="">Select...</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-700">State</label>
                    <input type="text" name="state" value={formData.state} onChange={handleChange} className="mt-1 p-2 w-full border rounded-lg" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-700">Annual Income (₹)</label>
                    <input type="number" name="income" value={formData.income} onChange={handleChange} className="mt-1 p-2 w-full border rounded-lg" />
                </div>
                
                <div className="col-span-2 mt-4 flex flex-wrap gap-4">
                    <label className="flex items-center gap-2"><input type="checkbox" name="farmer" checked={formData.farmer} onChange={handleChange} /> Farmer</label>
                    <label className="flex items-center gap-2"><input type="checkbox" name="student" checked={formData.student} onChange={handleChange} /> Student</label>
                    <label className="flex items-center gap-2"><input type="checkbox" name="disabled" checked={formData.disabled} onChange={handleChange} /> Disabled</label>
                </div>
                
                <div className="col-span-2 mt-6">
                    <button type="submit" className="px-6 py-2 bg-primary text-white rounded-lg font-medium hover:bg-secondary">Save Profile</button>
                    <button type="button" onClick={() => navigate('/dashboard')} className="ml-4 px-6 py-2 bg-slate-100 text-slate-700 rounded-lg font-medium hover:bg-slate-200">Cancel</button>
                </div>
            </form>
        </div>
    );
}
""")

# components/Chatbot.jsx
with open("src/components/Chatbot.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useState } from 'react';
import axios from 'axios';
import { X, Send, Loader } from 'lucide-react';

export default function Chatbot({ close }) {
    const [messages, setMessages] = useState([{ sender: 'bot', text: "Hello! I am JanSeva AI. Ask me anything about government schemes." }]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim()) return;
        
        const userMsg = input;
        setMessages([...messages, { sender: 'user', text: userMsg }]);
        setInput("");
        setLoading(true);

        try {
            const res = await axios.post('http://localhost:8000/api/chat', { question: userMsg });
            setMessages(prev => [...prev, { sender: 'bot', text: res.data.answer }]);
        } catch (err) {
            setMessages(prev => [...prev, { sender: 'bot', text: "Sorry, I am having trouble connecting to the server." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed bottom-24 right-6 w-80 md:w-96 bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col z-50 h-[500px]">
            <div className="bg-primary text-white p-4 flex justify-between items-center">
                <h3 className="font-bold">JanSeva AI Assistant</h3>
                <button onClick={close} className="hover:text-slate-200"><X size={20}/></button>
            </div>
            <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3 bg-slate-50">
                {messages.map((m, i) => (
                    <div key={i} className={`p-3 max-w-[85%] rounded-xl text-sm ${m.sender === 'user' ? 'bg-primary text-white self-end rounded-br-sm' : 'bg-white border text-slate-800 self-start rounded-bl-sm'}`}>
                        {m.text}
                    </div>
                ))}
                {loading && (
                    <div className="p-3 max-w-[85%] rounded-xl text-sm bg-white border text-slate-800 self-start rounded-bl-sm flex gap-2 items-center">
                        <Loader size={14} className="animate-spin text-primary" /> Typing...
                    </div>
                )}
            </div>
            <div className="p-3 bg-white border-t flex gap-2">
                <input 
                    type="text" 
                    className="flex-1 border rounded-full px-4 py-2 text-sm focus:outline-none focus:border-primary" 
                    placeholder="Ask a question..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                />
                <button onClick={handleSend} className="w-10 h-10 bg-primary text-white rounded-full flex items-center justify-center hover:bg-secondary"><Send size={16}/></button>
            </div>
        </div>
    );
}
""")

# App.jsx
with open("src/App.jsx", "w", encoding="utf-8") as f:
    f.write("""import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';

const PrivateRoute = ({ children }) => {
    const { user, loading } = useContext(AuthContext);
    if (loading) return <div>Loading...</div>;
    return user ? children : <Navigate to="/login" />;
};

function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
            <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
        </Routes>
    );
}

export default function App() {
    return (
        <AuthProvider>
            <Router>
                <AppRoutes />
            </Router>
        </AuthProvider>
    );
}
""")

# main.jsx
with open("src/main.jsx", "w", encoding="utf-8") as f:
    f.write("""import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
""")
