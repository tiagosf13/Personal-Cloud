try {
    (function(w, d) {
        !function(kL, kM, kN, kO) {
            kL[kN] = kL[kN] || {};
            kL[kN].executed = [];
            kL.zaraz = {
                deferred: [],
                listeners: []
            };
            kL.zaraz.q = [];
            kL.zaraz._f = function(kP) {
                return async function() {
                    var kQ = Array.prototype.slice.call(arguments);
                    kL.zaraz.q.push({
                        m: kP,
                        a: kQ
                    })
                }
            };
            for (const kR of ["track", "set", "debug"])
                kL.zaraz[kR] = kL.zaraz._f(kR);
            kL.zaraz.init = () => {
                var kS = kM.getElementsByTagName(kO)[0],
                    kT = kM.createElement(kO),
                    kU = kM.getElementsByTagName("title")[0];
                kU && (kL[kN].t = kM.getElementsByTagName("title")[0].text);
                kL[kN].x = Math.random();
                kL[kN].w = kL.screen.width;
                kL[kN].h = kL.screen.height;
                kL[kN].j = kL.innerHeight;
                kL[kN].e = kL.innerWidth;
                kL[kN].l = kL.location.href;
                kL[kN].r = kM.referrer;
                kL[kN].k = kL.screen.colorDepth;
                kL[kN].n = kM.characterSet;
                kL[kN].o = (new Date).getTimezoneOffset();
                if (kL.dataLayer)
                    for (const kY of Object.entries(Object.entries(dataLayer).reduce(((kZ, k$) => ({ ...kZ[1], ...k$[1] })), {}))) zaraz.set(kY[0], kY[1], { scope: "page" });
                kL[kN].q = [];
                for (; kL.zaraz.q.length;) {
                    const la = kL.zaraz.q.shift();
                    kL[kN].q.push(la)
                }
                kT.defer = !0;
                for (const lb of [localStorage, sessionStorage]) Object.keys(lb || {}).filter((ld => ld.startsWith("_zaraz_"))).forEach((lc => {
                    try {
                        kL[kN]["z_" + lc.slice(7)] = JSON.parse(lb.getItem(lc))
                    } catch {
                        kL[kN]["z_" + lc.slice(7)] = lb.getItem(lc)
                    }
                }));
                kT.referrerPolicy = "origin";
                kT.src = "/cdn-cgi/zaraz/s.js?z=" + btoa(encodeURIComponent(JSON.stringify(kL[kN])));
                kS.parentNode.insertBefore(kT, kS)
            };
            ["complete", "interactive"].includes(kM.readyState) ? zaraz.init() : kL.addEventListener("DOMContentLoaded", zaraz.init)
        }(w, d, "zarazData", "script");
    })(window, document)
} catch (e) {
    throw fetch("/cdn-cgi/zaraz/t"), e;
};


window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'UA-23581568-13');
