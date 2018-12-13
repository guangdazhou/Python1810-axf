
// 用于图片src属性修改脚本 【参考】
$(function () {
    // <img src="{% static 'img/research_ico.png' %}" alt="">

    $('img').each(function () {
        // $(this) 当前的img元素
        // console.log(1)

        // 获取当前的图片路径 src属性
        var img_path = $(this).attr('src')
        // console.log(img_path)

        // 字符串拼接
        img_path = "{% static '" + img_path + "' %}"
        // console.log(img_path)

        // 设置对应元素的src属性
        $(this).attr('src', img_path)
    })

    // 输出body >> 复制  >> 替换掉原有body内容  >> 删除该脚本
    console.log($('body').html())
})