// frontend/src/utils/api.js
const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export const fetchTranscripts = async () => {
  const response = await fetch(`${API_BASE_URL}/transcripts`);
  const data = await response.json();
  return data.data;
};

export const fetchTranscriptByTitle = async (title) => {
  const response = await fetch(`${API_BASE_URL}/transcript/${title}`);
  const data = await response.json();
  return data.data;
};

export const generateProtocol = async (episodeId) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ episode_id: episodeId }),
  });
  const data = await response.json();
  return data;
};

export const sendProtocolEmail = async (email, protocol) => {
  const response = await fetch(`${API_BASE_URL}/send_protocol`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, protocol }),
  });
  const data = await response.json();
  return data;
};