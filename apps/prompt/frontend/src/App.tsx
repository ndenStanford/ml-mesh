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
import {
  getPrompts,
  createPrompt,
  generateText,
  generateTextFromPrompt,
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

export default function App() {
  const dispatch = useGlobalDispatch();
  // TODO: add button to clear the states to their inital values.
  const { app, prompts, modals, chat } = useGlobalSelector(
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

  async function handleSendMessageWithPrompt(dct: Dictionary, id: string) {
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
    dispatch(generateTextFromPrompt({ prompt_id: id, body: dct })).then(
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
            dispatch(createPrompt({ template, alias })).then((content) => {
              // alert(JSON.stringify(content));
              if (String(content["type"]) == "prompts/create/fulfilled") {
                alert("Alias conflict, you must provide a unique alias");
              }
            });
            window.location.reload();
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
                  onSendClick: (dct: Dictionary, id: string) => {
                    handleSendMessageWithPrompt(dct, id);
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
