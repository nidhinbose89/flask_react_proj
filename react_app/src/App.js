import React, { Component, createContext } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Switch, withRouter } from 'react-router-dom';

import './App.css';

import Login from './components/Login';
import Register from './components/Register';
import UploadScreen from './components/UploadScreen';
import Loginscreen from './components/Loginscreen'
import URLNotFound from './components/URLNotFound'
import AppProvider from './AppContext'

const style = {
  margin: 15,
};


class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <AppProvider>
            <Switch>
              <Route path="/home" component={UploadScreen} exact/>
              <Route path="/login" component={Loginscreen} exact/>
              <Route path="/" component={Loginscreen} exact/>
              <Route path="/register" component={Register} exact/>
              <Route component={URLNotFound}/>
            </Switch>
          </AppProvider>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
