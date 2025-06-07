import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';
import { cn } from '../../lib/utils';
import CopyButton from './CopyButton';

interface MarkdownProps {
  content: string;
  className?: string;
}

const Markdown: React.FC<MarkdownProps> = ({ content, className }) => {
  return (
    <ReactMarkdown
      className={cn(
        'prose prose-sm prose-slate max-w-none break-words space-y-4',
        'prose-headings:font-semibold prose-headings:text-gray-900 prose-headings:mt-8 prose-headings:mb-4',
        'prose-p:text-gray-700 prose-p:leading-relaxed prose-p:mb-4',
        'prose-a:text-primary-600 prose-a:font-medium hover:prose-a:text-primary-700',
        'prose-strong:font-semibold prose-strong:text-gray-900',
        'prose-code:text-gray-800 prose-code:bg-gray-100 prose-code:rounded prose-code:px-1 prose-code:py-0.5',
        'prose-pre:bg-transparent prose-pre:p-0 prose-pre:mb-6',
        'prose-ol:text-gray-700 prose-ul:text-gray-700 prose-ol:mb-4 prose-ul:mb-4 prose-ol:pl-6 prose-ul:pl-6',
        'prose-li:marker:text-gray-500 prose-li:mb-2',
        'prose-table:w-full prose-table:border-collapse prose-table:my-6',
        'prose-th:border prose-th:border-gray-300 prose-th:bg-gray-100 prose-th:p-3 prose-th:text-left',
        'prose-td:border prose-td:border-gray-300 prose-td:p-3',
        className
      )}
      remarkPlugins={[remarkGfm]}
      components={{
        code: (({ inline, className, children, ...props }: React.ComponentProps<'code'> & { inline?: boolean }) => {
          const match = /language-(\w+)/.exec(className || '');
          return !inline && match ? (
            <div className="relative group">
              <SyntaxHighlighter
                language={match[1]}
                style={atomDark}
                PreTag="div"
                className="rounded-md my-4"
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
              <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                <CopyButton content={String(children)} />
              </div>
            </div>
          ) : (
            <code className={cn('text-sm font-mono', className)} {...props}>
              {children}
            </code>
          );
        }),
      }}
    >
      {content}
    </ReactMarkdown>
  );
};

export default Markdown;