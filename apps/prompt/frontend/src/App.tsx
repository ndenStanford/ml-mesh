import { useEffect, useRef } from "react";
import {
  Layout,
  SideBar,
  Chat,
  PromptListItem,
  PromptList,
} from "./components";
import { useGlobalSelector } from "./hooks/use-dispatch";
import { useSelector, useDispatch } from "react-redux";
import { GlobalState, GlobalDispatch } from "./state";
import { useGlobalDispatch } from "./hooks/use-dispatch";
import { listPrompts, getPrompts } from "./state/slices/prompts";
import { ThunkDispatch } from "@reduxjs/toolkit";
import { showToast, hideToast } from "./state/slices/app";

export default function App() {
  const dispatch = useDispatch<ThunkDispatch<any, any, any>>();
  const { app, prompts } = useGlobalSelector((state: GlobalState) => state);

  const handlePromptListItemOnClick = () => {
    dispatch(showToast());
  };

  const promptItems = useSelector(listPrompts);
  const firstRender = useRef(true);

  // to run on first render of the application
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      dispatch(getPrompts());
      dispatch(hideToast());
    }
  });

  return (
    <>
      <Layout state={app}>
        <SideBar>
          <PromptList>
            {promptItems.map((item, _) => (
              <PromptListItem
                alias={item.alias}
                template={item.template}
                created_at={item.created_at}
                onClick={handlePromptListItemOnClick}
              />
            ))}
          </PromptList>
        </SideBar>
        <Chat state={{ app, prompts }} />
      </Layout>
    </>
  );
}
