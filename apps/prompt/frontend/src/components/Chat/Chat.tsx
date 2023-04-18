import React from "react";
import styles from "./chat.module.scss";
import { Button } from "../Button";
import { Theme } from "../../constants";
import { GlobalState } from "@/src/types";
import { ReactComponent as LightIcon } from "../../icons/light.svg";
import { ReactComponent as AutoIcon } from "../../icons/auto.svg";
import { ReactComponent as DarkIcon } from "../../icons/dark.svg";
import { ReactComponent as SendWhiteIcon } from "../../icons/send-white.svg";
import { useDispatch } from "react-redux";
import { switchTheme } from "../../state/slices/app";

export default function Chat(props: { state: GlobalState }) {
  const dispatch = useDispatch();
  const handleSwitchTheme = (e: any) => {
    dispatch(switchTheme(e.target.value));
  };

  return (
    <div className={styles["window-content"]}>
      <div className={styles["chat"]}>
        <div className={styles["window-header"]}>
          <div className={styles["window-header-title"]}>
            <div
              className={`${styles["window-header-main-title"]} ${styles["chat-body-title"]}`}
            >
              Chat
            </div>
            <div className={styles["window-header-sub-title"]}>
              Send messages with prompt templates.
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
        <div className={styles["chat-body"]}></div>
        <div className={styles["chat-input-panel"]}>
          <div className={styles["chat-input-panel-inner"]}>
            <textarea className={styles["chat-input"]} />
            <Button
              icon={<SendWhiteIcon />}
              text={`Send`}
              className={styles["chat-input-send"]}
              noDark
            />
          </div>
        </div>
      </div>
    </div>
  );
}
