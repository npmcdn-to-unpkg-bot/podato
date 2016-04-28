import React from "react";
import ReactDOM from  "react-dom";
import {connect} from "react-redux";
import {Link} from "react-router";

import SearchResults from "./search-results.jsx";
import {search} from "../../actions/search-actions";

//todo Extract the div and input into a SearchInput component, so this can purely be a container.
const SearchBox = React.createClass({
    render(){
        const showResults = ((this.state.focus && this.props.results != null) || this.props.loading);
        const results = showResults ? <SearchResults results={this.props.results} fetching={this.props.loading} resultClicked={this.resultClicked} /> : null;
        //TODO move blur handler to the div, so that focussing on the search results doesn't hide them.
        return (
            <div {...this.props} style={{padding:"0.5rem"}}>
                <input type="search" name="search" style={{height:"1.5rem", width:"100%"}} placeholder="Find great podcasts." ref="input"
                    onFocus={this.focus} onChange={this.change} onBlur={this.blur} />
                {results}
            </div>
        )
    },
    getInitialState(){
        return {
            focus: false
        }
    },
    focus(){
        this.setState({focus: true});
    },
    blur(){
        //TODO I don't remember why I used setTimeout here. I probably should have left a comment explaining why.
        //It might be useful to experiment with this, and see what happens when it is removed.
        setTimeout( () => this.setState({focus: false}));
    },
    change(){
        const query = ReactDOM.findDOMNode(this.refs.input).value.trim();
        if(query.length > 3){
            search(query);
        }
    },
    resultClicked(res){
        ReactDOM.findDOMNode(this.refs.input).blur()
        ReactDOM.findDOMNode(this.refs.input).value = res.trackName;
    }
});

export default connect((state) => state.get("search").toObject())(SearchBox);