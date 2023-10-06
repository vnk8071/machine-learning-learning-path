import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className='App-header'>
        <h1
          onClick={() => {
            this.navTo('');
          }}
        >
          Travia by KhoiVN
        </h1>
        <h2
          onClick={() => {
            this.navTo('');
          }}
        >
          List Questions
        </h2>
        <h2
          onClick={() => {
            this.navTo('/add');
          }}
        >
          Add Question
        </h2>
        <h2
          onClick={() => {
            this.navTo('/play');
          }}
        >
          Play Quizz
        </h2>
      </div>
    );
  }
}

export default Header;
