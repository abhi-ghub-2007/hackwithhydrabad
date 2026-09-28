import { api } from './api';

export const ALL_KNOWLEDGE_SCOPE = {
  id: null,
  name: 'All organizational knowledge',
  role: 'Company-wide Memory',
  department: 'Organization',
  organization: 'Microsoft'
};

export const expertService = {
  async getExperts(params = {}) {
    try {
      const data = await api.getExperts(params);
      const list = data.map((exp) => ({
        id: exp.id,
        projectId: exp.project_id,
        name: exp.person?.full_name || `Expert #${exp.id}`,
        role: exp.role || 'Senior Architect',
        department: exp.department || 'Engineering',
        yearsOfExperience: exp.years_of_experience,
        status: exp.status || 'FORMER_EMPLOYEE',
        expertise: exp.expertise,
        biography: exp.biography
      }));
      return list;
    } catch (err) {
      console.warn('Failed to load experts from backend, using default roster:', err);
      return [
        { id: 1, name: 'Raj Mehta', role: 'Principal Architect (Payments)', department: 'Backend Engineering', projectId: 10 },
        { id: 2, name: 'Priya Sharma', role: 'Senior Platform Engineer', department: 'Platform Infrastructure', projectId: 11 },
        { id: 3, name: 'Vikram Rao', role: 'Principal Security Architect', department: 'Security & Auth', projectId: 12 },
        { id: 4, name: 'Ananya Iyer', role: 'Staff Data Engineer', department: 'Data Platform', projectId: 13 },
        { id: 5, name: 'Rohan Sen', role: 'Lead Payment Systems Architect', department: 'Financial Core', projectId: 14 }
      ];
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
        (e.department && e.department.toLowerCase().includes(q))
    );
  }
};
