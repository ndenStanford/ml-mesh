import { useEffect, useRef } from "react";
import {
  Layout,
  SideBar,
  Chat,
  PromptListItem,
  PromptList,
} from "./components";
import { useGlobalSelector, useGlobalDispatch } from "./hooks/use-dispatch";
import { GlobalState } from "./state";
import { getPrompts, createPrompt } from "./state/slices/prompts";
import { addModal, hideModal, showModal } from "./state/slices/modals";
import { APP_MODALS } from "./constants";

export default function App() {
  const dispatch = useGlobalDispatch();
  const { app, prompts, modals } = useGlobalSelector(
    (state: GlobalState) => state
  );

  const firstRender = useRef(true);

  // to run on first render of the application
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      dispatch(getPrompts());
      prompts.list.map((item) => dispatch(addModal(item.id)));
      dispatch(addModal(APP_MODALS.NEW_PROMPT));
    }
  });

  return (
    <>
      <Layout state={app}>
        <SideBar
          title={"Onclusive Prompt Manager"}
          subtitle={"Onclusive Machine Learning"}
          onActionClick={() => {
            dispatch(showModal(APP_MODALS.NEW_PROMPT));
          }}
          hideModal={() => {
            dispatch(hideModal(APP_MODALS.NEW_PROMPT));
          }}
          isNewPromptModalVisible={modals.list[APP_MODALS.NEW_PROMPT]}
          onModalActionClick={(template: string) => {
            dispatch(createPrompt(template));
          }}
        >
          <PromptList>
            {prompts.list.map((item) => (
              <PromptListItem
                item={{
                  id: item.id,
                  alias: item.alias,
                  template: item.template,
                  variables: item.variables,
                  created_at: item.created_at,
                  selected: item.selected,
                  onClick: () => {
                    dispatch(showModal(item.id));
                  },
                }}
                isModalVisible={modals.list[item.id]}
                hideModal={() => {
                  dispatch(hideModal(item.id));
                }}
              />
            ))}
          </PromptList>
        </SideBar>
        <Chat
          header={"Chat"}
          subtitle={"Send messages with prompt templates."}
          state={{ app, prompts, modals }}
        >
          <></>
        </Chat>
      </Layout>
    </>
  );
}
