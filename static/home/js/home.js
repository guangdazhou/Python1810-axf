$(function () {

    // 设置回到屏幕宽度
    $('.home').width(innerWidth)

    var topswiper = new Swiper('#topSwiper', {
        pagination: '.swiper-pagination',
        slidesPerView: 1,
        paginationClickable: true,
        spaceBetween: 30,
        loop: true,
        autoplay : 3000,
    });

    var mustbuySwiper = new Swiper('#mustbuySwiper', {
        spaceBetween: 3,
        loop: true,
        slidesPerView: 3,
    });
})