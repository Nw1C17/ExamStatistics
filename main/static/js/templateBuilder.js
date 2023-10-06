$(document).ready(function (){

    // Объявление csrf токена
    // Без него ajax не работает
    const csrftoken = getCookie('csrftoken');

    // HTML элементы списка образовательных учреждений
    const educInsts = document.getElementById('id_educInsts')
    const listRange = document.getElementById('id_list_range')
    let listRangeCount = 0

    // Если если список районов пустой кнопка блокируется
    if ($.isEmptyObject(JSON.parse(document.getElementById('districts').textContent))) {
        $("#id_param_0").prop("disabled", true);
        console.log('1')
    }

    // Объявление списка по предметам
    $('#id_subjects').multiSelect({
        columns: 1,
        placeholder: "Текст",
        search: true
    })

    // Объявление списка по образовательному учреждению
    $('#id_educInsts').multiSelect({
        columns: 1,
        placeholder: "Текст",
        search: true
    });

    // Объявление списка по району
    $('#id_districts').multiSelect({
        columns: 1,
        placeholder: "Текст",
        search: true,
        afterSelect: function(r){ // Ajax запрос после добавления элемента
            // console.log($('#id_districts').serializeArray())
            // console.log(r)
            $.ajax({
                data: $('#id_districts').serializeArray(),
                url: "/tempBuild/", //Название
                type: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                dataType: 'json',
                success: function (resp){ // Перед тем как изменить данные списка нужно отключить multiSelect
                    $("#id_educInsts").prop("disabled", false);
                    $('#id_educInsts').multiSelect("destroy") // Отключение multiSelect
                    educInsts.innerHTML = ""
                    const data = resp.educInsts
                    data.forEach(el => {
                        educInsts.innerHTML += `
                     <option value="${el[0]}">${el[1]}</option>
                   `
                    });

                    $('#id_educInsts').multiSelect({ // Включение multiSelect
                        columns: 1,
                        placeholder: "Текст",
                        search: true
                    }).prop('disabled', true)
                    // console.log($('#id_districts').serializeArray())
                }
            });
        },
        afterDeselect: function(dlt_dis){ // Ajax запрос после удаления элемента
            var d = [{name:'districts', value: dlt_dis[0]}]
            console.log(d)
            $.ajax({
                data: $('#id_districts').serializeArray() , //
                url: "/tempBuild/",
                type: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                dataType: 'json',
                success: function (resp){ // Перед тем как изменить данные списка нужно отключить multiSelect
                    $('#id_educInsts').multiSelect("destroy") // Отключение multiSelect
                    if($.isEmptyObject(resp)){
                        educInsts.innerHTML = ""
                    }else {
                        educInsts.innerHTML = "" // Очистка записей
                        const data = resp.educInsts
                        data.forEach(el => {
                            educInsts.innerHTML += `
                     <option value="${el[0]}">${el[1]}</option>
                   `
                        });
                        $("#id_educInsts").prop("disabled", false);
                    }
                    $('#id_educInsts').multiSelect({ // Включение multiSelect
                        columns: 1,
                        placeholder: "Текст",
                        search: true
                    })
                }
            });
        }
    });
    // Если список районов равен 1
    if((JSON.parse(document.getElementById('districts').textContent).length === 1)){
        $('#id_districts').multiSelect('select_all');
        $('#id_districts').multiSelect("destroy")
        $("#div_id_districts").remove()
        // $('#id_districts').multiSelect("destroy")
        $("#id_param_0").prop("disabled", true);
        // $('#id_educInsts').prop("disabled", false);
    }
    // Скрытие списка по предметам
    // $("#div_id_subjects").prop("hidden", true);

    // Скрытие списка по районам
    // $("#div_id_districts").prop("hidden", true);
    // $("#id_districts").prop("disabled", true);

    // Скрытие списка по образовательному учреждению
    $("#div_id_educInsts").prop("hidden", true);
    $("#id_educInsts").prop("disabled", true);

    //Скрытие формы создания срезов
    $("#div_id_range").prop("hidden", true);


    //////////////////////////////////////////////// Типы экзаменов //////////////////////////////////////////////

    //ЕГЭ
    $('#id_exam_type_0').trigger('click');
    $("#id_exam_type_0").change(function (){
        if( $(this).is(":checked") ){
            $("#id_stat_fields_3").prop("disabled", false);
        }
    })

    //ОГЭ
    $("#id_exam_type_1").change(function (){
        if( $(this).is(":checked") ){
            $("#id_stat_fields_3").prop("disabled", true).prop("checked", false);
            $("#div_id_range").prop("hidden", true);
            $('input[name="range"]').each(function (){
                $("#id_stat_fields_3").prop("disabled", true)
            })
        }
    })

    //////////////////////////////////////////////// Шапка //////////////////////////////////////////////

    //Предмет в шапке
    $('#id_head_1').trigger('click');
    $("#id_param_2").prop("disabled", true).prop("checked", false);

    $("#id_head_1").change(function (){
        if( $(this).is(":checked") ){
            $("#id_subjects").prop("disabled", false).prop("hidden", false); //Активация списка предметов
            $("#div_id_subjects").prop("hidden", false);
            $("#id_years").prop("disabled", true).prop("hidden", true);  //Блокировка списка годов
            $("#div_id_years").prop("hidden", true);
            $("#id_param_2").prop("disabled", true).prop("checked", false); //Блокировка предмета в Статистике по
        }
    })

    //Год
    $("#id_head_0").change(function (){
        if( $(this).is(":checked") ){
            $("#id_subjects").prop("disabled", true).prop("hidden", true); //Блокировка списка предметов
            $("#div_id_subjects").prop("hidden", true);
            $("#id_param_2").prop("disabled", false).prop("checked", false); //Активация предмета в Статистике по


        }
    })
    //////////////////////////////////////////////// Статистика по //////////////////////////////////////////////

    function f() {
        if($("#id_head_0").is(":checked")){
            $("#id_educInsts").prop("disabled", true);
            $("#div_id_educInsts").prop("hidden", true);
            $("#id_districts").prop("disabled", true);
            $("#div_id_districts").prop("hidden", true);
            $("#div_id_subjects").prop("hidden", true);
            $("#id_subjects").prop("disabled", true);
        }
        else {
            $("#id_educInsts").prop("disabled", true);
            $("#div_id_educInsts").prop("hidden", true);
            $("#id_districts").prop("disabled", true);
            $("#div_id_districts").prop("hidden", true);
        }

    }
    //Районы кнопка
    $('#id_param_0').trigger('click');
    $('#id_param_0').change(function(){
        if ($(this).is(':checked')){
            f()
            $("#id_districts").prop("disabled", false);
            $("#div_id_districts").prop("hidden", false); // Активация районов
            // console.log(document.getElementById('id_districts'))
            // $("#id_educInsts").prop("disabled", true);
            // $("#div_id_educInsts").prop("hidden", true);
        }
    });

    //Образовательное учреждение
    $('#id_param_1').change(function(){
        if ($(this).is(':checked')){
            f()
            $("#id_educInsts").prop("disabled", false);
            $("#div_id_educInsts").prop("hidden", false);
            // console.log(document.getElementById('id_educInsts'))
            $("#id_districts").prop("disabled", false);
            $("#div_id_districts").prop("hidden", false);
            // $("#div_id_subjects").prop("hidden", true);
            // $("#id_subjects").prop("disabled", true).prop("hidden", true);
        }
    });

    //Предметы
    $("#id_param_2").change(function (){
        if( $(this).is(":checked") ){
            f()
            $("#div_id_subjects").prop("hidden", false);
            $("#id_subjects").prop("disabled", false).prop("hidden", false); //Активация списка предметов
            // console.log(document.getElementById('id_subjects'))
            // $("#id_educInsts").prop("disabled", true);
            // $("#div_id_educInsts").prop("hidden", true);
            // $("#id_districts").prop("disabled", true);
            // $("#div_id_districts").prop("hidden", true); // Блокировка районов
        }
    })

    //////////////////////////////////////////////// Вычисляемые данные //////////////////////////////////////////////
    $('#id_stat_fields_0').trigger('click');
    $('#id_stat_fields_1').trigger('click');

    $("#id_stat_fields_3").change(function (){
        if( $(this).is(":checked") ){
            $("#div_id_range").prop("hidden", false);
            $('input[name="range"]').each(function (){
                $(this).prop("disabled", false)
            })
        } else {
            $("#div_id_range").prop("hidden", true);
            $('input[name="range"]').each(function (){
                $(this).prop("disabled", true)
            })

        }
    })


    ////////////////////////////////////////////////  //////////////////////////////////////////////

    //Кнопка добавить срез
    $('#id_button_add_range').click(function (){
        if(listRangeCount < 5){
            rndVal = getRandomInt(0, 1000);
            listRange.innerHTML += `
                      <div class="row my-1 justify-content-center" id="id_range_row_${rndVal}">
                          <div class="col-md-1">
                            <a class="btn my-2 " id="delete_id_range" data-action="${rndVal}">
                              <img src="/static/admin/img/icon-deletelink.svg" alt="Удалено">
                            </a>
                          </div>
                          <div class="col-md-4">
                            <input class="form-control" type="number" name="range" min="0" max="100" placeholder="от">
                          </div>
                          <div class="col-md-4">
                            <input class="form-control" type="number" name="range" min="0" max="100" placeholder="до">
                          </div>
                      </div>
        `
            listRangeCount += 1
        }
        // document.querySelectorAll('#id_range_row').forEach(slider => {
        //     console.log(slider)
        // });
        // console.log($('input[name="rangeMax"]').val())

        // $('input[name="rangeMax"]').each(function (){
        //     rangeMax.push($(this).val())
        // })
        // $('input[name="rangeMin"]').each(function (){
        //     rangeMin.push($(this).val())
        // })
        // let dataf = {
        //     'rangeMax': $('input[name="rangeMax"]').serializeArray(),
        //     'rangeMin': $('input[name="rangeMin"]').serializeArray()
        // }
        // $.ajax({
        //     data: $('input[name="range"]').serializeArray(),
        //     url: "/tempBuild/",
        //     type: 'POST',
        //     headers: {"X-CSRFToken": csrftoken},
        //     dataType: 'json',
        //     success: function (resp){
        //         $("#id_educInsts").prop("disabled", false);
        //         $('#id_educInsts').multiSelect("destroy") // Отключение multiSelect
        //         const data = resp.educInsts
        //         data.forEach(el => {
        //             educInsts.innerHTML += `
        //              <option value="${el[0]}">${el[1]}</option>
        //            `
        //         });
        //
        //         $('#id_educInsts').multiSelect({ // Включение multiSelect
        //             columns: 1,
        //             placeholder: "Текст",
        //             search: true
        //         }).prop('disabled', true)
        //     }
        // });
    })

    $('#id_list_range').on("click", "#delete_id_range", function (){
        $(this).parent().parent().remove()
        listRangeCount -= 1
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

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

})