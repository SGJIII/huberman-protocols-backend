import { useEffect, useState } from 'react';
import { fetchTranscripts } from '../../utils/api';
import Link from 'next/link';
import styles from './index.module.css';

export default function Blog() {
  const [transcripts, setTranscripts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTranscripts() {
      try {
        const data = await fetchTranscripts();
        setTranscripts(data);
      } catch (error) {
        console.error('Error fetching transcripts:', error);
      } finally {
        setLoading(false);
      }
    }
    loadTranscripts();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div className={styles.container}>
      <h1>Blog</h1>
      <div className={styles.listGroup}>
        {transcripts.map((transcript) => (
          <Link key={transcript.id} href={`/blog/${transcript.title}`}>
            <a className={styles.listGroupItem}>
              <h5>{transcript.title}</h5>
              <p>{transcript.summary.slice(0, 200)}...</p>
            </a>
          </Link>
        ))}
      </div>
    </div>
  );
}
