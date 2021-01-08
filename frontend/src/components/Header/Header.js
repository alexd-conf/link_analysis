import React from 'react';
import styles from './Header.module.css';

const Header = () => (
  <div className={styles.header} data-testid="Header">
    <div className={styles.title} data-testid="Title">Link Analysis</div>
    <div className={styles.links} data-testid="Links">
      <div>{process.env.REACT_APP_GITHUB_URL}</div>
    </div>
    <div className={styles.information} data-testid="Information">
      <div>1) Enter a URL into the Analysis Bar.</div>
      <div>2) Click the 'Analyze' Button.</div>
      <div>3) Appraise the results.</div>
    </div>
  </div>
);

export default Header;
