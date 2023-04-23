import React from "react";
import { Theme } from "@/src/constants";

export interface ButtonProps {
  onClick?: (() => void) | ((arg0: any) => void);
  icon?: JSX.Element;
  text?: string;
  noDark?: boolean;
  className?: string;
  title?: string;
  disabled?: boolean;
}

export interface ModalProps {
  title: string;
  children?: JSX.Element;
  actions?: JSX.Element[];
  onClose?: () => void;
}

export interface SidebarProps {
  title: string;
  subtitle: string;
  children?: JSX.Element;
  onActionClick?: (() => void) | ((arg0: any) => void);
  isNewPromptModalVisible: boolean;
  hideModal: any;
  onModalActionClick?: (() => void) | ((arg0: any) => void);
}

export interface IErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  info: React.ErrorInfo | null;
}

export interface InputRangeProps {
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  title?: string;
  value: number | string;
  className?: string;
  min: string;
  max: string;
  step: string;
}

export interface AppState {
  theme: Theme;
}

export interface ModalsState {
  list: { [id: string]: boolean };
}

export interface PromptsState {
  list: PromptListItemProps[];
}

export interface ChatMessage {
  id?: number;
  date: string;
  isError?: boolean;
  content: string;
  isLoading: boolean;
  isUser: boolean;
}

export interface ChatState {
  messages: ChatMessage[];
}

export interface LayoutProps {
  children: JSX.Element[];
  state: AppState;
}

export interface PromptListItemProps {
  id: string;
  alias: string;
  template: string;
  variables: string[];
  created_at?: string;
  selected?: boolean;
  onClick?: () => void;
  onDelete?: () => void;
}

export interface ChatProps {
  header: string;
  subtitle: string;
  state: GlobalState;
  children?: JSX.Element;
}

export interface GlobalState {
  app: AppState;
  prompts: PromptsState;
  modals: ModalsState;
}

export interface ChatMessageProps {
  message: ChatMessage;
}
