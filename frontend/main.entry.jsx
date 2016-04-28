import React from 'react';
import {render} from 'react-dom';
import {Router, Route, IndexRoute, browserHistory } from 'react-router'


const App = require("./components/app.jsx");
const Home = require("./components/pages/home.jsx");
const Podcast = require("./components/pages/podcast.jsx");
const User = require("./components/pages/user.jsx");

const routes = (
    <Router history={browserHistory}>
        <Route path="/" component={App}>
            <IndexRoute component={Home} />
            <Route path="podcasts/*" component={Podcast} />
            <Route path="users/:userId" component={User} />
        </Route>
        <Route path="/graphql" component={GraphQL}/>
    </Router>
);

window.ReactRouter = ReactRouter;

docReady(() => {
    ReactDOM.render(routes, document.getElementById("app"));
});
