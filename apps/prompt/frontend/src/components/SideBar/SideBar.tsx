import React from "react";
import styles from "./side-bar.module.scss";
import { Button } from "../Button";
import { Modal } from "../Modal";
import { ReactComponent as AddIcon } from "../../icons/add.svg";
import { ReactComponent as SettingsIcon } from "../../icons/settings.svg";
import { SidebarProps } from "@/src/types";

export default class SideBar extends React.Component<SidebarProps, any> {
  constructor(props: SidebarProps) {
    super(props);
    this.state = {
      textAreaValue: "",
      textAliasValue: "",
    };
  }

  handleTextAreaChange = (event: any) => {
    this.setState({ textAreaValue: event.target.value });
  };
  handleTextAliasChange = (event: any) => {
    this.setState({ textAliasValue: event.target.value });
  };

  render() {
    return (
      <>
        <div className={styles["sidebar"]}>
          <div className={styles["sidebar-header"]}>
            <div className={styles["sidebar-title"]}>{this.props.title}</div>
            <div className={styles["sidebar-sub-title"]}>
              {this.props.subtitle}
            </div>
          </div>
          <div className={styles["sidebar-body"]}>{this.props.children}</div>
          <div className={styles["sidebar-tail"]}>
            <div className={styles["sidebar-actions"]}>
              <div className={styles["sidebar-action"]}>
                <Button
                  icon={<AddIcon />}
                  text="New Prompt"
                  onClick={this.props.onActionClick}
                />
                <Button
                  icon={<SettingsIcon />}
                  text="Settings"
                  onClick={this.props.onSettingsClick}
                />
              </div>
            </div>
          </div>
          <div className={styles["sidebar-drag"]}></div>
        </div>
        {this.props.isNewPromptModalVisible && (
          <Modal
            title={"Create new Prompt."}
            actions={[
              <Button
                key="send"
                text={"Save"}
                onClick={() => {
                  if (
                    !(
                      this.state.textAreaValue === "" ||
                      this.state.textAliasValue == ""
                    )
                  )
                    this.props.onModalActionClick?.(
                      this.state.textAreaValue,
                      this.state.textAliasValue
                    );
                  this.props.hideModal();
                }}
              />,
            ]}
            onClose={this.props.hideModal}
          >
            <div className={styles["context-prompt"]}>
              <div className={styles["context-prompt-row"]}>
                <div className={styles["context-prompt-header"]}>
                  <span>New Prompt Template</span>
                  <div>
                    Please enter the template text and a unique alias for the
                    template:
                  </div>
                </div>
              </div>

              <div className={styles["context-prompt-row"]}>
                <div className={styles["context-role"]}>
                  <label>Template</label>
                </div>
                <textarea
                  rows={1}
                  className={styles["context-input"]}
                  onChange={this.handleTextAreaChange}
                ></textarea>
              </div>

              <div className={styles["context-prompt-row"]}>
                <div className={styles["context-role"]}>
                  <label>Alias</label>
                </div>
                <textarea
                  rows={1}
                  className={styles["context-input"]}
                  onChange={this.handleTextAliasChange}
                ></textarea>
              </div>
            </div>
          </Modal>
        )}
        {this.props.isSettingsVisible && (
          <Modal
            title={"Settings"}
            actions={[
              <Button
                key="send"
                text={"Save Settings"}
                onClick={() => {
                  if (
                    !(
                      this.state.textAreaValue === "" ||
                      this.state.textAliasValue == ""
                    )
                  )
                    this.props.onModalActionClick?.(
                      this.state.textAreaValue,
                      this.state.textAliasValue
                    );
                  this.props.hideSettingsModal();
                }}
              />,
            ]}
            onClose={this.props.hideSettingsModal}
          >
            <div className={styles["context-prompt"]}>
              <div className={styles["context-prompt-row"]}>
                <div className={styles["context-prompt-header"]}>
                  <span>Onclusive Prompt Settings</span>
                </div>
              </div>

              <div className={styles["context-prompt-row"]}>
                <div className={styles["context-role"]}>
                  <label>Models</label>
                </div>
                <select
                  className={styles["context-input"]}
                  // onChange={this.handleTextAreaChange}
                >
                  {this.props.models.list.map((model: any, index: any) => (
                    <option value={model.model_name}>{model.model_name}</option>
                  ))}
                </select>
              </div>
            </div>
          </Modal>
        )}
      </>
    );
  }
}
