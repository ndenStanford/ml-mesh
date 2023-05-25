import { useEffect, useRef, useState } from "react";
import {
  Layout,
  SideBar,
  Chat,
  PromptListItem,
  PromptList,
} from "./components";
import { useGlobalSelector, useGlobalDispatch } from "./hooks/use-dispatch";
import { GlobalState } from "./state";
import {
  getPrompts,
  createPrompt,
  generateText,
  generateTextFromPrompt,
  deletePrompt,
} from "./state/slices/prompts";
import { getModels } from "./state/slices/models";
import { addModal, hideModal, showModal } from "./state/slices/modals";
import {
  addMessage,
  clearMessages,
  setIsLoading,
  setHasFinishedLoading,
} from "./state/slices/chat";
import { APP_MODALS } from "./constants";
import { Message, Dictionary } from "./types";
import { v4 as uuidv4 } from "uuid";
import { MESSAGE_SEND_ANIMATION_DELAY } from "./constants";

export default function App() {
  var modelName = String(localStorage.getItem("modelName"));
  if (!modelName || modelName == "" || modelName == null) {
    modelName = "gpt-3.5-turbo";
  }
  const dispatch = useGlobalDispatch();
  // TODO: add button to clear the states to their inital values.
  const { app, prompts, models, modals, chat } = useGlobalSelector(
    (state: GlobalState) => state
  );

  const firstRender = useRef(true);
  function delay(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // to run on first render of the application
  useEffect(() => {
    if (firstRender.current) {
      dispatch(getPrompts());
      dispatch(getModels());
      firstRender.current = false;
      prompts.list.map((item) => dispatch(addModal(item.id)));
      models.list.map((item) => dispatch(addModal(item.id)));
      dispatch(addModal(APP_MODALS.NEW_PROMPT));
      dispatch(addModal(APP_MODALS.SETTINGS));
    }
  }, []);

  async function handleSendMessage(content: string) {
    const message = {
      id: uuidv4(),
      date: new Date().toLocaleString(),
      isError: false,
      content: content,
      isLoading: true,
      isUser: true,
    } as Message;
    dispatch(addMessage(message));
    dispatch(setIsLoading(message));
    await delay(MESSAGE_SEND_ANIMATION_DELAY);
    dispatch(setHasFinishedLoading(message));
    const response = {
      id: uuidv4(),
      date: new Date().toLocaleString(),
      isError: false,
      content: "",
      isLoading: true,
      isUser: false,
    } as Message;
    dispatch(addMessage(response));
    dispatch(generateText(message.content)).then((content) => {
      const final_response = {
        id: response.id,
        date: response.date,
        isError: response.isError,
        content: content.payload,
        isLoading: false,
        isUser: false,
      } as Message;
      dispatch(addMessage(final_response));
    });
  }

  async function handleDeletePrompt(alias: string) {
    dispatch(deletePrompt({ alias }));
    window.location.reload();
  }

  async function handleSendMessageWithPrompt(
    dct: Dictionary,
    id: string,
    alias: string,
    modelName: string
  ) {
    const message = {
      id: uuidv4(),
      date: new Date().toLocaleString(),
      isError: false,
      content: "",
      isLoading: true,
      isUser: true,
    } as Message;
    dispatch(addMessage(message));
    const response = {
      id: uuidv4(),
      date: new Date().toLocaleString(),
      isError: false,
      content: "",
      isLoading: true,
      isUser: false,
    } as Message;
    dispatch(addMessage(response));
    dispatch(
      generateTextFromPrompt({ alias: alias, body: dct, modelName: modelName })
    ).then(async (content) => {
      const final_message = {
        id: message.id,
        date: message.date,
        isError: message.isError,
        content: content.payload.prompt,
        isLoading: false,
        isUser: true,
      } as Message;
      const final_response = {
        id: response.id,
        date: response.date,
        isError: response.isError,
        content: content.payload.generated,
        isLoading: false,
        isUser: false,
      } as Message;
      dispatch(addMessage(final_message));
      await delay(1.5 * MESSAGE_SEND_ANIMATION_DELAY);
      dispatch(addMessage(final_response));
    });
  }
  return (
    <>
      <Layout state={app}>
        <SideBar
          defaultModelName={modelName}
          models={models.list}
          title={"Onclusive Prompt Manager"}
          subtitle={"Onclusive Machine Learning"}
          onActionClick={() => {
            dispatch(showModal(APP_MODALS.NEW_PROMPT));
          }}
          onSettingsClick={() => {
            dispatch(showModal(APP_MODALS.SETTINGS));
          }}
          hideModal={() => {
            dispatch(hideModal(APP_MODALS.NEW_PROMPT));
          }}
          hideSettingsModal={() => {
            dispatch(hideModal(APP_MODALS.SETTINGS));
          }}
          isNewPromptModalVisible={modals.list[APP_MODALS.NEW_PROMPT]}
          isSettingsVisible={modals.list[APP_MODALS.SETTINGS]}
          onModalActionClick={(template: string, alias: string) => {
            // NOTE: reloading the page here is a hack because redux should take
            // care of this when the state is updated.
            // dispatch(createPrompt({ template, alias }));

            dispatch(createPrompt({ template, alias })).then((content) => {
              // alert(JSON.stringify(content));
              // alert(JSON.stringify(content["payload"]["message"]));
              if ("payload" in content) {
                if ("message" in content["payload"]) {
                  if (String(content["payload"]["message"]) == "409") {
                    alert(
                      "A prompt with the same alias exists, please use a unique alias."
                    );
                  }
                }
              }
            });

            window.location.reload();
          }}
          onSettingsActionClick={(newModelName: string) => {
            localStorage.setItem("modelName", newModelName);
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
                  onSendClick: (dct: Dictionary, id: string, alias: string) => {
                    handleSendMessageWithPrompt(dct, id, alias, modelName);
                  },
                  onDeleteClick: (alias: string) => {
                    handleDeletePrompt(alias);
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
          state={{ app, prompts, models, modals, chat }}
          onChatActionClick={() => {
            dispatch(clearMessages());
          }}
          onChatSendClick={(content: string) => {
            handleSendMessage(content);
          }}
        />
      </Layout>
    </>
  );
}
