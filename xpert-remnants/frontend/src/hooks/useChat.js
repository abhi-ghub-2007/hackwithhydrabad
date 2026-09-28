import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import { chatService } from '../services/chatService';
import { expertService, ALL_KNOWLEDGE_SCOPE } from '../services/expertService';

export function useChat() {
  const [chats, setChats] = useState(() => chatService.getStoredChats());
  const [activeChatId, setActiveChatId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeExpert, setActiveExpert] = useState(ALL_KNOWLEDGE_SCOPE);
  const [activeProject, setActiveProject] = useState(null);
  const [backendStatus, setBackendStatus] = useState({ loading: true, online: false, data: null });
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  // Check backend health on mount
  useEffect(() => {
    let isMounted = true;
    api.checkHealth().then((res) => {
      if (isMounted) {
        if (res.status === 'ok') {
          setBackendStatus({ loading: false, online: true, data: res });
        } else {
          setBackendStatus({ loading: false, online: false, data: res });
        }
      }
    });
    return () => { isMounted = false; };
  }, []);

  // Save chats to localStorage whenever chats update
  useEffect(() => {
    chatService.saveChats(chats);
  }, [chats]);

  const selectProject = useCallback((project) => {
    setActiveProject(project || null);
    if (project && activeExpert?.projectId && activeExpert.projectId !== project.id) {
      setActiveExpert(ALL_KNOWLEDGE_SCOPE);
    }
  }, [activeExpert]);

  const selectExpert = useCallback((expert) => {
    setActiveExpert(expert || ALL_KNOWLEDGE_SCOPE);
    if (expert && expert.projectId && (!activeProject || activeProject.id !== expert.projectId)) {
      api.getProject(expert.projectId).then((p) => {
        if (p) setActiveProject(p);
      }).catch(() => {});
    }
  }, [activeProject]);

  const startNewChat = useCallback(() => {
    setActiveChatId(null);
    setMessages([]);
    setIsMobileSidebarOpen(false);
  }, []);

  const selectChat = useCallback(async (chatId) => {
    setActiveChatId(chatId);
    const selected = chats.find((c) => c.id === chatId);
    if (selected) {
      setMessages(selected.messages || []);
      if (selected.expertId) {
        const exp = await expertService.getExpertById(selected.expertId);
        setActiveExpert(exp);
      } else {
        setActiveExpert(ALL_KNOWLEDGE_SCOPE);
      }
    }
    setIsMobileSidebarOpen(false);
  }, [chats]);

  const handleSendMessage = useCallback(async (text) => {
    if (!text || !text.trim() || isLoading) return;

    const queryText = text.trim();
    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: queryText,
      timestamp: currentTime
    };

    // Temporary thinking message
    const thinkingMsgId = `thinking-${Date.now()}`;
    const thinkingMsg = {
      id: thinkingMsgId,
      sender: 'assistant',
      isThinking: true,
      text: 'XPERT REMNANTS is thinking...',
      timestamp: currentTime
    };

    const newMessages = [...messages, userMsg, thinkingMsg];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const askRes = await chatService.askQuestion(queryText, {
        expertId: activeExpert?.id,
        projectId: activeProject?.id,
        contextHint: activeExpert?.id
          ? `Focus on decisions from ${activeExpert.name}`
          : (activeProject?.id ? `Focus on project ${activeProject.name}` : null)
      });

      let botMsg;
      if (askRes.success) {
        botMsg = {
          id: `assistant-${Date.now()}`,
          sender: 'assistant',
          text: askRes.answer,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          originalQuery: queryText,
          matchScore: askRes.matchScore,
          sources: askRes.sources,
          evidenceCount: askRes.evidenceCount,
          decisionMemoryId: askRes.decisionMemoryId
        };
      } else {
        botMsg = {
          id: `error-${Date.now()}`,
          sender: 'assistant',
          isError: true,
          text: 'Something went wrong. Please try again.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          originalQuery: queryText
        };
      }

      // Replace thinking message with real bot response
      const finalizedMessages = [...messages, userMsg, botMsg];
      setMessages(finalizedMessages);

      // Update or create chat in state & storage
      if (!activeChatId) {
        const newId = `chat-${Date.now()}`;
        const cleanTitle = queryText.length > 36 ? queryText.substring(0, 36) + '...' : queryText;
        const newChatObj = {
          id: newId,
          title: cleanTitle,
          date: 'Just now',
          expertId: activeExpert?.id || null,
          messages: finalizedMessages
        };
        setChats((prev) => [newChatObj, ...prev]);
        setActiveChatId(newId);
      } else {
        setChats((prev) =>
          prev.map((c) =>
            c.id === activeChatId ? { ...c, messages: finalizedMessages } : c
          )
        );
      }
    } catch (err) {
      console.error('handleSendMessage error:', err);
      const errorMsg = {
        id: `error-${Date.now()}`,
        sender: 'assistant',
        isError: true,
        text: 'Something went wrong. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages([...messages, userMsg, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  }, [activeChatId, activeExpert, isLoading, messages]);

  const toggleMobileSidebar = useCallback(() => {
    setIsMobileSidebarOpen((prev) => !prev);
  }, []);

  const closeMobileSidebar = useCallback(() => {
    setIsMobileSidebarOpen(false);
  }, []);

  return {
    chats,
    activeChatId,
    messages,
    isLoading,
    activeExpert,
    selectExpert,
    activeProject,
    selectProject,
    backendStatus,
    isMobileSidebarOpen,
    startNewChat,
    selectChat,
    handleSendMessage,
    toggleMobileSidebar,
    closeMobileSidebar
  };
}
