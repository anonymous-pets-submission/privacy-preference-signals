(function () {
    function logInfo(data) {
        console.info("\x3cngfetch-info\x3e" + JSON.stringify(data) + "\x3c/ngfetch-info\x3e");
    }

    /* Check if there is a TCFv1/TCFv2 API, and interact with it if so. */
    ["__tcfapi", "__cmp"].forEach(function (cmpfun) {
        if (!window[cmpfun]) return;

        let logged_waiting = false;
        let ping = window.setInterval(function () {
            window[cmpfun]("ping", null, function (pong, success) {
                /* Some TCF implementations reply before being done, so we need to re-submit our ping. */
                if (pong && !pong.cmpLoaded && !logged_waiting) {
                    logInfo({type: "cmp-ping-waiting", cmpfun, pong, success})
                    logged_waiting = true;
                }
                if (pong && pong.cmpLoaded) {
                    logInfo({type: "cmp-ping-done", cmpfun, pong, success})
                    window.clearInterval(ping);
                }
            });
        }, 1);

    });

    logInfo({
        type: "js-info",
        data: Object.keys(window)
    });
})();
