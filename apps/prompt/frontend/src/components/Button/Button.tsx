import * as React from "react";

import styles from "./button.module.scss";
import { ButtonProps } from "@/src/types";

export default function Button(props: ButtonProps) {
  return (
    <button
      className={styles["icon-button"] + ` ${props.className ?? ""} clickable`}
      onClick={props.onClick}
      title={props.title}
      disabled={props.disabled}
      role="button"
    >
      {props.icon && (
        <div
          className={
            styles["icon-button-icon"] + ` ${props.noDark && "no-dark"}`
          }
        >
          {props.icon}
        </div>
      )}
      {props.text && (
        <div className={styles["icon-button-text"]}>{props.text}</div>
      )}
    </button>
  );
}
