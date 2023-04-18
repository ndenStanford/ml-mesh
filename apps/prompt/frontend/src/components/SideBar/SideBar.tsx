import React from "react";
import styles from "./side-bar.module.scss";
import { Button } from "../Button";
import { ReactComponent as AddIcon } from "../../icons/add.svg";

export default class SideBar extends React.Component<any, any> {
  render() {
    return (
      <div className={styles["sidebar"]}>
        <div className={styles["sidebar-header"]}>
          <div className={styles["sidebar-title"]}>
            Onclusive Machine Learning
          </div>
          <div className={styles["sidebar-sub-title"]}>Prompt Manager.</div>
        </div>
        <div className={styles["sidebar-body"]}>{this.props.children}</div>
        <div className={styles["sidebar-tail"]}>
          <div className={styles["sidebar-actions"]}>
            <div className={styles["sidebar-action"]}>
              <Button icon={<AddIcon />} text="New Prompt" />
            </div>
          </div>
        </div>
        <div className={styles["sidebar-drag"]}></div>
      </div>
    );
  }
}
