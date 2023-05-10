import React, { useRef, useLayoutEffect, useState } from "react";
import styles from "./chat-message.module.scss";
import { ChatMessageProps } from "@/src/types";
import { ChatMessageContent } from "../ChatMessageContent";

function useScrollToBottom() {
  // for auto-scroll
  const scrollRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const scrollToBottom = () => {
    const dom = scrollRef.current;
    if (dom) {
      setTimeout(() => (dom.scrollTop = dom.scrollHeight), 1);
    }
  };

  // auto scroll
  useLayoutEffect(() => {
    autoScroll && scrollToBottom();
  });

  return {
    scrollRef,
    autoScroll,
    setAutoScroll,
    scrollToBottom,
  };
}

export default function ChatMessage(props: ChatMessageProps) {
  const { scrollRef, setAutoScroll, scrollToBottom } = useScrollToBottom();

  return (
    <div
      className={
        props.message.isUser
          ? styles["chat-message-user"]
          : styles["chat-message"]
      }
    >
      <div className={styles["chat-message-container"]}>
        {props.message.isLoading && (
          <div className={styles["chat-message-status"]}>Loading...</div>
        )}
        <div className={styles["chat-message-item"]}>
          <ChatMessageContent message={props.message} parentRef={scrollRef} />
        </div>
        <div className={styles["chat-message-actions"]}>
          <div className={styles["chat-message-action-date"]}>
            {props.message.date}
          </div>
        </div>
      </div>
    </div>
  );
}
