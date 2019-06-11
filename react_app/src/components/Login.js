import React, { Component } from 'react'; 
import axios from 'axios';
import AppBar from 'material-ui/AppBar';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { Redirect } from 'react-router';
import { BrowserRouter, Route, Switch, withRouter } from 'react-router-dom';

import UploadScreen from './UploadScreen';
import {AppContext} from '../AppContext';


const style = {
    margin: 15,
};
class Login extends Component {

    render() {
        return (
          <div>
            <MuiThemeProvider>
                <AppContext.Consumer>
                    {(context) => (
                    <div>
                    <AppBar title="Login" />
                    <TextField
                            hintText="Enter your Username"
                            floatingLabelText="Username"
                            onChange={(event,newValue) => this.setState({username:newValue})}
                         />
                    <br/>
                        <TextField
                            type="password"
                            hintText="Enter your Password"
                            floatingLabelText="Password"
                            onChange = {(event,newValue) => this.setState({password:newValue})}
                        />
                        <br/>
                        <RaisedButton label="Submit" primary={true} style={style} onClick={(event) => this.handleClick(event, context)}/>
                    </div>
                    )}
                </AppContext.Consumer>
             </MuiThemeProvider>
          </div>
        );
      }
    handleClick(event, context) {
        var apiBaseUrl = "http://127.0.0.1:5000/api/";
        var self = this;
        var payload = {
            "username": this.state.username,
            "password": this.state.password
        }
        axios.post(apiBaseUrl + 'login', payload)
            .then(function(response) {
                    console.log(response);
                    if (response.status == 200) {
                            console.log("Login successfull");
                            var uploadScreen = [];
                            self.props.history.push('/home')
                            console.log(response);
                            context.authenticateUser(true,
                             { 
                                id: response.data.id,
                                email: response.data.email,
                                username: response.data.username,
                            } );
                        }
                        else if (response.data.code == 204) {
                            console.log("Username password do not match");
                            alert("username password do not match")
                        } else {
                            console.log("Username does not exists");
                            alert("Username does not exist");
                        }
                    })
                .catch(function(error) {
                    console.log(error);
                });
            }
    }
export default withRouter(Login);