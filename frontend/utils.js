var utils = {
    encodeQueryString(obj) {
        var pairs = [];
        for(var key in obj){
            if(obj.hasOwnProperty(key) && obj[key] !== void(0)) {
                pairs.push(key + "=" + encodeURIComponent(obj[key]));
            }
        }
        return "?" + pairs.join("&");
    },
    unique(a){
        return a.filter(function(item, pos, self) {
            return self.indexOf(item) == pos;
        })
    },
    naturalSort(strings, key){
        var sorted = strings.sort((a, b) => {
            if(key){
                a = key(a);
                b = key(b);
            }
            a = a.trim().toLowerCase();
            b = b.trim().toLowerCase();

            if(a.startsWith("the ")){
                a = a.slice(4).trim();
            }
            if(b.startsWith("the ")){
                b = b.slice(4).trim();
            }
            console.log("comparing "+a+" and "+b);
            if(a < b){
                return -1
            } else if(b < a){
                return 1
            }else{
                return 0
            }
        });
        console.log("sorted:");
        console.log(sorted);
        return sorted;
    },

    formatTime(d){
        const seconds = d % 60;
        d = d - seconds;
        const minutes = (d % 3600)/60
        d = d - minutes*60;
        const hours = d / 3600;
        var s = this.padNumber(minutes, 2) + ":" + this.padNumber(seconds, 2)
        if(hours > 0){
            s = this.padNumber(hours, 2) + ":" + s;
        }
        return s;
    },

    padNumber(n, l){
        n = Math.floor(n) + '';
        return n.length >= l ? n : new Array(l - n.length + 1).join("0") + n;
    },

    fetchJSONP(baseurl, params){
        const script = document.createElement("script");
        const callback = "_cb_" + new Date().getTime();
        params.callback = callback;
        return new Promise((resolve, reject) => {
            window[callback] = resolve;
            script.onError = reject;
            script.src = baseurl + this.encodeQueryString(params);
            document.head.appendChild(script);
        });
    }
};

export default utils;
