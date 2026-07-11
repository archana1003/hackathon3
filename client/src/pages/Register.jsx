import React, { useState, useContext } from 'react';
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
