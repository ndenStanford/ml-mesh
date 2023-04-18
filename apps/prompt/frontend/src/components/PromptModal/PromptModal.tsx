// import React from "react";
// import styles from "./prompt-modal.module.scss"

// export default class PromptModal extends React.Component<any, any> {

//     render() {
//         return (
//             <div
//                 className={styles["prompt-modal"]}
//             >
//             <div>
//               <div className={styles["prompt-modal-inner"]}>
//                 <div
//                   className="hidden sm:inline-block sm:h-screen sm:align-middle"
//                   aria-hidden="true"
//                 />

//                 <div
//                   ref={modalRef}
//                   className="dark:border-netural-400 inline-block max-h-[400px] transform overflow-y-auto rounded-lg border border-gray-300 bg-white px-4 pt-5 pb-4 text-left align-bottom shadow-xl transition-all dark:bg-[#202123] sm:my-8 sm:max-h-[600px] sm:w-full sm:max-w-lg sm:p-6 sm:align-middle"
//                   role="dialog"
//                 >
//                   <div className="text-sm font-bold text-black dark:text-neutral-200">
//                     {t('Name')}
//                   </div>
//                   <input
//                     ref={nameInputRef}
//                     className="mt-2 w-full rounded-lg border border-neutral-500 px-4 py-2 text-neutral-900 shadow focus:outline-none dark:border-neutral-800 dark:border-opacity-50 dark:bg-[#40414F] dark:text-neutral-100"
//                     placeholder={t('A name for your prompt.') || ''}
//                     value={name}
//                     onChange={(e) => setName(e.target.value)}
//                   />

//                   <div className="mt-6 text-sm font-bold text-black dark:text-neutral-200">
//                     {t('Description')}
//                   </div>
//                   <textarea
//                     className="mt-2 w-full rounded-lg border border-neutral-500 px-4 py-2 text-neutral-900 shadow focus:outline-none dark:border-neutral-800 dark:border-opacity-50 dark:bg-[#40414F] dark:text-neutral-100"
//                     style={{ resize: 'none' }}
//                     placeholder={t('A description for your prompt.') || ''}
//                     value={description}
//                     onChange={(e) => setDescription(e.target.value)}
//                     rows={3}
//                   />

//                   <div className="mt-6 text-sm font-bold text-black dark:text-neutral-200">
//                     {t('Prompt')}
//                   </div>
//                   <textarea
//                     className="mt-2 w-full rounded-lg border border-neutral-500 px-4 py-2 text-neutral-900 shadow focus:outline-none dark:border-neutral-800 dark:border-opacity-50 dark:bg-[#40414F] dark:text-neutral-100"
//                     style={{ resize: 'none' }}
//                     placeholder={
//                       t(
//                         'Prompt content. Use {} to denote a variable. Ex: Summarize in less that {n}-words this article: {text}',
//                       ) || ''
//                     }
//                     value={content}
//                     onChange={(e) => setContent(e.target.value)}
//                     rows={10}
//                   />

//                   <button
//                     type="button"
//                     className="w-full px-4 py-2 mt-6 border rounded-lg shadow border-neutral-500 text-neutral-900 hover:bg-neutral-100 focus:outline-none dark:border-neutral-800 dark:border-opacity-50 dark:bg-white dark:text-black dark:hover:bg-neutral-300"
//                     onClick={() => {
//                       const updatedPrompt = {
//                         ...prompt,
//                         name,
//                         description,
//                         content: content.trim(),
//                       };

//                       onUpdatePrompt(updatedPrompt);
//                       onClose();
//                     }}
//                   >
//                     {t('Save')}
//                   </button>
//                 </div>
//               </div>
//             </div>
//           </div>
//         )
//     }
// }

export {};
