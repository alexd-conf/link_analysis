import React from 'react';
import styles from './Input.module.css';

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import Output from '../Output/Output';

class Input extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      url: '',
      data: [],
      loading: false,
      error: false,
      errorMessage: ''
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    event.preventDefault();
    this.setState({url: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    
    this.setState({loading: true});

    // send a POST request to the backend's link endpoint
    //  where the body contains the target URL
    const options = { 
      method: 'POST',
      body: JSON.stringify({url: this.state.url})
    }
    fetch(process.env.REACT_APP_SERVER_URL + "/link", options)
    .then(res => res.json())
    .then(
      (result) => {
        // status equals 0 if there were no errors
        if (result['status'] !== 0) {
          // if there is an error, render the message sent from the backend
          this.setState({data: [], errorMessage: result['message'], error: true, loading: false})
        } else {
          // if there was no error, render the data sent from the backend
          this.setState({data: result['data'], error: false, loading: false});
        }
      },
      (error) => {
        // if there is an error with the request itself, render a generic error message
        let message = "An error has occurred, please try again.";
        this.setState({data: [], errorMessage: message, error: true, loading: false});
      }
    )
  }

  render() {
    return (
      <div>
        <div className={styles.input} data-testid="Input">
          <Form onSubmit={this.handleSubmit}>
            <Form.Group controlId="linkForm">
              <Form.Control data-testid="InputBar" onChange={this.handleChange} className={styles.linkBar} placeholder="Paste link here, http(s) and all" />
            </Form.Group>
            {this.state.loading?
            <Button data-testid="InputButtonLoading" className={styles.submitButton} variant="primary" disabled>
              <div className={styles.loader}></div>
            </Button>:
            <Button data-testid="InputButton" className={styles.submitButton} variant="primary" type="submit">
              Analyze
            </Button>}
          </Form>
        </div>
        <Output className={styles.output} data={this.state.data} errorMessage={this.state.errorMessage} error={this.state.error} />
      </div>
    );
  }
}

export default Input;
