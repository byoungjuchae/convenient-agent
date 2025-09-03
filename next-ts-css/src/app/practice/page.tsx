"use client";

import {useState, useEffect, useRef} from 'react';

type Msg = { id: string; role: "user" | "assistant"; content: string; at: number };
export default function Practice(){

    const [valInput,setInput] = useState(0)
    const [valbool,setBool] = useState(false)
    const [pending, setPending] = useState(false)
    const listRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const el = listRef.current;
        if (!el) return;
        const raf = requestAnimationFrame(() =>
            el.scrollTo({ top: el.scrollHeight, behavior: "smooth"}),
        );
        return () => cancelAnimationFrame(raf);
    })


    const onSend = async (raw:string) => {
        const text = raw.trim();

        if(!text || pending) return;
        const user: Msg = { id: crypto.randomUUID(), role: "user", content: text, at: Date.now()};


    };

    return (
        <main className= "mx-auto flex min-h-screen max-w-3xl flex-col bg-gray-50">
            <header className="sticky top-0 z-10 border-b bg-white/90 backdrop-blur p-4">
                <h1 className="text-lg font-semibold"> Chat</h1>
            </header>
            <div
            onSend={onSend}
            >   </div>
        </main>
    );
}