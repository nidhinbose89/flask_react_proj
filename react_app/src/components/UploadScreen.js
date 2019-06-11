import React, { Component } from 'react';
import axios from 'axios';
import AppBar from 'material-ui/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';

import { withRouter } from "react-router";
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {NavLink} from "react-router-dom";

import Login from './Login';
import {AppContext} from '../AppContext';

const style = {
    margin: 15,
};
class UploadScreen extends Component {
    constructor(props) {
        super(props);
        console.log(props)
    }
    handleClick(context) {
        var apiBaseUrl = "http://127.0.0.1:5000/api/";
        var self = this;

        axios.post(apiBaseUrl + 'logout')
            .then(function(response) {
                    console.log(response);
                    if (response.status == 200) {
                            console.log("Logout successfull");
                            var uploadScreen = [];
                            self.props.history.push('/login')
                            console.log(response);
                            context.authenticateUser(false, {} );
                        } else {
                            alert("Error while logout.");
                        }
                    })
                .catch(function(error) {
                    console.log(error);
                });


    }
    render() {
      let userData;
      if (localStorage.getItem('isLogin')) {
        userData = JSON.parse(localStorage.getItem('userData'));
      } else {
        userData = null
      }
      return (
        <div>
          <MuiThemeProvider>
          <AppContext.Consumer>
            {
              (context) => (
                    <div>
                      <AppBar title="Select Charts" position="static">
                        <Toolbar>
                          <Button color="inherit" onClick={() => this.handleClick(context)}>{ localStorage.getItem('isLogin') ? "Logout": "LogIn"}</Button>
                        </Toolbar>
                      </AppBar>
                      is auth  { localStorage.getItem('isLogin') ? "Logged in": "Not Logged in"}
                      <p>{userData.email || ''} </p>
                    </div>
              )}
          </AppContext.Consumer>
         </MuiThemeProvider>
      </div>
      );
    }

    }
// export default withRouter(UploadScreen);
export default withRouter(UploadScreen);
