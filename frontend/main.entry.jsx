import React from 'react';
import {render} from 'react-dom';
import { RelayRouter } from 'react-router-relay';
import {Router, Route, IndexRoute, browserHistory } from 'react-router'
import {provider} from 'react-redux';
import Relay from 'react-relay';

import store from "./store";
import {getQueries} from "./queries.js";

const App = require("./components/app.jsx");
const Home = require("./components/pages/home.jsx");
const Podcast = require("./components/pages/podcast.jsx");
const User = require("./components/pages/user.jsx");

Relay.injectNetworkLayer(
  new Relay.DefaultNetworkLayer('/graphql/', {
      credentials: "include",
      headers: {
          "X-CSRFToken": cookies.get("csrftoken")
      }
  })
);

const routes = (
    <RelayRouter history={browserHistory}>
        <Route path="/" component={App} queries={getQueries(["currentUser"])}>
            <IndexRoute component={Home} queries={getQueries(["currentUser"])} />
        </Route>
    </RelayRouter>
);

//wrap them with the react-redux provider
const root = (<Provider store={store}>routes</Provider>);

docReady(() => {
    ReactDOM.render(root, document.getElementById("app"));
});
