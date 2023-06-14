import React, { useState } from "react";
import styles from "./chat.module.scss";
import { Button } from "../Button";
import { Theme } from "../../constants";
import { ChatProps, Message } from "@/src/types";
import { ReactComponent as LightIcon } from "../../icons/light.svg";
import { ReactComponent as AutoIcon } from "../../icons/auto.svg";
import { ReactComponent as DarkIcon } from "../../icons/dark.svg";
import { ReactComponent as SendWhiteIcon } from "../../icons/send-white.svg";
import { ReactComponent as ClearIcon } from "../../icons/clear.svg";
import { useDispatch } from "react-redux";
import { switchTheme } from "../../state/slices/app";
import { ChatMessage } from "../ChatMessage";

export default function Chat(props: ChatProps) {
  const dispatch = useDispatch();
  const handleSwitchTheme = (e: any) => {
    dispatch(switchTheme(e.target.value));
  };
  const [value, setValue] = useState("");

  const handleSendMessage = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (value.trim() !== "") {
      props.onChatSendClick?.(value);
      setValue("");
    }
  };

  return (
    <div className={styles["window-content"]}>
      <div className={styles["chat"]}>
        <div className={styles["window-header"]}>
          <div className={styles["window-header-title"]}>
            <div
              className={`${styles["window-header-main-title"]} ${styles["chat-body-title"]}`}
            >
              {props.header}
            </div>
            <div className={styles["window-header-sub-title"]}>
              {props.subtitle}
            </div>
          </div>
          <div className={styles["window-actions"]}>
            <div className={styles["window-action-button"]}>
              <Button
                icon={
                  props.state.app.theme === Theme.AUTO ? (
                    <AutoIcon />
                  ) : props.state.app.theme === Theme.LIGHT ? (
                    <LightIcon />
                  ) : props.state.app.theme === Theme.DARK ? (
                    <DarkIcon />
                  ) : (
                    <AutoIcon />
                  )
                }
                onClick={handleSwitchTheme}
              />
            </div>
          </div>
        </div>
        <div className={styles["chat-body"]}>
          {Object.values(props.state.chat.messages).map((message: Message) => (
            <ChatMessage message={message} />
          ))}
        </div>
        <div className={styles["chat-input-panel"]}>
          <div className={styles["chat-input-actions"]}>
            <div className={`${styles["chat-input-action"]} clickable`}>
              <ClearIcon onClick={props.onChatActionClick} />
            </div>
          </div>
          <div>
            <form
              onSubmit={handleSendMessage}
              className={styles["chat-input-panel-inner"]}
            >
              <input
                className={styles["chat-input"]}
                type="text"
                value={value}
                onChange={(e) => setValue(e.target.value)}
              />
              <Button
                className={styles["chat-input-send"]}
                icon={<SendWhiteIcon />}
                noDark
              />
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
