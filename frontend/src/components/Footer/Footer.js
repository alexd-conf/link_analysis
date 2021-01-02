import React from 'react';
import styles from './Footer.module.css';

import Output from '../Output/Output';

class Footer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      error: false,
      errorMessage: ''
    };
  }

  componentDidMount() {
    // send a GET request to the backend's health endpoint
    const options = { 
      method: 'GET',
    }
    fetch(process.env.REACT_APP_SERVER_URL + "/health", options)
    .then(res => res.json())
    .then(
      (result) => {
        this.setState({data: result['data'], error: false});
      },
      (error) => {
        // if there is an error with the request itself, render a generic error message
        let message = "Could not reach the server at this time.";
        this.setState({data: [], errorMessage: message, error: true});
      }
    )
  }

  render() {
    return (
      <div className={styles.output} data-testid="Footer">
        <Output className={styles.output} data={this.state.data} errorMessage={this.state.errorMessage} error={this.state.error}/>
      </div>
    );
  }
}

export default Footer;
