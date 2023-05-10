import React from "react";
import { ErrorBoundary } from "../ErrorBoundary";
import styles from "./layout.module.scss";
import { LayoutProps } from "@/src/types";
import { setTheme } from "../../utils";

export class Layout extends React.Component<LayoutProps, any> {
  constructor(props: LayoutProps) {
    const theme = props.state.theme;
    setTheme(theme);
    super(props);
  }

  render() {
    return (
      <ErrorBoundary>
        <div className={styles["container"]}>{this.props.children}</div>
      </ErrorBoundary>
    );
  }
}
