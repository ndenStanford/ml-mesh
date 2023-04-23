import packageInfo from "../package.json";

export const IS_TEST = process.env.NODE_ENV === "test";
export const APP_MOUNT_URI = IS_TEST ? "/" : process.env.APP_MOUNT_URI || "/";
export const APP_DEFAULT_URI = "/";
export const PORT = parseInt(process.env.PORT || "4000");
export const API_URI = process.env.API_URI || `http://localhost:${PORT}/api/v1`;
export const API_KEY = process.env.API_KEY || "1234";
export const APP_VERSION = packageInfo.version;

export enum Theme {
  AUTO = "auto",
  DARK = "dark",
  LIGHT = "light",
}

export const DEFAULT_THEME = Theme.DARK;

export enum APP_MODALS {
  NEW_PROMPT = "NEW PROMPT",
}
