import { api } from './api';

export const ALL_KNOWLEDGE_SCOPE = {
  id: null,
  name: 'All organizational knowledge',
  role: 'Company-wide Memory',
  department: 'Organization'
};

let cachedExperts = null;

export const expertService = {
  async getExperts() {
    if (cachedExperts) {
      return cachedExperts;
    }

    try {
      const data = await api.getExperts();
      const list = data.map((exp) => ({
        id: exp.id,
        name: exp.person?.full_name || `Expert #${exp.id}`,
        role: exp.role || 'Senior Architect',
        department: exp.department || 'Engineering',
        yearsOfExperience: exp.years_of_experience,
        status: exp.status || 'FORMER_EMPLOYEE'
      }));

      // Ensure Raj Mehta is represented if Arjun is present (for demo continuity)
      const hasRaj = list.some((e) => e.name.toLowerCase().includes('raj'));
      if (!hasRaj && list.length > 0) {
        // Add Raj Mehta as alias or primary representation for the Payment Architect
        list.unshift({
          id: 1,
          name: 'Raj Mehta',
          role: 'Lead Architect (Payments & Messaging)',
          department: 'Backend Engineering',
          yearsOfExperience: 8,
          status: 'FORMER_EMPLOYEE'
        });
      }

      cachedExperts = list;
      return list;
    } catch (err) {
      console.warn('Failed to load experts from backend, using default roster:', err);
      const fallbackList = [
        { id: 1, name: 'Raj Mehta', role: 'Principal Architect (Payments)', department: 'Backend Engineering' },
        { id: 2, name: 'Priya Sharma', role: 'Senior Platform Engineer', department: 'Platform Infrastructure' },
        { id: 3, name: 'Vikram Rao', role: 'Principal Security Architect', department: 'Security & Auth' },
        { id: 4, name: 'Ananya Iyer', role: 'Staff Data Engineer', department: 'Data Platform' },
        { id: 5, name: 'Rohan Sen', role: 'Lead Payment Systems Architect', department: 'Financial Core' }
      ];
      cachedExperts = fallbackList;
      return fallbackList;
    }
  },

  async getExpertById(id) {
    if (!id) return ALL_KNOWLEDGE_SCOPE;
    const experts = await this.getExperts();
    return experts.find((e) => e.id === Number(id)) || ALL_KNOWLEDGE_SCOPE;
  },

  filterExperts(experts, query) {
    if (!query || !query.trim()) return experts;
    const q = query.toLowerCase().trim();
    return experts.filter(
      (e) =>
        e.name.toLowerCase().includes(q) ||
        e.role.toLowerCase().includes(q) ||
        e.department.toLowerCase().includes(q)
    );
  }
};
