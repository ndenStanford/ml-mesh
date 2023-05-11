import React, { useState } from "react";
import { PromptListItemProps, Dictionary } from "@/src/types";
import styles from "./prompt-list-item.module.scss";
import { ReactComponent as DeleteIcon } from "../../icons/delete.svg";
import { Button } from "../Button";
import { Modal } from "../Modal";
import { formatDate } from "../../utils";

export default function PromptListItem(props: {
  item: PromptListItemProps;
  isModalVisible: boolean;
  hideModal: any;
}) {
  const [dictionary, setDictionary] = useState<Dictionary>({});

  const handleTextareaChange = (key: string, value: string) => {
    setDictionary((prevDictionary) => ({
      ...prevDictionary,
      [key]: value,
    }));
  };

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
          <div className={styles["prompt-list-item-date"]}>
            {formatDate(props.item.created_at)}
          </div>
        </div>
      </div>
      {props.isModalVisible && (
        <Modal
          title={"Replace variables values."}
          actions={[
            <div className={styles["buttons"]}>
              <div className={styles["prompt-buttons"]}>
                <Button
                  key="send"
                  text={"Send"}
                  onClick={() => {
                    props.hideModal();
                    props.item.onSendClick(dictionary, props.item.id);
                  }}
                />
                ,
                <Button
                  key="send"
                  icon={<DeleteIcon />}
                  text={"Delete"}
                  onClick={() => {
                    props.hideModal();
                    props.item.onDeleteClick(props.item.id);
                  }}
                />
              </div>
            </div>,
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
                  id={variable}
                  value={dictionary[variable] || ""}
                  onChange={(e) =>
                    handleTextareaChange(variable, e.target.value)
                  }
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
