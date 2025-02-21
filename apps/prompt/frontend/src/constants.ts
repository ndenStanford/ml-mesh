import packageInfo from "../package.json";

export const IS_TEST = process.env.NODE_ENV === "test";
export const APP_MOUNT_URI = IS_TEST ? "/" : process.env.APP_MOUNT_URI || "/";
export const APP_DEFAULT_URI = "/";
export const API_URI: string = process.env.REACT_APP_API_URI!;
export const API_KEY: string = process.env.REACT_APP_API_KEY!;
export const APP_VERSION = packageInfo.version;
export const MESSAGE_SEND_ANIMATION_DELAY = 1000;

export enum Theme {
  AUTO = "auto",
  DARK = "dark",
  LIGHT = "light",
}

export const DEFAULT_THEME = Theme.LIGHT;

export enum APP_MODALS {
  NEW_PROMPT = "NEW PROMPT",
  SETTINGS = "SETTINGS",
}
