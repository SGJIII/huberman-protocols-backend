import React from 'react';
import Link from 'next/link';
import styles from './NavBar.module.css';

const NavBar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <Link href="/" legacyBehavior>
          <a className={styles.brand}>Huberman Protocol</a>
        </Link>
        <div className={styles.links}>
          <Link href="/blog" legacyBehavior>
            <a className={styles.link}>Blog</a>
          </Link>
          <Link href="/request" legacyBehavior>
            <a className={styles.link}>Request Protocol</a>
          </Link>
          <Link href="/login" legacyBehavior>
            <a className={styles.link}>Login</a>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
