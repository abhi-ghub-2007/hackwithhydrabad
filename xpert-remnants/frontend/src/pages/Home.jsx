import React, { useState } from 'react';
import { useChat } from '../hooks/useChat';
import { AppShell } from '../components/layout/AppShell';
import { WelcomeState } from '../components/chat/WelcomeState';
import { ConversationView } from '../components/chat/ConversationView';
import { MessageComposer } from '../components/chat/MessageComposer';
import './Home.css';

export function Home() {
  const {
    chats,
    activeChatId,
    messages,
    isLoading,
    activeExpert,
    selectExpert,
    activeProject,
    selectProject,
    backendStatus,
    startNewChat,
    selectChat,
    handleSendMessage
  } = useChat();

  const [externalPromptText, setExternalPromptText] = useState('');

  const handleSelectPrompt = (promptText) => {
    handleSendMessage(promptText);
  };

  return (
    <AppShell
      chats={chats}
      activeChatId={activeChatId}
      onSelectChat={selectChat}
      onNewChat={startNewChat}
      activeExpert={activeExpert}
      onSelectExpert={selectExpert}
      activeProject={activeProject}
      onSelectProject={selectProject}
      backendStatus={backendStatus}
    >
      <div className="home-content-container">
        {messages.length === 0 ? (
          <WelcomeState
            onSelectPrompt={handleSelectPrompt}
            activeExpert={activeExpert}
          />
        ) : (
          <ConversationView messages={messages} />
        )}

        <MessageComposer
          onSendMessage={handleSendMessage}
          externalText={externalPromptText}
          setExternalText={setExternalPromptText}
          isLoading={isLoading}
          activeExpert={activeExpert}
          activeProject={activeProject}
        />
      </div>
    </AppShell>
  );
}
