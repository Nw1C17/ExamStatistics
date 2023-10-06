$(document).ready(function (){
    const csrftoken = getCookie('csrftoken');

    const temps = JSON.parse(document.getElementById('templates').textContent)

    const listRange = document.getElementById('list_temp')

    temps.forEach(el => {
        listRange.innerHTML += `
        <li class="list-group-item" ><a class="nav-link active" target="_blank" href="/report/${el[0]}" >${el[1]}</a>
            <a class="btn my-2" id="dlt_btn_id" data-action="${el[0]}">
            <img src="/static/admin/img/icon-deletelink.svg" alt="Удалено">
            </a>
        </li>
        `
    })

    $('#list_temp').on("click", "#dlt_btn_id", function (){
        console.log($(this).attr('data-action'));
        $.ajax({
            data: {'id':$(this).attr('data-action')},
            url: "/profile/",
            type: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            dataType: 'json',
            success: function (temps){
                tmp = temps.templates
                listRange.innerHTML = ""
                tmp.forEach(el => {
                    listRange.innerHTML += `
                    <li class="list-group-item" ><a class="nav-link active" target="_blank" href="/report/${el[0]}" >${el[1]}</a>
                        <a class="btn my-2" id="dlt_btn_id" data-action="${el[0]}">
                        <img src="/static/admin/img/icon-deletelink.svg" alt="Удалено">
                        </a>
                    </li>
                    `
                })
            }
        });
    })

    // Функция создания токена
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})