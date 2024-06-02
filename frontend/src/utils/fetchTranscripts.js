export async function fetchTranscripts() {
    const res = await fetch(`${process.env.BACKEND_URL}/transcripts`);
    const data = await res.json();
    if (data.status === 'success') {
      return data.data;
    } else {
      throw new Error(data.message || 'Failed to fetch transcripts');
    }
  }
  
  export async function fetchTranscriptByTitle(title) {
    const res = await fetch(`${process.env.BACKEND_URL}/blog/${title}`);
    const data = await res.json();
    if (data.status === 'success') {
      return data.data;
    } else {
      throw new Error(data.message || 'Failed to fetch transcript');
    }
  }
  