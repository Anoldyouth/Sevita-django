const arrows = document.querySelectorAll('.arrow')
const photos = document.querySelectorAll('.product__preview')
var i = 0

for(const arrow of arrows){
    arrow.addEventListener('click', () => {
        if(arrow.classList.contains('right')){
            photos[i].classList.remove('active')
            i=i+1
            photos[i].classList.add('active')
            for(const arrow of arrows){
                arrow.classList.remove('limit')
            }
            if(i==2){
                arrow.classList.add('limit')
            }

        }
        if(arrow.classList.contains('left')){
            photos[i].classList.remove('active')
            i=i-1
            photos[i].classList.add('active')
            for(const arrow of arrows){
                arrow.classList.remove('limit')
            }
            if(i==0){
                arrow.classList.add('limit')
            }
        }
    })
}