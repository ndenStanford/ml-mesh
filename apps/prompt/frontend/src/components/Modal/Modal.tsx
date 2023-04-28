import React from "react";
import { ModalProps } from "@/src/types";
import styles from "./modal.module.scss";
import { ReactComponent as CloseIcon } from "../../icons/close.svg";

export default class Modal extends React.Component<ModalProps, any> {
  render() {
    return (
      <>
        <div className={styles["modal-mask"]}>
          <div className={styles["modal-container"]}>
            <div className={styles["modal-header"]}>
              <div className={styles["modal-title"]}>{this.props.title}</div>
              <div
                className={styles["modal-close-btn"]}
                onClick={this.props.onClose}
              >
                <CloseIcon />
              </div>
            </div>
            <div className={styles["modal-content"]}>{this.props.children}</div>
            <div className={styles["modal-footer"]}>
              <div className={styles["modal-actions"]}>
                {this.props.actions?.map((action, i) => (
                  <div key={i} className={styles["modal-action"]}>
                    {action}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }
}
