import { useRouter } from 'next/router';
import { fetchTranscriptByTitle } from '../../utils/api';
import { useEffect, useState } from 'react';
import styles from './[title].module.css';

export default function BlogPost() {
  const router = useRouter();
  const { title } = router.query;
  const [transcript, setTranscript] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (title) {
      async function loadTranscript() {
        try {
          const data = await fetchTranscriptByTitle(title);
          setTranscript(data);
        } catch (error) {
          console.error('Error fetching transcript:', error);
        } finally {
          setLoading(false);
        }
      }
      loadTranscript();
    }
  }, [title]);

  if (loading) return <p>Loading...</p>;
  if (!transcript) return <p>Transcript not found</p>;

  return (
    <div className={styles.container}>
      <h1>{transcript.title}</h1>
      <h3>Episode Summary</h3>
      <div>
        {transcript.summary.split(' - ').map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>
      <h3>Full Transcript of {transcript.title}</h3>
      <div>
        {transcript.content.split(' --> ').map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>
    </div>
  );
}
