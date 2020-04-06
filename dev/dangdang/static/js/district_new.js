var District = function () {
    this.provinceChanged = false
};
var fourareajson = {
    ALL: {
        "111": "\u5317\u4eac",
        "112": "\u5929\u6d25",
        "113": "\u6cb3\u5317",
        "114": "\u5c71\u897f",
        "115": "\u5185\u8499\u53e4",
        "121": "\u8fbd\u5b81",
        "122": "\u5409\u6797",
        "123": "\u9ed1\u9f99\u6c5f",
        "131": "\u4e0a\u6d77",
        "132": "\u6c5f\u82cf",
        "133": "\u6d59\u6c5f",
        "134": "\u5b89\u5fbd",
        "135": "\u798f\u5efa",
        "136": "\u6c5f\u897f",
        "137": "\u5c71\u4e1c",
        "141": "\u6cb3\u5357",
        "142": "\u6e56\u5317",
        "143": "\u6e56\u5357",
        "144": "\u5e7f\u4e1c",
        "145": "\u5e7f\u897f",
        "146": "\u6d77\u5357",
        "150": "\u91cd\u5e86",
        "151": "\u56db\u5ddd",
        "152": "\u8d35\u5dde",
        "153": "\u4e91\u5357",
        "154": "\u897f\u85cf",
        "161": "\u9655\u897f",
        "162": "\u7518\u8083",
        "163": "\u9752\u6d77",
        "164": "\u5b81\u590f",
        "165": "\u65b0\u7586",
        "171": "\u53f0\u6e7e",
        "172": "\u9999\u6e2f",
        "173": "\u6fb3\u95e8",
        "000": "\u9493\u9c7c\u5c9b"
    }
};
District.prototype = {
    bindEvent: function () {
        function Hide(e) {
            if ($(e.target).hasClass("area_pop") || $(e.target).parents().hasClass("area_pop") || $(e.target).hasClass("fn-select-address")) {
            } else {
                $(".area_pop").hide()
            }
            if ($(e.target).hasClass("fn-ck") || $(e.target).parents().hasClass("fn-ck")) {
            } else {
                $("#ck_tip").hide()
            }
        }

        function show_area_pop(e) {
            $(".area_pop").show();
            var chooseObj = $(e.target).parent().find("li.choose a");
            if (chooseObj.parent().hasClass("fn-show-province")) {
                show_province()
            } else {
                if (chooseObj.parent().prev().hasClass("fn-show-province")) {
                    $(".fn-show-city").show();
                    $(".fn-show-area").hide();
                    $(".fn-show-village").hide();
                    district.show_city_init(chooseObj)
                } else {
                    if (chooseObj.parent().prev().hasClass("fn-show-city")) {
                        $(".fn-show-area").show();
                        $(".fn-show-village").hide();
                        district.show_area_init(chooseObj)
                    } else {
                        if (chooseObj.parent().prev().hasClass("fn-show-area")) {
                            $(".fn-show-village").show();
                            district.show_village_init(chooseObj)
                        }
                    }
                }
            }
        }

        function show_province(e) {
            $.ajax({
                type: "GET", url: "get_province", cache: false, dataType: "json", success: function (result) {
                    if (result && result.code === -3) {
                        return false
                    }
                    if ("0" != result.code) {
                        alert("获取地区信息失败!");
                        return
                    } else {
                        $(".fn-show-city").hide();
                        $(".fn-show-area").hide();
                        $(".fn-show-village").hide();
                        $(".fn-show-city").removeClass("choose");
                        $(".fn-show-province").addClass("choose");
                        $(".fn-show-area").removeClass("choose");
                        $(".fn-show-village").removeClass("choose");
                        var area = eval("fourareajson.ALL;");
                        var html = "";
                        for (var i in area) {
                            html += "<li><a href=\"javascript:district.select_province('" + i + '\')" id="province_' + i + '">' + area[i] + "</a></li>"
                        }
                        $("ul.fn-adress").html(html)
                    }
                }, error: function () {
                    alert("系统异常，请联系当当管理员")
                }
            })
        }

        $(document).bind("click", Hide);
        $(".fn-select-address").bind("click", show_area_pop);
        $(".fn-show-province").bind("click", show_province)
    }, close: function () {
        $(".area_pop").hide()
    }, show_city_init: function (a) {
        if (!$(a).hasClass("fn-show-city")) {
            a = $(".fn-show-city a")
        }
        var b = $(a).parent().prev().find("a").attr("id").split("_")[1];
        if (b != "-1") {
            $.ajax({
                type: "GET",
                url: "get_city",
                cache: false,
                data: {province_id: b},
                dataType: "json",
                success: function (c) {
                    if (c && c.code === -3) {
                        return false
                    }
                    if ("0" != c.code) {
                        alert("获取地区信息失败!");
                        return
                    } else {
                        $(".fn-show-city").addClass("choose");
                        $(".fn-show-province").removeClass("choose");
                        $(".fn-show-area").removeClass("choose");
                        $(".fn-show-village").removeClass("choose");
                        $(".fn-show-area").hide();
                        $(".fn-show-village").hide();
                        var f = "";
                        if (c.body.data) {
                            for (var e = 0; e < c.body.data.length; e++) {
                                var g = c.body.data[e].province_id;
                                var h = c.body.data[e].city_id;
                                var d = c.body.data[e].city_name;
                                f += "<li><a href=\"javascript:district.select_city('" + g + "','" + h + '\')" id="city_' + h + '">' + d + "</a></li>"
                            }
                            $("ul.fn-adress").html(f)
                        }
                    }
                },
                error: function () {
                    alert("系统异常，请联系当当管理员")
                }
            })
        }
    }, show_area_init: function (c) {
        if (!$(c).hasClass("fn-show-area")) {
            c = $(".fn-show-area a")
        }
        var b = $(c).parent().prev().find("a").attr("id").split("_")[1];
        var a = $(c).parent().prev().prev().find("a").attr("id").split("_")[1];
        if (b != "-1" && a != "-1") {
            $.ajax({
                type: "GET",
                url: "get_area",
                cache: false,
                data: {city_id: b, province_id: a},
                dataType: "json",
                success: function (d) {
                    if (d && d.code === -3) {
                        return false
                    }
                    if ("0" != d.code) {
                        alert("获取地区信息失败!");
                        return
                    } else {
                        $(".fn-show-city").removeClass("choose");
                        $(".fn-show-province").removeClass("choose");
                        $(".fn-show-area").addClass("choose");
                        $(".fn-show-village").removeClass("choose");
                        $(".fn-show-village").hide();
                        var h = "";
                        if (d.body.data) {
                            for (var g = 0; g < d.body.data.length; g++) {
                                var j = d.body.data[g].province_id;
                                var k = d.body.data[g].city_id;
                                var f = d.body.data[g].area_id;
                                var e = d.body.data[g].area_name;
                                h += "<li><a href=\"javascript:district.select_area('" + j + "','" + k + "','" + f + '\')" id="area_' + f + '">' + e + "</a></li>"
                            }
                            $("ul.fn-adress").html(h)
                        }
                    }
                },
                error: function () {
                    alert("系统异常，请联系当当管理员")
                }
            })
        }
    }, show_village_init: function (d) {
        if (!$(d).hasClass("fn-show-village")) {
            d = $(".fn-show-village a")
        }
        var c = $(d).parent().prev().find("a").attr("id").split("_")[1];
        var b = $(d).parent().prev().prev().find("a").attr("id").split("_")[1];
        var a = $(d).parent().prev().prev().prev().find("a").attr("id").split("_")[1];
        if (b != "-1" && a != "-1" && c != "-1") {
            $.ajax({
                type: "GET",
                url: "get_village",
                cache: false,
                data: {city_id: b, province_id: a, area_id: c},
                dataType: "json",
                success: function (e) {
                    if (e && e.code === -3) {
                        return false
                    }
                    if ("0" != e.code) {
                        alert("获取地区信息失败!");
                        return
                    } else {
                        var j = "";
                        if (e.body.data) {
                            for (var h = 0; h < e.body.data.length; h++) {
                                var l = e.body.data[h].province_id;
                                var m = e.body.data[h].city_id;
                                var g = e.body.data[h].area_id;
                                var f = e.body.data[h].village_id;
                                var k = e.body.data[h].village_name;
                                j += "<li><a href=\"javascript:district.select_village('" + l + "','" + m + "','" + g + "','" + f + '\')" id="village_' + f + '">' + k + "</a></li>"
                            }
                            $("ul.fn-adress").html(j)
                        }
                    }
                },
                error: function () {
                    alert("系统异常，请联系当当管理员")
                }
            })
        }
    }, select_province: function (a) {
        if (a == "000") {
            return
        }
        if (district.get_cookie_province_id() != a) {
            district.provinceChanged = true
        }
        $.ajax({
            type: "GET",
            url: "get_city",
            cache: false,
            data: {province_id: a},
            dataType: "json",
            success: function (c) {
                if (c && c.code === -3) {
                    return false
                }
                if ("0" != c.code) {
                    alert("获取地区信息失败!");
                    return
                } else {
                    $(".fn-show-city").show();
                    var b = $(".fn-show-province a");
                    b.text($("#province_" + a).text());
                    b.attr("id", "selected_" + a);
                    var g = "";
                    if (c.body.data) {
                        for (var f = 0; f < c.body.data.length; f++) {
                            var h = c.body.data[f].province_id;
                            var j = c.body.data[f].city_id;
                            var e = c.body.data[f].city_name;
                            g += "<li><a href=\"javascript:district.select_city('" + h + "','" + j + '\')" id="city_' + j + '">' + e + "</a></li>"
                        }
                    }
                    $("ul.fn-adress").html(g);
                    if (c.body.length == 1) {
                        $(".fn-show-area").show();
                        $(".fn-show-city").removeClass("choose");
                        $(".fn-show-province").removeClass("choose");
                        $(".fn-show-area").addClass("choose");
                        $(".fn-show-village").removeClass("choose");
                        $(".fn-show-village").hide();
                        var j = $("ul.fn-adress a").attr("id").split("_")[1];
                        district.select_city(a, j)
                    } else {
                        if (c.body.length > 1) {
                            $(".fn-show-area").hide();
                            $(".fn-show-village").hide();
                            $(".fn-show-city").addClass("choose");
                            $(".fn-show-province").removeClass("choose");
                            $(".fn-show-area").removeClass("choose");
                            $(".fn-show-village").removeClass("choose")
                        }
                        var d = $(".fn-show-city a");
                        d.text("请选择");
                        d.attr("id", "selected_-1")
                    }
                }
            },
            error: function () {
                alert("系统异常，请联系当当管理员")
            }
        })
    }, select_city: function (a, b) {
        $.ajax({
            type: "GET",
            url: "get_area",
            cache: false,
            data: {city_id: b, province_id: a},
            dataType: "json",
            success: function (o) {
                if (o && o.code === -3) {
                    return false
                }
                if ("0" != o.code) {
                    alert("获取地区信息失败!");
                    return
                } else {
                    var l = $(".fn-show-city a");
                    l.text($("#city_" + b).text());
                    l.attr("id", "selected_" + b);
                    var k = "";
                    if (o.body.data) {
                        for (var j = 0; j < o.body.data.length; j++) {
                            var g = o.body.data[j].province_id;
                            var h = o.body.data[j].city_id;
                            var d = o.body.data[j].area_id;
                            var m = o.body.data[j].area_name;
                            k += "<li><a href=\"javascript:district.select_area('" + g + "','" + h + "','" + d + '\')" id="area_' + d + '">' + m + "</a></li>"
                        }
                    }
                    $("ul.fn-adress").html(k);
                    if (o.body.length == 1) {
                        var f = $("ul.fn-adress a").attr("id").split("_")[1];
                        district.select_area(a, b, f);
                        $(".fn-show-village").show();
                        $(".fn-show-city").removeClass("choose");
                        $(".fn-show-province").removeClass("choose");
                        $(".fn-show-area").removeClass("choose");
                        $(".fn-show-village").addClass("choose")
                    } else {
                        $(".fn-show-province").removeClass("choose");
                        $(".fn-show-village").removeClass("choose");
                        var e = $(".fn-show-area a");
                        e.text("请选择");
                        e.attr("id", "selected_-1");
                        if (o.body.length > 1) {
                            $(".fn-show-area").addClass("choose");
                            $(".fn-show-city").removeClass("choose");
                            $(".fn-show-area").show()
                        } else {
                            $(".fn-show-area").removeClass("choose");
                            $(".fn-show-city").addClass("choose");
                            var n = $(".fn-show-province a").text();
                            var c = $(".fn-show-city a").text();
                            $(".fn-select-address").text(n + c);
                            if (n == "香港" || n == "澳门") {
                                $(".fn-select-address").text(c)
                            }
                            $(".area_pop").hide();
                            $.cookie.raw = true;
                            $.cookie("dest_area", escape("country_id=9000&province_id=" + a + "&city_id=" + b + "&district_id=0&town_id=0"), {
                                expires: 365,
                                path: "/",
                                domain: "dangdang.com"
                            });
                            if (district.should_refresh_cart(NAMESPACE_CART.need4LevelCacheProvinceId)) {
                                cart.commit("newShow");
                                district.provinceChanged = false
                            }
                        }
                    }
                }
            },
            error: function () {
                alert("系统异常，请联系当当管理员")
            }
        })
    }, select_area: function (a, c, b) {
        $.ajax({
            type: "GET",
            url: "get_village",
            cache: false,
            data: {city_id: c, province_id: a, area_id: b},
            dataType: "json",
            success: function (r) {
                if (r && r.code === -3) {
                    return false
                }
                if ("0" != r.code) {
                    alert("获取地区信息失败!");
                    return
                } else {
                    var h = $(".fn-show-area a");
                    h.text($("#area_" + b).text());
                    h.attr("id", "selected_" + b);
                    var o = "";
                    if (r.body.data) {
                        for (var n = 0; n < r.body.data.length; n++) {
                            var k = r.body.data[n].province_id;
                            var l = r.body.data[n].city_id;
                            var f = r.body.data[n].area_id;
                            var q = r.body.data[n].village_id;
                            var m = r.body.data[n].village_name;
                            o += "<li><a href=\"javascript:district.select_village('" + k + "','" + l + "','" + f + "','" + q + '\')" id="village_' + q + '">' + m + "</a></li>"
                        }
                    }
                    $("ul.fn-adress").html(o);
                    if (r.body.length == 1) {
                        $(".fn-show-city").removeClass("choose");
                        $(".fn-show-province").removeClass("choose");
                        $(".fn-show-area").removeClass("choose");
                        $(".fn-show-village").addClass("choose");
                        var j = $("ul.fn-adress a").attr("id").split("_")[1];
                        district.select_village(a, c, b, j)
                    } else {
                        var e = $(".fn-show-village a");
                        if (r.body.length > 1) {
                            $(".fn-show-city").removeClass("choose");
                            $(".fn-show-province").removeClass("choose");
                            $(".fn-show-area").removeClass("choose");
                            $(".fn-show-village").addClass("choose");
                            e.text("请选择");
                            e.attr("id", "selected_-1");
                            $(".fn-show-village").show()
                        } else {
                            var p = $(".fn-show-province a").text();
                            var d = $(".fn-show-city a").text();
                            var g = $(".fn-show-area a").text();
                            $(".fn-select-address").text(p + d + g);
                            if (p == "北京" || p == "上海" || p == "天津" || p == "重庆" || p == "香港" || p == "澳门") {
                                $(".fn-select-address").text(d + g)
                            }
                            $(".area_pop").hide();
                            $.cookie.raw = true;
                            $.cookie("dest_area", escape("country_id=9000&province_id=" + a + "&city_id=" + c + "&district_id=" + b + "&town_id=0"), {
                                expires: 365,
                                path: "/",
                                domain: "dangdang.com"
                            });
                            if (district.should_refresh_cart(NAMESPACE_CART.need4LevelCacheProvinceId)) {
                                cart.commit("newShow");
                                district.provinceChanged = false
                            }
                        }
                    }
                }
            },
            error: function () {
                alert("系统异常，请联系当当管理员")
            }
        })
    }, select_village: function (i, b, e, g) {
        var c = $(".fn-show-village a");
        c.text($("#village_" + g).text());
        c.attr("id", "selected_" + g);
        var h = $(".fn-show-province a").text();
        var a = $(".fn-show-city a").text();
        var d = $(".fn-show-area a").text();
        var f = c.text();
        $(".fn-select-address").text(h + a + d + f);
        if (h == "北京" || h == "上海" || h == "天津" || h == "重庆" || h == "香港" || h == "澳门") {
            $(".fn-select-address").text(a + d + f)
        }
        $(".area_pop").hide();
        $.cookie.raw = true;
        $.cookie("dest_area", escape("country_id=9000&province_id=" + i + "&city_id=" + b + "&district_id=" + e + "&town_id=" + g), {
            expires: 365,
            path: "/",
            domain: "dangdang.com"
        });
        if (district.should_refresh_cart(NAMESPACE_CART.need4LevelCacheProvinceId)) {
            cart.commit("newShow");
            district.provinceChanged = false
        }
    }, get_cookie_province_id: function () {
        var c = $.cookie("dest_area");
        c = decodeURIComponent(c);
        var b = c.split("&");
        for (var a in b) {
            if (b[a].indexOf("province_id=") >= 0) {
                return b[a].split("=")[1]
            }
        }
        return ""
    }, should_refresh_cart: function (a) {
        return a.indexOf(",2_" + district.get_cookie_province_id() + ",") >= 0 || district.provinceChanged
    }
};
var district = new District();
window.district = district;
district.bindEvent();