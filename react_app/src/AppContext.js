import React, { Component, createContext } from 'react';

export const AppContext = createContext();

class AppProvider extends Component {
  state = {
    isLogin: false,
    userData: {
      id: '',
      username: '',
      email: ''
    }
  }
  render() {
    return (
      <AppContext.Provider value={{
           state: this.state,
           authenticateUser: (isLogin, userData) => {
            localStorage.setItem('isLogin', isLogin);
            localStorage.setItem("userData", JSON.stringify(userData))
            // this.setState({
            //   isLogin: isLogin,
            //   userData: userData
            // })
          },
         }} >
        { this.props.children }
      </AppContext.Provider>
    );
  }
}

export default AppProvider;
