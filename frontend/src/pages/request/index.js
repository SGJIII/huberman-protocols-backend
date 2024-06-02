// frontend/src/pages/request/index.js
import React, { useState } from 'react';
import axios from 'axios';
import styles from './Request.module.css';
import { withPageAuthRequired } from '@auth0/nextjs-auth0';

const RequestProtocol = () => {
  const [episodeId, setEpisodeId] = useState('');
  const [protocol, setProtocol] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRequest = async () => {
    setLoading(true);
    setMessage(''); // Clear previous messages
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/chat`, { episode_id: episodeId });
      console.log('Response data:', response.data); // Debug log
      if (response.data && typeof response.data.response === 'string') {
        setProtocol(response.data.response);
      } else {
        setMessage('Invalid protocol format');
      }
    } catch (error) {
      console.error('Error generating protocol:', error); // Error log
      setMessage('Error generating protocol');
    } finally {
      setLoading(false);
    }
  };

  const handleEmail = async () => {
    setLoading(true);
    setMessage(''); // Clear previous messages
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/send_protocol`, { email, protocol });
      setMessage('Protocol sent successfully');
    } catch (error) {
      console.error('Error sending protocol:', error); // Error log
      setMessage('Error sending protocol');
    } finally {
      setLoading(false);
    }
  };

  console.log('Protocol:', protocol); // Debug log

  return (
    <div className={styles.container}>
      <h1>Request Your Protocol</h1>
      <div className={styles.formGroup}>
        <label htmlFor="episode-select">Select an episode:</label>
        <input
          type="text"
          value={episodeId}
          onChange={(e) => setEpisodeId(e.target.value)}
          placeholder="Enter episode ID"
        />
        <button className={styles.button} onClick={handleRequest} disabled={loading}>
          {loading ? 'Loading...' : 'Get Protocol'}
        </button>
      </div>
      {protocol && (
        <div className={styles.results}>
          <h2>Protocol</h2>
          <p>{typeof protocol === 'string' ? protocol : 'Invalid protocol format'}</p>
          <div className={styles.formGroup}>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email..."
            />
            <button className={styles.button} onClick={handleEmail} disabled={loading}>
              {loading ? 'Sending...' : 'Send PDF'}
            </button>
          </div>
        </div>
      )}
      {message && <p>{message}</p>}
    </div>
  );
};

export default withPageAuthRequired(RequestProtocol);
