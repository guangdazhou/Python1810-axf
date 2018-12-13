$(function () {
    // 屏幕宽度处理
    $('.market').width(innerWidth)

    // 获取 typeIndex
    var typeIndex = $.cookie('typeIndex')
    if (typeIndex){ // 有下标记录
        // 根据下标获取对应li，并添加上'active'
        $('.type-slider .type-item').eq(typeIndex).addClass('active')
    } else {    // 没有下标记录
        // 默认就是第一个
        $('.type-slider .type-item:first').addClass('active')
    }


    // 侧边栏 分类 点击
    // 问题描述: 当点击分类时，样式添加成功，之后又会消失
    // 问题分析: 点击分类是 a标签，在样式设置完成后，会重新刷新页面；重新刷新页面，样式会被重置
    // 问题解决: 记录点击分类的下标

    // 用什么记录？  cookie
    // 为了方便操作cookie，引入 jquery.cookie.js
    // 设置cookie    $.cookie(key, value, opthions)
    // 获取cookie    $.cookie(key)
    // 删除cookie    $.cookie(key, null)
    // opthions选项  {'expires': 过期时间, path: 路径}
    $('.type-slider .type-item').click(function () {
        // $(this) 被点击的 li
        // $(this).addClass('active')

        // 记录 分类 下标    $(this).index()
        $.cookie('typeIndex', $(this).index(), {expires: 3, path: '/'})
    })



    // 全部类型 点击
    var categoryShow = false
    $('#category-bt').click(function () {
        console.log('全部类型')
        // 取反
        categoryShow = !categoryShow
        categoryShow ? categoryViewShow() : categoryViewHide()
    })


    // 综合排序 点击
    var sortShow = false
    $('#sort-bt').click(function () {
        console.log('综合排序')
        sortShow = !sortShow
        sortShow ? sortViewShow() : sortViewHide()
    })


    // 问题: (排序按钮中)点击两次才能显示
    //      点击 ‘全部类型’ 按钮  >>>  ‘子类信息view’ 显示    【categoryShow>true】
    //      点击 蒙层  >>>  ‘子类信息view’            隐藏
    //      点击 ‘全部类型’ 按钮  >>>  ‘子类信息view’    不显示    【categoryShow>false】
    //      点击 ‘全部类型’ 按钮  >>>  ‘子类信息view’    才显示


    // 正常
    //      点击 ‘全部类型’ 按钮  >>>  ‘子类信息view’ 显示    【categoryShow>true】
    //      点击 蒙层  >>>  ‘子类信息view’            隐藏    【categoryShow>false】
    //      点击 ‘全部类型’ 按钮  >>>  ‘子类信息view’    显示    【categoryShow>true】

    // 蒙层
    $('.bounce-view').click(function () {
        categoryViewHide()
        categoryShow = false

        sortViewHide()
        sortShow = false
    })

    function categoryViewShow() {
        sortShow = false
        sortViewHide()

        $('.bounce-view.category-view').show()
        // glyphicon-arrow-down
        // 先移除 glyphicon-arrow-up，再添加glyphicon-arrow-down
        $('#category-bt i').removeClass('glyphicon-arrow-up').addClass('glyphicon-arrow-down')
    }

    function categoryViewHide() {
        $('.bounce-view.category-view').hide()
        $('#category-bt i').removeClass('glyphicon-arrow-down').addClass('glyphicon-arrow-up')
    }

    function sortViewShow() {
        categoryShow = false
        categoryViewHide()

        $('.bounce-view.sort-view').show()
        $('#sort-bt i').removeClass('glyphicon-arrow-up').addClass('glyphicon-arrow-down')
    }

    function sortViewHide() {
        $('.bounce-view.sort-view').hide()
        $('#sort-bt i').removeClass('glyphicon-arrow-down').addClass('glyphicon-arrow-up')
    }





    ////////////////////////
    // 默认不显示
    // $('.bt-wrapper .glyphicon-minus').hide()
    // $('.bt-wrapper .num').hide()

    // 假如商品个数不为0，显示
    $('.bt-wrapper .num').each(function () {
        var num = parseInt($(this).html())
        if (num) {  // 显示
            $(this).prev().show()
            $(this).show()
        } else {    // 隐藏
            $(this).prev().hide()
            $(this).hide()
        }
    })

    // 加操作
    $('.bt-wrapper .glyphicon-plus').click(function () {
        // $(this)  >> 对应的加按钮
        var goodsid = $(this).attr('goodsid')
        // console.log($(this))

        // 保存起来
        var $that = $(this)

        // 发起ajax请求
        // jQuery.get( url [, data ] [, success(data, textStatus, jqXHR) ] [, dataType ] )
        $.get('/axf/addcart/', {'goodsid':goodsid}, function (response) {
            console.log(response)
            if (response.status == -1){     // 未登录，直接跳转到登录
                // DOM  BOM
                window.open('/axf/login/', target='_self')
            } else if(response.status == 1){    // 添加成功
                // 有问题!!!!
                // $('.bt-wrapper .num').show().html(response.number)
                // $('.bt-wrapper .glyphicon-minus').show()

                // 兄弟节点
                // 问题: 操作不了
                // 分析: prev()上一个兄弟节点【没问题】， 问题只能是 $(this)
                // console.log($(this))
                // $(this) 指向有问题， 因为是由ajax触发的，所以这里指向ajax
                // $(this).prev().show().html(response.number)
                // $(this).prev().prev().show()

                $that.prev().show().html(response.number)
                $that.prev().prev().show()
            }
        })
    })

    $('.bt-wrapper .glyphicon-minus').click(function () {
        var goodsid = $(this).attr('goodsid')
        var $that = $(this)

        $.get('/axf/subcart/', {'goodsid':goodsid}, function (response) {
            console.log(response)
            if (response.status == 1){  // 操作成功
                if (response.number > 0){   // 改变数据
                    $that.next().html(response.number)
                } else {    // 隐藏处理
                    $that.next().hide()
                    $that.hide()
                }
            }
        })
    })
})