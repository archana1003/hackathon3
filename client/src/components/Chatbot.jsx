import React, { useState } from 'react';
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
            const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/chat`, { question: userMsg });
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
