import React from "react";
import styles from "./prompt-list.module.scss";

export default class PromptList extends React.Component<any, any> {
  render() {
    return <div className={styles["prompt-list"]}>{this.props.children}</div>;
  }
}
