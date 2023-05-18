import React, { RefObject } from "react";
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
  onModalActionClick?: (() => void) | ((arg0: any, arg1: any) => void);
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

export interface Message {
  id: string;
  date: string;
  isError?: boolean;
  content: string;
  isLoading: boolean;
  isUser: boolean;
}

export interface ChatState {
  messages: { [id: string]: Message };
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
  created_at: string;
  selected?: boolean;
  onClick?: () => void;
  onSendClick: (dct: Dictionary, id: string, alias: string) => void;
  onDeleteClick: (alias: string) => void;
}

export interface ChatProps {
  header: string;
  subtitle: string;
  state: GlobalState;
  children?: JSX.Element;
  onChatActionClick?: () => void;
  onChatSendClick?: (content: string) => void;
}

export interface GlobalState {
  app: AppState;
  prompts: PromptsState;
  modals: ModalsState;
  chat: ChatState;
}

export interface ChatMessageProps {
  message: Message;
}

export interface ChatMessageContentProps {
  message: Message;
  parentRef: RefObject<HTMLDivElement>;
}

export interface Dictionary {
  [key: string]: string;
}
