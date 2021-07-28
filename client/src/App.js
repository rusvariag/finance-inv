// import stuff
import React, { useState } from 'react';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';

// import styles
import './styles.css';

const App = () => {
  // initail state for app
  const initialValues = {
    phoneNumber: '',
  };
  // states
  const [status, setStatus] = useState('calling...');

  // validate form field
  // TODO: build other test for phone number
  const phoneRegExp =
    /^((\\+[1-9]{1,4}[ \\-]*)|(\\([0-9]{2,3}\\)[ \\-]*)|([0-9]{2,4})[ \\-]*)*?[0-9]{3,4}?[ \\-]*[0-9]{3,4}?$/;
  const validationSchema = Yup.object({
    phoneNumber: Yup.string()
      // .matches(phoneRegExp, 'Phone number is not valid')
      .required('Required'),
  });
  // submit handler
  const onSubmitHandler = values => {
    fetch('/call', {
      method: 'POST', // or 'PUT'
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(values),
    })
      .then(response => response.json())
      .then(data => {
        setStatus(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <div className="App">
      <h1>Twilio Outbound Call</h1>
      <main className="main">
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={onSubmitHandler}
        >
          <Form className="form">
            <label className="label" htmlFor="phoneNumber">
              Enter Phone Number
            </label>
            <Field
              className="input-field"
              type="text"
              id="phoneNumber"
              name="phoneNumber"
              placeholder="Phone number"
            />
            <button type="submit" className="btn">
              get started
            </button>
          </Form>
        </Formik>
        <div className="status">{JSON.stringify(status)}</div>
      </main>
    </div>
  );
};

export default App;
