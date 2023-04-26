import React, { useRef, useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import "katex/dist/katex.min.css";
import RemarkMath from "remark-math";
import RemarkBreaks from "remark-breaks";
import RehypeKatex from "rehype-katex";
import RemarkGfm from "remark-gfm";
import RehypeHighlight from "rehype-highlight";
import styles from "./chat-message-content.module.scss";
import { ChatMessageContentProps } from "@/src/types";
import { ReactComponent as LoadingIcon } from "../../icons/three-dots.svg";
import { formatDate } from "../../utils";

export default function ChatMessageContent(props: ChatMessageContentProps) {
  const ref = useRef<HTMLPreElement>(null);
  const mdRef = useRef<HTMLDivElement>(null);
  const md = mdRef.current;
  const rendered = useRef(true);
  const [counter, setCounter] = useState(0);
  const parent = props.parentRef.current;

  useEffect(() => {
    setCounter(counter + 1);
  }, [props.message.isLoading]);

  const inView =
    rendered.current ||
    (() => {
      if (parent && md) {
        const parentBounds = parent.getBoundingClientRect();
        const mdBounds = md.getBoundingClientRect();
        const isInRange = (x: number) =>
          x <= parentBounds.bottom && x >= parentBounds.top;
        const inView = isInRange(mdBounds.top) || isInRange(mdBounds.bottom);
        if (inView) {
          rendered.current = true;
        }
        return inView;
      }
    })();

  const shouldLoading = props.message.isLoading || !inView;

  return (
    <>
      <div className={styles["chat-message-content-body"]} ref={mdRef}>
        {shouldLoading ? (
          <LoadingIcon />
        ) : (
          <ReactMarkdown
            remarkPlugins={[RemarkMath, RemarkGfm, RemarkBreaks]}
            rehypePlugins={[
              RehypeKatex,
              [
                RehypeHighlight,
                {
                  detect: false,
                  ignoreMissing: true,
                },
              ],
            ]}
            components={{
              pre: (props: { children: any }) => {
                return <pre ref={ref}>{props.children}</pre>;
              },
            }}
            linkTarget={"_blank"}
          >
            {props.message.content}
          </ReactMarkdown>
        )}
      </div>
    </>
  );
}
