import React, { createContext, useContext, useEffect, useState } from 'react';
import { useUserPreferences } from './UserPreferencesContext';

type Theme = 'light' | 'dark' | 'system';
type ThemeState = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  currentTheme: ThemeState;
  setTheme: (theme: Theme) => void;
  isTransitioning: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { preferences, updatePreference } = useUserPreferences();
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [currentTheme, setCurrentTheme] = useState<ThemeState>('light');
  const theme = preferences.theme;

  const setTheme = (newTheme: Theme) => {
    setIsTransitioning(true);
    updatePreference('theme', newTheme);
    // Reset transition state after animation completes
    setTimeout(() => setIsTransitioning(false), 200);
  };

  const applyTheme = (isDark: boolean) => {
    const root = window.document.documentElement;
    
    // Add transition class before changing theme
    root.classList.add('theme-transition');
    
    if (isDark) {
      root.classList.add('dark');
      setCurrentTheme('dark');
    } else {
      root.classList.remove('dark');
      setCurrentTheme('light');
    }

    // Remove transition class after animation completes
    setTimeout(() => {
      root.classList.remove('theme-transition');
    }, 200);
  };

  useEffect(() => {
    const root = window.document.documentElement;
    
    // Add base styles for transition
    root.style.setProperty('--theme-transition-duration', '200ms');

    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = (e: MediaQueryListEvent | MediaQueryList) => {
        applyTheme(e.matches);
      };

      handleChange(mediaQuery);
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    } else {
      applyTheme(theme === 'dark');
    }
  }, [theme]);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      if (theme === 'system') {
        if (mediaQuery.matches) {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ 
      theme, 
      setTheme, 
      currentTheme, 
      isTransitioning 
    }}>
      {children}
    </ThemeContext.Provider>
  );
};