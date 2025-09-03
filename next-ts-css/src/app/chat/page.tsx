"use client";

import { useEffect, useRef, useState } from "react";
import ChatBubble from "@/components/ChatBubble";
import ChatInput from "@/components/ChatInput";

type Msg = { id: string; role: "user" | "assistant"; content: string; at: number };

export default function ChatPage() {
  const [msgs, setMsgs] = useState<Msg[]>(() => [
  ]);
  const [pending, setPending] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  // 새 메시지마다 자동 스크롤
  useEffect(() => {
    const el = listRef.current;
    if (!el) return;
    const raf = requestAnimationFrame(() =>
      el.scrollTo({ top: el.scrollHeight, behavior: "smooth" }),
    );
    return () => cancelAnimationFrame(raf);
  }, [msgs, pending]);


  const onSend = async (raw: string) => {
    const text = raw.trim();
    if (!text || pending) return;

    const user: Msg = { id: crypto.randomUUID(), role: "user", content: text, at: Date.now() };
    setMsgs((m) => [...m, user]);
    setPending(true);
    try {
        const url = new URL("http://localhost:8001/chat");
        url.search = new URLSearchParams({ query: text }).toString(); 

        const res = await fetch(url.toString(), {
        method: "POST",
        headers: { accept: "application/json" }, 
        cache: "no-store",
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json(); 

        const reply: string =
            typeof data === "string"
                ? data
                : JSON.stringify(data); 
        setMsgs(m => [...m, { id: crypto.randomUUID(), role: "assistant", content: reply, at: Date.now() }]);
    } catch {
        setMsgs(m => [...m, { id: crypto.randomUUID(), role: "assistant", content: "오류가 발생했어요.", at: Date.now() }]);
    } finally {
        setPending(false);
    }
    };
   
    abortRef.current?.abort();
    const ac = new AbortController();
    abortRef.current = ac;


  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col bg-gray-50">
      {/* 상단바 */}
      <header className="sticky top-0 z-10 border-b bg-white/90 backdrop-blur p-4">
        <h1 className="text-lg font-semibold">Chat</h1>
      </header>

      {/* 메시지 리스트 */}
      <div
        ref={listRef}
        className="flex-1 overflow-y-auto p-4 space-y-3"
        aria-live="polite"
        aria-relevant="additions"
      >
        {msgs.map((m) => (
          <ChatBubble key={m.id} role={m.role} text={m.content} time={new Date(m.at).toLocaleTimeString()} />
        ))}

        {/* 타이핑 인디케이터 */}
        {pending && (
          <div className="flex justify-start">
            <div className="rounded-2xl border border-gray-100 bg-white px-4 py-2 text-gray-500 shadow">
              <span className="inline-flex items-center gap-2">
                <span className="relative flex h-2 w-2">
                  <span className="absolute h-full w-full animate-ping rounded-full bg-gray-400 opacity-75" />
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-gray-400" />
                </span>
                작성 중…
              </span>
            </div>
          </div>
        )}
      </div>

      {/* 입력바 */}
      <ChatInput onSend={onSend} disabled={pending} />
    </main>
  );
}
