import React from "react";
import { Theme } from "@/src/constants";

export interface ButtonProps {
  onClick?: (() => void) | ((arg0: any) => void);
  icon: JSX.Element;
  text?: string;
  noDark?: boolean;
  className?: string;
  title?: string;
  disabled?: boolean;
}

export interface ToastProps {
  content: string;
  action?: {
    text: string;
    onClick: () => void;
  };
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
  showToast: boolean;
}

export interface PromptsState {
  list: PromptListItemProps[];
}

export interface Message {
  id?: number;
  date: string;
  isError?: boolean;
  content: string;
}

export interface ChatSessionState {
  id: number;
  messages: Message[];
  lastUpdate: string;
}

export interface LayoutProps {
  children: JSX.Element[];
  state: AppState;
}

export interface PromptListItemProps {
  id?: string;
  alias: string;
  template: string;
  created_at?: string;
  selected?: boolean;
  onClick?: () => void;
  onDelete?: () => void;
}

export interface GlobalState {
  app: AppState;
  prompts: PromptsState;
}
