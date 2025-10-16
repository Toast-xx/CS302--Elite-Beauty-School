document.addEventListener('DOMContentLoaded', function () {
    const mainImg = document.getElementById('mainProductImg');
    const thumbs = document.querySelectorAll('.product-gallery-img');
    thumbs.forEach(function (thumb) {
        thumb.addEventListener('click', function () {
            mainImg.src = this.getAttribute('data-img');
        });
    });
});