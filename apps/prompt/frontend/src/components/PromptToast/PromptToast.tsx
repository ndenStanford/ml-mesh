import React from "react";
import styles from "./prompt-modal.module.scss";
import { ToastProps } from "@/src/types";

export default function PromptToast(props: ToastProps) {
  return (
    <div className={styles["prompt-toast-container"]}>
      <div className={styles["prompt-toast-content"]}>
        <span>{props.content}</span>
        {props.action && (
          <button
            onClick={props.action.onClick}
            className={styles["prompt-toast-action"]}
          >
            {props.action.text}
          </button>
        )}
      </div>
    </div>
  );
}
