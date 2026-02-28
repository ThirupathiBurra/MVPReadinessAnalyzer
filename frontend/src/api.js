import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5001/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const submitIdea = async (structuredIdea) => {
    // structuredIdea matches StructuredIdeaInput in backend
    const response = await api.post('/ideas', { structured_idea: structuredIdea });
    return response.data;
};

export const triggerAnalysis = async (ideaId) => {
    const response = await api.post(`/ideas/${ideaId}/analyze`);
    return response.data;
};

export const fetchReport = async (ideaId) => {
    const response = await api.get(`/ideas/${ideaId}/report`);
    return response.data;
};

export const fetchMetrics = async () => {
    const response = await api.get('/metrics');
    return response.data;
}

export default api;
