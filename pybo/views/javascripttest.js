const delete_element=document.getElementsByClassName('delete');
Array.from(delete_element).forEach(function(element){
    element.addEventListener('click',function(){
        if(confirm('정말삭제?')){
            location.href=this.dataset.uri;
        }

    });

});
const recommend_element=document.getElementsByClassName('recommend');
Array.from(recommend_element).forEach(function(element){
    element.addEventListener('click',function(){
        if(confirm('정말추천?')){
            location.href=this.dataset.uri;
        }

    });

});
const page_elements=document.getElementsByClassName('page-link');
Array.from(page_elements).forEach(function(element){
    element.addEventListener('click',function(){
        document.getElementById('page')=this.dataset.page;
        document.getElementById('searchForm').onsubmit()
    });
});
const btn_search=document.getElementById('btn_search');
btn_search.addEventListener('click',function(){
    document.getElementById('kw').value=document.getElementById('search_kw').value;
    document.getElementById('page').value=1;
    document.getElementById('searchForm').onsubmit();

});