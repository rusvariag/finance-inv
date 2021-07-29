// import stuff
import React, { useState, useRef, useEffect } from 'react';
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import socketIOClient from 'socket.io-client';
import { Device } from '@twilio/voice-sdk';

// import styles
import './styles.css';

// constants
const NEW_EVENT = 'newStatus';

const App = () => {
  const socketRef = useRef();
  const deviceRed = useRef();

  // states
  const [status, setStatus] = useState(undefined);

  // validate form field
  // TODO: build other test for phone number
  const phoneRegExp =
    /^((\\+[1-9]{1,4}[ \\-]*)|(\\([0-9]{2,3}\\)[ \\-]*)|([0-9]{2,4})[ \\-]*)*?[0-9]{3,4}?[ \\-]*[0-9]{3,4}?$/;
  const validationSchema = Yup.object({
    phoneNumber: Yup.string()
      .matches(phoneRegExp, '* Phone number is not valid')
      .required('* Required'),
  });

  // start application services
  useEffect(() => {
    socketRef.current = socketIOClient('/');
    socketRef.current.on(NEW_EVENT, message => {
      setStatus(message);
    });

    fetch('/token')
      .then(res => res.json())
      .then(({ token }) => {
        deviceRed.current = new Device(token, {
          warnings: false,
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);

  // submit handler
  const onSubmitHandler = async values => {
    var params = {
      // get the phone number to call from the DOM
      // MAYBE: add country choice
      phone: `+972${values.phoneNumber}`,
    };
    // Twilio.Device.connect() returns a Call object
    const call = await deviceRed.current.connect({ params });

    // add listeners to the Call
    call.addListener('accept', () => {
      console.log('Call in progress ...');
    });
  };

  return (
    <div className="App">
      <h1>Twilio Outbound Call</h1>
      <main className="main">
        <Formik
          initialValues={{ phoneNumber: '' }}
          validationSchema={validationSchema}
          onSubmit={onSubmitHandler}
        >
          {({ errors, touched }) => (
            <Form className="form">
              <label className="label" htmlFor="phoneNumber">
                Enter Phone Number ( Israel only - without leading zero )
              </label>
              <Field
                className="input-field"
                type="text"
                id="phoneNumber"
                name="phoneNumber"
                placeholder="Phone number"
              />
              {errors.phoneNumber && touched.phoneNumber ? (
                <div className='error'>{errors.phoneNumber}</div>
              ) : null}
              <button type="submit" className="btn">
                get started
              </button>
            </Form>
          )}
        </Formik>
        <div className="status-label">Call status: </div>
        <div className="status">{JSON.stringify(status)}</div>
      </main>
    </div>
  );
};

export default App;
