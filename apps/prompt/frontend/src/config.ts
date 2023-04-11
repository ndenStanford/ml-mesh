import packageInfo from "../../package.json";

export const APP_VERSION: string = packageInfo.version;

export const API_PORT: number = parseInt(process.env.API_PORT || "5000", 10);

export const API_URI: string =
  process.env.API_URI || `http://localhost:${API_PORT}/api/v1/`;
