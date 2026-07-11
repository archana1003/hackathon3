import React from 'react';
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
