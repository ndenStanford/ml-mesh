import React from "react";
import { PromptListItemProps } from "@/src/types";
import styles from "./prompt-list-item.module.scss";
import { ReactComponent as DeleteIcon } from "../../icons/delete.svg";
import { PromptToast } from "../PromptToast";

export default function PromptListItem(
  item: PromptListItemProps,
  showToast: boolean,
  hideModal?: () => void
) {
  return (
    <div
      className={`${styles["prompt-list-item"]} ${
        item.selected && styles["prompt-list-item-selected"]
      }`}
      onClick={item.onClick}
    >
      <div className={styles["prompt-list-item-alias"]}>{item.alias}</div>
      <div className={styles["prompt-list-item-info"]}>
        <div className={styles["prompt-list-item-template"]}>
          {item.template}
        </div>
        <div className={styles["prompt-list-item-date"]}>{item.created_at}</div>
      </div>
      <div
        className={styles["prompt-list-item-delete"]}
        onClick={item.onDelete}
      >
        <DeleteIcon />
      </div>
      {/* {showModal && (
        <PromptToast
          prompt={item}
          onClose={() => hideModal()}
          onUpdatePrompt={handleUpdate}
        />
      )} */}
    </div>
  );
}
