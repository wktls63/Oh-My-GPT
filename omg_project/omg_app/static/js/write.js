const dataType1 = document.querySelector('.data-type1');
const dataType2 = document.querySelector('.data-type2');

dataType1.addEventListener('click', () => {
    dataType2.classList.remove('type-select');
    dataType1.classList.add('type-select');
})
dataType2.addEventListener('click', () => {
    dataType1.classList.remove('type-select');
    dataType2.classList.add('type-select');
})

document.getElementById('file').addEventListener('change', function() {
    var filename = this.value.split('\\').pop();
    document.querySelector('.select-data').textContent = filename;
});