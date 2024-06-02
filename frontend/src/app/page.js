// src/app/page.js
import React from 'react';
import Head from 'next/head';
import Link from 'next/link';
import styles from './page.module.css';

const Home = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>Huberman Protocol</title>
        <meta name="description" content="Huberman Protocol - Improve your life with daily practices based on Huberman's podcast transcripts" />
      </Head>

      <header className={styles.header}>
        <h1>Welcome to Huberman Protocol</h1>
        <p>Improve your life with daily practices based on Huberman's podcast transcripts</p>
        <Link href="/blog" className={styles.button}>
          Visit Our Blog
        </Link>
        <Link href="/request" className={styles.button}>
          Request Your Protocol
        </Link>
      </header>

      <section className={styles.features}>
        <div className={styles.feature}>
          <h2>Personalized Protocols</h2>
          <p>Get personalized daily practices tailored to your needs.</p>
        </div>
        <div className={styles.feature}>
          <h2>Expert Insights</h2>
          <p>Gain insights from experts to enhance your daily routine.</p>
        </div>
        <div className={styles.feature}>
          <h2>Community Support</h2>
          <p>Join our community and get support from like-minded individuals.</p>
        </div>
      </section>

      <footer className={styles.footer}>
        <p>&copy; 2024 Huberman Protocol. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;