import React from "react";
import styles from "./chat-message.module.scss";
import { ChatMessageProps } from "@/src/types";

export default function ChatMessage(props: ChatMessageProps) {
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
          <div className={styles["chat-message-status"]}>Loading..</div>
        )}
      </div>
      <ChatMessageContent
        content={props.message.content}
        loading={props.message.isLoading}
        parentRef={scrollRef}
      />
    </div>
  );
}
