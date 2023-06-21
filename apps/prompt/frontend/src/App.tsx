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
import styles from "./components/SideBar/side-bar.module.scss";
export default function App() {
  const dispatch = useGlobalDispatch();
  // TODO: add button to clear the states to their inital values.
  const { app, prompts, modals, chat } = useGlobalSelector(
    (state: GlobalState) => state
  );
  const [searchQuery, setSearchQuery] = useState("");

  const firstRender = useRef(true);
  function delay(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // to run on first render of the application
  useEffect(() => {
    if (firstRender.current) {
      dispatch(getPrompts());
      firstRender.current = false;
      prompts.list.map((item) => dispatch(addModal(item.id)));
      dispatch(addModal(APP_MODALS.NEW_PROMPT));
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
    alias: string
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
    dispatch(generateTextFromPrompt({ alias: alias, body: dct })).then(
      async (content) => {
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
      }
    );
  }

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
          onModalActionClick={(template: string, alias: string) => {
            // NOTE: reloading the page here is a hack because redux should take
            // care of this when the state is updated.
            // dispatch(createPrompt({ template, alias }));

            dispatch(createPrompt({ template, alias })).then((content) => {
              if ("payload" in content) {
                if (content["payload"]) {
                  if ("message" in content["payload"]) {
                    if (String(content["payload"]["message"]) == "409") {
                      alert(
                        "A prompt with the same alias exists, please provide a unique alias."
                      );
                    }
                  }
                }
              }
            });

            window.location.reload();
          }}
        >
          <PromptList>
            <div>
              <input
                type="text"
                value={searchQuery}
                placeholder="Search prompts"
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{
                  padding: "8px",
                  marginBottom: "16px",
                  width: "100%",
                  boxSizing: "border-box",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  fontSize: "16px",
                }}
              />
            </div>
            {prompts.list
              .filter((item) =>
                item.alias.toLowerCase().includes(searchQuery.toLowerCase())
              )
              .map((item) => (
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
                    onSendClick: (
                      dct: Dictionary,
                      id: string,
                      alias: string
                    ) => {
                      handleSendMessageWithPrompt(dct, id, alias);
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
          state={{ app, prompts, modals, chat }}
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
