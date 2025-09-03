"use client";
import { useState } from "react";

export default function ChatInput({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void;
  disabled?: boolean;
}) {
  const [text, setText] = useState("");

  const send = () => {
    const t = text.trim();
    if (!t || disabled) return;
    onSend(t);
    setText("");
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        send();
      }}
      className="border-t bg-white p-2"
      aria-label="메시지 입력 영역"
    >
      <div className="flex items-end gap-2">
        <textarea
          className="max-h-40 min-h-[44px] flex-1 resize-y rounded-xl border border-gray-200 bg-white px-3 py-2 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-200"
          placeholder="메시지 입력… (Shift+Enter 줄바꿈)"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            // 한글 조합 중 전송 방지
            // @ts-ignore
            if (e.isComposing) return;
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send();
            }
          }}
          disabled={disabled}
          aria-label="메시지 입력"
        />
        <button
          type="submit"
          className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2 text-white shadow transition hover:brightness-110 disabled:opacity-50"
          disabled={disabled || text.trim().length === 0}
          aria-label="메시지 보내기"
          title="보내기"
        >
          {/* 종이비행기 아이콘 (SVG) */}
          <svg viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor" aria-hidden>
            <path d="M2 21l20-9L2 3v7l14 2-14 2v7z" />
          </svg>
          보내기
        </button>
      </div>
    </form>
  );
}
