import React, { useState } from 'react';
import { Sun, Moon, Monitor, Settings } from 'lucide-react';
import { useUserPreferences } from '../context/UserPreferencesContext';
import { motion, AnimatePresence } from 'framer-motion';
import Button from './ui/Button';
import { cn } from '../lib/utils';
import SettingsPanel from './SettingsPanel';

const iconVariants = {
  initial: { scale: 0.5, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  exit: { scale: 0.5, opacity: 0 },
  hover: { scale: 1.1 }
};

const containerVariants = {
  initial: { opacity: 0, y: -20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 20 }
};

const ThemeToggle: React.FC = () => {
  const { preferences, updatePreference } = useUserPreferences();
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isHovering, setIsHovering] = useState(false);

  const handleThemeChange = (theme: 'light' | 'dark' | 'system') => {
    updatePreference('theme', theme);
  };

  return (
    <motion.div 
      className="flex items-center gap-1"
      variants={containerVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <motion.div 
        className="bg-gray-100 dark:bg-gray-700 rounded-full p-1 flex items-center backdrop-blur-sm"
        animate={{
          scale: isHovering ? 1.02 : 1,
          boxShadow: isHovering ? '0 8px 20px rgba(0,0,0,0.1)' : '0 4px 12px rgba(0,0,0,0.05)'
        }}
        transition={{ duration: 0.2 }}
        onHoverStart={() => setIsHovering(true)}
        onHoverEnd={() => setIsHovering(false)}
      >
        <AnimatePresence mode="wait">
          <motion.button
            key="light"
            onClick={() => handleThemeChange('light')}
            className={cn(
              "p-1.5 rounded-full transition-all duration-200",
              preferences.theme === 'light' 
                ? "bg-white dark:bg-gray-600 text-amber-500 shadow-lg" 
                : "text-gray-500 dark:text-gray-400 hover:text-amber-500"
            )}
            variants={iconVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            whileHover="hover"
            aria-label="Light mode"
          >
            <Sun size={18} />
          </motion.button>
          <motion.button
            key="dark"
            onClick={() => handleThemeChange('dark')}
            className={cn(
              "p-1.5 rounded-full transition-all duration-200",
              preferences.theme === 'dark' 
                ? "bg-white dark:bg-gray-600 text-blue-500 shadow-lg" 
                : "text-gray-500 dark:text-gray-400 hover:text-blue-500"
            )}
            variants={iconVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            whileHover="hover"
            aria-label="Dark mode"
          >
            <Moon size={18} />
          </motion.button>
          <motion.button
            key="system"
            onClick={() => handleThemeChange('system')}
            className={cn(
              "p-1.5 rounded-full transition-all duration-200",
              preferences.theme === 'system' 
                ? "bg-white dark:bg-gray-600 text-purple-500 shadow-lg" 
                : "text-gray-500 dark:text-gray-400 hover:text-purple-500"
            )}
            variants={iconVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            whileHover="hover"
            aria-label="System theme"
          >
            <Monitor size={18} />
          </motion.button>
        </AnimatePresence>
      </motion.div>
      
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsSettingsOpen(true)}
          className="rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200 ml-1"
          aria-label="Open settings"
        >
          <Settings size={18} className="text-gray-600 dark:text-gray-400" />
        </Button>
      </motion.div>
      
      <SettingsPanel isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
    </motion.div>
  );
};

export default ThemeToggle;