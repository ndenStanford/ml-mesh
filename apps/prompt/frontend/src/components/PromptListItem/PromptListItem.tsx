import React from "react";
import { PromptListItemProps } from "@/src/types";
import styles from "./prompt-list-item.module.scss";
import { ReactComponent as DeleteIcon } from "../../icons/delete.svg";
import { Button } from "../Button";
import { Modal } from "../Modal";

export default function PromptListItem(props: {
  item: PromptListItemProps;
  isModalVisible: boolean;
  hideModal: any;
}) {
  return (
    <>
      <div
        className={`${styles["prompt-list-item"]} ${
          props.item.selected && styles["prompt-list-item-selected"]
        }`}
        onClick={props.item.onClick}
      >
        <div className={styles["prompt-list-item-alias"]}>
          {props.item.alias}
        </div>
        <div className={styles["prompt-list-item-info"]}>
          <div className={styles["prompt-list-item-template"]}>
            {props.item.template}
          </div>
        </div>
      </div>
      {props.isModalVisible && (
        <Modal
          title={"Replace variables values."}
          actions={[
            <Button key="send" text={"Send"} onClick={props.hideModal} />,
          ]}
          onClose={props.hideModal}
        >
          <div className={styles["context-prompt"]}>
            <div className={styles["context-prompt-row"]}>
              <div className={styles["context-prompt-header"]}>
                <span>Prompt Template</span>
                <div>{props.item.template}</div>
              </div>
            </div>
            {props.item.variables.map((variable, index) => (
              <div className={styles["context-prompt-row"]}>
                <div className={styles["context-role"]} key={index}>
                  <label>{variable}</label>
                </div>
                <textarea
                  rows={1}
                  className={styles["context-input"]}
                ></textarea>
              </div>
            ))}
          </div>
        </Modal>
      )}
    </>
  );
}
