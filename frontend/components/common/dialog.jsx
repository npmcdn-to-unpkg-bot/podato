import React from "react";
import ReactModal from "react-modal";

const Dialog = React.createClass({
    componentWillMount(){
        ReactModal.setAppElement(document.body);
    },
    render(){
        return (
            <ReactModal {...this.props}>
                <div className="clearfix bg-red white">
                    <div className="col col-12 px2">
                        <h2>{this.props.title}</h2>
                    </div>
                </div>
                <div className="clearfix  bg-white overflow-scroll">
                    {this.props.children}
                </div>
            </ReactModal>
        )

    }
});

export default Dialog;
