import React from 'react';
import { PlusCircle, MessageSquare } from 'lucide-react';
import { useChat } from '../context/ChatContext';
import { cn, truncate, formatDate } from '../lib/utils';
import Button from './ui/Button';
import '../styles/home.css';

const ConversationList: React.FC = () => {
  const { conversations, currentConversation, selectConversation, startNewConversation } = useChat();

  return (
    <div className="flex flex-col h-full conversation-list">
      <div className="p-3 flex-shrink-0">
        <Button
          onClick={startNewConversation}
          leftIcon={<PlusCircle size={18} />}
          className="w-full justify-start hover:bg-primary-100 transition-colors"
          variant="outline"
        >
          New Chat
        </Button>
      </div>
      <div className="overflow-y-auto flex-1 px-2">
        {conversations.length === 0 ? (
          <div className="text-sm text-gray-500 p-4 text-center">
            No conversations yet
          </div>
        ) : (
          <ul className="space-y-1 p-2">
            {conversations.map((conversation) => (
              <li key={conversation.id}>
                <button
                  onClick={() => selectConversation(conversation.id)}
                  className={cn(
                    'w-full text-left px-4 py-3 rounded-lg transition-all conversation-item',
                    'flex items-start gap-3',
                    conversation.id === currentConversation?.id
                      ? 'bg-primary-100 text-primary-900'
                      : 'hover:bg-primary-50 text-primary-700'
                  )}
                >
                  <MessageSquare size={20} className="flex-shrink-0 mt-0.5 text-primary-600" />
                  <div className="flex-1 min-w-0">
                    <div className="conversation-title">{truncate(conversation.title, 24)}</div>
                    <div className="conversation-timestamp">
                      {formatDate(conversation.timestamp)}
                    </div>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ConversationList;