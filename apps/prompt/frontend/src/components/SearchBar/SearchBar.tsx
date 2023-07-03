import React from "react";
import styles from "./search-bar.module.scss";
export default function SearchBar({
  value,
  onChange,
}: {
  value: any;
  onChange: any;
}) {
  return (
    <input
      type="text"
      placeholder="Search Prompts"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className={styles["search-bar-input"]}
    />
  );
}
