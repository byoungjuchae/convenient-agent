type Props = { role: "user" | "assistant"; text: string; time?: string };

export default function ChatBubble({ role, text, time }: Props) {
  const me = role === "user";
  return (
    <div className={`flex ${me ? "justify-end" : "justify-start"}`}>
      <div className={`flex items-end gap-2 ${me ? "flex-row-reverse" : ""}`}>
        {/* 아바타 */}
        <div
          className={`grid h-8 w-8 place-items-center rounded-full text-xs font-semibold shadow
            ${me ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-700"}`}
          aria-hidden
        >
          {me ? "U" : "A"}
        </div>

        {/* 말풍선 */}
        <div
          className={[
            "relative max-w-[78%] whitespace-pre-wrap break-words rounded-2xl px-4 py-2 shadow",
            me
              ? "bg-gradient-to-br from-blue-600 to-blue-500 text-white rounded-br-sm"
              : "bg-white text-gray-900 rounded-bl-sm border border-gray-100",
          ].join(" ")}
          role="group"
          aria-label={me ? "내 메시지" : "어시스턴트 메시지"}
        >
          <p>{text}</p>
          {time && <span className={`mt-1 block text-[11px] opacity-70 ${me ? "text-blue-100" : "text-gray-500"}`}>{time}</span>}

          {/* 말풍선 꼬리 */}
          <span
            className={[
              "absolute -bottom-1 h-3 w-3 rotate-45",
              me ? "right-2 bg-blue-600" : "left-2 bg-white border-b border-l border-gray-100",
            ].join(" ")}
            aria-hidden
          />
        </div>
      </div>
    </div>
  );
}
