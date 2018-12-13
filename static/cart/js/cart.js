$(function () {
    $('.cart').width(innerWidth)

    total()

    // 选中处理
    $('.cart .confirm-wrapper').click(function () {
        var cartid = $(this).attr('cartid')
        var $span = $(this).find('span')

        $.get('/axf/changecartstatus/', {'cartid':cartid}, function (response) {
            console.log(response)
            if (response.status){
                var isselect = response.isselect
                if (isselect){
                    $span.removeClass('no').addClass('glyphicon glyphicon-ok')
                } else {
                    $span.removeClass('glyphicon glyphicon-ok').addClass('no')
                }
            }

            total()
        })
    })


    // 全选/取消全选
    $('.cart .all').click(function () {
        var isall = $(this).attr('isall')
        isall = (isall == 'false') ? true : false
        $(this).attr('isall', isall)

        // 样式显示
        var $span = $(this).find('span')

        if (isall){
             $span.removeClass('no').addClass('glyphicon glyphicon-ok')
        } else {
            $span.removeClass('glyphicon glyphicon-ok').addClass('no')
        }


        // 发起ajax请求
        $.get('/axf/changecartisall/', {'isall':isall}, function (response) {
            console.log(response)
            if (response.status){
                // 遍历
                $('.cart .confirm-wrapper').each(function () {
                    if (isall){ // 全选
                        $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
                    } else {    // 取消全选
                        $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
                    }
                })

                total()
            }
        })
    })

    // 计算总数
    function total() {
        var sum = 0

        // 个数 × 单价 【选中】
        $('.goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            if ($confirm.find('.glyphicon-ok').length){ // 选中
                var num = $content.find('.num').attr('num')
                var price = $content.find('.price').attr('price')

                sum += num * price
            }
        })

        // 显示金额
        $('.bill .total b').html(parseInt(sum))
    }

    $('#generateorder').click(function () {
        $.get('/axf/generateorder/',function (response) {
            console.log(response)

            if (response.status == 1){
                window.open('/axf/orderdetail/' +response.identifier + '/',target='_self')
            }
        })
    })

})