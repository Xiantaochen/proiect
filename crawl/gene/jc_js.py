HashCode = '''
function encode(e) {
     return window.OO00 = {
                    encode: function(e) {
                        var t, l, r, n, i, o;
                        for (e = utf16to8(e),
                        r = e.length,
                        l = 0,
                        t = ""; l < r; ) {
                            if (n = 255 & e.charCodeAt(l++),
                            l == r) {
                                t += a.charAt(n >> 2),
                                t += a.charAt((3 & n) << 4),
                                t += "==";
                                break
                            }
                            if (i = e.charCodeAt(l++),
                            l == r) {
                                t += a.charAt(n >> 2),
                                t += a.charAt((3 & n) << 4 | (240 & i) >> 4),
                                t += a.charAt((15 & i) << 2),
                                t += "=";
                                break
                            }
                            o = e.charCodeAt(l++),
                            t += a.charAt(n >> 2),
                            t += a.charAt((3 & n) << 4 | (240 & i) >> 4),
                            t += a.charAt((15 & i) << 2 | (192 & o) >> 6),
                            t += a.charAt(63 & o)
                        }
                    },
                    encodeHash: function() {
                        var e;
                        return e = OOO0.excess.indexOf("Chrome") >= 0 ? "cv3sdf@#$f3" : OOO0.excess.indexOf("Firefox") >= 0 ? "df23Sc@sS" : "vdf@s4df9sd@s2"
                    },
                    setCode: function() {
                        return "vxcasd#$asDG#$dwe"
                    }
                },
                OOOO.encode(e)
}
'''
