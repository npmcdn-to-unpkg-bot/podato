var xml = (txt) => {
    var parser, xmlDoc;
    if (window.DOMParser){
        parser=new DOMParser();
        xmlDoc=parser.parseFromString(txt,"text/xml");
    }
    else { // Internet Explorer
        xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
        xmlDoc.async=false;
        xmlDoc.loadXML(txt);
    }
    return xmlDoc;
};

export default xml;
