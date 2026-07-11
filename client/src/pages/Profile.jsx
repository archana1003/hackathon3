import React, { useContext, useState } from 'react';
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
