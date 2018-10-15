import React, { Component } from 'react';
import './App.css';
const logo = require("./loading.gif");
const axios = require('axios');

class App extends Component {

  state = {
    url: "",
    depth: "",
    data: {},
    loading: false
  }

  getCrawledData = (event) => {
    event.stopPropagation();
    event.preventDefault();
    const body = {
      seed_url: this.state.url,
      depth: parseInt(this.state.depth)
    }
    this.setState({
      loading: true
    })
    axios({
      url: 'http://127.0.0.1:8000/crawl/',
      method: 'POST',
      mode: 'no-cors',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      data: JSON.stringify(body)
    })
    .then((response) => {
      console.log(response);
      this.setState({
        data: response.data,
        loading: false
      });
    })
    .catch((error) => {
      console.log(error)
    })
  };

  handleOnChange = (event, label) => {
    const updatedKeyword = event.target.value;
    this.setState({
      [label]: updatedKeyword
    })
  }

  render() {
    return (
      <div className="App container">
        <form className="row">
          <div className="form-group flex-row col-sm-7">
            <label className="label-width">URL</label>
            <input type="url" value={this.state.url}
              onChange={(event) => this.handleOnChange(event, 'url')} className="flex-1 form-control" />
          </div>
          <div className="form-group flex-row col-sm-4">
            <label className="label-width">Depth</label>
            <input type="number" value={this.state.depth} min="1" max="10"
              onChange={(event) => this.handleOnChange(event, 'depth')} className="flex-1 form-control" />
          </div>
          <div className="form-group col-sm-1">
            <button type="submit" className="btn btn-primary" onClick={this.getCrawledData}>Crawl</button>
          </div>
        </form>
        {
          this.state.loading ?
            <div className="text-center">
              <img width="150" src={logo} alt="loading ..." />
            </div> :
            <div>
              {
                this.state && this.state.data && Object.keys(this.state.data).map((url, key) => {
                  return (
                    <div key={key}>
                      <div className="url-text">
                        <a href={url} target="_blank" rel='noopener noreferrer'>{url}</a>
                      </div>
                      <div className="row">
                        {
                          this.state.data[url].urls.map((img, key1) => {
                            return (
                              <div key={key + "" + key1} className="col-sm-3">
                                <img src={img} className="max-width" />
                              </div>
                            )
                          })
                        }
                      </div>
                    </div>
                  )
                })
              }
            </div>
        }
      </div>
    );
  }
}

export default App;
