import React, { useState, useContext } from 'react';
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
