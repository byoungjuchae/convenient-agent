"use client";

import { useState } from "react";



export default function ChatPractice(){

    const [value, setValue] = useState("");

    return (
        <div className="mx-h"> 
            <form onSubmit={(e) => {
                e.preventDefault();
                console.log(value);
            }}>
                <h1>Chat</h1>
            </form>
        </div>
    );
}