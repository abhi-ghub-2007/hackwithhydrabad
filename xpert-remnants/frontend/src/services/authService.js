const THEME_KEY = 'xpert_theme_v1';
const USER_KEY = 'xpert_user_profile_v1';

export const authService = {
  getCurrentUser() {
    try {
      const raw = localStorage.getItem(USER_KEY);
      if (raw) return JSON.parse(raw);
    } catch (_) {}

    const defaultUser = {
      id: 'usr-4412',
      name: 'Lead Engineer',
      email: 'engineer@northstar.internal',
      role: 'Staff Engineer',
      initials: 'LE'
    };
    try {
      localStorage.setItem(USER_KEY, JSON.stringify(defaultUser));
    } catch (_) {}
    return defaultUser;
  },

  getTheme() {
    try {
      const saved = localStorage.getItem(THEME_KEY);
      if (saved === 'light' || saved === 'dark') {
        return saved;
      }
    } catch (_) {}
    return 'dark'; // Default to sleek dark mode
  },

  setTheme(theme) {
    const validTheme = theme === 'light' ? 'light' : 'dark';
    try {
      localStorage.setItem(THEME_KEY, validTheme);
    } catch (_) {}
    document.documentElement.setAttribute('data-theme', validTheme);
    return validTheme;
  },

  initTheme() {
    const theme = this.getTheme();
    document.documentElement.setAttribute('data-theme', theme);
    return theme;
  }
};
