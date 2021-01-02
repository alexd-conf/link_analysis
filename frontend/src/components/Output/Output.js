import React from 'react';
import PropTypes from 'prop-types';
import styles from './Output.module.css';

import ListGroup from 'react-bootstrap/ListGroup';

class Output extends React.Component {

  render() {
    // get the error message, whether one was passed or the default
    let errorMessage = this.props.errorMessage;
    // get the error state, whether one was passed or the default
    let error = this.props.error;
    // initialize what will be rendered
    let result = null;

    // if there is no error, the result to be rendered contains the data passed from the backend
    if (error === false) {
      // get the data passed from the backend
      let data = this.props.data;
      // turn the data passed from the backend into ListGroup Items to be rendered
      result = data.map(
        (datum, d) =>
        <div key={d} className={styles.wrapper} data-testid="OutputData">
          {/* category */}
          <div className={styles.category}>{datum['category']}</div>
          <ListGroup>
            {/* items */}
            {datum['content'].map(
              (item, i) =>
                <ListGroup.Item key={i} variant="secondary" className={styles.item}><span className={styles.bullet}>*</span>{item}</ListGroup.Item>
            )}
          </ListGroup>
        </div>
      );
    // if there is an error, the result to be rendered contains an error message
    } else {
      result =
        <div className={styles.wrapper}>
          <div className={styles.error} data-testid="OutputError">{errorMessage}</div>
        </div>
    }

    // render the result from above
    return (
      <div className={styles.output} data-testid="Output">
        {result}
      </div>
    );
  }
}

Output.propTypes = {
  data: PropTypes.array,
  error: PropTypes.bool,
  errorMessage: PropTypes.string
};

Output.defaultProps = {
  data: [],
  error: false,
  errorMessage: ''
};

export default Output;
