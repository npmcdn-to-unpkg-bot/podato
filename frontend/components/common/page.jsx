import React from "React";

var Page = React.createClass({
    render(){
        return (<div className="bg-white rounded p2 px4">{this.props.children}</div>);
    }
});

export default Page;