import { Theme } from "./constants";
import { DEFAULT_THEME } from "./constants";

export function toggleTheme(theme: Theme): Theme {
  if (theme === Theme.AUTO) {
    return Theme.LIGHT;
  }
  if (theme === Theme.LIGHT) {
    return Theme.DARK;
  }
  if (theme === Theme.DARK) {
    return Theme.AUTO;
  }
  return DEFAULT_THEME;
}

export function setTheme(theme: Theme): Theme {
  document.body.classList.remove("light");
  document.body.classList.remove("dark");
  const metaDescriptionDark = document.querySelector(
    'meta[name="theme-color"][media]'
  );
  const metaDescriptionLight = document.querySelector(
    'meta[name="theme-color"]:not([media])'
  );

  if (theme === Theme.LIGHT) {
    document.body.classList.add("light");
  }
  if (theme === Theme.DARK) {
    document.body.classList.add("dark");
  }
  if (theme === Theme.AUTO) {
    metaDescriptionDark?.setAttribute("content", "#151515");
    metaDescriptionLight?.setAttribute("content", "#fafafa");
  }
  return theme;
}

// NOTE: this should probably be a hook instead
export function updateTheme(theme: Theme): Theme {
  const newTheme = toggleTheme(theme);
  return setTheme(newTheme);
}
