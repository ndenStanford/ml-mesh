import React from "react";
import { PromptListItemProps } from "@/src/types";
import styles from "./prompt-list-item.module.scss";
import { ReactComponent as DeleteIcon } from "../../icons/delete.svg";

export default function PromptItem(props: PromptListItemProps) {
  return (
    <div
      className={`${styles["prompt-list-item"]} ${
        props.selected && styles["prompt-list-item-selected"]
      }`}
      onClick={props.onClick}
    >
      <div className={styles["prompt-list-item-alias"]}>{props.alias}</div>
      <div className={styles["prompt-list-item-info"]}>
        <div className={styles["prompt-list-item-template"]}>
          {props.template}
        </div>
        <div className={styles["prompt-list-item-date"]}>
          {props.created_at}
        </div>
      </div>
      <div
        className={styles["prompt-list-item-delete"]}
        onClick={props.onDelete}
      >
        <DeleteIcon />
      </div>
    </div>
  );
}
