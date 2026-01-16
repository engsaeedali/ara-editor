"use client";

import { useState, useRef } from "react";
import { Send, BookOpen, Shield, Paperclip, Copy, Check, Clipboard, Download, RefreshCw, ArrowLeft, Cpu } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    tokenUsage?: {
        input_tokens?: number;
        output_tokens?: number;
        total_tokens?: number;
    };
}

interface MetricScores {
    strictness: number;
    majesty: number;
    superiority: number;
}

interface Violation {
    type: string;
    text: string;
    suggestion: string;
}

interface AnalysisResult {
    manuscript: string;
    editor_notes: string[];
    metric_scores: MetricScores;
    violations: Violation[];
}

export default function SovereignChat() {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [copiedId, setCopiedId] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Calculate total tokens
    const totalTokens = messages.reduce((acc, msg) => acc + (msg.tokenUsage?.total_tokens || 0), 0);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg: Message = { id: Date.now().toString(), role: "user", content: input };
        setMessages((prev) => [...prev, userMsg]);
        setInput("");
        setLoading(true);

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMsg.content }),
            });
            const data = await res.json();


            const assistantMsg: Message = {
                id: (Date.now() + 1).toString(),
                role: "assistant",
                content: data.manuscript,
                tokenUsage: data.token_usage
            };
            setMessages((prev) => [...prev, assistantMsg]);

        } catch (error: any) {
            console.error("Error:", error);
            const errorText = error.message || "عذراً، حدث خطأ في الاتصال بالمهندس السيادي.";
            const errorMsg: Message = { id: Date.now().toString(), role: "assistant", content: `❌ ${errorText}` };
            setMessages((prev) => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    };

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // Reset input so same file can be selected again
        e.target.value = "";

        const userMsg: Message = { id: Date.now().toString(), role: "user", content: `📎 جاري تحليل الملف: ${file.name}...` };
        setMessages((prev) => [...prev, userMsg]);
        setLoading(true);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/upload`, {
                method: "POST",
                body: formData,
            });

            if (!res.ok) throw new Error("Upload failed");

            const data = await res.json();

            const assistantMsg: Message = {
                id: (Date.now() + 1).toString(),
                role: "assistant",
                content: data.manuscript,
                tokenUsage: data.token_usage
            };
            setMessages((prev) => [...prev, assistantMsg]);

        } catch (error: any) {
            console.error("Error:", error);
            const errorText = error.message || "عذراً، حدث خطأ داخلي في النظام.";
            const errorMsg: Message = { id: Date.now().toString(), role: "assistant", content: `❌ ${errorText}` };
            setMessages((prev) => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = async (text: string, id: string) => {
        try {
            await navigator.clipboard.writeText(text);
            setCopiedId(id);
            setTimeout(() => setCopiedId(null), 2000);
        } catch (err) {
            console.error("Failed to copy:", err);
        }
    };

    const pasteFromClipboard = async () => {
        try {
            const text = await navigator.clipboard.readText();
            setInput((prev) => prev + text);
        } catch (err) {
            console.error("Failed to paste:", err);
        }
    };

    const handleDownload = (content: string, id: string) => {
        const element = document.createElement("a");
        const file = new Blob([content], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = `sovereign_output_${id}.txt`;
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();
        document.body.removeChild(element);
    }

    const handleNewChat = () => {
        if (window.confirm("هل أنت متأكد من بدء جلسة جديدة؟ سيتم مسح المحادثة الحالية.")) {
            setMessages([]);
            setInput("");
            setCopiedId(null);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-[#0a0a0a] text-[#e5e5e5] font-sans selection:bg-[#d4af37] selection:text-black" dir="rtl">
            <header className="p-6 border-b border-[#333] flex items-center justify-between bg-[#0a0a0a]/90 backdrop-blur z-50">
                <h1 className="text-xl font-bold tracking-widest uppercase text-[#d4af37]">
                    مساعد التحرير
                </h1>

                <div className="flex items-center gap-6">
                    {/* Token Counter */}
                    <div className="flex items-center gap-2 text-xs font-mono text-[#d4af37]/70 bg-[#d4af37]/10 px-3 py-1 rounded-full border border-[#d4af37]/20">
                        <Cpu size={14} />
                        <span>{totalTokens.toLocaleString()} TKN</span>
                    </div>

                    <button
                        onClick={handleNewChat}
                        className="flex items-center gap-2 text-sm text-gray-400 hover:text-red-400 transition-colors"
                        title="بدء جلسة جديدة"
                    >
                        <RefreshCw size={16} />
                        <span className="hidden md:inline">جلسة جديدة</span>
                    </button>

                    <div className="flex items-center gap-2 text-xs text-gray-500 border-r border-[#333] pr-6">
                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                        <span>متصل</span>
                    </div>
                </div>
            </header>

            <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-8 max-w-5xl mx-auto w-full">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-64 text-gray-600 opacity-50">
                        <BookOpen size={64} className="mb-4" />
                        <p>ابدأ بكتابة النص أو ارفع ملف لمعالجته...</p>
                    </div>
                )}

                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={cn(
                            "p-6 rounded-lg leading-loose shadow-xl text-lg relative group",
                            msg.role === "user"
                                ? "bg-[#1a1a1a] mr-auto max-w-[80%] border border-[#333] text-right"
                                : "bg-[#111] w-full border border-[#d4af37]/20 text-right border-r-4 border-r-[#d4af37]"
                        )}
                    >
                        {msg.role === "assistant" && (
                            <>
                                <div className="absolute top-2 right-4 text-xs text-[#d4af37]/50 flex items-center gap-1">
                                    <Shield size={10} />
                                    النص بعد التحرير
                                </div>
                                <div className="absolute top-2 left-2 flex gap-2">
                                    <button
                                        onClick={() => handleDownload(msg.content, msg.id)}
                                        className="p-1 text-gray-500 hover:text-[#d4af37] transition-colors"
                                        title="تصدير (تحميل)"
                                    >
                                        <Download size={16} />
                                    </button>
                                    <button
                                        onClick={() => copyToClipboard(msg.content, msg.id)}
                                        className="p-1 text-gray-500 hover:text-[#d4af37] transition-colors"
                                        title="نسخ النص"
                                    >
                                        {copiedId === msg.id ? <Check size={16} /> : <Copy size={16} />}
                                    </button>
                                </div>
                            </>
                        )}
                        <div className="whitespace-pre-wrap pt-6">{msg.content}</div>
                        {msg.role === "assistant" && (
                            <div className="mt-6 pt-4 border-t border-[#333]/50 flex justify-end gap-3 opacity-50 hover:opacity-100 transition-opacity flex-wrap items-center">
                                {/* Token Usage Stats */}
                                {msg.tokenUsage && (
                                    <div className="flex items-center gap-3 text-[10px] text-gray-600 font-mono ml-auto bg-black/30 px-2 py-1 rounded">
                                        <span>IN: {msg.tokenUsage.input_tokens}</span>
                                        <span>OUT: {msg.tokenUsage.output_tokens}</span>
                                        <span className="text-[#d4af37]">TOT: {msg.tokenUsage.total_tokens}</span>
                                    </div>
                                )}

                                <div className="flex gap-3">
                                    <button
                                        onClick={() => handleDownload(msg.content, msg.id)}
                                        className="flex items-center gap-1 text-sm text-gray-500 hover:text-[#d4af37] transition-colors"
                                        title="تصدير (تحميل)"
                                    >
                                        <Download size={14} />
                                        <span>تحميل</span>
                                    </button>
                                    <button
                                        onClick={() => copyToClipboard(msg.content, msg.id)}
                                        className="flex items-center gap-1 text-sm text-gray-500 hover:text-[#d4af37] transition-colors"
                                        title="نسخ النص"
                                    >
                                        {copiedId === msg.id ? <Check size={14} /> : <Copy size={14} />}
                                        <span>نسخ</span>
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                ))}
                {loading && (
                    <div className="flex items-center justify-center gap-3 text-[#d4af37] animate-pulse py-8">
                        <span className="w-2 h-2 bg-[#d4af37] rounded-full"></span>
                        <span className="w-2 h-2 bg-[#d4af37] rounded-full animation-delay-200"></span>
                        <span className="w-2 h-2 bg-[#d4af37] rounded-full animation-delay-400"></span>
                    </div>
                )}
            </div>

            <form onSubmit={handleSubmit} className="p-4 md:p-6 border-t border-[#333] bg-[#0a0a0a] max-w-5xl mx-auto w-full">
                <div className="relative flex items-center gap-2">
                    {/* File Upload Button */}
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileSelect}
                        accept=".docx"
                        className="hidden"
                    />
                    <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        disabled={loading}
                        className="p-4 bg-[#111] border border-[#333] rounded-md text-gray-400 hover:text-[#d4af37] transition-all"
                        title="إرفاق ملف Word"
                    >
                        <Paperclip size={20} />
                    </button>

                    <button
                        type="button"
                        onClick={pasteFromClipboard}
                        disabled={loading}
                        className="p-4 bg-[#111] border border-[#333] rounded-md text-gray-400 hover:text-[#d4af37] transition-all"
                        title="لصق من الحافظة"
                    >
                        <Clipboard size={20} />
                    </button>

                    <div className="relative flex-1">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="أدخل النص للتحرير..."
                            className="w-full bg-[#111] border border-[#333] rounded-md py-4 px-6 pl-12 focus:outline-none focus:border-[#d4af37] transition-all placeholder:text-gray-600 text-right text-lg shadow-inner"
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="absolute left-4 top-1/2 -translate-y-1/2 text-[#d4af37] hover:text-white transition-colors"
                        >
                            <ArrowLeft size={24} />
                        </button>
                    </div>
                </div>
            </form>
        </div>
    );
}
